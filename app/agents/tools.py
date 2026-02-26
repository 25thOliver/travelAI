import asyncio
from langchain.tools import tools
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

embedding_service = EmbeddingService()
vector_service = VectorService()

def _search_destinations_sync(query: str) -> str:
    async def _run():
        query_vector = await embedding_service.embed(query)
        results = vector_service.search(query_vector, limit=3)

        if not results:
            return "No relevant destinations found in the database."

        output_lines = []
        for r in results:
            payload = r.payload if hasattr(r, "payload") else r.get("payload", {})
            title = payload.get("title", "Unknown")
            description = payload.get("description", "")[:500]
            source = payload.get("source", "")

            output_lines.append(
                f"**{title}**\n{description}\nSource: {source}"
            )

        return "\n\n---\n\n".join(output_lines)

    return asyncio.run(_run())

@tool
def search_destinations(query: str) -> str:
    """
    Search the Kenya travel database for destinations, national parks, safaris,
    beaches, or activities matching the user's query.
    Use this tool whenever the user asks about places to visit, things to do,
    or travel recommendations in Kenya.
    """
    return _search_destinations_sync(query)
