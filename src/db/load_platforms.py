import psycopg2
from src.config import settings
from src.api.coinlist_client import dimension_fetch
from src.db.load_coinlist import load_coinlist

def load_platforms(data_to_load : list):
    if not data_to_load :
        print('No data!')
    sql_truncate = """TRUNCATE TABLE bronze.coin_platform_contracts RESTART IDENTITY;"""
    sql_insert  = """INSERT INTO bronze.coin_platform_contracts (
        coin_id,
        platform_id,
        contract_address
        ) VALUES (%s, %s, %s)"""
    try :
        with psycopg2.connect(**settings.DB_CONFIG) as conn :
            with conn.cursor() as cursor:
                cursor.execute(sql_truncate)
                for data in data_to_load :
                    platforms = data.get('platforms', {})
                    if platforms :
                        for platforms_id, contract_address in platforms.items() :
                            db_contract_address = contract_address if contract_address else None
                            
                            platforms_record = (
                                data.get('id'),
                                platforms_id,
                                db_contract_address
                            )
                            cursor.execute(sql_insert, platforms_record)
            conn.commit()
            print('Commit Complete!')
    except psycopg2.Error as e:
        print(f"Database error occurred: {e}")
        raise

load_coinlist(dimension_fetch(settings.URL_COINLIST))
load_platforms(dimension_fetch(settings.URL_INC_PLATFORMS))                   