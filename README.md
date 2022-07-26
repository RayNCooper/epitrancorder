# Epitrancorder Backend
## Requirements
Easy Setup:
- [Docker (includes Compose)](https://www.docker.com/)

Manual:
- [Python](https://www.python.org/) 3.9 or later
- [Poetry](https://github.com/python-poetry/poetry)

## Setup:
Docker-Compose (incl. Frontend):
1. `cd ..`
2. `docker compose up`

Via Dockerfile:
1. `docker build -t epitrancorder-backend .`
2. `docker run -p 8000:8000 epitrancorder-backend`

Manual:
1. `poetry install`
2. `poetry run uvicorn main:app` 
