# Travel AI

A full-stack travel assistant that helps users discover destinations, plan trips, and explore travel recommendations. The project contains a FastAPI backend (with scraping, search, vector embeddings, and agent capabilities) and a React + Vite frontend chat UI — designed so developers can run the whole stack with Docker or run parts locally for development.

This README is written for both non-technical readers (what this project is and how to use it) and technical readers (how to run, configure, develop, and deploy it).

Table of contents
- What is Travel AI?
- Features
- Architecture at a glance
- Quick start (Docker, recommended)
- Run locally (backend / frontend separately)
- Configuration (.env and credentials)
- Development notes (testing, linting, building)
- Troubleshooting & FAQs
- Contributing
- License & credits

What is Travel AI?
- For non-technical users: Travel AI is an interactive web app where you can ask questions like "Tell me about Hell's Gate National Park" or "Plan a 7-day Kenya safari" and get helpful, context-aware travel guidance. The UI is a simple chat interface — similar to a conversation with a travel agent.
- For technical users: Travel AI is a modular codebase that combines web APIs, background tasks, scraping tools, vector stores and an LLM-driven agent to provide conversational search and planning.

Key features
- Conversational chat interface (React + Vite)
- FastAPI backend with endpoints for chat, agent, search, scraping, and health checks
- Background processing with Celery (for scraping and scheduled tasks)
- Vector search/embeddings support (e.g., Qdrant) for retrieval-augmented responses
- Optional Ollama / local LLM integrations (or remote LLMs via environment configuration)
- Docker Compose setup to run all services locally (Postgres, Redis, Qdrant, Ollama, API, frontend)

Architecture (high-level)
- Frontend (React + Vite)
  - Chat UI, settings, local storage for API keys
  - Calls backend endpoints (agent/chat/search)
- Backend (FastAPI)
  - API routes: chat, agent, scraping, health, monitoring
  - Services: embedding, vector service, LLM adapter, scrape service
  - DB: Postgres for metadata; Redis for caching/queues; Qdrant for vector storage
  - Background worker: Celery for async tasks and scraping jobs
- Optional components:
  - Ollama (local LLM runtime) or remote LLM provider
  - NGINX for a single entry point in production

Quick start (Docker Compose — recommended)
- Summary: Use the provided `docker-compose.yml` to bring up the API, frontend, Postgres, Redis, Qdrant and optional services (Ollama, Celery worker). This is the simplest way to run the entire stack locally.
- Steps:

1) Prepare environment
```bash
cp .env.example .env
# Edit .env and set required values:
# - API_KEY (frontend <> backend shared secret)
# - POSTGRES_* (database connection)
# - REDIS_URL (broker + cache)
# - QDRANT_URL (vector store)
# - OLLAMA_URL (optional local LLM)
```

2) Start the stack
```bash
docker compose up -d --build
```

3) Verify services and view logs
```bash
# List running containers and status
docker compose ps

# Stream logs for the API (replace `api` with service name if different)
docker compose logs -f api
```

4) Open the app
- If `nginx`/proxy is enabled in compose: http://localhost (recommended)
- Frontend dev server (if running separately): http://localhost:3000
- Backend API (direct): http://localhost:8000

Notes
- If you edit `.env` after containers are running, restart the stack:
```bash
docker compose down
docker compose up -d --build
```
- To stop and remove containers:
```bash
docker compose down
```

Running the frontend and backend separately (for development)
- Frontend (dev):
```/dev/null/commands.sh#L1-6
cd frontend
npm install
npm run dev
# By default set VITE_API_BASE_URL to your backend (e.g. http://localhost:8000) in a .env file used by the frontend
```

