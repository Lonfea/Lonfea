# AI Engineering Systems Lab

Production-oriented AI systems built to demonstrate that I can move beyond notebooks and ship reliable AI software.

## Status

The six most complete systems also live in standalone repositories, which are the maintained versions.

| System | Core capability | Status |
|---|---|---|
| [Production RAG with Citations](https://github.com/Lonfea/production-rag-citations) | PDF Q&A, hybrid retrieval, reranking, grounding, page citations | Standalone repo |
| [Cost-Optimized Model Router](https://github.com/Lonfea/cost-optimized-model-router) | Complexity routing, spend tracking, fallbacks | Standalone repo |
| [Multi-Agent Research System](https://github.com/Lonfea/multi-agent-research-system) | Supervisor, specialist agents, approval gates | Standalone repo |
| [Automated Eval Harness](https://github.com/Lonfea/ai-evaluation-harness) | Golden tests, regression gates, quality trends | Standalone repo |
| [Security Guardrail Middleware](https://github.com/Lonfea/llm-security-guardrails) | Prompt injection, PII, rate limits, sandboxing | Standalone repo |
| [Agentic Automation Pipeline](https://github.com/Lonfea/agentic-automation-platform) | Async jobs, idempotency, retries, DLQ | Standalone repo |
| [Agent Memory System](./agent-memory) | Short/long-term memory, compression, eviction | Prototype with tests |
| [Vector Search](./vector-search) | Hybrid search, metadata filtering, caching | Prototype with tests |
| [Human-in-the-Loop Workflow](./human-in-loop) | Pause/resume, approvals, validated context | Prototype with tests |
| [Multi-Tenant SaaS Agent](./multi-tenant-agent) | Isolation, quotas, billing, audit trail | Prototype with tests |
| [LoRA Fine-Tuning Pipeline](./fine-tuning) | SFT, preference alignment, before/after evals | Prototype with tests |
| [Climate Policy Benchmark](./climate-policy-benchmark) | Reproducible grounded-QA eval suite | Prototype with tests |
| [Real-Time Observability](./observability) | Traces, latency, cost, errors, alerts | Reference configuration |
| [Production Inference Server](./inference-server) | vLLM on Kubernetes, batching, cache, quantization | Reference configuration |
| [AI CI/CD](./ai-cicd) | Quality gates, canary deploys, rollback | Reference configuration |
| [Local-First AI Environment](./local-first) | Offline inference and production-parity development | Reference configuration |
| [Streaming Copilot UI](./streaming-copilot) | Token streaming, recovery, graceful degradation | Early UI prototype |
| [Open-Source Contribution](./open-source-contribution) | Feature/bug/docs contribution to an AI framework | Not started |

"Reference configuration" means deployment manifests, configs and docs without an automated test suite.

The goal is not to collect framework names. Each system is designed around a concrete engineering concern: reliability, evaluation, observability, cost, security, latency, or multi-user operation.
