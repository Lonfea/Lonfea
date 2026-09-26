from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from app.risk import assess_uncertainty


class State(TypedDict, total=False):
    question: str
    context: list[str]
    draft: str
    risk_score: float
    risk_reasons: list[str]
    approved: bool
    reviewer_feedback: str
    final: str


class ApprovalWorkflow:
    def __init__(self, db_path: str = "hitl_checkpoints.db", model: str = "gpt-5.6-terra"):
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.checkpointer = SqliteSaver.from_conn_string(db_path)
        self.graph = self._build()

    def _draft(self, state: State) -> State:
        context = "\n\n".join(state.get("context", []))
        response = self.llm.invoke(
            "Answer only from the validated context. If context is insufficient, say so.\n\n"
            f"QUESTION:\n{state['question']}\n\nCONTEXT:\n{context}"
        )
        draft = str(response.content)
        risk = assess_uncertainty(draft, len(state.get("context", [])))
        return {
            "draft": draft,
            "risk_score": risk.score,
            "risk_reasons": list(risk.reasons),
        }

    def _review(self, state: State) -> State:
        decision = interrupt(
            {
                "type": "approval_request",
                "draft": state["draft"],
                "risk_score": state["risk_score"],
                "risk_reasons": state["risk_reasons"],
                "validated_context": state.get("context", []),
            }
        )
        if not isinstance(decision, dict) or "approved" not in decision:
            return {
                "approved": False,
                "reviewer_feedback": "Invalid human decision payload.",
            }
        return {
            "approved": bool(decision["approved"]),
            "reviewer_feedback": str(decision.get("feedback", "")),
        }

    @staticmethod
    def _finalize(state: State) -> State:
        if state.get("approved"):
            return {"final": state["draft"]}
        return {
            "final": (
                "Human review rejected the draft. "
                f"Feedback: {state.get('reviewer_feedback', '')}"
            )
        }

    def _build(self):
        graph = StateGraph(State)
        graph.add_node("draft", self._draft)
        graph.add_node("review", self._review)
        graph.add_node("finalize", self._finalize)
        graph.add_edge(START, "draft")
        graph.add_edge("draft", "review")
        graph.add_edge("review", "finalize")
        graph.add_edge("finalize", END)
        return graph.compile(checkpointer=self.checkpointer)

    def start(self, thread_id: str, question: str, context: list[str]):
        config = {"configurable": {"thread_id": thread_id}}
        return self.graph.invoke({"question": question, "context": context}, config=config)

    def resume(self, thread_id: str, approved: bool, feedback: str = ""):
        config = {"configurable": {"thread_id": thread_id}}
        return self.graph.invoke(
            Command(resume={"approved": approved, "feedback": feedback}),
            config=config,
        )
