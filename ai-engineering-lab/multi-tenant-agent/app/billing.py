import uuid

import stripe


def record_meter_event(
    stripe_customer_id: str | None,
    *,
    value: int,
    event_name: str = "ai_agent_requests",
) -> str | None:
    if not stripe_customer_id:
        return None

    identifier = str(uuid.uuid4())
    stripe.billing.MeterEvent.create(
        event_name=event_name,
        identifier=identifier,
        payload={
            "stripe_customer_id": stripe_customer_id,
            "value": str(value),
        },
    )
    return identifier
