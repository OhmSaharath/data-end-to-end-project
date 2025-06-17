# src/api/coingecko_client.py

import requests
from src.config import settings # Import settings เพื่อใช้ API_HEADERS

# แก้ไขบรรทัด def ให้รับพารามิเตอร์ 2 ตัว
def fetch_data(coin_ids: list, currency: str) -> list:
    """(E)xtract: ดึงข้อมูลจาก CoinGecko API ตามรายชื่อเหรียญที่รับเข้ามา"""
    
    print(f"Fetching data for coins: {coin_ids}")
    
    # ใช้พารามิเตอร์ที่รับเข้ามาเพื่อสร้าง URL
    ids_string = ','.join(coin_ids)
    url = f"https://api.coingecko.com/api/v3/coins/markets?ids={ids_string}&vs_currency={currency}"
    
    # ใช้ API_HEADERS จากไฟล์ settings
    response = requests.get(url, headers=settings.API_HEADERS)
    response.raise_for_status() # ทำให้ Task fail ถ้า API ตอบกลับมาเป็น error
    
    print("Fetch complete.")
    return response.json()
