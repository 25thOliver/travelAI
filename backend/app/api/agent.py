from app import dependencies
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.agents.travel_agent import TravelAgent
from app.dependencies.auth import require_api_key
import json
import asyncio
from app.dependencies.rate_limit import check_rate_limit

router = APIRouter(prefix="/agent", tags=["agent"])
travel_agent = TravelAgent()

class AgentRequest(BaseModel):
    session_id: str
    message: str

class RateLimitTestResponse(BaseModel):
    ok: bool
    remaining_window_seconds: int | None = None

class AgentResponse(BaseModel):
    answer: str
    sources: list[str]

@router.post("/chat", response_model=AgentResponse, dependencies=[Depends(require_api_key)])
async def agent_chat(request: AgentRequest) -> AgentResponse:
    try:
        check_rate_limit(request.session_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e),
        )

    try:
        # 90 second timeout - plenty of time for LLM response
        result = await asyncio.wait_for(
            travel_agent.chat(
                session_id=request.session_id,
                message=request.message,
            ),
            timeout=90.0
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="LLM response took too long. Please try a simpler question.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}",
        )

    print(json.dumps({
        "event": "agent_chat",
        "session_id": request.session_id,
        "message": request.message,
        "answer_preview": result["answer"][:80] if result["answer"] else "",
        "sources_count": len(result["sources"]),
    }), flush=True)

    return AgentResponse(answer=result["answer"], sources=result["sources"])


@router.get("/rate-test", response_model=RateLimitTestResponse, dependencies=[Depends(require_api_key)])
async def rate_test(session_id: str) -> RateLimitTestResponse:
    try:
        check_rate_limit(session_id)
        return RateLimitTestResponse(ok=True, remaining_window_seconds=None)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e),
        )