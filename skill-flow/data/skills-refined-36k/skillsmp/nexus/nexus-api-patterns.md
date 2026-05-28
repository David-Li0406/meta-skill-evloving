---
skill: nexus-api-patterns
description: REST API usage patterns, endpoints, requests, and responses for Nexus workflows
priority: HIGH
tags: [nexus, api, rest, http, endpoints]
---

# Nexus API Patterns

Master REST API usage patterns for Nexus workflows.

## Core API Endpoints

Every registered workflow automatically gets these endpoints:

```bash
# Execute workflow
POST /workflows/{workflow_name}/execute

# Get workflow schema
GET /workflows/{workflow_name}/schema

# List all workflows
GET /workflows

# Health check
GET /health

# OpenAPI documentation
GET /docs
```

## Custom REST Endpoints

Create custom FastAPI-style endpoints with path parameters, query parameters, and rate limiting:

```python
from nexus import Nexus
from fastapi import Request

app = Nexus()

# Custom endpoint with path parameters
@app.endpoint("/api/conversations/{conversation_id}", methods=["GET"], rate_limit=50)
async def get_conversation(conversation_id: str):
    """Get conversation by ID."""
    result = await app._execute_workflow("chat_workflow", {"id": conversation_id})
    return {"conversation_id": conversation_id, "data": result}

# Query parameters (built-in FastAPI support)
@app.endpoint("/api/search")
async def search(q: str, limit: int = 10, offset: int = 0):
    """Search with pagination."""
    result = await app._execute_workflow("search_workflow", {
        "query": q,
        "limit": limit,
        "offset": offset
    })
    return result

# Multiple HTTP methods (CRUD)
@app.endpoint("/api/messages/{msg_id}", methods=["GET", "PUT", "DELETE"])
async def manage_message(msg_id: str, request: Request):
    """Full CRUD on messages."""
    if request.method == "GET":
        return await app._execute_workflow("get_message", {"id": msg_id})
    elif request.method == "PUT":
        body = await request.json()
        return await app._execute_workflow("update_message", {"id": msg_id, **body})
    elif request.method == "DELETE":
        return await app._execute_workflow("delete_message", {"id": msg_id})
```

### Key Features (v1.1.0):
- ✅ **Path Parameters**: Automatically validated by FastAPI
- ✅ **Query Parameters**: Type coercion, defaults, `pattern` validation
- ✅ **Rate Limiting**: Per-endpoint with automatic cleanup (default 100 req/min)
- ✅ **Security**: Input size (10MB max), dangerous key blocking, key length (256 chars)
- ✅ **HTTP Methods**: GET, POST, PUT, DELETE, PATCH
- ✅ **Workflow Integration**: Use `_execute_workflow()` helper

## Basic Workflow Execution

```bash
curl -X POST http://localhost:8000/workflows/my-workflow/execute \
  -H "Content-Type: application/json" \
  -d '{"inputs": {"param1": "value1"}}'
```

## Request Format

```json
{
  "inputs": {
    "param1": "value1",
    "param2": 123,
    "param3": true
  },
  "session_id": "optional-session-id",
  "context": {
    "user_id": "user123",
    "request_id": "req-abc"
  }
}
```

### Request Fields

- **inputs** (required): Parameters passed to workflow
- **session_id** (optional): For session continuity
- **context** (optional): Metadata for tracking

## Response Format

