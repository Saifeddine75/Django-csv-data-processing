## Introduction

You will be provided a couple of \*.csv files. These files will consist of four columns (timestamps, x, y and z) containing numbers.

The website should allow a user to upload one of the csv files and compute the min, max,
mean, median and standard deviation of each axis as well as the norm.
Those results should be displayed back to the user and the user should be able to go back to the results of previously uploaded files.

Bonus:

- Plot the values of x, y, z and the norm on the frontend
- Deploy the website

## Development

The provided code is a skeleton of the final project you are to deliver. It consists of:

- A Django backend in directory "backend"
- A NextJS frontend in directory "frontend"
- A .env.dist file listing the environment variables you are to provide in a .env file
- A docker-compose.yml file for launching the services

You need to use a Django backend but you can use whatever JS based frontend solution or framework. The one we provide is based on NextJS.

## Evaluation criteria

- Understanding of the assignement
- The solution should be fully functional by following the steps in the README file and ready for deployment (local deployment is sufficient)
- Be prepared to justify your implementation, technological choices and architecture.
- The code should be clear, well structured and easy to read
- The UI should be simple and easy to understand. We value a visually appealing UI design but we understand that this is a time-limited task, so don't spend an excessive amount of time on it.

## The Backend:Django CSV Dataset processing

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
