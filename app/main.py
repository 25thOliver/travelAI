from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.chat import router as chat_router
from app.api.scrape import router as scrape_router

app = FastAPI(title="Travel AI Agent")

app.include_router(health_router)
app.include_router(chat_router)
app.include_router(scrape_router)


@app.get("/")
async def root():
    return {"message": "Travel AI Agent is running"}