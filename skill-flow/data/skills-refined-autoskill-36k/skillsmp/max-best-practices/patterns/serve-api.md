---
title: MAX Serve API Features
description: Streaming, token budgets, structured output, function calling, LoRA adapters, and health endpoints
impact: HIGH
category: serve
tags: streaming, tokens, structured-output, function-calling, lora, health
error_patterns:
  - "streaming"
  - "token budget"
  - "structured output"
  - "function calling"
  - "LoRA"
  - "health check"
  - "API error"
scenarios:
  - "Enable streaming responses"
  - "Configure token budgets"
  - "Use structured output"
  - "Implement function calling"
  - "Manage LoRA adapters"
  - "Configure health endpoints"
consolidates:
  - serve-streaming.md
  - serve-token-budget.md
  - serve-structured-output.md
  - serve-function-calling.md
  - serve-lora-lifecycle.md
  - serve-health-endpoints.md
---

# MAX Serve API Features

**Category:** serve | **Impact:** HIGH

Comprehensive guide to MAX Serve API features including streaming responses, token budgets, structured output, function calling, LoRA adapter management, and health endpoints.

---

## Core Concepts

### Streaming Responses

Enable streaming for lowest time-to-first-token (TTFT) and better user experience.

**Pattern:**

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="none")

# Streaming response
stream = client.chat.completions.create(
    model="llama",
    messages=[{"role": "user", "content": "Hello!"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

**Benefits:**
- Immediate first token delivery
- Better user experience for chat interfaces
- Chunked token responses (v26.1+)

### Token Budgets

Token budgets control how many tokens are processed per batch. Understanding `--max-batch-input-tokens` (active token budget) and `--max-batch-total-tokens` is essential for optimizing throughput and latency.

**Budget Overview:**

| Budget | CLI Flag | Default | Purpose |
|--------|----------|---------|---------|
| Active Token Budget | `--max-batch-input-tokens` | 8192 | Limits tokens processed per CE batch |
| Total Context Budget | `--max-batch-total-tokens` | None | Limits total context across batch |

**Throughput vs Latency Tradeoffs:**

| Configuration | Throughput | Latency | Use Case |
|--------------|------------|---------|----------|
| High `--max-batch-input-tokens` | Higher | Higher TTFT | Batch processing |
| Low `--max-batch-input-tokens` | Lower | Lower TTFT | Interactive apps |
| With `--max-batch-total-tokens` | Controlled | Predictable | Memory-constrained |

**Tuning for Model Sizes:**

| Model Size | Recommended `--max-batch-input-tokens` | Notes |
|------------|---------------------------------------|-------|
| Small (7-8B params) | 4096-8192 | Good default for most GPUs |
| Medium (13-14B params) | 8192-12288 | Balance memory and throughput |
| Large (70B+ params) | 16384-32768 | Higher budget utilizes compute |

### Structured Output

Enable structured output for enforced JSON schema compliance.

**Pattern:**

```bash
# Enable structured output on server
max serve --model-path ... --enable-structured-output
```

```python
# Use response_format in request
response = client.chat.completions.create(
    model="llama",
    messages=[{"role": "user", "content": "Extract entities"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "entities",
            "schema": {
                "type": "object",
                "properties": {
                    "names": {"type": "array", "items": {"type": "string"}},
                    "locations": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["names", "locations"]
            }
        }
    }
)
```

### Function Calling

MAX supports OpenAI-compatible function calling / tool use for agentic workflows.

**Pattern:**

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="none")

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
}]

response = client.chat.completions.create(
    model="llama",
    messages=[{"role": "user", "content": "Weather in SF?"}],
    tools=tools,
    tool_choice="auto"
)
```

**Note:** Function calling support added in v25.1. Works with models that support tool use.

### LoRA Adapter Lifecycle

LoRA (Low-Rank Adaptation) adapters enable serving multiple fine-tuned model variants from a single base model. MAX Serve manages adapters through an LRU cache.

**Key Constraints:**
- LoRA adapters are mutually exclusive with `data_parallel_degree > 1`
- `max_num_loras` controls how many adapters can be active simultaneously
- Protected adapters (in use by TG requests) cannot be evicted
- Memory scales linearly: each adapter adds `2 * rank * hidden_size * num_layers` parameters

**Server Configuration:**

```bash
# Enable LoRA with capacity limits
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --enable-lora \
  --max-num-loras 4 \
  --max-lora-rank 16 \
  --lora-paths "adapter1=/path/to/adapter1,adapter2=/path/to/adapter2"
```

**Memory Impact per Adapter (approximate for 8B model):**
- rank=8:  ~25MB per adapter
- rank=16: ~50MB per adapter
- rank=32: ~100MB per adapter
- rank=64: ~200MB per adapter

**API Reference:**

```bash
# Load adapter at runtime
curl -X POST http://localhost:8000/v1/load_lora_adapter \
  -H "Content-Type: application/json" \
  -d '{"lora_name": "my_adapter", "lora_path": "/path/to/adapter"}'

