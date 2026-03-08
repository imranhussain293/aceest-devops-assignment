# ACEest DevOps Assignment 1 — Flask + SQLite

This repository implements a minimal REST API for **ACEest Fitness & Gym** using **Flask** with **SQLite persistence** and **Pytest** test coverage. It will be extended with **Docker**, **GitHub Actions CI**, and a **Jenkins BUILD pipeline** as part of the DevOps assignment.

## What’s implemented (current)
- Flask API endpoints for programs, clients, and progress logging
- SQLite database with `clients` and `progress` tables
- Automated tests with Pytest (4 tests passing locally)
- Containerization via Docker (Gunicorn)
- CI via GitHub Actions (lint + docker build + in-container tests)
- Jenkins BUILD / quality gate pipeline (Docker-based)

## API Endpoints

### Health
- `GET /health` → `{ "status": "healthy" }`

### Programs
- `GET /programs` → returns the available programs and their calorie factors

### Clients
- `POST /clients` → create/update a client and calculate calories

Request body:
```json
{
  "name": "JohnDoe",
  "age": 30,
  "weight": 70,
  "program": "Fat Loss (FL)"
}
```

Response:
```json
{
  "client": {
    "name": "JohnDoe",
    "age": 30,
    "weight": 70.0,
    "program": "Fat Loss (FL)",
    "calories": 1540
  }
}
```

- `GET /clients/<name>` → returns client details and up to 10 latest progress rows

### Progress
- `POST /clients/<name>/progress` → log adherence for a given week

Request body:
```json
{
  "week": "Week 10 - 2026",
  "adherence": 90
}
```

Response:
```json
{ "message": "Progress logged successfully" }
```

## Local Setup (Windows PowerShell)

```powershell
py -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

## Run the App

```powershell
py app.py
```

The server runs on: `http://localhost:5000`

## Run Tests

```powershell
py -m pytest
```

## Lint (Ruff)

```powershell
ruff check .
```

## Configuration

Environment variables:
- `DATABASE_PATH` (optional): path to the SQLite database file  
  - Default: `aceest_fitness.db`

Example:
```powershell
$env:DATABASE_PATH = "aceest_test.db"
py -m pytest
```

## Docker

Build:

```powershell
docker build -t aceest:local .
```

Run (Gunicorn):

```powershell
docker run --rm -p 5000:5000 aceest:local
```

Then:

- `GET http://localhost:5000/health`

Run tests inside the container (matches CI/Jenkins):

```powershell
docker run --rm aceest:local python -m pytest
```

## GitHub Actions CI overview

Workflow: `.github/workflows/main.yml`

Trigger:

- Every `push`
- Every `pull_request`

Stages:

1. Syntax + lint: `python -m compileall app.py` and `ruff check .`
2. Docker build: `docker build ...`
3. Tests (in-container): `docker run ... python -m pytest`

## Jenkins BUILD & quality gate overview

Pipeline: `Jenkinsfile`

High-level logic:

- Jenkins checks out the repo
- Builds the Docker image (`docker build ...`)
- Runs quality gates inside that image:
  - Syntax check (`python -m compileall app.py`)
  - Lint (`ruff check .`)
- Runs Pytest inside the same container image (`python -m pytest`)

## Jenkins (Docker Desktop) local setup

This repository includes a Docker Compose-based Jenkins setup so anyone can launch Jenkins locally and run the provided `Jenkinsfile` pipeline.

### Prereqs (Windows)

- WSL2 enabled (recommended for Docker Desktop)
- Docker Desktop installed and running (Linux containers)

Sanity check:

```powershell
docker version
```

### Start Jenkins + Docker engine (DinD)

From the repo root:

```powershell
docker compose -f docker-compose.jenkins.yml up -d --build
docker compose -f docker-compose.jenkins.yml ps
```

Open Jenkins UI:

- http://localhost:8080

Get the initial admin password:

```powershell
docker compose -f docker-compose.jenkins.yml exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Then install “Suggested plugins” and create an admin user.

Verify Jenkins can run Docker commands:

```powershell
docker compose -f docker-compose.jenkins.yml exec jenkins bash -lc "docker version"
```

### Create Jenkins job (Pipeline from SCM)

1. Jenkins → **New Item** → choose **Pipeline**
2. Under **Pipeline**:
  - **Definition**: *Pipeline script from SCM*
  - **SCM**: *Git*
  - **Repository URL**: your GitHub repo URL
  - **Branches to build**: `*/main`
  - **Script Path**: `Jenkinsfile`
3. Save → **Build Now**

Expected stages:

- Checkout
- Build Docker Image
- Quality Gate - Lint
- Test

### Stop Jenkins

```powershell
docker compose -f docker-compose.jenkins.yml down
```

Notes:

- `docker-compose.jenkins.yml` runs a Docker-in-Docker daemon (`docker:dind`) using `privileged: true` for local development.
