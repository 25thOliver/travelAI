from langchain_ollama import OllamaLLM
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain import hub
from app.agents.tools import search_destinations
from app.config import settinggs

# One memory store per session, keyed by session_id
_session_memories: dict[str, ConversationBufferWindowMemory] = {}

def _get_memory(session_id: str) -> ConversationBufferWindowMemory:
    if session_id not in _session_memories:
        _session_memories[session_id] = ConversationBufferWindowMemory(
            k=5,
            memory_key="chat_history",
            return_messages=True,
        )
    return _session_memories[session_id]

class TravelAgent:
    def __init__(self):
        self.llm = OllamaLLM(
            base_url=settings.ollama_base_url,
            model="mistral",
            temperature=0.3,
        )

        self.tools = [search_destinations]
        self.prompt = hub.pull("hwchase17/react-chat")

    def _build_executor(self, session_id: str) -> AgentExecutor:
        memory = _get_memory(session_id)
        agent = create_recat_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt,
        )
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5,
        )

    async def chat(self, session_id: str, message: str) -> dict:
        executor = self._build_executor(session_id)
        result = await executor.ainvoke({"input": message})
        output = result.get("output", "")

        # Extract source URLs from tool call outputs
        sources = []
        for step in result.get("internediate_steps", []):
            if len(step) == 2:
                tool_output = step[1]
                if isinstance(tool_output, str):
                    for line in tool_output.split("\n"):
                        if line.startswith("Source: ") and line [8:].strip():
                            url = line[8:].strip()
                            if url not in sources:
                                sources.append(url)

        return {"answer": output, "sources": sources}