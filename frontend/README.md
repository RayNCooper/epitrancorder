# Epitrancorder Frontend
## Requirements
Easy Setup:
- [Docker (includes Compose)](https://www.docker.com/)

Manual:
- [NPM/Node.js](https://docs.npmjs.com/cli/v7/configuring-npm/install)
## Setup:
Docker-Compose (incl. Backend):
1. `cd ..`
2. `docker compose up`

Via Dockerfile:
1. `docker build -t epitrancorder-frontend .`
2. `docker run -p 8080:8080 epitrancorder-frontend`

Manual:
1. `npm install`
2. `npm run dev` 
