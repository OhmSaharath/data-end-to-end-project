import requests
from src.config import settings

def dimension_fetch(url : str):
    print('Fetch data API form Coingecko!')

    response = requests.get(url, settings.API_HEADERS)
    response.raise_for_status()
    return response.json()

print(dimension_fetch(settings.URL_ASSET_PLATFORMS))