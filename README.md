# 🧠 Data Engineering Projects Collection  
## 🚀 End-to-End Data Pipeline with Airflow, Docker, and GCP

Build an automated data pipeline using **Apache Airflow**, **Docker**, and **Google Cloud Platform (GCP)**  
to extract public API data, transform it with Python, and load it into **Cloud SQL** for analytics and dashboarding.

---

### 🔧 Stack Used
- Apache Airflow 2.8+
- Docker + Docker Compose
- Python 3.8+
- Google Cloud (Compute Engine, Cloud SQL, Cloud Storage)
- PostgreSQL or MSSQL
- Looker Studio (Dashboard)

---

### 📌 Project Goals
- [x] Automate data ingestion from public APIs
- [x] Run DAGs using Airflow on Docker in GCP VM
- [x] Store data in Cloud SQL
- [x] Optional: Visualize with Looker Studio / Google Sheets

---

### 📂 Folder Structure
```plaintext
.
├── dags/                # All Airflow DAGs
├── docker-compose.yaml  # Services: Airflow, Postgres
├── requirements.txt     # Python dependencies
├── setup/               # Shell scripts / config for GCP
├── README.md
