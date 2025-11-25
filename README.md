# GeoSense — Full Project (Option A)

This repository contains a production-ready skeleton for **GeoSense**:
- Frontend: Vite + React + MapLibre (TomTom tiles)
- Backend: Flask + SQLAlchemy + PostGIS
- TomTom routing integration (backend service)
- Docker + docker-compose for local development
- Report generation (PDF/CSV) and basic traffic/POI endpoints

---

## Contents
- `frontend/` — React app (Vite). Uses MapLibre for TomTom tiles and talks to backend for routing.
- `backend/` — Flask app with routes, services, models, PostGIS support.
- `docker-compose.yml` — brings up PostGIS DB, backend, and frontend.
- `nginx/` — optional nginx config for reverse proxy.
- `Makefile` — helper targets for building and running locally.

---

## Prerequisites (on your machine)
You can run everything with Docker, which is the recommended approach.

Required:
- Docker (Engine) — https://docs.docker.com/get-docker/
- docker-compose (v2) — often bundled with Docker Desktop
- (Optional) Node.js + npm if you want to run frontend locally without Docker

For development inside VS Code:
- VS Code (latest) — https://code.visualstudio.com/
- Recommended extensions: Python, Pylance, Docker, ESLint, Prettier, Tailwind CSS IntelliSense, Remote - Containers (optional)

---

## Quick start (Docker, recommended)

1. Copy `.env.example` to `.env` at the project root (create a `.env` file) and set your TomTom key:
   ```
   TOMTOM_API_KEY=your_real_tomtom_key
   ```

2. Build and start services:
   ```
   make up
   ```
   This runs `docker-compose up -d --build` and exposes:
   - Frontend (Vite dev) at http://localhost:5173
   - Backend (Gunicorn) at http://localhost:8000
   - PostGIS DB on port 5432

3. Initialize PostGIS extensions (run once after DB is healthy):
   ```
   make init-db
   ```
   This runs SQL to create `postgis` and `postgis_topology` extensions inside the DB.

4. Open the frontend:
   Visit http://localhost:5173 and plan routes via the UI.

5. View backend health:
   ```
   curl http://localhost:8000/health
   ```

---

## Running frontend locally (without Docker)
1. Install Node.js & npm
2. From the `frontend/` folder:
   ```
   npm install
   VITE_TOMTOM_API_KEY=your_key npm run dev
   ```

By default Vite proxies `/api` to `http://localhost:8000` (see `vite.config.js`).

---

## Running backend locally (without Docker)
1. Create Python venv:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt
   ```
2. Set env vars:
   ```
   export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/geosense
   export TOMTOM_API_KEY=your_key
   ```
3. Start DB (Postgres + PostGIS) locally or via `docker-compose` (recommended).
4. Initialize DB extensions (see `init-db` target).
5. Run backend:
   ```
   cd backend
   python -m app.main
   ```
   Or use gunicorn:
   ```
   gunicorn -b 0.0.0.0:8000 app.main:app --workers 3
   ```

---

## VS Code — recommended setup & tips

1. Open the repository folder in VS Code.
2. Install these recommended extensions:
   - Python (ms-python.python)
   - Pylance
   - Docker
   - ESLint
   - Prettier - Code formatter
   - Tailwind CSS IntelliSense
   - Remote - Containers (optional)

3. Recommended tasks (you can create `.vscode/tasks.json`):
   - `make up` — Start the stack
   - `make down` — Stop the stack
   - `make logs` — Tail backend logs

4. Optional: Use Dev Containers / Remote Containers — create a `.devcontainer` to run the workspace inside a consistent container.

---

## Post-deploy notes & next steps
- Replace in-process TTL cache with Redis for multi-instance deployments.
- Add authentication + rate limiting for public endpoints.
- Add tests (pytest) and CI pipeline.
- Add monitoring (Prometheus) and centralized logging (ELK / Loki + Grafana).
- Use a managed secrets store (AWS Secrets Manager, HashiCorp Vault, etc.) for TOMTOM_API_KEY.

---

## Troubleshooting
- If the frontend can't reach the backend in dev, check `vite.config.js` proxy settings and backend port.
- If database errors occur, ensure PostGIS container is healthy and extensions are created.
- TomTom API errors: ensure `TOMTOM_API_KEY` is valid and has routing/tiles permissions. Monitor rate limits.

--- 
