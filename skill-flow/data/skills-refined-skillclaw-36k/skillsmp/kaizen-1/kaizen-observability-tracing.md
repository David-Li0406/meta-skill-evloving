# Kaizen Distributed Tracing

**Quick reference for OpenTelemetry tracing with Jaeger integration**

## Overview

Production-ready distributed tracing with OpenTelemetry and Jaeger OTLP exporter. Track agent execution across services with automatic span creation, parent-child relationships, and zero overhead (<1ms per span).

**Performance**: <1ms per span creation, -0.06% production overhead

## Quick Start

```python
from kaizen.core.base_agent import BaseAgent

# Enable tracing (one line!)
agent = BaseAgent(config=config, signature=signature)
agent.enable_observability(
    service_name="my-agent",
    enable_tracing=True
)

# All operations automatically traced
result = agent.run(question="test")
```

**Access Jaeger UI**: `http://localhost:16686`

## TracingManager

OpenTelemetry tracer with Jaeger OTLP exporter:

```python
from kaizen.core.autonomy.observability import TracingManager

manager = TracingManager(
    service_name="my-service",
    jaeger_host="localhost",
    jaeger_port=4317,              # OTLP gRPC port
    batch_size=512,                # Max queue size
    batch_timeout_ms=5000,         # Export timeout
    max_export_batch_size=512,     # Max spans per batch
)
```

**Methods**:
- `create_span_from_context(context, parent_span)`: Create span from HookContext
- `update_span_from_result(span, result)`: Update span with result
- `record_exception(span, exception)`: Record exception in span
- `force_flush(timeout=30)`: Export pending spans
- `shutdown(timeout=30)`: Shutdown and export all

## TracingHook

Automatic span creation for hook events:

```python
from kaizen.core.autonomy.hooks.builtin import TracingHook
from kaizen.core.autonomy.hooks import HookEvent

hook = TracingHook(
    tracing_manager=manager,
    events_to_trace=[HookEvent.PRE_TOOL_USE, HookEvent.POST_TOOL_USE]  # Optional
)

# Register with agent
agent._hook_manager.register_hook(hook)
```

## Traced Events

All hook events are traceable:

**Agent Lifecycle**:
- `PRE_AGENT_LOOP` / `POST_AGENT_LOOP`: Agent execution

**Tool Operations**:
- `PRE_TOOL_USE` / `POST_TOOL_USE`: Tool executions

**LLM Operations**:
- `PRE_LLM_CALL` / `POST_LLM_CALL`: LLM API calls

**Memory Operations**:
- `PRE_MEMORY_READ` / `POST_MEMORY_READ`: Memory retrieval

**Custom Events**: Any custom hook events

## Span Hierarchy

TracingHook creates parent-child relationships:

```
pre_agent_loop (root span)
├── pre_tool_use:load_data
│   └── post_tool_use:load_data (child, actual duration)
├── pre_tool_use:analyze_data
│   └── post_tool_use:analyze_data
└── post_agent_loop (ends root span)
```

**Features**:
- PRE events create long-running spans
- POST events end PRE spans with actual duration
- Composite keys: `(trace_id, event_pair:tool_name)` for multiple calls
- Span attributes from HookContext (agent_id, event_type, tool_name)

## BaseAgent Integration

```python
# One-line setup
agent.enable_observability(
    service_name="production-agent",
    enable_tracing=True,
    jaeger_host="jaeger.prod.example.com",
    jaeger_port=4317
)

# Or manual setup
manager = TracingManager(service_name="my-agent")
hook = TracingHook(tracing_manager=manager)
agent._hook_manager.register_hook(hook)
```

## Event Filtering

Trace only specific events:

```python
hook = TracingHook(
    tracing_manager=manager,
    events_to_trace=[
        HookEvent.PRE_TOOL_USE,
        HookEvent.POST_TOOL_USE,
        HookEvent.PRE_LLM_CALL,
        HookEvent.POST_LLM_CALL,
    ]
)
```

## Multi-Agent Tracing

Share TracingManager across agents:

```python
# Shared manager
manager = TracingManager(service_name="multi-agent-system")

# Each agent gets unique trace_id
agent1 = SupervisorAgent(config=config)
agent1.enable_observability()  # Uses agent class name

agent2 = WorkerAgent(config=config)
agent2.enable_observability()  # Uses agent class name

# Search in Jaeger by agent_id or service_name
```