- Backend (dev):
```/dev/null/commands.sh#L1-8
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Set environment variables (e.g. via .env or export) and run:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Key endpoints (examples)
- GET /health — health checks
- POST /agent/chat or POST /chat — send chat messages (headers may require an API key if configured)
- POST /scrape — start a scrape job for a destination (used by internal tools)

Configuration (.env)
- Copy `.env.example` to `.env` in the project root.
- Key settings you will typically set:
  - API_KEY — shared secret for the frontend to call the API
  - DATABASE_URL — Postgres connection string
  - REDIS_URL — Redis connection string
  - QDRANT_URL — Qdrant vector db URL (if used)
  - OLLAMA_URL / LLM provider configs — for local model hosting or remote API keys
- The frontend expects `VITE_API_BASE_URL` (or you can use the root NGINX to proxy).

Common development tasks
- Install frontend dependencies: `cd frontend && npm install`
- Start frontend: `npm run dev`
- Build frontend for production: `npm run build`
- Install backend dependencies: `pip install -r backend/requirements.txt`
- Run backend: `uvicorn app.main:app --reload`
- Run Celery worker:
```/dev/null/commands.sh#L1-6
# from project root (example)
celery -A backend.app.celery_app worker --loglevel=info
# or use docker-compose worker service
```

Testing & linting
- Frontend:
  - Run tests: `npm run test`
  - Lint: `npm run lint`
- Backend:
  - Use pytest (if tests exist) or run unit tests per module
  - Ensure you set up a test database for integration tests

Troubleshooting (Docker Compose–focused)
- Service won't start or exits immediately:
  - Run `docker compose ps` to check container statuses.
  - Use `docker compose logs <service>` (for example `docker compose logs api` or `docker compose logs frontend`) to inspect errors.
  - Common fixes: missing variables in `.env`, DB not ready, or port conflicts on the host.
- API returns 401 Unauthorized:
  - Make sure `API_KEY` in the root `.env` matches the key saved in the frontend Settings UI.
  - If you're using a proxy (NGINX), ensure the proxy forwards the `X-API-Key` header to the API.
- Frontend shows blank page / static assets fail:
  - If served by the container, check `docker compose logs frontend` or `docker compose logs nginx`.
  - For local development, run:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
- Database (Postgres) connection errors:
  - Check `docker compose logs postgres`. Confirm `POSTGRES_*` env vars are correct and the DB container is healthy.
  - If you changed the DB schema, you may need to run migrations or recreate the DB (use `docker compose down --volumes` to remove volumes if you want a fresh DB).
- Celery / background jobs not running:
  - Confirm worker service is up (`docker compose ps`) and inspect `docker compose logs worker` (service name may vary).
  - Ensure `REDIS_URL` is correct and Redis container is healthy.
- Qdrant / embeddings issues:
  - Verify the `qdrant` service is up and reachable. Inspect `docker compose logs qdrant`.
  - If vector search returns no results, re-run indexing tasks or the scraping pipeline that populates embeddings.
- After updating `.env` or Dockerfile:
  - Rebuild and restart:
    ```bash
    docker compose down
    docker compose up -d --build
    ```
- Still stuck?
  - Collect these outputs and include them when asking for help:
    - `docker compose ps`
    - `docker compose logs api --tail=200`
    - `docker compose logs frontend --tail=200`
    - any browser console errors (open DevTools)
  - Create an issue or share the logs so the problem can be diagnosed quickly.

Security & privacy
- The app stores your API key locally in browser storage for convenience. Do not paste production secrets into a public environment.
- When deploying, secure your `.env` and secrets (use environment variables, secret managers).
- Consider enabling SSL/TLS in front of the app in production (TLS termination via NGINX/load balancer).

Deployment guidance
- Build frontend: `cd frontend && npm run build`
- Use the backend `Dockerfile` or container images to run the API in your infra.
- Typical production stack:
  - Managed Postgres/Redis
  - Managed or self-hosted Qdrant (or alternative vector DB)
  - LLM provider (Ollama or cloud LLM provider) — ensure credentials and rate limits
  - Reverse proxy (NGINX) + SSL termination
  - Container orchestration (Cloud Run, Kubernetes, ECS) or plain Docker Compose for small deployments
- Scale components independently:
  - Frontend: static assets on CDN
  - API: stateless autoscaled replicas
  - Celery workers: scale based on job throughput
  - Vector DB: scale or use managed service

How to contribute
- Pick an issue or feature: check the repository Issues or TODOs
- Suggested workflow:
  - Fork the repo, create a feature branch
  - Run tests and linters locally
  - Open a PR with a clear description and testing steps
- Coding standards:
  - Backend: follow Python type hints and PEP8
  - Frontend: prefer TypeScript types, descriptive component names, and accessibility-friendly UI
- If you're making large changes, open an issue first to discuss the approach.

FAQ
- Q: Do I need an OpenAI key or paid LLM to run this?
  - A: Not necessarily. The project supports local LLM runtime (Ollama) and can be configured to use remote providers. See `backend/app/config.py` for available LLM adapter options.
- Q: Is the data stored centrally?
  - A: By default, data is stored in Postgres and Qdrant you run locally. Nothing is shipped to any third party unless you configure a remote LLM or external services.
- Q: I get TypeScript errors about DOM types when starting the frontend — what do I do?
  - A: Ensure Node and the project's TypeScript are installed, and that `frontend/tsconfig.*` are present. Run `npm install` from `frontend` and then `npx tsc --noEmit` to inspect diagnostics.

Credits
- Built with: FastAPI, React, Vite, Tailwind CSS, Celery, Postgres, Redis, Qdrant, Ollama (optional)
- Icons and UI components: lucide-react, radix-ui
- Thanks to contributors and maintainers of the open-source libraries used here.

License
- This repository includes its own license file (check `LICENSE` in the repo root). Use according to the terms specified there.

Contact & help
- If you need help running the project locally or want a walkthrough, open an Issue in the repo with:
  - Your OS and Node/Python versions
  - Which steps you ran and the exact error output
  - Any relevant logs (frontend console, backend logs, Docker compose logs)

Enjoy exploring Travel AI! If you'd like, I can:
- Add step-by-step pictures/screenshots to this README
- Create a short troubleshooting script for common issues
- Prepare a minimal "demo data" seeding script to populate Postgres and Qdrant with a few Kenyan destinations