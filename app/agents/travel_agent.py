from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from app.config import settings

_session_memories: dict[str, ConversationBufferWindowMemory] = {}


def _get_memory(session_id: str) -> ConversationBufferWindowMemory:
    if session_id not in _session_memories:
        _session_memories[session_id] = ConversationBufferWindowMemory(
            k=5,
            memory_key="chat_history",
            return_messages=True,
            output_key="answer",
        )
    return _session_memories[session_id]


class TravelAgent:
    def __init__(self):
        self.llm = OllamaLLM(
            base_url=settings.ollama_base_url,
            model="mistral",
            temperature=0.3,
        )

        embeddings = OllamaEmbeddings(
            base_url=settings.ollama_base_url,
            model="nomic-embed-text",
        )

        self.qdrant_client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
        )

        # LangChain-native Qdrant wrapper; content_payload_key tells it
        # which field in our payload is the actual text
        self.vectorstore = QdrantVectorStore(
            client=self.qdrant_client,
            collection_name="destinations",
            embedding=embeddings,
            content_payload_key="description",
        )

    def _build_chain(self, session_id: str) -> ConversationalRetrievalChain:
        memory = _get_memory(session_id)
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True,
            verbose=True,
        )

    async def chat(self, session_id: str, message: str) -> dict:
        chain = self._build_chain(session_id)
        result = await chain.ainvoke({"question": message})

        output = result.get("answer", "")

        # langchain_qdrant only returns _id in metadata
        sources = []
        for doc in result.get("source_documents", []):
            doc_id = doc.metadata.get("_id")
            if doc_id is not None:
                points = self.qdrant_client.retrieve(
                    collection_name="destinations",
                    ids=[doc_id],
                    with_payload=["source"],
                )
                if points and points[0].payload:
                    source = points[0].payload.get("source", "")
                    if source and source not in sources:
                        sources.append(source)

        return {"answer": output, "sources": sources}

