from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from qdrant_client import QdrantClient
from app.config import settings
from collections import deque

# Per-session chat history: list of (human, ai) string tuples
_session_histories: dict[str, deque] = {}

PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["context", "chat_history", "question"],
    template="""You are a knowledgeable and enthusiastic travel guide expert for Kenya.

Always provide specific, actionable information. Make direct comparisons when asked.
Use the provided context confidently. Be concise but thorough with practical details.
When comparing destinations, highlight unique characteristics, best suited traveler type,
facilities, best time to visit, and give a clear recommendation.

Context from travel database:
{context}

Previous conversation:
{chat_history}

Question: {question}

Answer:""",
)


from langchain_groq import ChatGroq

def _get_history(session_id: str) -> deque:
    if session_id not in _session_histories:
        _session_histories[session_id] = deque(maxlen=3)  # keep last 3 turns
    return _session_histories[session_id]

def _format_history(history: deque) -> str:
    if not history:
        return "None"
    lines = []
    for human, ai in history:
        lines.append(f"Human: {human}")
        lines.append(f"Assistant: {ai}")
    return "\n".join(lines)


class TravelAgent:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model="llama-3.1-8b-instant",
            temperature=0.1,
            max_tokens=400,
        )

        self.embeddings = OllamaEmbeddings(
            base_url=settings.ollama_base_url,
            model="nomic-embed-text",
        )

        self.qdrant_client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
        )

        self.vectorstore = QdrantVectorStore(
            client=self.qdrant_client,
            collection_name="destinations",
            embedding=self.embeddings,
            content_payload_key="description",
        )

        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

    async def chat(self, session_id: str, message: str) -> dict:
        history = _get_history(session_id)

        # Step 1: retrieve relevant docs (single embedding call)
        try:
            docs: list[Document] = await self.retriever.ainvoke(message)
        except Exception as e:
            return {"answer": f"Error retrieving context: {str(e)}", "sources": []}

        # Step 2: build context string
        context = "\n\n---\n\n".join(
            doc.page_content[:600] for doc in docs
        ) or "No relevant information found."

        # Step 3: build prompt & call LLM — single call
        prompt = PROMPT_TEMPLATE.format(
            context=context,
            chat_history=_format_history(history),
            question=message,
        )

        try:
            answer: str = await self.llm.ainvoke(prompt)
        except Exception as e:
            return {"answer": f"Error generating response: {str(e)}", "sources": []}

        # Step 4: update session history
        history.append((message, answer))

        # Step 5: extract source URLs from retrieved docs
        sources = []
        for doc in docs:
            doc_id = doc.metadata.get("_id")
            if doc_id is not None:
                try:
                    points = self.qdrant_client.retrieve(
                        collection_name="destinations",
                        ids=[doc_id],
                        with_payload=["source"],
                    )
                    if points and points[0].payload:
                        source = points[0].payload.get("source", "")
                        if source and source not in sources:
                            sources.append(source)
                except Exception:
                    pass

        return {"answer": answer, "sources": sources}
