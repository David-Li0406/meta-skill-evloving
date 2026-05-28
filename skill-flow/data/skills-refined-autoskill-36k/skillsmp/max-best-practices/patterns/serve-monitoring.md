---
title: MAX Serve Monitoring and Telemetry
description: Metric levels, telemetry configuration, worker lifecycle, and disaggregated inference
impact: HIGH
category: serve
tags: metrics, telemetry, monitoring, workers, disaggregated
error_patterns:
  - "metrics"
  - "telemetry"
  - "monitoring"
  - "worker"
  - "TTFT"
  - "latency"
  - "throughput"
scenarios:
  - "Monitor MAX Serve deployment"
  - "Configure metrics collection"
  - "Set up telemetry"
  - "Debug performance issues"
  - "Track TTFT and latency"
  - "Monitor worker lifecycle"
consolidates:
  - serve-metric-levels.md
  - serve-metrics-telemetry.md
  - serve-model-worker-lifecycle.md
  - serve-disaggregated-inference.md
---

# MAX Serve Monitoring and Telemetry

**Category:** serve | **Impact:** HIGH

Comprehensive guide to monitoring MAX Serve deployments including metric levels, telemetry configuration, worker lifecycle management, and disaggregated inference architecture.

---

## Core Concepts

### Metric Levels

MAX Serve provides three metric granularity levels via `MAX_SERVE_METRIC_LEVEL`. Choosing the wrong level can degrade production performance or leave you blind during debugging.

**Level Comparison:**

| Level | Value | Metrics Collected | Performance Impact | Use Case |
|-------|-------|-------------------|-------------------|----------|
| `NONE` | 0 | No metrics | Zero overhead | Minimal latency requirements |
| `BASIC` | 10 | Request counts, TTFT, input/output tokens | Minimal (<1%) | Production deployments |
| `DETAILED` | 20 | ITL, batch size, cache hit rates, preemption | Moderate (5-15%) | Debugging, optimization |

**Metrics by Level:**

| Metric | Level | Description |
|--------|-------|-------------|
| `maxserve.request_count` | BASIC | HTTP request count |
| `maxserve.request_time` | BASIC | Request latency (ms) |
| `maxserve.time_to_first_token` | BASIC | TTFT latency (ms) |
| `maxserve.num_input_tokens` | BASIC | Input token count |
| `maxserve.num_output_tokens` | BASIC | Output token count |
| `maxserve.model_load_time` | BASIC | Model load time (ms) |
| `maxserve.num_requests_queued` | BASIC | Requests waiting |
| `maxserve.num_requests_running` | BASIC | Requests processing |
| `maxserve.itl` | DETAILED | Inter-token latency (ms) |
| `maxserve.batch_size` | DETAILED | Batch size distribution |
| `maxserve.batch_execution_time` | DETAILED | Batch execution time |
| `maxserve.cache.hit_rate` | DETAILED | Prefix cache hit rate |
| `maxserve.cache.preemption_count` | DETAILED | Memory preemption events |
| `maxserve.cache.num_used_blocks` | DETAILED | KV cache block usage |
| `maxserve.cache.num_total_blocks` | DETAILED | Total KV cache blocks |

### Recording Methods

| Method | Description | Overhead | Use Case |
|--------|-------------|----------|----------|
| `NOOP` | No recording | None | Disable telemetry entirely |
| `SYNC` | Synchronous in-process | Highest | Testing only |
| `ASYNCIO` | Async in main process | Low | Development |
| `PROCESS` | Separate process | Minimal | Production (isolated) |

### Model Worker Lifecycle

MAX Serve uses a factory pattern with async context management for model worker lifecycle. Configure timeouts and heartbeats for production reliability.

**Pattern - Model Worker Startup:**

