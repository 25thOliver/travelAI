from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_qdrant import QdrantVectorStore
from langchain.prompts import PromptTemplate
from qdrant_client import QdrantClient
from app.config import settings
import asyncio

_session_memories: dict[str, ConversationBufferWindowMemory] = {}
_session_chains: dict[str, ConversationalRetrievalChain] = {}

SYSTEM_PROMPT = """You are a knowledgeable and enthusiastic travel guide expert for Kenya. Your role is to:

1. **Always provide specific, actionable information** - Don't say "it's difficult to determine" or hedge unnecessarily
2. **Make direct comparisons** when asked - Compare beaches, destinations, and attractions directly with facts
3. **Use provided context confidently** - Base answers on the retrieved documents while being honest about limitations
4. **Be concise but thorough** - Give clear, well-organized responses with specific details
5. **Include practical details** - Such as best time to visit, activities, access, and what makes each place unique
6. **Highlight differences** - When comparing multiple destinations, clearly explain what sets each apart

When answering questions about multiple destinations (like beaches), structure your response to highlight:
- Unique characteristics of each beach
- Best suited for (adventure, relaxation, families, etc.)
- Facilities and infrastructure
- Best time to visit
- Overall recommendation based on traveler type

Be confident and authoritative while grounding responses in the provided information."""

def _get_memory(session_id: str) -> ConversationBufferWindowMemory:
    if session_id not in _session_memories:
        _session_memories[session_id] = ConversationBufferWindowMemory(
            k=3,
            memory_key="chat_history",
            return_messages=True,
            output_key="answer",
        )
    return _session_memories[session_id]


class TravelAgent:
    def __init__(self):
        self.llm = OllamaLLM(
            base_url=settings.ollama_base_url,
            model="mistral:latest",
            temperature=0.1,
            num_predict=200,
            top_p=0.7,
            top_k=30,
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
        # Return cached chain if available
        if session_id in _session_chains:
            return _session_chains[session_id]
        
        memory = _get_memory(session_id)
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 2})

        # Simplified prompt template for faster generation
        prompt_template = PromptTemplate(
            input_variables=["context", "chat_history", "question"],
            template="""You are a travel expert for Kenya. Answer the question directly and concisely using the provided context.

Context:
{context}

Previous conversation:
{chat_history}

Question: {question}

Answer:"""
        )

        chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True,
            verbose=False,
            combine_docs_chain_kwargs={"prompt": prompt_template},
        )
        
        # Cache the chain for this session
        _session_chains[session_id] = chain
        return chain

    async def chat(self, session_id: str, message: str) -> dict:
        chain = self._build_chain(session_id)
        
        try:
            result = await chain.ainvoke({"question": message})
        except Exception as e:
            return {
                "answer": f"Error: {str(e)}",
                "sources": []
            }

        output = result.get("answer", "")

        # langchain_qdrant only returns _id in metadata
        sources = []
        for doc in result.get("source_documents", []):
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
                except:
                    pass

        return {"answer": output, "sources": sources}

