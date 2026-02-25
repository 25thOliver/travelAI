import httpx
from app.config import settings

class LLMService:
    async def generate(self, prompt: str) -> str:
        timeout = httpx.Timeout(60.0)

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{settings.ollama_base_url}/api/generate",
                json={
                    "model": "mistral",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 300
                    }
                }
            )
            response.raise_for_status()
            return response.json()["response"]