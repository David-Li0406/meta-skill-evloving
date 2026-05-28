# MCP Advanced Features

You are an expert in advanced MCP features including structured tools, progress reporting, and resource management.

## Source Documentation
- `/Users/esperie/repos/dev/kailash_python_sdk/sdk-users/3-development/27-mcp-advanced-features-guide.md`

## Core Responsibilities

### 1. Structured Tools with Pydantic
```python
from kailash.core.mcp_server import MCPServer
from pydantic import BaseModel, Field

server = MCPServer(name="advanced-server")

class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    limit: int = Field(default=10, ge=1, le=100)
    filters: dict = Field(default_factory=dict)

@server.tool(
    name="structured_search",
    description="Search with structured parameters"
)
def search(request: SearchRequest) -> dict:
    return {
        "results": perform_search(request.query, request.limit, request.filters),
        "query": request.query,
        "limit": request.limit
    }
```

### 2. Progress Reporting
```python
@server.tool(
    name="long_running_task",
    description="Task with progress updates"
)
def long_task(items: list, progress_callback=None) -> dict:
    total = len(items)

    for i, item in enumerate(items):
        process_item(item)

        # Report progress
        if progress_callback:
            progress_callback({
                "current": i + 1,
                "total": total,
                "percentage": ((i + 1) / total) * 100,
                "message": f"Processing item {i + 1} of {total}"
            })

    return {"processed": total, "status": "complete"}
```

### 3. Resource Subscriptions
```python
@server.resource(
    uri="realtime://updates",
    name="Realtime Updates",
    subscribable=True
)
def realtime_updates():
    """Streaming resource with subscriptions."""
    while True:
        yield {"timestamp": datetime.now().isoformat(), "data": get_latest_data()}
        time.sleep(1)
```

## When to Engage
- User asks about "MCP advanced", "structured tools", "MCP progress"
- User needs complex MCP patterns
- User wants progress reporting

## Integration with Other Skills
- Route to **mcp-development** for basic MCP
- Route to **mcp-specialist** for expert guidance
