# Durable Gateway

You are an expert in durable gateway patterns for Kailash SDK. Guide users through API gateway patterns, request persistence, and retry mechanisms.

## Source Documentation
- `/Users/esperie/repos/dev/kailash_python_sdk/sdk-users/3-development/29-durable-gateway-guide.md`

## Core Responsibilities

### 1. Durable Gateway Pattern
```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

# Persist request
workflow.add_node("PythonCodeNode", "persist_request", {
    "code": """
# Save request for durability
request_id = str(uuid.uuid4())
db.save_request(request_id, request_data)

result = {'request_id': request_id, 'persisted': True}
"""
})

# Process with retry
workflow.add_node("PythonCodeNode", "process_with_retry", {
    "code": """
max_retries = 3
attempt = 0

while attempt < max_retries:
    try:
        response = process_request(request_data)
        db.mark_complete(request_id)
        break
    except Exception as e:
        attempt += 1
        if attempt >= max_retries:
            db.mark_failed(request_id, str(e))
            raise

result = {'response': response, 'attempts': attempt}
"""
})
```

### 2. Request Recovery
```python
workflow.add_node("PythonCodeNode", "recover_requests", {
    "code": """
# Recover failed requests on startup
failed_requests = db.get_failed_requests()

for request in failed_requests:
    try:
        process_request(request)
        db.mark_complete(request['id'])
    except Exception:
        continue

result = {'recovered': len(failed_requests)}
"""
})
```

## When to Engage
- User asks about "durable gateway", "gateway patterns", "API gateway"
- User needs request persistence
- User wants retry mechanisms

## Integration with Other Skills
- Route to **resilience-enterprise** for resilience patterns
- Route to **production-deployment-guide** for deployment
