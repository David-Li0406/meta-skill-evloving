# Kaizen Metrics Collection

**Quick reference for Prometheus metrics with p50/p95/p99 percentiles**

## Overview

Production-ready metrics collection with Prometheus exposition format. Track agent execution rates, latencies, success/failure rates with counters, gauges, and histograms.

**Performance**: -0.06% overhead (validated with 100 OpenAI calls)

## Quick Start

```python
from kaizen.core.base_agent import BaseAgent

# Enable metrics (one line!)
agent = BaseAgent(config=config, signature=signature)
agent.enable_observability(
    service_name="my-agent",
    enable_metrics=True
)

# Metrics automatically collected
result = agent.run(question="test")
```

**Access Prometheus**: `http://localhost:9090`

## MetricsCollector

Prometheus-compatible metrics collection:

```python
from kaizen.core.autonomy.observability import MetricsCollector

collector = MetricsCollector()

# Counter (monotonic increment)
collector.increment_counter("agent_loop_total", labels={"agent_id": "qa-agent"})

# Gauge (current value)
collector.set_gauge("agent_active_loops", value=5)

# Histogram (duration tracking)
collector.record_histogram("agent_loop_duration_seconds", value=0.234)
```

## Metric Types

### Counter
Monotonically increasing values (total requests, errors):

```python
# Increment counter
collector.increment_counter(
    name="agent_loop_total",
    labels={"agent_id": "qa-agent", "status": "success"}
)

# Example output:
# agent_loop_total{agent_id="qa-agent",status="success"} 156
```

### Gauge
Current value that can go up/down (active connections, memory usage):

```python
# Set gauge value
collector.set_gauge(
    name="agent_active_loops",
    value=3
)

# Increment/decrement
collector.increment_gauge("agent_active_loops", delta=1)
collector.decrement_gauge("agent_active_loops", delta=1)

# Example output:
# agent_active_loops 3
```

### Histogram
Distribution of values with percentiles (latency, request size):

```python
# Record observation
collector.record_histogram(
    name="agent_loop_duration_seconds",
    value=0.234,
    labels={"agent_id": "qa-agent"}
)

# Automatically calculates p50, p95, p99
# Example output:
# agent_loop_duration_seconds{quantile="0.5"} 0.150
# agent_loop_duration_seconds{quantile="0.95"} 0.450
# agent_loop_duration_seconds{quantile="0.99"} 0.780
# agent_loop_duration_seconds_sum 45.6
# agent_loop_duration_seconds_count 200
```

## MetricsHook

Automatic metrics collection via hooks:

```python
from kaizen.core.autonomy.hooks.builtin import MetricsHook

hook = MetricsHook(metrics_collector=collector)
agent._hook_manager.register_hook(hook)
```

**Metrics collected automatically**:
- `agent_loop_total`: Total agent executions
- `agent_loop_duration_seconds`: Execution duration (p50/p95/p99)
- `agent_loop_errors_total`: Error count
- `agent_active_loops`: Currently executing agents

## Prometheus Format Export

```python
# Export metrics in Prometheus text format
metrics_text = collector.export_prometheus_metrics()
print(metrics_text)
```

**Example output**:
```
# HELP agent_loop_duration_seconds Agent loop duration
# TYPE agent_loop_duration_seconds histogram
agent_loop_duration_seconds{quantile="0.5"} 0.150
agent_loop_duration_seconds{quantile="0.95"} 0.450
agent_loop_duration_seconds{quantile="0.99"} 0.780
agent_loop_duration_seconds_sum 45.6
agent_loop_duration_seconds_count 200

# HELP agent_loop_total Total agent loops executed
# TYPE agent_loop_total counter
agent_loop_total{agent_id="qa-agent"} 156

# HELP agent_loop_errors_total Total agent loop errors
# TYPE agent_loop_errors_total counter
agent_loop_errors_total{agent_id="qa-agent"} 3

# HELP agent_active_loops Currently active agent loops
# TYPE agent_active_loops gauge
agent_active_loops 2
```

