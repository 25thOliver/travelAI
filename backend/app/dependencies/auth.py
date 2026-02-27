from fastapi import Security, HTTPException, status 
from fastapi.security import APIKeyHeader
from app.config import settings 

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def require_api_key(key: str = Security(api_key_header)) -> str:
    if key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key. Pass it as 'X-API-Key' header.",
        )
    return key
