# ACEest DevOps Assignment 1

This repo is for Assignment 1 (ACEest Fitness & Gym). It starts with a minimal Flask API and Pytest tests, and will be extended with Docker, GitHub Actions CI, and Jenkins.

## Prerequisites

- Windows PowerShell
- Python (via `py` launcher) and/or a virtual environment

## Setup (virtual environment)

From the repo folder:

```powershell
py -m venv .venv
# If PowerShell blocks activation, you can run this once per terminal session:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

## Run the app

```powershell
py app.py
```

Endpoints:

- `GET /health` → returns `{ "status": "healthy" }`
- `GET /programs` → returns program list + calorie factors

## Run tests

```powershell
py -m pytest
```
