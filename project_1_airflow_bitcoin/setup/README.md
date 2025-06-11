# ☁️ GCP Setup for Airflow Bitcoin Project

This guide describes how to set up a Google Cloud Platform (GCP) VM instance to run Docker and Apache Airflow for ingesting Bitcoin price data.

---

## 📌 Prerequisites

- ✅ Google Cloud account
- ✅ Billing enabled
- ✅ IAM permission to create VM
- ✅ GitHub repo cloned on VM (or access to clone it)

---

## 🖥️ Step 1: Create a VM Instance

1. Go to: https://console.cloud.google.com/compute/instances
2. Click **"Create Instance"**
3. Use the following settings:

| Setting            | Value                      |
|--------------------|----------------------------|
| Name               | `data-eng-vm-project`      |
| Region             | `asia-southeast1-b`        |
| Machine type       | `e2-micro` (2 vCPUs, 1 GB Memory)|
| Boot disk          | Ubuntu 22.04 LTS           |
| Firewall           | ✅ Allow HTTP + HTTPS       |
| External IP        | Ephemeral (or Static if needed) |
| IP forwarding      | ❌ Off (can change later)  |

---

## 🔑 Step 2: SSH into the VM

```bash
gcloud compute ssh data-eng-vm-project --zone=asia-southeast1-b
```

## 🐳 Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/OhmSaharath/project_1_airflow_bitcoin.git
cd project_1_airflow_bitcoin

docker-compose up --build -d

docker exec -it project_1_airflow_bitcoin_webserver_1 airflow db init

docker exec -it project_1_airflow_bitcoin_webserver_1 airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin
```
