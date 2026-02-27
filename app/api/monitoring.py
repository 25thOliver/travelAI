import time
from fastapi import APIRouter

from app.db.session import engine
from app.config import settings
import redis

router = APIRouter(prefix="/monitoring", tags=["monitoring"])

@router.get("/status")
async def monitoring_status():
    # Uptime in seconds
    from app.main import APP_START_TIME
    uptime_seconds = int(time.time() - APP_START_TIME)

    # Check Postgres
    db_ok = False
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        db_ok = True
    except Exception:
        db_ok = False

    # Check Redis
    redis_ok = False
    try:
        r = redis.from_url(settings.redis_url)
        r.ping()
        redis_ok = True
    except Exception:
        redis_ok = False

    return {
        "status": "ok",
        "uptime_seconds": uptime_seconds,
        "dependencies": {
            "database": "ok" if db_ok else "error",
            "redis": "ok" if redis_ok else "error",
        },
    }