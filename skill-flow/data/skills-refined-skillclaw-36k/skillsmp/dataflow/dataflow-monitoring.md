---
name: dataflow-monitoring
description: "DataFlow monitoring and metrics. Use when asking 'dataflow monitoring', 'dataflow metrics', or 'dataflow performance'."
---

# DataFlow Monitoring

> **Skill Metadata**
> Category: `dataflow`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`

## Enable Monitoring

```python
from dataflow import DataFlow

db = DataFlow("postgresql://localhost/app")

# Enable query logging
db.configure(
    echo_sql=True,  # Log all SQL queries
    track_metrics=True  # Track operation metrics
)

# Access metrics
metrics = db.get_metrics()
print(f"Total queries: {metrics['query_count']}")
print(f"Avg query time: {metrics['avg_query_ms']}ms")
print(f"Failed operations: {metrics['error_count']}")
```

## Query Performance Monitoring

```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

# Monitor slow queries
workflow.add_node("UserListNode", "get_users", {
    "filters": {"status": "active"},
    "track_performance": True  # Enable timing
})

# Log performance
workflow.add_node("ConditionalNode", "check_slow", {
    "condition": "{{get_users.execution_time_ms}} > 1000",
    "true_branch": "log_slow_query"
})

workflow.add_node("DatabaseExecuteNode", "log_slow_query", {
    "query": "INSERT INTO slow_queries (operation, duration_ms) VALUES (?, ?)",
    "parameters": ["UserListNode", "{{get_users.execution_time_ms}}"]
})
```

## Documentation

- **Monitoring Guide**: [`sdk-users/apps/dataflow/11-monitoring.md`](../../../../sdk-users/apps/dataflow/11-monitoring.md)

<!-- Trigger Keywords: dataflow monitoring, dataflow metrics, dataflow performance, query performance -->
