# COMSATS University, Islamabad
## Department of Computer Science
### CSC336 - Parallel and Distributed Computing (DevOps)
**Assignment 2 Report**

- **Student Name**: [Your Name]
- **Registration Number**: [Your Reg ID]
- **Class**: BSE VII-A/B
- **Instructor**: Dr. Muhammad Imran
- **Live AWS EC2 URL**: `http://<YOUR_EC2_PUBLIC_IP>`

---

## 1. Application Overview
The application developed for this assignment is a containerized full-stack **Cloud Task & Resource Manager**. It allows users to create, view, update, and manage persistent task records while monitoring real-time container metrics and database health.

### Technology Stack:
- **Frontend**: React (built with Vite) providing a responsive interface with real-time health polling and Docker metadata display.
- **Backend**: Express.js REST API providing CRUD operations and database health status endpoints.
- **Database Server**: **PostgreSQL 16 (Alpine)**, selected for native Docker secrets integration, strict ACID compliance, and named volume persistence.
- **Containerization**: Multi-stage Dockerfile (Build stage and lightweight Alpine runtime stage).
- **Orchestration**: Docker Compose with named volume persistence and Docker Compose secrets.
- **Cloud Infrastructure**: Amazon Web Services (AWS) EC2 virtual machine instance (IaaS).

---

## 2. Micro-Steps & Implementation

### Micro-Step 1: Multi-stage Dockerfile Implementation
A two-stage Dockerfile was authored to optimize the final image size and enforce secure separation between the build environment and production runtime:
- **Stage 1 (Builder)**: Utilizes `node:20-alpine` to install full dependencies, compile the React production bundle, and install production server dependencies.
- **Stage 2 (Runtime)**: Utilizes a clean `node:20-alpine` image, copying only the compiled frontend assets into the Express public directory and the pruned `node_modules`. It runs as the non-root `node` user for security hardening.

*(Insert screenshot of Dockerfile and local docker build process)*

### Micro-Step 2: Docker Compose Configuration & Explicit Container Naming
`docker-compose.yml` was configured to launch two interconnected services without relying on prebuilt images for the application tier:
- **`web` service**: Explicitly named `pdc_web_app`, configured to build directly from `./Dockerfile`.
- **`db` service**: Explicitly named `pdc_db`, running `postgres:16-alpine`.

*(Insert screenshot of docker-compose.yml)*

### Micro-Step 3: Database Named Volume for Persistence
To ensure that all stored records persist across container restarts, teardowns, and updates, a named volume (`pdc_db_data`) is attached to `/var/lib/postgresql/data`.

*(Insert screenshot verifying data persists after running `docker compose down` and `docker compose up -d`)*

### Micro-Step 4: Managing Sensitive Data via Docker Secrets
Instead of hardcoding database credentials or passing them via plaintext environment variables, Docker Compose secrets were implemented:
- Three secrets defined: `db_password`, `db_user`, and `db_name`.
- Files stored securely in `./secrets/` directory on the host.
- Mounted at runtime into `/run/secrets/` inside the containers.
- PostgreSQL reads them directly via `POSTGRES_PASSWORD_FILE`, `POSTGRES_USER_FILE`, and `POSTGRES_DB_FILE`.
- The Express backend dynamically resolves credentials from `/run/secrets/`.

*(Insert screenshot of secret file paths and docker-compose secrets block)*

### Micro-Step 5: AWS EC2 Provisioning and Cloud Deployment
1. Launched an Amazon EC2 `t2.micro` / `t3.micro` instance running Ubuntu 24.04 LTS.
2. Configured Security Group Inbound Rules:
   - Port 22 (SSH)
   - Port 80 (HTTP)
   - Port 5000 (Custom TCP)
3. Installed Docker and Docker Compose plugin on EC2.
4. Cloned project repository and executed `docker compose up --build -d`.

*(Insert screenshot of AWS EC2 Console showing running instance and public IP)*
*(Insert screenshot of EC2 terminal running `docker compose ps` and `docker compose logs`)*
*(Insert screenshot of browser accessing `http://<EC2_PUBLIC_IP>` displaying connected database, container hostname, and added tasks)*

---

## 3. Configuration Files

### Multi-stage Dockerfile
```dockerfile
# See repository Dockerfile
```

### Docker Compose File
```yaml
# See repository docker-compose.yml
```

### Docker Secrets Definition
```yaml
secrets:
  db_password:
    file: ./secrets/db_password.txt
  db_user:
    file: ./secrets/db_user.txt
  db_name:
    file: ./secrets/db_name.txt
```
