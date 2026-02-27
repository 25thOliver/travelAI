from fastapi import FastAPI, Request
from app.api.health import router as health_router
from app.api.chat import router as chat_router
from app.api.scrape import router as scrape_router
from app.db.base import Base
from app.db.session import engine
from app.services.vector_service import VectorService
from app.api.search import router as search_router
from app.api.agent import router as agent_router
import logging
import json
import time

# Logger setup
logger = logging.getLogger("travel_ai")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(message)s"))

logger.handlers.clear()
logger.addHandler(handler)
logger.propagate = False


app = FastAPI(title="Travel AI Agent")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = None
    try:
        response = await call_next(request)
        return response
    finally:
        process_time_ms = int((time.time() - start) * 1000)
        log_payload = {
            "event": "http_request",
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code if response else None,
            "process_time_ms": process_time_ms,
        }
        logger.info(json.dumps(log_payload))

app.include_router(health_router)
app.include_router(chat_router)
app.include_router(scrape_router)
app.include_router(search_router)
app.include_router(agent_router)

@app.get("/")
async def root():
    return {"message": "Travel AI Agent is running"}

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        vector_service = VectorService()
        vector_service.create_collection()