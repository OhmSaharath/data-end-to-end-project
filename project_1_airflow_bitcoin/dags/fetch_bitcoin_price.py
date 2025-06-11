from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import pandas as pd

def fetch_bitcoin_price():
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    response = requests.get(url)
    data = response.json()
    price = data["bpi"]["USD"]["rate_float"]
    time = data["time"]["updatedISO"]

    df = pd.DataFrame([{"timestamp": time, "usd_price": price}])
    df.to_csv("/opt/airflow/dags/bitcoin_price.csv", index=False)
    print("Bitcoin price saved.")

with DAG(
    dag_id="fetch_bitcoin_price",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["bitcoin", "api"],
) as dag:
    fetch_task = PythonOperator(
        task_id="fetch_price",
        python_callable=fetch_bitcoin_price
    )
