import os
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.audit import AuditLog
from app.workflow import ApprovalWorkflow

app = FastAPI(title="Human-in-the-Loop AI Workflow", version="0.1.0")
workflow = ApprovalWorkflow(model=os.getenv("MODEL_ID", "gpt-5.6-terra"))
audit = AuditLog()


class StartRequest(BaseModel):
    question: str = Field(min_length=3, max_length=10_000)
    validated_context: list[str] = Field(default_factory=list)


class DecisionRequest(BaseModel):
    approved: bool
    feedback: str = Field(default="", max_length=5000)


@app.post("/runs")
def start_run(request: StartRequest) -> dict:
    thread_id = str(uuid.uuid4())
    audit.write(
        thread_id,
        "run_started",
        {"question": request.question, "context_count": len(request.validated_context)},
    )
    result = workflow.start(thread_id, request.question, request.validated_context)
    interrupts = result.get("__interrupt__", [])
    if interrupts:
        payload = interrupts[0].value
        audit.write(thread_id, "approval_requested", payload)
        return {"thread_id": thread_id, "status": "awaiting_approval", "review": payload}

    audit.write(thread_id, "completed", {"result": result})
    return {"thread_id": thread_id, "status": "completed", "result": result}


@app.post("/runs/{thread_id}/decision")
def decide(thread_id: str, request: DecisionRequest) -> dict:
    audit.write(thread_id, "human_decision", request.model_dump())
    try:
        result = workflow.resume(thread_id, request.approved, request.feedback)
    except Exception as exc:
        raise HTTPException(status_code=409, detail="Unable to resume workflow.") from exc

    audit.write(thread_id, "completed", {"approved": request.approved})
    return {"thread_id": thread_id, "status": "completed", "result": result}


@app.get("/runs/{thread_id}/audit")
def audit_trail(thread_id: str) -> dict:
    return {"thread_id": thread_id, "events": audit.read(thread_id)}
