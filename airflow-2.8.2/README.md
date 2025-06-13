# Airflow 2.8.2 + Docker + GCP (VM Instance) Roadmap

## ☁️ GCP Setup
## 🖥️ Step 1: Create a VM Instance

1. Go to: https://console.cloud.google.com/compute/instances
2. Click **"Create Instance"**
3. Use the following settings:

| Setting            | Value                      |
|--------------------|----------------------------|
| Name               | `gcp-docker-airflow`      |
| Region             | `asia-southeast1-b`        |
| Machine type       | `e2-medium (2 vCPUs, 4 GB Memory)`|
| Boot disk          | debian-12-bookworm-v20250610 |
| Firewall           | ✅ Allow HTTP + HTTPS       |
| External IP        | Ephemeral (or Static if needed) |
| IP forwarding      | ❌ Off (can change later)  |

4. Let's create firewalls rule for port 8080.
| Setting              | Value              |
|----------------------|--------------------|
| name-rules           | allow-airflow-8080 |
| logs                 | off                |
| Network              | default            |
| Priority             | 1000               |
| Direction of traffic | ingress            |
| Action on match      | Allow              |
| IPv4 ranges          | 0.0.0.0/0          |
| Protocols and ports  | TCP, 8080          |

5. Let's create global


## 🐳 Step 2: Install docker
### Reference : https://docs.docker.com/engine/install/debian/

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
### Set $USER for run command docker
```bash
sudo usermod -aG docker $USER
```
## 🎶 Step 3: Airflow

1. Let's create "Airflow" folder.
2. Go to "Airflow" folder.
```bash
# go to path "Airflow"
cd Airflow

# Linux User
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env

# download docker-compose.yaml (!! RECCOMMEND Version 2.8.2 BECAUSE IT'S STABLE)
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.2/docker-compose.yaml'

# (Only)First-time let's run.
docker compose up airflow-init

# After finished
docker compose up -d

# Check docker
docker ps
```
### You should be see all text.
```bash
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS                    PORTS                              NAMES
247ebe6cf87a   apache/airflow:3.0.2   "/usr/bin/dumb-init …"   3 minutes ago    Up 3 minutes (healthy)    8080/tcp                           compose_airflow-worker_1
ed9b09fc84b1   apache/airflow:3.0.2   "/usr/bin/dumb-init …"   3 minutes ago    Up 3 minutes (healthy)    8080/tcp                           compose_airflow-scheduler_1
7cb1fb603a98   apache/airflow:3.0.2   "/usr/bin/dumb-init …"   3 minutes ago    Up 3 minutes (healthy)    0.0.0.0:8080->8080/tcp             compose_airflow-api_server_1
74f3bbe506eb   postgres:13            "docker-entrypoint.s…"   18 minutes ago   Up 17 minutes (healthy)   5432/tcp                           compose_postgres_1
0bd6576d23cb   redis:latest           "docker-entrypoint.s…"   10 hours ago     Up 17 minutes (healthy)   0.0.0.0:6379->6379/tcp             compose_redis_1
```
### After docker run
Let's go to http://<EXTERNAL_ID>:8080
You'll see UI interface of airflow.