```python
@asynccontextmanager
async def start_model_worker(
    model_factory: PipelinesFactory,
    pipeline_config: PipelineConfig,
    settings: Settings,
    metric_client: MetricClient,
    scheduler_zmq_configs: SchedulerZmqConfigs,
) -> AsyncGenerator[ProcessManager]:
    worker_name = "MODEL_" + str(uuid.uuid4())

    # Use spawn context for GPU models (fork is unsafe)
    mp = multiprocessing.get_context("spawn")

    async with subprocess_manager("Model Worker") as proc:
        alive = mp.Event()
        proc.start(...)

        # Wait for model to be ready
        await proc.ready(alive, timeout=settings.mw_timeout_s)

        # Enable heartbeat monitoring for production
        if settings.use_heartbeat:
            proc.watch_heartbeat(alive, timeout=settings.mw_health_fail_s)

        yield proc
```

**Environment Variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_SERVE_MW_TIMEOUT` | None | Model worker startup timeout (seconds) |
| `MAX_SERVE_USE_HEARTBEAT` | False | Enable periodic heartbeat checks |
| `MAX_SERVE_MW_HEALTH_FAIL` | 60.0 | Max seconds without heartbeat |

### Disaggregated Inference

Disaggregated inference separates prefill (context encoding) and decode (token generation) into different workers for high-throughput scenarios.

**Architecture:**

```
                       Dispatcher
                          |
           +--------------+--------------+
           |                             |
    Prefill Workers              Decode Workers
    (Context Encoding)           (Token Generation)
           |                             |
           +--[KV Transfer]-->-----------+
```

**Trade-offs:**

| Aspect | Unified | Disaggregated |
|--------|---------|---------------|
| Latency | Lower for small requests | Higher (transfer overhead) |
| Throughput | Good | Better at scale |
| Complexity | Simple | More operational overhead |
| GPU utilization | Variable | More consistent |

---

## Common Patterns

### Production Metrics Configuration

**When:** Deploying to production with monitoring infrastructure

**Do:**
```bash
# Production: BASIC metrics with process isolation
export MAX_SERVE_METRIC_LEVEL=BASIC
export MAX_SERVE_METRIC_RECORDING_METHOD=PROCESS
export MAX_SERVE_METRICS_ENDPOINT_PORT=8001

max serve --model-path meta-llama/Llama-3.1-8B-Instruct
```

**Don't:**
```bash
# DETAILED level adds per-token measurements that accumulate overhead
export MAX_SERVE_METRIC_LEVEL=DETAILED
export MAX_SERVE_METRIC_RECORDING_METHOD=SYNC  # Synchronous = blocking

max serve --model-path meta-llama/Llama-3.1-8B-Instruct
# Result: 5-15% latency increase from ITL measurements on every token
```

### Debug/Optimization Metrics

**When:** Debugging performance issues or optimizing configuration

**Do:**
```bash
# Development/Debugging: DETAILED metrics for optimization
export MAX_SERVE_METRIC_LEVEL=DETAILED
export MAX_SERVE_METRIC_RECORDING_METHOD=ASYNCIO
export MAX_SERVE_DETAILED_METRIC_BUFFER_FACTOR=20  # Buffer detailed metrics

max serve --model-path meta-llama/Llama-3.1-8B-Instruct
```

### Worker Timeout Configuration

**When:** Deploying large models (70B+ parameters)

**Do:**
```bash
# Configure timeouts based on model size
export MAX_SERVE_MW_TIMEOUT=600       # 10 min startup timeout
export MAX_SERVE_USE_HEARTBEAT=true   # Enable health monitoring
export MAX_SERVE_MW_HEALTH_FAIL=60    # 60s heartbeat threshold

max serve --model-path meta-llama/Llama-3.1-70B-Instruct
```

**Don't:**
```bash
# Model may hang indefinitely on large model loads
max serve --model-path meta-llama/Llama-3.1-70B-Instruct
```

### Grafana Dashboard Queries

**When:** Building observability dashboards

```promql
# P99 TTFT (Time to First Token)
histogram_quantile(0.99, rate(maxserve_time_to_first_token_milliseconds_bucket[5m]))

# Token throughput (tokens/sec)
rate(maxserve_num_output_tokens_total[5m])

