from fastapi import APIRouter
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

router = APIRouter(prefix="/search", tags=["search"])

embbedding_service = EmbeddingService()
vector_service = VectorService()


@router.post("/")
async def semantic_search(query: str):
    query_vector = await embbedding_service.embed(query)

    results = vector_service.search(query_vector)

    return [
        {
            "score": r.score,
            "payload": r.payload,
        }
        for r in results
    ]