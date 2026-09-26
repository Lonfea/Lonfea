# Agent Memory System

A two-tier memory architecture with Redis short-term conversation buffers and Qdrant semantic long-term recall.

## Memory tiers

### Short-term
- keyed by both user and session;
- bounded by number of turns;
- TTL-based cleanup;
- context compression before model calls.

### Long-term
- user-scoped semantic memories in Qdrant;
- vector recall with score threshold and top-k limit;
- explicit memory IDs;
- deletion constrained by both user ID and requested memory IDs.

## Cross-session behavior

Short-term state is session-specific. Long-term memories are user-specific, so a new session can recall durable context without inheriting the entire previous transcript.

## Eviction policy

- Redis list trimming prevents unbounded conversation growth.
- Redis TTL removes abandoned sessions.
- semantic retrieval has a score threshold and maximum result count.
- explicit `forget()` supports durable memory deletion.

## Run

    docker compose up -d
    pip install -e ".[dev]"

## Production upgrades

- LLM-based semantic compression with deterministic fallback;
- memory salience scoring before long-term writes;
- deduplication and contradiction handling;
- retention policies by memory type;
- encryption and auditable deletion workflows.
