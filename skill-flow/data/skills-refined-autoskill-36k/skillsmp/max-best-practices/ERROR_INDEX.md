# Max Best Practices Error Index

This index maps common error messages to relevant patterns.

## Error Message Lookup

| Error Message | Pattern | Category |
|--------------|---------|----------|
| `API error` | [serve-api](patterns/serve-api.md) | serve |
| `Buffer not found in max.driver` | [engine-operations](patterns/engine-operations.md), [breaking-changes](references/breaking-changes.md) | engine |
| `Could not find mojo kernel` | [engine-operations](patterns/engine-operations.md) | engine |
| `DLPack` | [engine-weights](patterns/engine-weights.md) | engine |
| `DeviceRef has no attribute 'from_device'` | [engine-operations](patterns/engine-operations.md) | engine |
| `Failed to resolve module path for MOGGKernelAPI` | [engine-operations](patterns/engine-operations.md) | engine |
| `GGUF` | [model-loading](patterns/model-loading.md) | model |
| `GPTQ` | [engine-quantization](patterns/engine-quantization.md) | engine |
| `GPU OOM` | [multigpu-scaling](patterns/multigpu-scaling.md) | multigpu |
| `Graph` | [graph-construction](patterns/graph-construction.md) | graph |
| `HuggingFace` | [model-loading](patterns/model-loading.md) | model |
| `KV cache` | [serve-kv-cache](patterns/serve-kv-cache.md) | serve |
| `LoRA` | [serve-api](patterns/serve-api.md) | serve |
| `NCCL` | [multigpu-scaling](patterns/multigpu-scaling.md) | multigpu |
| `OOM` | [serve-kv-cache](patterns/serve-kv-cache.md) | serve |
| `TTFT` | [serve-monitoring](patterns/serve-monitoring.md) | serve |
| `TensorType` | [graph-construction](patterns/graph-construction.md) | graph |
| `TensorType missing required argument 'device'` | [engine-operations](patterns/engine-operations.md) | engine |
| `accuracy` | [engine-quantization](patterns/engine-quantization.md) | engine |
| `architecture` | [model-loading](patterns/model-loading.md) | model |
| `batch` | [perf-inference](patterns/perf-inference.md) | perf |
| `batch size exceeds` | [serve-configuration](patterns/serve-configuration.md) | serve |
| `buffer` | [engine-weights](patterns/engine-weights.md) | engine |
| `cache hit` | [serve-kv-cache](patterns/serve-kv-cache.md) | serve |
| `communication` | [multigpu-scaling](patterns/multigpu-scaling.md) | multigpu |
| `compilation` | [graph-construction](patterns/graph-construction.md) | graph |
| `connection closed` | [serve-request-lifecycle](patterns/serve-request-lifecycle.md) | serve |
| `container` | [deploy-deployment](patterns/deploy-deployment.md) | deploy |
| `context length exceeded` | [serve-configuration](patterns/serve-configuration.md) | serve |
| `custom() missing required argument 'device'` | [engine-operations](patterns/engine-operations.md) | engine |
| `deployment failed` | [deploy-deployment](patterns/deploy-deployment.md) | deploy |
| `device` | [multigpu-scaling](patterns/multigpu-scaling.md) | multigpu |
| `device mismatch` | [engine-weights](patterns/engine-weights.md) | engine |
| `disconnect` | [serve-request-lifecycle](patterns/serve-request-lifecycle.md) | serve |
| `docker` | [deploy-deployment](patterns/deploy-deployment.md) | deploy |
| `error propagation` | [serve-request-lifecycle](patterns/serve-request-lifecycle.md) | serve |
| `float8` | [engine-quantization](patterns/engine-quantization.md) | engine |
| `foreach` / `no matching function in call to 'foreach'` | [engine-operations](patterns/engine-operations.md), [breaking-changes](references/breaking-changes.md) | engine |
| `fp8` | [engine-quantization](patterns/engine-quantization.md) | engine |
| `func has different type` / version mismatch | [breaking-changes](references/breaking-changes.md) | engine |
| `function calling` | [serve-api](patterns/serve-api.md) | serve |
| `health check` | [serve-api](patterns/serve-api.md) | serve |
| `image` | [deploy-deployment](patterns/deploy-deployment.md) | deploy |
| `kernel compilation failed` | [engine-operations](patterns/engine-operations.md) | engine |
| `kubernetes` | [deploy-deployment](patterns/deploy-deployment.md) | deploy |
| `kv-cache` | [serve-kv-cache](patterns/serve-kv-cache.md) | serve |
| `latency` | [perf-inference](patterns/perf-inference.md) | perf |
| `latency` | [serve-monitoring](patterns/serve-monitoring.md) | serve |
| `loading failed` | [model-loading](patterns/model-loading.md) | model |
| `memory exhausted` | [serve-kv-cache](patterns/serve-kv-cache.md) | serve |
| `metrics` | [serve-monitoring](patterns/serve-monitoring.md) | serve |
| `model not found` | [model-loading](patterns/model-loading.md) | model |
| `model too large` | [multigpu-scaling](patterns/multigpu-scaling.md) | multigpu |
| `module` | [graph-construction](patterns/graph-construction.md) | graph |
| `monitoring` | [serve-monitoring](patterns/serve-monitoring.md) | serve |
| `mount` | [deploy-deployment](patterns/deploy-deployment.md) | deploy |
| `multi-GPU` | [multigpu-scaling](patterns/multigpu-scaling.md) | multigpu |
| `out of memory` | [serve-configuration](patterns/serve-configuration.md) | serve |
| `out of memory` | [serve-kv-cache](patterns/serve-kv-cache.md) | serve |
| `page size` | [serve-kv-cache](patterns/serve-kv-cache.md) | serve |
| `pod` | [deploy-deployment](patterns/deploy-deployment.md) | deploy |
| `precision loss` | [engine-quantization](patterns/engine-quantization.md) | engine |
| `preemption` | [serve-request-lifecycle](patterns/serve-request-lifecycle.md) | serve |
| `prefill` | [perf-inference](patterns/perf-inference.md) | perf |
| `prefix caching` | [serve-kv-cache](patterns/serve-kv-cache.md) | serve |
| `quantization` | [engine-quantization](patterns/engine-quantization.md) | engine |
| `request cancelled` | [serve-request-lifecycle](patterns/serve-request-lifecycle.md) | serve |
| `scale` | [engine-quantization](patterns/engine-quantization.md) | engine |
| `scheduling error` | [serve-configuration](patterns/serve-configuration.md) | serve |
| `shape mismatch` | [graph-construction](patterns/graph-construction.md) | graph |
| `sharding` | [engine-weights](patterns/engine-weights.md) | engine |
| `slow inference` | [perf-inference](patterns/perf-inference.md) | perf |
| `stream` | [serve-request-lifecycle](patterns/serve-request-lifecycle.md) | serve |
| `streaming` | [serve-api](patterns/serve-api.md) | serve |
| `structured output` | [serve-api](patterns/serve-api.md) | serve |
| `swapping` | [perf-inference](patterns/perf-inference.md) | perf |
| `symbolic dimension` | [graph-construction](patterns/graph-construction.md) | graph |
| `telemetry` | [serve-monitoring](patterns/serve-monitoring.md) | serve |
| `tensor parallel` | [multigpu-scaling](patterns/multigpu-scaling.md) | multigpu |
| `throughput` | [perf-inference](patterns/perf-inference.md) | perf |
| `throughput` | [serve-monitoring](patterns/serve-monitoring.md) | serve |
| `timeout` | [serve-request-lifecycle](patterns/serve-request-lifecycle.md) | serve |
| `token` | [model-loading](patterns/model-loading.md) | model |
| `token budget` | [serve-api](patterns/serve-api.md) | serve |
| `token limit exceeded` | [serve-configuration](patterns/serve-configuration.md) | serve |
| `transfer` | [engine-weights](patterns/engine-weights.md) | engine |
| `unable to locate module 'max'` | [engine-operations](patterns/engine-operations.md) | engine |
| `unsupported model` | [model-loading](patterns/model-loading.md) | model |
| `volume` | [deploy-deployment](patterns/deploy-deployment.md) | deploy |
| `weight` | [engine-weights](patterns/engine-weights.md) | engine |
| `worker` | [serve-monitoring](patterns/serve-monitoring.md) | serve |

## Patterns by Error Count

| Pattern | Category | Error Patterns Covered |
|---------|----------|----------------------|
| [deploy-deployment](patterns/deploy-deployment.md) | deploy | 8 |
| [serve-kv-cache](patterns/serve-kv-cache.md) | serve | 8 |
| [engine-operations](patterns/engine-operations.md) | engine | 7 |
| [engine-quantization](patterns/engine-quantization.md) | engine | 7 |
| [model-loading](patterns/model-loading.md) | model | 7 |
| [multigpu-scaling](patterns/multigpu-scaling.md) | multigpu | 7 |
| [serve-api](patterns/serve-api.md) | serve | 7 |
| [serve-monitoring](patterns/serve-monitoring.md) | serve | 7 |
| [serve-request-lifecycle](patterns/serve-request-lifecycle.md) | serve | 7 |
| [engine-weights](patterns/engine-weights.md) | engine | 6 |
| [graph-construction](patterns/graph-construction.md) | graph | 6 |
| [perf-inference](patterns/perf-inference.md) | perf | 6 |
| [serve-configuration](patterns/serve-configuration.md) | serve | 5 |

---

*Auto-generated by `scripts/build_error_index.py`*