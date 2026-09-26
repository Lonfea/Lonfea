# Real-Time AI Observability

A local observability stack for the AI Engineering Systems Lab using **OpenTelemetry, Prometheus, and Grafana**.

It is designed to observe real AI services rather than a synthetic dashboard. The model router exports request, spend, failure, and latency metrics; both the router and RAG services can emit OpenTelemetry traces.

## Signals

- distributed traces across HTTP and model calls;
- request volume and error counts;
- model tier and model name;
- estimated LLM spend;
- latency histograms and p50/p95/p99 queries;
- health checks and anomaly-oriented Prometheus alerts.

## Run

From this directory:

    docker compose up -d

Prometheus: http://localhost:9090  
Grafana: http://localhost:3000

Grafana credentials in local development are `admin/admin`; change them outside local use.

## PromQL examples

p95 router latency:

    histogram_quantile(
      0.95,
      sum by (le) (rate(ai_router_latency_seconds_bucket[5m]))
    )

spend rate:

    sum(rate(ai_router_request_cost_usd_total[1h]))

error rate:

    sum(rate(ai_router_failures_total[5m]))
      /
    clamp_min(sum(rate(ai_router_requests_total[5m])), 1)

## Alert philosophy

The included rules demonstrate symptoms worth paging on:
- elevated error ratio;
- high p95 latency;
- sudden absence of requests.

Real thresholds should be tuned from actual traffic rather than copied blindly from a demo.
