# Django CSV Dataset processing 

A django project that allow to process CSV heavy 2 dimensional data array to show curves

## Requirements
- Python 3.11
- Django > 3.2 < 4.0
- Postgresql

## ⚙️ Configure your environment

First, install python-uv package, this package allows to manage python the project and dependencies efficiently.
Furthermore, like poetry it ensuring running reproductibility using a lock file.

### 1. Install `python-uv` Package Manager
`pip install python-uv`

### 2. Create your virtual env vile and activate it:
`uv venv .venv`
`source .venv/bin/activate   # On Windows: .venv\Scripts\activate`

### 3. Install and lock the packages with uv using pyproject.toml file:
`uv sync` 
or
`uv sync --extra test` for test environment
`uv lock`


## 🚀 Deployment

## Option 1: Deploy with default django dev web server (Only recommanded for local developpement)
python manage.py runserver 8000
## Option 2: Deploy with docker compose
docker-compose up --build 

