# Airflow + Docker + GCP + Postgresql
# Detailed Infrastructure Setup Guide

This document provides a complete, step-by-step guide to setting up the necessary infrastructure from scratch on Google Cloud Platform (GCP) to run the CoinGecko ETL Pipeline.

## Step 1: Create a GCP VM Instance & Firewall Rules

First, we need a virtual server to host our Docker environment.

### 1.1. Create the VM Instance

1. Navigate to the **Compute Engine > VM instances** page in your GCP Console.
2. Click **"CREATE INSTANCE"**.
3. Configure the instance with the following specifications:
   - **Name:** `gcp-docker-airflow`
   - **Region:** `asia-southeast1` (Singapore)
   - **Zone:** `asia-southeast1-b`
   - **Machine configuration:**
     - Series: **E2**
     - Machine type: **e2-medium** (2 vCPUs, 4 GB Memory)
   - **Boot disk:**
     - Click **"Change"**.
     - Operating system: **Debian**
     - Version: **Debian GNU/Linux 12 (bookworm)**
     - Click **"Select"**.
   - **Firewall:**
     - Check ✅ **Allow HTTP traffic**
     - Check ✅ **Allow HTTPS traffic**
4. Click **"Create"**. Wait for the instance to be created and get its External IP address.

### 1.2. Create Firewall Rules

We need to open specific ports for the Airflow UI and for remote PostgreSQL connections.

