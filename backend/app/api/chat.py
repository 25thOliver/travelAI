from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.ollama_service import OllamaService
from app.dependencies.auth import require_api_key



router = APIRouter(prefix="/chat", tags=["chat"])
Ollama_service = OllamaService()

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str


@router.post("/", response_model=ChatResponse, dependencies=[Depends(require_api_key)])
async def chat(request: ChatRequest) -> ChatResponse:
    try: 
        result = await Ollama_service.generate(request.prompt)
        return ChatResponse(response=result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))