import requests

target_coins = [
    'bitcoin',
    'ethereum',
    'solana',
    'sui'
]

ids_strings = ','.join(target_coins)
vs_currency = 'usd'

url = f"https://api.coingecko.com/api/v3/coins/markets?ids={ids_strings}&vs_currency={vs_currency}"
headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": "CG-LMygQ4HtUSikgaWtcAqzbZ3i"
}

response = requests.get(url, headers=headers)
coin_list = response.json() # ได้ข้อมูลมาเป็น List of Dictionaries

def get_data(data_list) :
    key_list = ['id','symbol','name','current_price','market_cap_rank','price_change_24h','last_updated']
    final_data = []
    for coin_dict in data_list :
        select_data = {}
        for key in key_list:
            select_data[key] = coin_dict.get(key)
        final_data.append(select_data)
    
    return final_data

print(get_data(coin_list))
