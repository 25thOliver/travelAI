from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ollama_service import OllamaService


router = APIRouter(prefix="/chat", tags=["chat"])
Ollama_service = OllamaService()

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try: 
        result = await Ollama_service.generate(request.prompt)
        return ChatResponse(response=result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))