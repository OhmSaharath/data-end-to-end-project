from __future__ import annotations

import pendulum
from airflow.decorators import dag, task

# Import ฟังก์ชันที่เราแยกไว้จากโฟลเดอร์ dags/src/
# (ตรวจสอบให้แน่ใจว่า Path ถูกต้องตามโครงสร้างของคุณ)
from src.config import settings
from src.api.coingecko_client import fetch_data
from src.core.transformations import transform_data
from src.db.postgres_loader import load_data

@dag(
    dag_id="coingecko_production_pipeline",
    schedule="*/10 * * * *",
    start_date=pendulum.datetime(2025, 6, 14, tz="Asia/Bangkok"), # ตั้งเป็นวันที่ในอดีต
    catchup=False,
    tags=["production", "coingecko"],
)
def coingecko_pipeline():
    """
    This DAG fetches data from CoinGecko, transforms it, and loads it into PostgreSQL.
    """

    @task
    def extract_task():
        """Fetches data from the CoinGecko API."""
        return fetch_data(settings.TARGET_COINS, settings.VS_CURRENCY)

    @task
    def transform_task(raw_data: list):
        """Transforms the raw data into the desired format."""
        if not raw_data:
            return []
        return transform_data(raw_data, settings.KEYS_TO_KEEP)

    @task
    def load_task(processed_data: list):
        """Loads the processed data into the PostgreSQL database."""
        if not processed_data:
            print("No data to load, skipping.")
            return

        db_table_columns = [
            "id_coin", "symbol", "name_coin", "current_price", 
            "market_cap_rank", "price_change_24h", "last_updated"
        ]
        
        # ใช้ Connection ID ที่ตั้งค่าไว้ใน Airflow UI
        load_data(
            data_to_load=processed_data,
            postgres_conn_id="postgres_default",
            target_table="bronze.data_coin_list",
            target_fields=db_table_columns
        )

    # กำหนดลำดับการทำงาน
    raw_api_data = extract_task()
    processed_data = transform_task(raw_api_data)
    load_task(processed_data)

# สร้าง instance ของ DAG
coingecko_pipeline()
