# CI/CD for AI Systems

A deployment pattern where software correctness and AI quality are separate gates before progressive delivery.

## Release flow

1. unit/lint/build checks;
2. run the 100+ case AI evaluation harness against the candidate;
3. reject the release when quality thresholds fail;
4. publish an immutable image;
5. update the Argo Rollout image;
6. canary at 10%, then 50%, then 100%;
7. run Prometheus analyses during the canary;
8. Argo Rollouts aborts/rolls back when analysis fails.

## Why two quality gates?

Pre-deploy evals catch known behavioral regressions on golden cases. Canary analysis catches operational failures and traffic-dependent problems that an offline suite cannot reproduce.

## Feature flags

The example ConfigMap keeps risky behavior changes independently switchable from deployment. In a real platform, use a dedicated feature-flag service for dynamic targeting and audit history.

## Automatic rollback

Argo Rollouts treats failed analysis as a failed canary. Stable traffic remains on the prior ReplicaSet instead of promoting the new version.

## Required platform components

- GitHub Actions
- container registry
- Kubernetes
- Argo Rollouts
- NGINX ingress traffic routing
- Prometheus
- the eval harness from this lab

No successful deployment is claimed until these workflows run against a configured cluster and secrets.
