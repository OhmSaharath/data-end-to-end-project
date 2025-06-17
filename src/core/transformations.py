# src/core/transformations.py

# ไม่จำเป็นต้อง import settings ที่นี่ ถ้าเราจะรับ keys มาเป็นพารามิเตอร์

# แก้ไขบรรทัด def ให้รับพารามิเตอร์ 2 ตัว คือ raw_data และ keys
def transform_data(raw_data: list, keys: list) -> list:
    """(T)ransform: จัดรูปแบบข้อมูลดิบตาม key ที่ต้องการ"""
    
    print("Transforming data...")
    
    # ใช้ List Comprehension และใช้ 'keys' ที่รับเข้ามา
    processed_data = [{key: coin_dict.get(key) for key in keys} for coin_dict in raw_data]
    
    print("Transform complete.")
    return processed_data
