#!/usr/bin/env bash
set -euo pipefail

# Example for a model whose checkpoint is compatible with AWQ.
vllm serve "$MODEL_ID"   --host 0.0.0.0   --port 8000   --quantization awq   --gpu-memory-utilization 0.90   --max-model-len auto   --enable-prefix-caching
