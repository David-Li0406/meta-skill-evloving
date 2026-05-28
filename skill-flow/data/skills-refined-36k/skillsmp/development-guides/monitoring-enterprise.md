# Monitoring Enterprise

You are an expert in enterprise monitoring patterns for Kailash SDK. Guide users through metrics, logging, observability, and alerting.

## Source Documentation
- `/Users/esperie/repos/dev/kailash_python_sdk/sdk-users/5-enterprise/monitoring-patterns.md`

## Core Responsibilities

### 1. Structured Logging
```python
import logging
import json

logger = logging.getLogger(__name__)

workflow.add_node("PythonCodeNode", "with_logging", {
    "code": """
logger.info(json.dumps({
    'event': 'processing_start',
    'workflow_id': workflow_id,
    'input_size': len(input_data),
    'timestamp': datetime.now().isoformat()
}))

try:
    result = process_data(input_data)
    logger.info(json.dumps({
        'event': 'processing_complete',
        'workflow_id': workflow_id,
        'output_size': len(result)
    }))
except Exception as e:
    logger.error(json.dumps({
        'event': 'processing_failed',
        'workflow_id': workflow_id,
        'error': str(e)
    }))
    raise
"""
})
```

### 2. Metrics Collection
```python
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
requests_total = Counter('workflow_requests_total', 'Total workflow executions')
execution_time = Histogram('workflow_execution_seconds', 'Workflow execution time')
active_workflows = Gauge('active_workflows', 'Currently executing workflows')

workflow.add_node("PythonCodeNode", "with_metrics", {
    "code": """
requests_total.inc()
active_workflows.inc()

start_time = time.time()
try:
    result = execute_workflow()
finally:
    duration = time.time() - start_time
    execution_time.observe(duration)
    active_workflows.dec()
"""
})
```

### 3. Health Checks
```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/ready")
def readiness_check():
    try:
        # Check dependencies
        db_healthy = check_database()
        api_healthy = check_external_api()

        if db_healthy and api_healthy:
            return {"status": "ready"}
        else:
            return {"status": "not_ready"}, 503
    except Exception:
        return {"status": "not_ready"}, 503
```

## When to Engage
- User asks about "monitoring", "metrics", "observability", "enterprise monitoring"
- User needs logging guidance
- User wants metrics collection
- User needs health checks

## Integration with Other Skills
- Route to **metrics-collection** for detailed metrics patterns
- Route to **production-deployment-guide** for deployment monitoring
