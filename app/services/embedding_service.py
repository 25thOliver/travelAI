import httpx
from app.config import settings


class EmbeddingService:
    async def embed(self, text: str) -> list[float]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.ollama_base_url}/api/embeddings",
                json={
                    "model": "mistral",
                    "prompt": text
                }
            )
            response.raise_for_status()
            return response.json()["embedding"]
        