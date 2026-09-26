# Multi-Tenant SaaS Agent

A SaaS-oriented LangGraph agent backend demonstrating tenant isolation, membership verification, per-tenant quotas, usage metering, Stripe billing events, data partitioning, and audit trails.

## Request path

1. validate the Supabase access token;
2. require an explicit tenant ID;
3. verify the user belongs to that tenant;
4. enforce the tenant quota;
5. invoke the LangGraph agent;
6. persist usage and audit events with the tenant ID;
7. emit an idempotency-friendly Stripe meter event identifier.

The API never trusts the tenant header by itself.

## Database isolation

The Supabase migration enables RLS and uses membership-aware policies for client-readable tenant data. Server-side service credentials remain backend-only.

## Usage billing

Each accepted agent request is written to the internal usage ledger first and then reported as a Stripe billing meter event. The Stripe customer identifier lives on the tenant, not the user.

## Run

    pip install -e ".[dev]"
    cp .env.example .env
    uvicorn app.main:app --reload

## Production upgrades

- Redis-backed distributed rate limiting;
- async/outbox delivery for Stripe meter events;
- request-token metering rather than request counts;
- webhook reconciliation;
- tenant-specific model budgets and routing policy.
