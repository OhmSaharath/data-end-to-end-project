# 1. เริ่มจาก Image สำเร็จรูปของ Airflow
FROM apache/airflow:2.8.2

# 2. คัดลอก "รายการวัตถุดิบ" เข้าไปข้างใน
COPY requirements.txt /requirements.txt

# 3. สั่งให้ "pip" ทำการติดตั้งทุกอย่างในรายการนั้น
RUN pip install --no-cache-dir -r /requirements.txt
