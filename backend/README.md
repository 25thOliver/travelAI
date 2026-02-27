# Travel AI — Backend

FastAPI app, Celery worker, and supporting services. Designed to run via Docker from the repo root; env is loaded from root `.env`.

## Layout

- `app/` — FastAPI app, agents, API routes, DB, services, scraping
- `requirements.txt` — Python dependencies
- `Dockerfile` — Image for `api` and `celery_worker` services

## Run via Docker (from repo root)

```bash
docker compose up -d api postgres redis qdrant ollama
# Optional: celery_worker, nginx, frontend
```

## Run API locally (no Docker)

Create a virtualenv, install deps, set env (e.g. from root `.env`), then:

```bash
uvicorn app.main:app --reload --port 8000
```

Ensure Postgres, Redis, Qdrant, and Ollama are reachable at the URLs in your env.
