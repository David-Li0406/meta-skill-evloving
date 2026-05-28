---
name: nodes-monitoring-reference
description: "Monitoring nodes reference (metrics, alerts, deadlocks). Use when asking 'monitoring node', 'metrics', 'alerts', 'deadlock detection', or 'performance monitoring'."
---

# Monitoring Nodes Reference

Complete reference for monitoring and observability nodes.

> **Skill Metadata**
> Category: `nodes`
> Priority: `LOW`
> SDK Version: `0.9.25+`
> Related Skills: [`nodes-quick-index`](nodes-quick-index.md)
> Related Subagents: `pattern-expert` (monitoring patterns)

## Quick Reference

```python
from kailash.nodes.monitoring import (
    TransactionMetricsNode,
    TransactionMonitorNode,
    DeadlockDetectorNode,
    RaceConditionDetectorNode,
    PerformanceAnomalyNode
)
```

## Transaction Metrics

### TransactionMetricsNode
```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

workflow.add_node("TransactionMetricsNode", "metrics", {
    "operation": "collect",
    "transaction_id": "txn_123",
    "metrics": {
        "duration_ms": 150,
        "status": "success"
    }
})
```

## Real-Time Monitoring

### TransactionMonitorNode
```python
workflow.add_node("TransactionMonitorNode", "monitor", {
    "operation": "trace",
    "transaction_id": "txn_123",
    "alert_thresholds": {
        "duration_ms": 1000,
        "error_rate": 0.05
    }
})
```

## Issue Detection

### DeadlockDetectorNode
```python
workflow.add_node("DeadlockDetectorNode", "deadlock_check", {
    "operation": "detect",
    "timeout_seconds": 30
})
```

### RaceConditionDetectorNode
```python
workflow.add_node("RaceConditionDetectorNode", "race_check", {
    "operation": "analyze",
    "resource_id": "resource_123"
})
```

### PerformanceAnomalyNode
```python
workflow.add_node("PerformanceAnomalyNode", "anomaly_check", {
    "operation": "detect",
    "metric": "response_time",
    "threshold": 1000
})
```

## Related Skills

- **Node Index**: [`nodes-quick-index`](nodes-quick-index.md)

## Documentation

- **Monitoring Nodes**: [`sdk-users/2-core-concepts/nodes/monitoring-nodes.md`](../../../../sdk-users/2-core-concepts/nodes/monitoring-nodes.md)

<!-- Trigger Keywords: monitoring node, metrics, alerts, deadlock detection, performance monitoring, TransactionMetricsNode -->
