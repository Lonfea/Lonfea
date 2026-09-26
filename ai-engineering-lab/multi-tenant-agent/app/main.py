import os
import time
import uuid

import stripe
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from supabase import create_client

from app.agent import TenantAgent
from app.billing import record_meter_event
from app.limiter import TenantLimiter
from app.tenant import resolve_tenant, tenant_headers

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"],
)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
limiter = TenantLimiter(int(os.getenv("TENANT_REQUESTS_PER_MINUTE", "60")))
agent = TenantAgent(os.getenv("MODEL_ID", "gpt-5.6-terra"))

app = FastAPI(title="Multi-Tenant SaaS Agent", version="0.1.0")


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20_000)


@app.post("/chat")
def chat(
    request: ChatRequest,
    headers: tuple[str | None, str | None] = Depends(tenant_headers),
) -> dict:
    authorization, tenant_id = headers
    context = resolve_tenant(supabase, authorization, tenant_id)

    if not limiter.allow(context.tenant_id):
        raise HTTPException(status_code=429, detail="Tenant request quota exceeded.")

    request_id = str(uuid.uuid4())
    started = time.perf_counter()
    response = agent.invoke(request.prompt)
    latency_ms = int((time.perf_counter() - started) * 1000)

    usage = {
        "tenant_id": context.tenant_id,
        "user_id": context.user_id,
        "request_id": request_id,
        "units": 1,
        "latency_ms": latency_ms,
    }
    supabase.table("usage_events").insert(usage).execute()
    supabase.table("audit_events").insert(
        {
            "tenant_id": context.tenant_id,
            "user_id": context.user_id,
            "event_type": "agent_request",
            "request_id": request_id,
            "metadata": {"latency_ms": latency_ms},
        }
    ).execute()

    meter_event_id = record_meter_event(context.stripe_customer_id, value=1)
    return {
        "request_id": request_id,
        "response": response,
        "tenant_id": context.tenant_id,
        "meter_event_id": meter_event_id,
    }
