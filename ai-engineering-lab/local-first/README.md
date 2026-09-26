# Local-First AI Development Environment

A zero-API-cost development environment that mirrors the production RAG architecture while keeping model inference and document data local.

## Stack

- **Ollama** for local LLM inference
- **FastAPI** production RAG service
- **SQLite + sqlite-vec** for local hybrid retrieval
- **Docker Compose** for reproducibility
- optional **LanceDB** smoke test for teams comparing embedded local vector stores

## Why local-first matters

Developers can test ingestion, retrieval, prompts, citations, and API integration without sending documents to a hosted model provider or incurring per-token costs.

The same FastAPI application can later switch to a hosted model with environment configuration rather than a separate codebase.

## Start

From this directory:

    docker compose up --build

Then pull the local model once:

    docker compose exec ollama ollama pull llama3.2:3b

RAG API: http://localhost:8002

## Persistence

- Ollama models use the `ollama-data` volume.
- the RAG SQLite database uses the `rag-data` volume.
- no application data needs to leave the Docker host.

## Optional LanceDB experiment

    python lancedb_smoke.py

This creates a local LanceDB directory and verifies vector write/search behavior. The production RAG implementation continues to use sqlite-vec so the backend can be compared without changing the API contract.
