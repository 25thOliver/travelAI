import httpx
from app.config import settings

class OllamaService:
    def __init__(self) -> None:
        self.base_url = settings.ollama_base_url
        self.model = "mistral"

    async def generate(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")