# Request throughput
rate(maxserve_request_count_total[5m])

# Batch size distribution
histogram_quantile(0.95, rate(maxserve_batch_size_bucket[5m]))

# Cache hit rate (requires DETAILED)
rate(maxserve_cache_hit_rate_sum[5m]) / rate(maxserve_cache_hit_rate_count[5m])

# Preemption rate (memory pressure indicator)
rate(maxserve_cache_preemption_count_total[5m])
```

### Disaggregated Inference Setup

**When:** High-throughput deployments with 4+ GPUs and long prompts

**Do:**
```bash
# Dispatcher bind address
export MAX_SERVE_DI_BIND_ADDRESS="tcp://127.0.0.1:5555"

# Deployment architecture example:
# GPUs 0-1: Prefill workers (handle prompt encoding)
# GPUs 2-3: Decode workers (handle token generation)
#
# Prefill optimized for:
# - Large batch input tokens
# - Chunked prefill
# - Memory for long contexts
#
# Decode optimized for:
# - Low latency per token
# - Continuous batching
# - In-flight batching
```

**Don't:**
```bash
# Unified scheduler may bottleneck at scale
max serve --model-path meta-llama/Llama-3.1-70B-Instruct \
  --num-gpus 8
```

---

## Decision Guide

| Scenario | Metric Level | Recording Method | Notes |
|----------|--------------|------------------|-------|
| Production | BASIC | PROCESS | Minimal overhead, isolated |
| Development | DETAILED | ASYNCIO | Full visibility |
| Debugging | DETAILED | ASYNCIO | Temporarily enable |
| Latency-critical | NONE or BASIC | PROCESS | Minimize overhead |
| Capacity planning | DETAILED | PROCESS | Monitor cache metrics |

| Scenario | Architecture | When to Use |
|----------|--------------|-------------|
| Standard deployment | Unified | <4 GPUs, mixed workloads |
| High-scale production | Disaggregated | 4+ GPUs, long prompts |
| RAG workloads | Disaggregated | Long context, short generation |

---

## Quick Reference

- **BASIC metrics**: <1% overhead, recommended for production
- **DETAILED metrics**: 5-15% overhead, use for debugging only
- **PROCESS recording**: Isolates metrics collection from model worker
- **MW_TIMEOUT**: Set based on model size (~30s per 10B parameters)
- **Heartbeat**: Enable for production to detect hung workers
- **Disaggregated**: Use for 4+ GPU deployments with long prompts

---

## Prometheus Endpoint

```bash
# Metrics exposed at dedicated port
curl http://localhost:8001/metrics

# Example Prometheus output
maxserve_time_to_first_token_milliseconds_bucket{le="100.0"} 42
maxserve_request_count_total{code="200",path="/v1/chat/completions"} 1234
maxserve_batch_size_bucket{le="16"} 89
```

---

## Best Practices

1. **Production**: Use `BASIC` level with `PROCESS` recording
2. **Large models**: Set `MW_TIMEOUT` based on model size
3. **Reliability**: Enable heartbeat for production
4. **Debugging**: Temporarily enable `DETAILED`, then disable
5. **Alerting**: Monitor preemption counts and TTFT P99
6. **Buffer factor**: Set `MAX_SERVE_DETAILED_METRIC_BUFFER_FACTOR=20` to batch detailed metrics
7. **Spawn context**: Use `spawn` multiprocessing context (not fork) for GPU models

---

## Related Patterns

- [`serve-configuration.md`](serve-configuration.md) - Environment configuration
- [`serve-kv-cache.md`](serve-kv-cache.md) - KV cache monitoring
- [`serve-request-lifecycle.md`](serve-request-lifecycle.md) - Error and preemption handling

---

## References

- [MAX Serve Configuration](https://docs.modular.com/max/serve)
- [MAX Serve Observability](https://docs.modular.com/max/serve)
- Source: `max/serve/config.py`, `max/serve/telemetry/metrics.py`
