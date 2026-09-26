from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict, total=False):
    prompt: str
    response: str


class TenantAgent:
    def __init__(self, model: str):
        self.llm = ChatOpenAI(model=model, temperature=0)
        graph = StateGraph(AgentState)
        graph.add_node("respond", self._respond)
        graph.add_edge(START, "respond")
        graph.add_edge("respond", END)
        self.graph = graph.compile()

    def _respond(self, state: AgentState) -> AgentState:
        response = self.llm.invoke(
            "You are a concise SaaS assistant. Do not infer data from other tenants.\n\n"
            f"USER:\n{state['prompt']}"
        )
        return {"response": str(response.content)}

    def invoke(self, prompt: str) -> str:
        return self.graph.invoke({"prompt": prompt})["response"]
