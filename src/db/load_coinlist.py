import psycopg2
from src.config import settings
from src.api.coinlist_client import dimension_fetch

def load_coinlist(data_to_load: list):
    if not data_to_load :
        print("No data!")
        return
    print('Truncate and Load data!')
    sql_truncate = """TRUNCATE TABLE bronze.coin_master CASCADE;"""
    sql_insert = """INSERT INTO bronze.coin_master (
        coin_id, 
        symbol, 
        name_coin)
        VALUES (%s, %s, %s);"""
    try:
        with psycopg2.connect(**settings.DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_truncate)
                for data in data_to_load:
                    column_record = (
                        data.get('id'),
                        data.get('symbol'),
                        data.get('name')
                    )              
                    cursor.execute(sql_insert, column_record)
                conn.commit()
    except psycopg2.Error as e:
        print(f"Error during database operation: {e}")
        # อาจจะ raise error ขึ้นไปอีกครั้งเพื่อให้ Airflow รู้ว่า Task ล้มเหลว
        raise

