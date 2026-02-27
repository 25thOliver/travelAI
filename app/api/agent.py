from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.agents.travel_agent import TravelAgent
from app.dependencies.auth import require_api_key
import logging
import json

logger = logging.getLogger("travel_ai.agent")

router = APIRouter(prefix="/agent", tags=["agent"])
travel_agent = TravelAgent()

class AgentRequest(BaseModel):
    session_id: str
    message: str

class AgentResponse(BaseModel):
    answer: str
    sources: list[str]

@router.post("/chat", response_model=AgentResponse, dependencies=[Depends(require_api_key)])
async def agent_chat(request: AgentRequest) -> AgentResponse:
    result = await travel_agent.chat(
        session_id=request.session_id,
        message=request.message,
    )
    logger.info(json.dumps({
        "event": "agent_chat",
        "session_id": request.session_id,
        "message": request.message,
        "answer_preview": result["answer"][:80],
        "sources_count": len(result["sources"]),
    }))
    return AgentResponse(answer=result["answer"], sources=result["sources"])