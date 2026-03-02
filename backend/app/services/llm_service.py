from langchain_groq import ChatGroq
from app.config import settings

class LLMService:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=300,
        )

    async def generate(self, prompt: str) -> str:
        # ChatGroq.ainvoke returns an AIMessage, we just want the string content
        response = await self.llm.ainvoke(prompt)
        return response.content