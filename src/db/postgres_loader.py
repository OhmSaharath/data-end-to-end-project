# src/db/postgres_loader.py

import psycopg2  # <-- Import psycopg2 กลับมา
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.log.logging_mixin import LoggingMixin

# ฟังก์ชันยังคงรับพารามิเตอร์เหมือนเดิมทุกอย่าง
def load_data(data_to_load: list, postgres_conn_id: str, target_table: str, target_fields: list):
    """
    (L)oad: บันทึกข้อมูลลง PostgreSQL โดยใช้ psycopg2 โดยตรง
    แต่ยังคงดึง Connection จาก Airflow Hook เพื่อความปลอดภัย
    """
    log = LoggingMixin().log
    
    # 1. สร้าง Hook ขึ้นมาเพื่อใช้เป็น "ตัวกลาง" ในการดึง Connection
    pg_hook = PostgresHook(postgres_conn_id=postgres_conn_id)
    
    log.info("Connecting to PostgreSQL using psycopg2 via Airflow Hook...")
    
    # 2. ใช้ with-statement เพื่อจัดการ connection และ transaction อัตโนมัติ
    #    pg_hook.get_conn() จะดึง connection object ของ psycopg2 ออกมาให้เรา
    try:
        with pg_hook.get_conn() as conn:
            # 3. เมื่อได้ conn มาแล้ว เราก็สร้าง cursor แบบ psycopg2 ปกติ
            with conn.cursor() as cursor:
                log.info(f"Preparing to load {len(data_to_load)} records into table: {target_table}...")

                # 4. สร้าง SQL statement ที่มี Placeholders (%s)
                #    เราจะใช้ ','.join() เพื่อสร้าง string ของชื่อคอลัมน์และ placeholders โดยอัตโนมัติ
                fields_str = ', '.join(target_fields)
                placeholders_str = ', '.join(['%s'] * len(target_fields))
                
                sql_insert_query = f"INSERT INTO {target_table} ({fields_str}) VALUES ({placeholders_str});"
                log.info(f"Executing SQL: {sql_insert_query}")

                # 5. วนลูปเพื่อ execute ข้อมูลทีละแถว
                for data_dict in data_to_load:
                    # สร้าง Tuple ของข้อมูลตามลำดับของ keys ที่เราใช้
                    keys_in_order = ['id', 'symbol', 'name', 'current_price', 'market_cap_rank', 'price_change_24h', 'last_updated']
                    record_to_insert = tuple(data_dict.get(key) for key in keys_in_order)
                    
                    # สั่ง execute แบบ psycopg2 ปกติ
                    cursor.execute(sql_insert_query, record_to_insert)

            # 6. การ commit transaction
            #    เมื่อโค้ดทำงานจบในบล็อก `with pg_hook.get_conn() as conn:` โดยไม่มี Error,
            #    Hook จะทำการ conn.commit() ให้เราโดยอัตโนมัติครับ
            log.info("Transaction will be committed automatically upon exiting 'with' block.")

    except psycopg2.Error as e:
        log.error(f"Database error occurred: {e}")
        # raise error ขึ้นไปอีกครั้ง เพื่อให้ Airflow รู้ว่า Task นี้ "ล้มเหลว" (Failed)
        raise
        
    log.info(f"Load process finished for {len(data_to_load)} records.")
