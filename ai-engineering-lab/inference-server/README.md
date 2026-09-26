# Production Inference Server — vLLM on Kubernetes

A Kubernetes deployment pattern for OpenAI-compatible vLLM inference with multiple replicas, shared model cache, health probes, load balancing, autoscaling, KV-cache-aware memory configuration, prefix caching, and a quantized serving example.

## Serving path

Client -> Kubernetes Service -> healthy vLLM pod -> continuous-batching inference engine.

The Kubernetes Service spreads requests across ready replicas. vLLM handles model execution and batching inside each pod.

## KV cache and throughput

The deployment reserves 90% of device memory for the vLLM executor through `--gpu-memory-utilization`. The exact value should be benchmarked per model/GPU because model weights, activations, and KV cache compete for accelerator memory.

`--enable-prefix-caching` is enabled for workloads with repeated prompt prefixes.

## Quantization

`quantized-example.sh` demonstrates AWQ. The quantization method must match the model checkpoint and the target hardware. It is not enabled blindly in the base Kubernetes deployment.

## Load balancing and scaling

- two replicas avoid a single serving pod;
- readiness probes stop traffic to unready replicas;
- ClusterIP Service load-balances across ready pods;
- HPA provides a portable baseline;
- production GPU services should replace CPU utilization with queue depth, token throughput, or another inference-specific signal.

## Apply

    kubectl apply -f k8s/pvc.yaml
    kubectl apply -f k8s/deployment.yaml
    kubectl apply -f k8s/service.yaml
    kubectl apply -f k8s/hpa.yaml

## Production concerns

- pin image and model revisions rather than using floating tags;
- measure time-to-first-token and inter-token latency separately;
- choose tensor parallelism when a model cannot fit on one GPU;
- benchmark quantization quality and throughput;
- configure PodDisruptionBudgets, topology spread, authentication, and network policy.
