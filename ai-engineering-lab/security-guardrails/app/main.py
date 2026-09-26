from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from app.guards import PrivacyGuard
from app.injection import detect_prompt_injection
from app.rate_limit import SlidingWindowLimiter
from app.sandbox import UnsafeExpression, safe_calculate

app = FastAPI(title="AI Security Guardrail Middleware", version="0.1.0")
limiter = SlidingWindowLimiter(limit=30, window_seconds=60)
privacy = PrivacyGuard()


class GuardRequest(BaseModel):
    text: str = Field(min_length=1, max_length=30_000)


class CalculateRequest(BaseModel):
    expression: str = Field(min_length=1, max_length=200)


@app.middleware("http")
async def rate_limit(request: Request, call_next):
    client = request.client.host if request.client else "unknown"
    if not limiter.allow(client):
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")
    return await call_next(request)


@app.post("/guard/input")
def guard_input(request: GuardRequest) -> dict:
    findings = detect_prompt_injection(request.text)
    if findings:
        return {
            "allowed": False,
            "reason": "prompt_injection",
            "findings": [finding.rule for finding in findings],
        }

    sanitized = privacy.sanitize(request.text)
    return {"allowed": True, "sanitized": sanitized}


@app.post("/guard/output")
def guard_output(request: GuardRequest) -> dict:
    sanitized = privacy.sanitize(request.text)
    return {"allowed": True, "sanitized": sanitized}


@app.post("/tools/calculate")
def calculate(request: CalculateRequest) -> dict:
    try:
        return {"result": safe_calculate(request.expression)}
    except (UnsafeExpression, SyntaxError, ZeroDivisionError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
