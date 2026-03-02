from langchain_xai import ChatXAI
from app.config import settings

class LLMService:
    def __init__(self):
        self.llm = ChatXAI(
            xai_api_key=settings.xai_api_key,
            model="grok-2-latest",
            temperature=0.3,
            max_tokens=300,
        )

    async def generate(self, prompt: str) -> str:
        # ChatXAI.ainvoke returns an AIMessage, we just want the string content
        response = await self.llm.ainvoke(prompt)
        return response.content