```json
{
  "success": true,
  "result": {
    "data": "workflow output here"
  },
  "workflow_id": "wf-12345",
  "execution_time": 1.23,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Response Fields

- **success**: Boolean indicating execution status
- **result**: Workflow output data
- **workflow_id**: Unique execution identifier
- **execution_time**: Duration in seconds
- **timestamp**: Execution timestamp

## Error Handling

```json
{
  "success": false,
  "error": {
    "type": "ValidationError",
    "message": "Invalid parameter: param1",
    "details": {
      "field": "param1",
      "expected": "string",
      "received": "number"
    }
  },
  "workflow_id": "wf-12345",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## API Configuration

```python
from nexus import Nexus

app = Nexus(
    api_port=8000,
    api_host="0.0.0.0",
    enable_docs=True,
    enable_cors=True
)

# Fine-tune API behavior
app.api.response_compression = True
app.api.request_timeout = 30
app.api.max_concurrent_requests = 100
app.api.max_request_size = 10 * 1024 * 1024  # 10MB
```

## Advanced Request Patterns

### With Session Management

```bash
# Create and use session
curl -X POST http://localhost:8000/workflows/process/execute \
  -H "Content-Type: application/json" \
  -H "X-Session-ID: session-123" \
  -d '{"inputs": {"step": 1}}'

# Continue with same session
curl -X POST http://localhost:8000/workflows/process/execute \
  -H "X-Session-ID: session-123" \
  -d '{"inputs": {"step": 2}}'
```

### With Authentication

```bash
curl -X POST http://localhost:8000/workflows/secure-workflow/execute \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"inputs": {"data": "value"}}'
```

### With Custom Headers

```bash
curl -X POST http://localhost:8000/workflows/my-workflow/execute \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: req-12345" \
  -H "X-User-ID: user-789" \
  -d '{"inputs": {"param": "value"}}'
```

## SSE Streaming for Real-Time Chat

```python
# Execute workflow in streaming mode
# POST /execute with {"mode": "stream"}

# Browser JavaScript client
const eventSource = new EventSource('/workflows/chat/execute?mode=stream');

eventSource.addEventListener('start', (e) => {
    const data = JSON.parse(e.data);
    console.log('Workflow started:', data.workflow_id);
});

eventSource.addEventListener('complete', (e) => {
    const data = JSON.parse(e.data);
    console.log('Result:', data.result);
});

eventSource.addEventListener('error', (e) => {
    const data = JSON.parse(e.data);
    console.error('Error:', data.error);
});
```

```bash
# Python client with httpx
import httpx

with httpx.stream("POST", "http://localhost:8000/execute",
                  json={"inputs": {}, "mode": "stream"}) as response:
    for line in response.iter_lines():
        if line.startswith('data:'):
            data = json.loads(line[5:])  # Remove 'data:' prefix
            print(data)
```

**SSE Format Specification:**
- `id: <event-id>` - For reconnection support
- `event: <type>` - Event types: start, complete, error, keepalive
- `data: <json>` - JSON payload
- `\n\n` - Event terminator

**Event Types:**
1. **start** - Workflow execution started
2. **complete** - Workflow finished successfully
3. **error** - Execution failed
4. **keepalive** - Connection maintenance

**📚 Complete SSE Guide**: See [SSE Streaming](../../apps/kailash-nexus/docs/technical/sse_streaming.md)

## Batch Operations

```bash
# Execute multiple workflows in batch
curl -X POST http://localhost:8000/workflows/batch \
  -H "Content-Type: application/json" \
  -d '{
    "workflows": [
      {
        "name": "workflow1",
        "inputs": {"param": "value1"}
      },
      {
        "name": "workflow2",
        "inputs": {"param": "value2"}
      }
    ]
  }'
```

## Query Parameters

```bash
# With query parameters
curl -X POST "http://localhost:8000/workflows/search/execute?limit=10&offset=0" \
  -H "Content-Type: application/json" \
  -d '{"inputs": {"query": "search term"}}'
```

## Workflow Schema Discovery

```bash
# Get workflow input/output schema
curl http://localhost:8000/workflows/my-workflow/schema

# Response
{
  "name": "my-workflow",
  "inputs": {
    "param1": {"type": "string", "required": true},
    "param2": {"type": "integer", "default": 10}
  },
  "outputs": {
    "result": {"type": "object"}
  }
}
```

## Python Client Examples

### Using Requests

```python
import requests

class NexusClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def execute_workflow(self, workflow_name, inputs, session_id=None):
        url = f"{self.base_url}/workflows/{workflow_name}/execute"

        headers = {"Content-Type": "application/json"}
        if session_id:
            headers["X-Session-ID"] = session_id

        response = self.session.post(
            url,
            json={"inputs": inputs},
            headers=headers
        )

        response.raise_for_status()
        return response.json()

    def get_schema(self, workflow_name):
        url = f"{self.base_url}/workflows/{workflow_name}/schema"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def list_workflows(self):
        url = f"{self.base_url}/workflows"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

# Usage
client = NexusClient()
result = client.execute_workflow("my-workflow", {"param": "value"})
print(result)
```

### Async Client

```python
import aiohttp
import asyncio

class AsyncNexusClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    async def execute_workflow(self, workflow_name, inputs):
        url = f"{self.base_url}/workflows/{workflow_name}/execute"

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json={"inputs": inputs}
            ) as response:
                return await response.json()

    async def execute_many(self, workflows):
        tasks = [
            self.execute_workflow(wf["name"], wf["inputs"])
            for wf in workflows
        ]
        return await asyncio.gather(*tasks)

# Usage
async def main():
    client = AsyncNexusClient()
    results = await client.execute_many([
        {"name": "wf1", "inputs": {"param": "val1"}},
        {"name": "wf2", "inputs": {"param": "val2"}}
    ])
    print(results)

asyncio.run(main())
```

## Rate Limiting

```python
# Configure rate limiting
app = Nexus(
    rate_limit=1000,  # Requests per minute
    rate_limit_burst=100  # Burst capacity
)
```

```bash
# Rate limit headers in response
HTTP/1.1 200 OK
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1705315200
```

## CORS Configuration

```python
# Configure CORS
app = Nexus()

app.api.cors_enabled = True
app.api.cors_origins = ["https://example.com", "https://app.example.com"]
app.api.cors_methods = ["GET", "POST"]
app.api.cors_headers = ["Content-Type", "Authorization"]
app.api.cors_credentials = True
```

## API Versioning

```python
# Version your API
app = Nexus(api_prefix="/api/v1")

# Endpoints become:
# POST /api/v1/workflows/{name}/execute
```

## Health Checks

```bash
# Basic health check
curl http://localhost:8000/health

# Response
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": 3600,
  "workflows": 5,
  "active_sessions": 3
}

# Detailed health check
curl http://localhost:8000/health/detailed

# Response
{
  "status": "healthy",
  "components": {
    "api": {"status": "healthy"},
    "database": {"status": "healthy"},
    "cache": {"status": "healthy"}
  }
}
```

## Monitoring and Metrics

```bash
# Prometheus metrics
curl http://localhost:8000/metrics

# Response (Prometheus format)
# HELP nexus_requests_total Total requests
# TYPE nexus_requests_total counter
nexus_requests_total{workflow="my-workflow"} 123
nexus_requests_total{workflow="other-workflow"} 456
```

## Error Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Workflow executed successfully |
| 400 | Bad Request | Invalid input parameters |
| 401 | Unauthorized | Missing or invalid auth token |
| 404 | Not Found | Workflow does not exist |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Error | Workflow execution failed |
| 503 | Service Unavailable | Server overloaded |

## Best Practices

1. **Use Sessions for Multi-Step Workflows**
2. **Handle Errors Gracefully**
3. **Implement Retry Logic** with exponential backoff
4. **Set Appropriate Timeouts**
5. **Monitor Rate Limits**
6. **Use Async Clients** for concurrent requests
7. **Validate Inputs** before sending
8. **Log Request IDs** for debugging

## Testing API Endpoints

```python
import pytest
import requests

class TestNexusAPI:
    base_url = "http://localhost:8000"

    def test_workflow_execution(self):
        response = requests.post(
            f"{self.base_url}/workflows/test-workflow/execute",
            json={"inputs": {"param": "value"}}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "result" in data

    def test_workflow_not_found(self):
        response = requests.post(
            f"{self.base_url}/workflows/nonexistent/execute",
            json={"inputs": {}}
        )

        assert response.status_code == 404

    def test_invalid_input(self):
        response = requests.post(
            f"{self.base_url}/workflows/test-workflow/execute",
            json={"inputs": {"wrong_param": "value"}}
        )

        assert response.status_code == 400

    def test_health_check(self):
        response = requests.get(f"{self.base_url}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
```

## Key Takeaways

- Every workflow gets automatic REST endpoints
- Use `inputs` field for workflow parameters
- Sessions enable multi-step workflows
- Configure CORS, rate limiting, and auth as needed
- Use async clients for concurrent requests
- Monitor via health checks and metrics
- Test all endpoints thoroughly

## Related Skills

- [nexus-multi-channel](#) - API, CLI, MCP overview
- [nexus-api-input-mapping](#) - How inputs map to nodes
- [nexus-sessions](#) - Session management
- [nexus-enterprise-features](#) - Auth and rate limiting
- [nexus-troubleshooting](#) - Fix API issues
