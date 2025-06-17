# CoinGecko ETL Pipeline with Airflow

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-2.8.2-blueviolet?style=for-the-badge&logo=apache-airflow&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)

An automated ETL (Extract, Transform, Load) data pipeline orchestrated by Apache Airflow. This project fetches the latest market data for a defined list of cryptocurrencies from the CoinGecko API every 10 minutes, transforms the data into a clean format, and loads it into a PostgreSQL database for long-term storage and analysis. The entire system is containerized using Docker and Docker Compose for easy deployment and scalability.

---

## ✨ Features

* **Automated Data Ingestion:** Schedules data fetching from the CoinGecko API to run every 10 minutes.
* **Dynamic Configuration:** Easily add or remove target cryptocurrencies by modifying a central configuration file.
* **Modular & Maintainable Code:** The project is structured with a clear separation of concerns (API client, transformations, database loading).
* **Persistent Storage:** Data is reliably stored in a PostgreSQL database, ready for analysis.
* **Orchestration & Monitoring:** Full workflow management and monitoring via the Apache Airflow Web UI.
* **Containerized Environment:** All services (Airflow, PostgreSQL, Redis) are containerized, ensuring a consistent and reproducible setup.

## 🛠️ Tech Stack

* **Orchestrator:** Apache Airflow 2.8.2
* **Database:** PostgreSQL 13
* **Containerization:** Docker & Docker Compose
* **Language:** Python 3.8
* **Core Libraries:** `requests`, `pandas`, `psycopg2` (via Airflow Provider)
* **Data Source:** CoinGecko API

## 📂 Project Structure

The project is structured to separate the orchestration logic (DAGs) from the core application logic (`src`), promoting reusability and maintainability.

```
coingecko-airflow-pipeline/
├── dags/
│   └── coingecko_pipeline_dag.py
├── src/
│   ├── __init__.py
│   ├── api/
│   │   └── coingecko_client.py
│   ├── core/
│   │   └── transformations.py
│   ├── db/
│   │   └── postgres_loader.py
│   └── config/
│       └── settings.py
├── logs/
├── plugins/
├── .env
├── docker-compose.yml
└── requirements.txt
```

## 🚀 Setup and Installation

This guide assumes you have a host machine (e.g., a GCP VM) with Docker and Docker Compose already installed.

> For a complete, step-by-step guide on setting up the entire infrastructure from scratch (including GCP VM, Docker installation, and Firewall rules), please refer to the [**Detailed Infrastructure Setup Guide**](./docs/infrastructure_setup.md).

### 1. Clone the Repository

```bash
git clone [https://github.com/](https://github.com/)[your-github-username]/[your-repo-name].git
cd [your-repo-name]
```

### 2. Configure Environment (Linux/macOS Host)

To avoid file permission issues between the host and the Docker containers, you need to set your local user and group ID.

* Find your User ID and Group ID:

    ```bash
    echo "AIRFLOW_UID=$(id -u)" >> .env
    echo "AIRFLOW_GID=$(id -g)" >> .env
    ```

* This will create a `.env` file in the project root with the correct values.

### 3. Configure the Pipeline

* Open `src/config/settings.py`.
* Update `API_HEADERS` with your valid CoinGecko API key.
* Modify the `TARGET_COINS` list to include the cryptocurrencies you want to track.

### 4. Initialize the Database Schema

Before running the pipeline for the first time, you need to create the target table in your PostgreSQL database. Connect to your PostgreSQL instance and run the schema definition script (you can place this in `sql/schema.sql` for reference).

### 5. Launch Airflow

Run all services using Docker Compose from the project root directory.

```bash
docker-compose up -d
```

Wait for 3-5 minutes for all services to initialize, especially on the first run. Check the status with `docker ps`. All services should show a `(healthy)` status.

## 💻 Usage

1.  **Access the Airflow UI:**
    * Open your web browser and navigate to `http://<your_vm_ip>:8080`.
    * Log in with the default credentials: `airflow` / `airflow`.

2.  **Enable and Trigger the DAG:**
    * On the DAGs page, find `coingecko_production_pipeline`.
    * Click the toggle button on the left to un-pause and activate the DAG.
    * The DAG will start running automatically based on its schedule (`*/10 * * * *`). You can also trigger it manually by clicking the "Play" button on the right.

3.  **Verify Data in PostgreSQL:**
    * Connect to your PostgreSQL database using your preferred client (e.g., DBeaver, pgAdmin) or via the command line.
    * Run a query to see the data being inserted:
        ```sql
        SELECT * FROM bronze.data_coin_list ORDER BY fetch_timestamp DESC LIMIT 10;
        ```

## 🔮 Future Improvements

-   [ ] **Secret Management:** Migrate API keys and other sensitive data to Airflow's secret backends (like HashiCorp Vault or GCP Secret Manager) instead of using the config file.
-   [ ] **Data Quality Checks:** Implement a dedicated task to validate data after the transform step (e.g., check for null prices, ensure data types are correct) using a library like Great Expectations.
-   [ ] **Idempotent Loads:** Refactor the `load_task` to be idempotent (using an UPSERT or DELETE-then-INSERT pattern) to handle re-runs and backfills safely.
-   [ ] **Alerting:** Set up `on_failure_callback` to send notifications to Slack or email when a task fails.
-   [ ] **Dashboarding:** Connect a BI tool like Apache Superset or Metabase to the PostgreSQL database to visualize the collected data.
