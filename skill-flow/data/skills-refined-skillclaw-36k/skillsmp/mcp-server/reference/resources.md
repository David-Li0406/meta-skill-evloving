# MCP Resources Reference

Resources expose data for reading via URI-based access. Unlike tools, resources are read-only and provide data to AI agents.

## Basic Resource Definition

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting."""
    return f"Hello, {name}!"
```

**Key points:**
- Use `@mcp.resource(uri_template)` decorator
- URI template uses `{param}` for path parameters
- Returns string data (text content)
- Read-only - no side effects

## Static Resource

```python
@mcp.resource("config://app")
def get_app_config() -> str:
    """Get application configuration."""
    return """{
        "app_name": "Todo App",
        "version": "1.0.0",
        "features": ["tasks", "categories", "reminders"]
    }"""
```

## Dynamic Resource with Parameters

```python
@mcp.resource("tasks://{user_id}")
def get_user_tasks(user_id: str) -> str:
    """Get all tasks for a specific user."""
    tasks = fetch_tasks_from_db(user_id)
    return json.dumps([task.model_dump() for task in tasks])
```

## Resource with Multiple Parameters

```python
@mcp.resource("tasks://{user_id}/{status}")
def get_tasks_by_status(user_id: str, status: str) -> str:
    """Get tasks filtered by status for a user."""
    tasks = fetch_tasks_from_db(user_id, status=status)
    return json.dumps([task.model_dump() for task in tasks])
```

## Async Resource

```python
@mcp.resource("stats://{user_id}")
async def get_user_stats(user_id: str) -> str:
    """Get task statistics for a user."""
    async with get_async_session() as session:
        total = await session.scalar(
            select(func.count(Task.id)).where(Task.user_id == user_id)
        )
        completed = await session.scalar(
            select(func.count(Task.id)).where(
                Task.user_id == user_id,
                Task.completed == True
            )
        )

    return json.dumps({
        "total_tasks": total,
        "completed_tasks": completed,
        "completion_rate": completed / total if total > 0 else 0
    })
```

## Resource with Context

```python
from mcp.server.fastmcp import Context, FastMCP

@mcp.resource("data://{table}")
def get_table_data(table: str, ctx: Context) -> str:
    """Get data from a database table."""
    app_ctx = ctx.request_context.lifespan_context
    db = app_ctx.db

    # Use lifespan-managed database connection
    rows = db.query(f"SELECT * FROM {table} LIMIT 100")
    return json.dumps(rows)
```

## Resource with Icons

```python
from mcp.server.fastmcp import FastMCP, Icon

data_icon = Icon(src="data-icon.png", mimeType="image/png")

@mcp.resource("report://summary", icons=[data_icon])
def get_summary_report() -> str:
    """Get summary report with custom icon."""
    return json.dumps({"report": "data"})
```

## Resource URI Patterns

| Pattern | Example URI | Parameters |
|---------|-------------|------------|
| `tasks://{user_id}` | `tasks://user123` | `user_id="user123"` |
| `tasks://{user_id}/{status}` | `tasks://user123/pending` | `user_id="user123", status="pending"` |
| `config://app` | `config://app` | None (static) |
| `file://{path}` | `file://docs/readme` | `path="docs/readme"` |

## Reading Resources (Client Side)

```python
# From MCP client
resource = await session.read_resource(AnyUrl("tasks://user123"))
content = resource.contents[0]
if isinstance(content, types.TextContent):
    data = json.loads(content.text)
```

## List Available Resources (Client Side)

```python
# List all resources
resources = await session.list_resources()
for resource in resources.resources:
    print(f"URI: {resource.uri}, Name: {resource.name}")

# List resource templates (for dynamic resources)
templates = await session.list_resource_templates()
for template in templates.resourceTemplates:
    print(f"Template: {template.uriTemplate}")
```

## Resource vs Tool

| Aspect | Resource | Tool |
|--------|----------|------|
| Purpose | Read data | Perform actions |
| Side effects | None | Can have |
| Access pattern | URI-based | Function call |
| Caching | Can be cached | Not cached |
| Use case | Data retrieval | CRUD operations |

## Best Practices

1. **Use resources for read-only data** - If it modifies state, use a tool
2. **Return JSON strings** - Easy for agents to parse
3. **Include useful metadata** - Help agents understand the data
4. **Use descriptive URI schemes** - `tasks://`, `users://`, `config://`
5. **Handle missing data gracefully** - Return empty results, not errors
6. **Document URI parameters** - Clear docstrings help agents
