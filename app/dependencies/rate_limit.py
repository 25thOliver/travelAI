import time
import json
from typing import Optional

import redis

from app.config import settings

RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 5

def _get_redis_client() -> redis.Redis:
    return redis.from_url(settings.redis_url, decode_responses=True)

def _rate_limit_key(session_id: str) -> str:
    return f"rate_limit:agent_chat:{session_id}"

def check_rate_limit(session_id: Optional[str]) -> None:
    # Raises a ValueError if the client exceeds the limit.
    if not session_id:
        return

    r = _get_redis_client()
    key = _rate_limit_key(session_id)
    now = int(time.time())

    pipe = r.pipeline()
    pipe.get(key)
    pipe.ttl(key)
    current_count, ttl = pipe.execute()

    if current_count is None:
        # First request in this window
        pipe = r.pipeline()
        pipe.set(key, 1, ex=RATE_LIMIT_WINDOW_SECONDS)
        pipe.execute()
        return

    count = int(current_count)
    if count >= RATE_LIMIT_MAX_REQUESTS:
        # Already at or above limit
        raise ValueError(
            json.dumps(
                {
                    "error": "rate_limited",
                    "message": "Too many requests. Please wait before trying again.",
                    "window_seconds": RATE_LIMIT_WINDOW_SECONDS,
                    "max_requests": RATE_LIMIT_MAX_REQUESTS,
                    "remaining_ttl": ttl,
                }
            )
        )

    # Increment within same window
    r.incr(key)