## Common Patterns

### Performance Monitoring

```python
import time

# Start timer
start_time = time.time()

# Execute operation
result = agent.run(question="test")

# Record duration
duration = time.time() - start_time
collector.record_histogram("agent_loop_duration_seconds", duration)
```

### Success/Failure Tracking

```python
# Count by status
if result.get("success"):
    collector.increment_counter("agent_loop_total", {"status": "success"})
else:
    collector.increment_counter("agent_loop_total", {"status": "failure"})
    collector.increment_counter("agent_loop_errors_total")
```

### Resource Monitoring

```python
# Track active operations
collector.increment_gauge("agent_active_loops", delta=1)
try:
    result = agent.run(question="test")
finally:
    collector.decrement_gauge("agent_active_loops", delta=1)
```

### Multi-Agent Metrics

```python
# Per-agent metrics with labels
for agent in agents:
    collector.increment_counter(
        "agent_loop_total",
        labels={"agent_id": agent.agent_id, "agent_type": agent.__class__.__name__}
    )
```

## Production Deployment

### Expose Metrics Endpoint

```python
from flask import Flask, Response

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    metrics_text = collector.export_prometheus_metrics()
    return Response(metrics_text, mimetype="text/plain")

if __name__ == "__main__":
    app.run(port=8000)
```

### Prometheus Configuration

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'kaizen-agents'
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:8000']
```

### Docker Compose Stack

```bash
# Start Prometheus + Grafana
cd docs/observability
docker-compose up -d
```

**Included**:
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`
- Pre-built dashboards

## Grafana Dashboards

### Agent Performance Dashboard
- Request rate (requests/sec)
- Latency percentiles (p50, p95, p99)
- Error rate (%)
- Active agents (gauge)

### PromQL Queries

**Request rate**:
```promql
rate(agent_loop_total[5m])
```

**p95 latency**:
```promql
histogram_quantile(0.95, agent_loop_duration_seconds)
```

**Error rate**:
```promql
rate(agent_loop_errors_total[5m]) / rate(agent_loop_total[5m])
```

**Active agents**:
```promql
agent_active_loops
```

## Testing

```python
import pytest

def test_metrics_collection():
    collector = MetricsCollector()

    # Record metrics
    collector.increment_counter("test_counter")
    collector.set_gauge("test_gauge", value=42)
    collector.record_histogram("test_histogram", value=0.123)

    # Export and verify
    metrics_text = collector.export_prometheus_metrics()

    assert "test_counter 1" in metrics_text
    assert "test_gauge 42" in metrics_text
    assert "test_histogram" in metrics_text
```

## Custom Metrics

```python
# Business metrics
collector.increment_counter("questions_answered_total")
collector.record_histogram("answer_quality_score", value=0.85)
collector.set_gauge("pending_questions", value=12)

# Cost tracking
collector.increment_counter("llm_api_calls_total", labels={"model": "gpt-4"})
collector.record_histogram("llm_cost_usd", value=0.003)
```

## Alerting

### Example Alert Rules

```yaml
# alerts.yml
groups:
  - name: kaizen_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(agent_loop_errors_total[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate in agent execution"

      - alert: HighLatency
        expr: histogram_quantile(0.95, agent_loop_duration_seconds) > 1.0
        for: 10m
        annotations:
          summary: "p95 latency exceeds 1 second"
```

## Examples

See `examples/autonomy/hooks/prometheus_metrics_example.py`:
- Complete metrics setup
- Multi-agent monitoring
- Prometheus export format
- Custom business metrics

## Resources

- **Implementation**: `src/kaizen/core/autonomy/observability/metrics_collector.py`
- **Hook**: `src/kaizen/core/autonomy/hooks/builtin/metrics_hook.py`
- **Tests**: `tests/unit/core/autonomy/observability/test_metrics_collector.py`
- **Prometheus Docs**: https://prometheus.io/docs/
- **Grafana**: https://grafana.com/docs/
