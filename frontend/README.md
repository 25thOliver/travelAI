# Travel AI — Frontend

React + Vite + TypeScript chat UI for the Travel AI backend. Part of the `travel-ai` monorepo (backend lives in `../backend`).

## Setup

```bash
npm install
```

## Configuration

Create a `.env` file:

```env
VITE_API_BASE_URL=http://localhost
VITE_API_KEY=your-api-key-here
```

Or set the API key in the browser via the Settings dialog (top-right gear icon).

## Development

```bash
npm run dev
```

## Docker

```bash
docker build -t travel-frontend --build-arg VITE_API_BASE_URL=http://localhost .
docker run -p 3000:3000 travel-frontend
```

### Docker Compose

The root `docker-compose.yml` already includes a `frontend` service. From the repo root:

```bash
docker compose up -d frontend
```

When using NGINX at port 80, the frontend is built with `VITE_API_BASE_URL=""` so API calls use the same origin.

## Features

- 💬 Chat with travel AI agent
- 🔐 Configurable API key (env or browser settings)
- 📊 Live backend status monitoring
- ⚠️ Graceful error handling (401, 429, 5xx)
- 🐳 Docker-ready with NGINX
