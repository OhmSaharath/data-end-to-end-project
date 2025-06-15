# Airflow 2.8.2 + Docker + GCP (VM Instance) RoadmapMore actions

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

4. Let's create firewalls rule for port 8080 and 5432.

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

| Setting              | Value              |
|----------------------|--------------------|
| name-rules           | allow-postgres-5432 |
| logs                 | off                |
| Network              | default            |
| Priority             | 1000               |
| Direction of traffic | ingress            |
| Action on match      | Allow              |
| IPv4 ranges          | 0.0.0.0/0          |
| Protocols and ports  | TCP, 5432          |

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

1. Let's create "Airflow"(You can change a name of folder) folder.
```bash
mkdir airflow-2.8.2
```
2. Go to "airflow-2.8.2" folder.
```bash
# go to path "Airflow"
cd airflow-2.8.2

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
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS                    PORTS                                         NAMES
8998b72a7018   apache/airflow:2.8.2   "/usr/bin/dumb-init …"   40 minutes ago   Up 40 minutes (healthy)   8080/tcp                                      airflow-282-airflow-triggerer-1
ade215024c70   apache/airflow:2.8.2   "/usr/bin/dumb-init …"   40 minutes ago   Up 40 minutes (healthy)   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp   airflow-282-airflow-webserver-1
26dac849853e   apache/airflow:2.8.2   "/usr/bin/dumb-init …"   40 minutes ago   Up 40 minutes (healthy)   8080/tcp                                      airflow-282-airflow-worker-1
34d1be8a090e   apache/airflow:2.8.2   "/usr/bin/dumb-init …"   40 minutes ago   Up 40 minutes (healthy)   8080/tcp                                      airflow-282-airflow-scheduler-1
dd008978ceb9   postgres:13            "docker-entrypoint.s…"   40 minutes ago   Up 40 minutes (healthy)   5432/tcp                                      airflow-282-postgres-1
675cca046001   redis:latest           "docker-entrypoint.s…"   40 minutes ago   Up 40 minutes (healthy)   6379/tcp                                      airflow-282-redis-1
```
### After docker run
Let's go to ```http://<EXTERNAL_ID>:8080```
You'll see UI interface of airflow.

## 😎 Step 4: Create user airflow.
1. let's run this command for bash.
```bash
docker exec -it <container-name> bash
```
2. You can see container-name from ```docker ps``` in last column.
3. After run, You can use "airflow" command.
```bash
# create an admin user
# You can change info from this.
airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org
```
4. If you need save logs when you `docker compose down`.
```bash
volumes:
  postgres-db-volume:
  airflow-logs: # This line is important because if you don't have this line. When you `docker compose down` all config ex. USER will lost after down docker. You'll need to save this logs for when you start docker again.
```
5. If you need to close example.
```bash
# Let's go to path airflow folder.
cd airflow-2.8.2

# check file
ls -la

# Let's edit file docker-compose.yaml
nano docker-compose.yaml
```
### Let's find 
```bash
# Change from 'true' to 'false'
environment:
....................
    AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
....................
```
