from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=3)
}

def fetch_bitcoin_price():
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    response = requests.get(url)
    data = response.json()
    print(json.dumps(data, indent=2))  # log only for now

with DAG(
    dag_id='fetch_bitcoin_price',
    default_args=default_args,
    description='Fetch current Bitcoin price from API',
    schedule_interval='@hourly',
    start_date=datetime(2025, 6, 11),
    catchup=False,
) as dag:
    task1 = PythonOperator(
        task_id='get_bitcoin_price',
        python_callable=fetch_bitcoin_price
    )