# Unload adapter to free memory
curl -X POST http://localhost:8000/v1/unload_lora_adapter \
  -H "Content-Type: application/json" \
  -d '{"lora_name": "my_adapter"}'

# List loaded adapters (included in models list)
curl http://localhost:8000/v1/models

# Use adapter for inference
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "my_adapter", "messages": [{"role": "user", "content": "Hello"}]}'
```

### Health Endpoints

Use `/health` endpoint for Kubernetes readiness probes and load balancer checks.

**Pattern:**

```yaml
# Kubernetes readiness probe
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

**Note:** `/health` endpoint added in v25.5 for lm-eval and similar tools.

---

## Common Patterns

### Token Budget for Long-Context Throughput

**When:** Serving 70B+ models with 128K context

**Do:**
```bash
# Increase budget for large model with long context
max serve --model-path meta-llama/Llama-3.3-70B-Instruct \
  --max-batch-size 64 \
  --max-batch-input-tokens 16384 \
  --max-batch-total-tokens 131072
```

**Don't:**
```bash
# Default 8192 tokens may underutilize GPU for long-context workloads
max serve --model-path meta-llama/Llama-3.3-70B-Instruct \
  --max-batch-size 64
```

### Token Budget for Interactive Latency

**When:** Building responsive chat applications

**Do:**
```bash
# Lower budget for responsive chat
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --max-batch-size 32 \
  --max-batch-input-tokens 4096 \
  --enable-in-flight-batching
```

### LoRA Lifecycle Management

**When:** Multi-tenant deployments with customer-specific adapters

**Do:**
```python
import requests

class LoRALifecycleManager:
    """Manages LoRA adapter lifecycle with capacity awareness."""

    def __init__(self, base_url: str, max_active: int = 4):
        self.base_url = base_url
        self.max_active = max_active
        self.loaded_adapters: set[str] = set()

    def load_adapter(self, name: str, path: str) -> bool:
        """Load adapter with capacity check."""
        if name in self.loaded_adapters:
            return True

        response = requests.post(
            f"{self.base_url}/v1/load_lora_adapter",
            json={"lora_name": name, "lora_path": path}
        )

        if response.status_code == 200:
            self.loaded_adapters.add(name)
            return True
        return False

    def unload_adapter(self, name: str) -> bool:
        """Explicitly unload adapter to free memory."""
        response = requests.post(
            f"{self.base_url}/v1/unload_lora_adapter",
            json={"lora_name": name}
        )

        if response.status_code == 200:
            self.loaded_adapters.discard(name)
            return True
        return False

# Usage
manager = LoRALifecycleManager("http://localhost:8000", max_active=4)

# Pre-load high-priority adapters at startup
for adapter in ["premium_customer_1", "premium_customer_2"]:
    manager.load_adapter(adapter, f"/adapters/{adapter}")
```

**Don't:**
```python
# BAD: Loading unlimited adapters without lifecycle management
# This exhausts GPU memory as each adapter consumes ~50-200MB
for adapter in adapters:
    requests.post(
        "http://localhost:8000/v1/load_lora_adapter",
        json={"lora_name": adapter, "lora_path": f"/adapters/{adapter}"}
    )
```

### Health Check Configuration

**When:** Kubernetes or load balancer deployment

**Do:**
```yaml
# Use dedicated health endpoint
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

**Don't:**
```yaml
# Using inference endpoint for health - expensive
readinessProbe:
  httpGet:
    path: /v1/models
```

---

## Decision Guide

| Feature | When to Use | Configuration |
|---------|-------------|---------------|
| Streaming | Chat interfaces, interactive apps | `stream=True` in request |
| High token budget | Batch processing, long context | `--max-batch-input-tokens 16384` |
| Low token budget | Interactive latency | `--max-batch-input-tokens 4096` |
| Structured output | API integrations, data extraction | `--enable-structured-output` |
| Function calling | Agentic workflows, tool use | Model must support tools |
| LoRA adapters | Multi-tenant personalization | `--enable-lora --max-num-loras N` |
| Health endpoint | K8s, load balancers | `/health` |

---

## Quick Reference

- **Streaming**: Enable with `stream=True` for immediate TTFT
- **Token budget**: 4096-8192 for interactive, 16384+ for batch
- **Chunked prefill**: Enable for long context with `--enable-chunked-prefill`
- **Structured output**: Requires `--enable-structured-output` server flag
- **Function calling**: Added in v25.1, check model compatibility
- **LoRA**: Mutually exclusive with data parallelism
- **Health endpoint**: Use `/health` not `/v1/models` for probes

---

## Related Patterns

- [`serve-configuration.md`](serve-configuration.md) - Batch and scheduling configuration
- [`serve-kv-cache.md`](serve-kv-cache.md) - Memory management for KV cache
- [`serve-monitoring.md`](serve-monitoring.md) - Metrics and observability

---

## References

- [MAX Serve Configuration](https://docs.modular.com/max/serve)
- [OpenAI API Compatibility](https://docs.modular.com/max/cli/serve)
