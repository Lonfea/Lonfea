# Security Guardrail Middleware

A reusable security layer for LLM applications with prompt-injection screening, PII/secret redaction, rate limiting, output sanitization, and constrained tool execution.

## Controls

### Prompt injection
Deterministic high-signal patterns catch common instruction override, secret-exfiltration, and role-hijacking attempts before they reach the model.

This is a **defense layer, not a claim of perfect detection**. Production systems should combine deterministic rules with model-based or specialized injection classifiers.

### PII and secrets
Guardrails AI validators sanitize personally identifiable information and common secret patterns on both input and output paths.

### Rate limiting
A thread-safe sliding-window limiter demonstrates per-client quotas. A distributed deployment should move counters to Redis or an API gateway.

### Sandboxed execution
The included calculator never calls Python `eval` or `exec`. It parses the expression into an AST and allows numeric constants plus a small arithmetic operator allow-list only.

Imports, names, function calls, attribute access, comprehensions, file/network access, and arbitrary code are rejected.

## API

- POST /guard/input
- POST /guard/output
- POST /tools/calculate

## Run

    cd ai-engineering-lab/security-guardrails
    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"
    uvicorn app.main:app --reload

## Threat-model notes

This layer is intentionally explicit about what it does **not** solve:
- indirect injection hidden inside retrieved documents;
- data poisoning;
- compromised upstream tools;
- authorization mistakes;
- distributed rate limiting;
- isolation of arbitrary user-supplied code.

Those require additional controls rather than broader regexes.
