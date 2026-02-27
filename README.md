# Travel AI

Full-stack Travel AI: FastAPI backend (agent, search, scraping, monitoring) and React frontend, with optional NGINX for a single entry point.

## Project layout

- **`backend/`** — Python FastAPI app, Celery worker, Postgres, Redis, Qdrant, Ollama
- **`frontend/`** — React + Vite + TypeScript chat UI
- **Root** — `docker-compose.yml`, `nginx.conf`, `.env` for running everything together

## Quick start (Docker)

1. Create `.env` from the example and set your API key:

   ```bash
   cp .env.example .env
   # Edit .env: set API_KEY and other values (see backend/app/config.py)
   ```

2. From the repo root:

   ```bash
   docker compose up -d
   ```

3. Open in the browser:
   - **Via NGINX (recommended):** http://localhost — frontend and API on port 80
   - **Frontend only:** http://localhost:3000 (set API base URL to http://localhost:8000 or http://localhost for API)
   - **API only:** http://localhost:8000

## Running backend or frontend separately

- **Backend (API + infra):** from root, `docker compose up -d api postgres redis qdrant ollama` (and optionally `celery_worker`, `nginx`). API on port 8000.
- **Frontend (dev):** `cd frontend && npm install && npm run dev`. Use `.env` with `VITE_API_BASE_URL=http://localhost:8000` (or http://localhost if using NGINX).

## Deployment

- **Backend:** deploy `backend/` (Dockerfile + app + requirements); run with your own Postgres, Redis, Qdrant, Ollama (or equivalents).
- **Frontend:** build with `cd frontend && npm run build`; serve `dist/` with any static host, or use the frontend Docker image. Point `VITE_API_BASE_URL` at your public API URL.

See `backend/` and `frontend/` for more detail in their own READMEs.
