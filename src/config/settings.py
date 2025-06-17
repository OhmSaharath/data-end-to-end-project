# src/config/settings.py
TARGET_COINS = ['bitcoin', 'ethereum', 'solana', 'sui']
VS_CURRENCY = 'usd'
URL_COINLIST = "https://api.coingecko.com/api/v3/coins/list"
URL_INC_PLATFORMS = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
URL_ASSET_PLATFORMS = "https://api.coingecko.com/api/v3/asset_platforms"
URL_CATEGORIES_LIST = "https://api.coingecko.com/api/v3/coins/categories/list"
URL_EXCHANGE_LIST = "https://api.coingecko.com/api/v3/exchanges/list"
URL_NFTS_LIST = "https://api.coingecko.com/api/v3/nfts/list"
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
