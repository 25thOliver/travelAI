from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.chat import router as chat_router
from app.api.scrape import router as scrape_router
from app.db.base import Base
from app.db.session import engine
from app.services.vector_service import VectorService
from app.api.search import router as search_router

app = FastAPI(title="Travel AI Agent")

app.include_router(health_router)
app.include_router(chat_router)
app.include_router(scrape_router)
app.include_router(search_router)


@app.get("/")
async def root():
    return {"message": "Travel AI Agent is running"}

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        vector_service = VectorService()
        vector_service.create_collection()