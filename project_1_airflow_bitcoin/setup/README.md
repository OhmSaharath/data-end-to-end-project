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
