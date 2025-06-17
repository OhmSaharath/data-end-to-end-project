from src.config import settings
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.log.logging_mixin import LoggingMixin
from src.api.coinlist_client import dimension_fetch

def load_assets_platforms(data_to_load : list, postgres_conn_id : str):
    """
    (L)oads asset platform data into the bronze.asset_platforms table.
    This function performs a "Truncate and Load" operation.
    
    Args:
        data_to_load (list): A list of dictionaries, where each dictionary is an asset platform.
        postgres_conn_id (str): The Airflow Connection ID for the PostgreSQL database.
    """
    log = LoggingMixin().log
    if not data_to_load :
        print("No asset platform data to load. Skipping.")
    sql_truncate = """TRUNCATE TABLE bronze.asset_platforms CASCADE;"""
    target_table = 'bronze.asset_platforms'
    target_fields = [ 'platform_id',
        'chain_identifier',
        'name_platform',
        'shortname',
        'native_coin_id' ] 
    pg_hook = PostgresHook(postgres_conn_id = postgres_conn_id)
    try :
        rows_to_insert = [
            (
                data.get('id'),
                data.get('chain_identifier'),
                data.get('name'),
                data.get('shortname'),
                data.get('native_coin_id')
            )
            for data in data_to_load
        ]
        log.info(f"Preparing to load {len(rows_to_insert)} records into {target_table}...")
        log.info(f"Truncating table: {target_table}...")
        pg_hook.run(sql_truncate)
        log.info("Inserting new rows...")
        pg_hook.insert_rows(
            table = target_table,
            rows = rows_to_insert,
            target_fields = target_fields
            )
        log.info("Load complete!")
    except Exception as e:
        log.error(f"เกิดข้อผิดพลาดร้ายแรงระหว่างการโหลดข้อมูล: {e}")
        raise

load_assets_platforms(dimension_fetch(settings.URL_ASSET_PLATFORMS), 'postgres_default')