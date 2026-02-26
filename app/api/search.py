from fastapi import APIRouter
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.services.llm_service import LLMService


router = APIRouter(prefix="/search", tags=["search"])

embbedding_service = EmbeddingService()
vector_service = VectorService()
llm_service = LLMService()


@router.post("/")
async def semantic_search(query: str):
    # Embed user query
    query_vector = await embbedding_service.embed(query)

    # Retrieve similar destinations
    results = vector_service.search(query_vector, limit=3)

    # Build context
    context_blocks = []

    for r in results[:3]:
        payload = r.payload if hasattr(r, "payload") else r["payload"]

        context_blocks.append(
            payload.get("description", "")[:1000]  # limit each chunk
        )

    context = "\n\n".join(context_blocks)

    # Grounded prompt
    prompt = f"""
    You are a Kenya travel assistant.

    Answer the question ONLY using the information in the provided context.

    If the information is not present in the context, respond with:
    "I do not have enough information in the database."

    DO NOT use outside knowledge.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    # Generate answer
    answer = await llm_service.generate(prompt)

    
    # Extract unique source URLs
    sources = []

    for r in results:
        payload = r.payload if hasattr(r, "payload") else r.get("payload", {})
        source_url = payload.get("source")

        if source_url and source_url not in sources:
            sources.append(source_url)

    return {
        "answer": answer,
        "sources": sources
    }