## Long-Running Operations

PRE spans stay active until POST event:

```python
# PRE event starts span
context_pre = HookContext(
    event_type=HookEvent.PRE_TOOL_USE,
    agent_id=agent.agent_id,
    trace_id=trace_id,
    timestamp=time.time(),
    data={"operation": "batch_processing"}
)
await hook.handle(context_pre)

# ... long operation (10s, 1m, 10m+) ...
time.sleep(600)  # 10 minutes

# POST event ends span with actual duration
context_post = HookContext(
    event_type=HookEvent.POST_TOOL_USE,
    agent_id=agent.agent_id,
    trace_id=trace_id,
    timestamp=time.time(),
    data={"operation": "batch_processing", "status": "completed"}
)
await hook.handle(context_post)
```

## Production Deployment

### Docker Compose Stack

```bash
# Start Jaeger + Grafana stack
cd docs/observability
docker-compose up -d
```

**Included**:
- Jaeger UI: `http://localhost:16686`
- Grafana: `http://localhost:3000`
- Pre-built dashboards

### Production Configuration

```python
import os

agent.enable_observability(
    service_name=os.getenv("SERVICE_NAME", "my-agent"),
    enable_tracing=True,
    jaeger_host=os.getenv("JAEGER_HOST", "localhost"),
    jaeger_port=int(os.getenv("JAEGER_PORT", "4317"))
)
```

### Advanced Configuration

```python
manager = TracingManager(
    service_name="production-agent",
    jaeger_host="jaeger.prod.example.com",
    jaeger_port=4317,
    insecure=False,              # Use secure gRPC
    batch_size=1024,             # Larger batch
    batch_timeout_ms=10000,      # Longer timeout
    max_export_batch_size=512
)

# Force export before shutdown
manager.force_flush(timeout=30)
manager.shutdown(timeout=30)
```

## Testing

### Integration Testing (NO MOCKING - Tier 2)

```python
import pytest
from tests.utils.docker_config import JAEGER_CONFIG, is_jaeger_available

@pytest.mark.skipif(not is_jaeger_available(), reason="Jaeger not running")
async def test_agent_tracing():
    # Setup
    manager = TracingManager(service_name="test-service")
    hook = TracingHook(tracing_manager=manager)
    agent._hook_manager.register_hook(hook)

    # Execute
    result = agent.run(question="test")

    # Verify in Jaeger
    manager.force_flush()
    time.sleep(2)  # Wait for indexing

    traces = query_jaeger_traces("test-service")
    assert len(traces) > 0
```

### Query Jaeger API

```python
import requests

def query_jaeger_traces(service_name: str) -> List[Dict]:
    response = requests.get(
        f"{JAEGER_CONFIG['base_url']}/api/traces",
        params={"service": service_name, "limit": 100}
    )
    return response.json().get("data", [])
```

## Troubleshooting

### Spans Not Appearing

**Check Jaeger is running**:
```bash
curl http://localhost:16686/api/services
```

**Verify OTLP endpoint**:
```python
# Correct: OTLP gRPC port (4317)
agent.enable_observability(jaeger_port=4317)

# Wrong: UI port (16686) or collector HTTP (14268)
```

**Force flush and wait**:
```python
manager.force_flush()
time.sleep(2)  # Wait for indexing
```

### Missing Child Spans

**Issue**: Only 2 spans when expecting 8

**Cause**: PRE events without matching POST events

**Fix**: Always send POST after PRE:
```python
await hook.handle(pre_context)
# ... operation ...
await hook.handle(post_context)  # Required!
```

### Invalid Parent Span IDs

**Cause**: Broken parent-child relationships

**Fix**: Ensure all PRE spans end with POST events

## Examples

See `examples/autonomy/hooks/`:
- `distributed_tracing_example.py`: Complete tracing setup
- Multi-agent tracing patterns
- Custom event filtering

## Resources

- **Implementation**: `src/kaizen/core/autonomy/observability/tracing_manager.py`
- **Hook**: `src/kaizen/core/autonomy/hooks/builtin/tracing_hook.py`
- **Tests**: `tests/unit/core/autonomy/observability/test_tracing_manager.py`
- **Jaeger Docs**: https://www.jaegertracing.io/docs/
- **OpenTelemetry**: https://opentelemetry.io/docs/languages/python/
