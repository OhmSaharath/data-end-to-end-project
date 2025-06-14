# src/config/settings.py
TARGET_COINS = ['bitcoin', 'ethereum', 'solana', 'sui']
VS_CURRENCY = 'usd'
API_HEADERS = {
    "accept": "application/json",
    "x-cg-demo-api-key": "CG-LMygQ4HtUSikgaWtcAqzbZ3i"
}
DB_CONFIG = {
    "database": "airflow",
    "host": "localhost",
    "user": "airflow",
    "password": "airflow",
    "port": "5432"
}
KEYS_TO_KEEP = ['id', 'symbol', 'name', 'current_price', 'market_cap_rank', 'price_change_24h', 'last_updated']
