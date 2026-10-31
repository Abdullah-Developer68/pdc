# CSC336 - Parallel and Distributed Computing (DevOps)
## Assignment 2: Containerized Multi-Tier Web Application on AWS EC2

### 1. Database Selection: Why PostgreSQL?
For this DevOps assignment, **PostgreSQL** is the optimal choice for the following reasons:
1. **Native Docker Secrets Support**: The official PostgreSQL Docker image natively supports reading credentials directly from secret files via environment variables such as `POSTGRES_PASSWORD_FILE: /run/secrets/db_password`, `POSTGRES_USER_FILE: /run/secrets/db_user`, and `POSTGRES_DB_FILE: /run/secrets/db_name`. This eliminates the need for entrypoint workarounds or insecure plaintext credentials.
2. **Reliable Named Volume Persistence**: PostgreSQL stores its cluster in `/var/lib/postgresql/data`, which cleanly binds to the Docker named volume `pdc_db_data`. When containers are stopped, removed, or recreated, all stored data remains intact.
3. **Lightweight & Efficient**: PostgreSQL runs with minimal memory footprint (~30–50 MB RAM at idle), making it ideal for running alongside Node.js on a free-tier Amazon EC2 instance (e.g., `t2.micro` or `t3.micro` with 1 GB RAM).
4. **Clean Integration with Express**: Standard Node.js `pg` driver supports pooled connections, transactions, and robust health checks.

---

### 2. Architecture Overview
- **Frontend**: React (Vite, modern responsive dark-mode UI with live system diagnostics, Docker secrets indicator, and task management).
- **Backend**: Express.js REST API (`/api/tasks`, `/api/health`), connecting to PostgreSQL via pooled connections with automatic retry logic.
- **Static Serving**: In production, the Express container serves the compiled React build directly, allowing the entire web tier to run as a single, optimized service (`web`).
- **Database**: PostgreSQL 16 on Alpine Linux (`db`).
- **Containerization**:
  - Multi-stage `Dockerfile`:
    - **Stage 1 (Builder)**: `node:20-alpine` builds the React frontend and compiles server production dependencies.
    - **Stage 2 (Runtime)**: Minimal `node:20-alpine` runtime copying only the compiled artifacts, running as non-root user `node`.
  - `docker-compose.yml`:
    - Defines `web` (container name `pdc_web_app`) and `db` (container name `pdc_db`).
    - Uses named volume `pdc_db_data`.
    - Implements Docker Compose secrets from `./secrets/*.txt` mounted into `/run/secrets/`.

---

### 3. Local Quickstart (Testing with Docker)

1. **Verify or create the secret files in `secrets/`**:
   - `secrets/db_password.txt`
   - `secrets/db_user.txt`
   - `secrets/db_name.txt`

2. **Build and launch the containers**:
   ```bash
   docker compose up --build -d
   ```

3. **Check container status and logs**:
   ```bash
   docker compose ps
   docker compose logs -f
   ```

4. **Access the application**:
   - Web application: Open [http://localhost:5000](http://localhost:5000) or [http://localhost:80](http://localhost:80)
   - Health endpoint: [http://localhost:5000/api/health](http://localhost:5000/api/health)

5. **Test Data Persistence**:
   - Add a task through the web UI.
   - Stop and remove the containers:
     ```bash
     docker compose down
     ```
   - Restart the containers:
     ```bash
     docker compose up -d
     ```
   - Refresh the page: Your data is preserved by the `pdc_db_data` named volume!

---

### 4. Step-by-Step Deployment Guide to AWS EC2

#### Step 1: Launch an Amazon EC2 Instance
1. Log in to the [AWS Management Console](https://console.aws.amazon.com/ec2/).
2. Navigate to **EC2** > **Instances** > **Launch an instance**.
3. Configure the instance:
   - **Name**: `PDC-DevOps-Assignment2`
   - **AMI**: Ubuntu Server 24.04 LTS (HVM), SSD Volume Type
   - **Instance type**: `t2.micro` or `t3.micro` (Free tier eligible)
   - **Key pair**: Select an existing key pair or create a new one (download the `.pem` file).
4. **Network Settings / Security Group**:
   Allow the following inbound rules:
   - **SSH**: Port `22`, Source: `Anywhere` (`0.0.0.0/0`) or `My IP`
   - **HTTP**: Port `80`, Source: `Anywhere` (`0.0.0.0/0`)
   - **Custom TCP**: Port `5000`, Source: `Anywhere` (`0.0.0.0/0`)
5. Click **Launch Instance**. Note the **Public IPv4 address** (e.g., `54.210.xx.xx`).

#### Step 2: Connect to the EC2 Instance
From your local terminal:
```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>
```

#### Step 3: Install Docker and Docker Compose on EC2
Run the following commands on the EC2 instance:
```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io docker-compose-v2 git

# Add ubuntu user to docker group
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# Verify Docker installation
docker --version
docker compose version
```

#### Step 4: Transfer / Clone Project to EC2
Option A: Clone via Git (Recommended)
```bash
git clone <your-github-repo-url>
cd PDC
```

Option B: Transfer files via `scp` from your local machine:
```bash
scp -i your-key.pem -r /home/abdullah/Desktop/Dev/PDC ubuntu@<EC2-PUBLIC-IP>:~/PDC
```

#### Step 5: Start the Multi-Container Application on EC2
On the EC2 instance inside the `PDC` directory:
```bash
# Build and start services in detached mode
docker compose up --build -d

# Verify both containers are running and healthy
docker compose ps
```

#### Step 6: Access Application and Capture Evidence
1. Open your browser and navigate to:
   ```text
   http://<EC2-PUBLIC-IP>
   ```
2. You will see the **Cloud Task Manager** running live with:
   - Container hostname (matching the EC2 container ID).
   - PostgreSQL status: Active and connected via Docker Secrets.
   - Named volume persistence verified.
3. Take screenshots of:
   - The AWS EC2 console showing your running instance and public IP.
   - The terminal running `docker compose ps` and `docker compose logs`.
   - The browser showing the web application and adding/persisting tasks.
