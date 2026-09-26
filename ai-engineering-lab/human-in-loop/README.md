# Human-in-the-Loop AI Workflow

A LangGraph workflow with validated context, uncertainty signals, durable pause/resume, explicit human approval, and a separate audit trail.

## Flow

Question + validated context -> draft -> uncertainty assessment -> human review interrupt -> approve/reject -> final output.

## Durable approval gate

LangGraph `interrupt()` pauses execution and the SQLite checkpointer stores state. A reviewer later resumes the **same thread ID** with `Command(resume=...)`.

The model cannot silently skip the approval node.

## Review payload

The reviewer sees:
- draft response;
- uncertainty score and reasons;
- the validated context supplied to the model.

The human can approve or reject and leave feedback.

## Auditability

A separate append-only application audit database records:
- run start;
- approval request;
- human decision;
- completion.

This is intentionally separate from LangGraph checkpoints: checkpoints support execution; audit events support review and accountability.

## API

- POST /runs
- POST /runs/{thread_id}/decision
- GET /runs/{thread_id}/audit

## Production upgrades

- Postgres checkpointer and immutable audit sink;
- role-based approver authorization;
- signed decisions;
- timeout/escalation paths;
- approval UI integrated with the streaming copilot;
- risk thresholds learned from reviewed historical cases.
