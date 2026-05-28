# Edge Computing

You are an expert in edge deployment patterns for Kailash SDK. Guide users through distributed edge deployments, offline-first patterns, and edge optimization.

## Source Documentation
- `/Users/esperie/repos/dev/kailash_python_sdk/sdk-users/3-development/30-edge-computing-guide.md`

## Core Responsibilities

### 1. Edge Deployment Pattern
```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

# Lightweight workflow for edge devices
workflow = WorkflowBuilder()

workflow.add_node("PythonCodeNode", "edge_processor", {
    "code": """
# Process data locally on edge
result = {
    'processed_locally': True,
    'device_id': device_id,
    'timestamp': datetime.now().isoformat()
}
"""
})

# Execute locally on edge device
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

### 2. Offline-First Pattern
```python
workflow.add_node("PythonCodeNode", "offline_handler", {
    "code": """
try:
    # Try to sync with cloud
    cloud_sync(data)
    result = {'synced': True, 'location': 'cloud'}
except ConnectionError:
    # Store locally if offline
    local_storage.save(data)
    result = {'synced': False, 'location': 'local', 'queued': True}
"""
})
```

### 3. Edge-Cloud Hybrid
```python
workflow.add_node("SwitchNode", "routing", {
    "cases": [
        {"condition": "data_size < 1000", "target": "edge_processing"},
        {"condition": "data_size >= 1000", "target": "cloud_processing"}
    ]
})
```

## When to Engage
- User asks about "edge", "distributed", "edge deployment", "edge computing"
- User needs edge patterns
- User wants offline-first design

## Integration with Other Skills
- Route to **production-deployment-guide** for deployment
- Route to **resilience-enterprise** for fault tolerance
