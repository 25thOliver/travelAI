from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.travel_agent import TravelAgent

router = APIRouter(prefix="/agent", tags=["agent"])
travel_agent = TravelAgent()

class AgentRequest(BaseModel):
    session_id: str
    message: str

class AgentResponse(BaseModel):
    answer: str
    sources: list[str]

@router.post("/chat", response_model=AgentResponse)
async def agent_chat(request: AgentRequest) -> AgentResponse:
    result = await travel_agent.chat(
        session_id=request.session_id,
        message=request.message,
    )
    return AgentResponse(answer=result["answer"], sources=result["sources"])