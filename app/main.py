from fastapi import FastAPI
from app.api.health import router as health_router

app = FastAPI(title="Travel AI Agent")

app.include_router(health_router)


@app.get("/")
async def root():
    return {"message": "Travel AI Agent is running"}