1. In the GCP Console, navigate to **VPC network > Firewall**.
2. Click **"CREATE FIREWALL RULE"**.
3. **Rule for Airflow UI (Port 8080):**
   - **Name:** `allow-airflow-ui`
   - **Direction of traffic:** `Ingress`
   - **Action on match:** `Allow`
   - **Targets:** `All instances in the network` (or use a specific target tag that you've added to your VM).
   - **Source IPv4 ranges:** Enter your own public IP address followed by `/32` (e.g., `123.45.67.89/32`). This is the most secure option. To allow access from any IP (less secure), use `0.0.0.0/0`.
   - **Protocols and ports:** Select `Specified protocols and ports`, check `TCP`, and enter `8080`.
   - Click **"Create"**.
4. **Rule for PostgreSQL (Port 5432):**
   - Create another rule with the same settings as above, but with these changes:
   - **Name:** `allow-postgres-external`
   - **Protocols and ports:** For `TCP`, enter `5432`.
   - Click **"Create"**.

---

## Step 2: Install Docker and Set User Permissions

Next, SSH into your newly created VM and install the Docker environment.

```bash
# SSH into your VM first
gcloud compute ssh gcp-docker-airflow --zone=asia-southeast1-b
```

Once inside the VM, run the following commands:

```bash
# 1. Update package lists
sudo apt-get update

# 2. Install prerequisite packages
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

# 3. Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL [https://download.docker.com/linux/debian/gpg](https://download.docker.com/linux/debian/gpg) | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 4. Add the Docker repository to Apt sources
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] [https://download.docker.com/linux/debian](https://download.docker.com/linux/debian) \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Update package lists again with the new repo
sudo apt-get update

# 6. Install Docker Engine, CLI, and Docker Compose
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 7. Add your current user to the 'docker' group to run docker commands without 'sudo'
# This is a critical step for convenience and for Airflow's permissions.
sudo usermod -aG docker $USER

# 8. IMPORTANT: Log out and log back in for the group changes to take effect.
exit
```

After you log back in, verify the installation by running `docker --version`.

---

## Step 3: Set up Airflow using Docker Compose

We will use the official `docker-compose.yml` file from the Airflow project.

```bash
# Make sure you are in your home directory
cd ~

# 1. Create a project directory
mkdir project-data-pipeline
cd project-data-pipeline

# 2. Download the official docker-compose.yml file
curl -LfO "[https://airflow.apache.org/docs/apache-airflow/2.8.2/docker-compose.yaml](https://airflow.apache.org/docs/apache-airflow/2.8.2/docker-compose.yaml)"

# 3. Create necessary directories that will be mounted into the containers
mkdir -p ./dags ./logs ./plugins ./src

# 4. Create the .env file for setting the correct file permissions
# This ensures that files created by Airflow inside Docker are owned by you on the host machine.
echo "AIRFLOW_UID=$(id -u)" > .env
echo "AIRFLOW_GID=$(id -g)" >> .env

# 5. Initialize the Airflow environment and database
# The airflow-init service will run, create the default 'airflow' user, and then exit.
docker-compose up airflow-init

# 6. Run all services in the background
docker-compose up -d
```

Wait a few minutes for all services to become healthy. You can check their status with `docker ps`.

---

## Step 4: Set up Python Project Folder and Virtual Environment

While the project logic will run inside Docker, it's a best practice to have a local development environment for testing and dependency management.

```bash
# Ensure you are in the project root (e.g., ~/project-data-pipeline)

# 1. Set up a Python virtual environment
python3 -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate

# 3. Create the requirements.txt file with necessary libraries
# This file will list all Python packages your project needs.
cat > requirements.txt << EOF
apache-airflow[postgres,http]
pandas
requests
EOF

# 4. Install all dependencies from the requirements file
pip install -r requirements.txt
```

Your Python scripts will be placed inside the `src/` directory. The virtual environment (`venv`) is used for local testing and validation, while the Docker containers have their own isolated Python environment.

---

## Step 5: Edit Path in `docker-compose.yaml`

To allow your DAGs in the `dags/` folder to import custom modules from the `src/` folder, you must edit the `docker-compose.yaml` file.

1.  Open `docker-compose.yaml` with a text editor (e.g., `nano docker-compose.yaml`).
2.  Find the `x-airflow-common:` section at the top.
3.  Modify the `volumes:` and `environment:` sections as shown below:

```yaml
x-airflow-common:
  &airflow-common
  # ... other settings ...
  environment:
    &airflow-common-env
    # ... other environment variables ...
    PYTHONPATH: /opt/airflow  # <-- ADD THIS LINE
    # ...
  volumes:
    - ./dags:/opt/airflow/dags
    - ./src:/opt/airflow/src      # <-- ADD THIS LINE
    - ./logs:/opt/airflow/logs
    - ./plugins:/opt/airflow/plugins
  # ...
```

After saving the file, you must **recreate the containers** for the changes to take effect:

```bash
docker-compose down && docker-compose up -d
```

### 5.1. Understanding Data Persistence and Ports

#### PostgreSQL Port (`5432`)

In the `services:` section, under the `postgres` service definition, you will find this block:
```yaml
  ports:
    - "5432:5432"
```
This is the **Port Mapping**. It tells Docker to forward any traffic that arrives on **port 5432 of your GCP VM** to **port 5432 inside the PostgreSQL container**. This is what allows you to connect to the database from your desktop using a tool like DBeaver or pgAdmin.

#### Top-Level Volumes (e.g., `postgres-db-volume`)

At the very end of the `docker-compose.yaml` file, you see this block:
```yaml
volumes:
  postgres-db-volume:
  airflow-logs:
```
This section **defines named volumes**.
* **`postgres-db-volume`**: This is the most important volume for data persistence. It is used by the `postgres` service (`- postgres-db-volume:/var/lib/postgresql/data`) to store the **entire PostgreSQL database**. This includes all Airflow metadata (users, connections, variables, DAG run history) and any data you load with your ETL pipeline (like the `bronze.data_coin_list` table). When you run `docker-compose down`, this volume is **not** deleted, so your data is safe.
* **`airflow-logs`**: In the default configuration, this named volume is defined but not actively used. The Airflow task logs are saved to your host machine via the **bind mount** you see in the `x-airflow-common` section: `- ./logs:/opt/airflow/logs`. This makes it easy for you to access the logs directly from the `./logs` folder in your project directory.

---

## Step 6: Set up GitHub

Finally, set up a Git repository to track your project's history and collaborate.

1.  **Create a new repository on GitHub.com.** Do not initialize it with a README or .gitignore.
2.  In your project folder on the VM, initialize a local Git repository:
    ```bash
    git init
    ```
3.  **Configure your Git Username and Email.** This is a crucial step so that your commits are correctly attributed to your GitHub account.
    ```bash
    # Replace with your GitHub username and email
    git config --global user.name "Your Name"
    git config --global user.email "your.email@example.com"
    ```
4.  **Create a `.gitignore` file** to exclude temporary files, logs, and secrets:
    ```bash
    cat > .gitignore << EOF
    # Python virtual environment
    venv/

    # Python cache and compiled files
    __pycache__/
    *.pyc

    # Docker environment file (contains secrets)
    .env

    # Airflow logs
    logs/

    # IDE and OS-specific files
    .vscode/
    .idea/
    .DS_Store
    EOF
    ```
5.  **Add all your project files and commit them:**
    ```bash
    git add .
    git commit -m "Initial commit of CoinGecko ETL project"
    ```
6.  **Link your local repository to the remote one on GitHub and push:**
    ```bash
    # Replace the URL with your own repository's URL
    git remote add origin [https://github.com/](https://github.com/)[your-github-username]/[your-repo-name].git
    git branch -M main
    git push -u origin main
    ```

Your project is now fully set up and version-controlled on GitHub.
