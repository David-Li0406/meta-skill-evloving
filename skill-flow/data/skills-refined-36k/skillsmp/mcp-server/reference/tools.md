# MCP Tools Reference

Tools are functions that perform actions, computations, or have side effects. They are the primary way for AI agents to interact with your server.

## Basic Tool Definition

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b
```

**Key points:**
- Use `@mcp.tool()` decorator
- Docstring becomes the tool description (required for good UX)
- Type hints define the input schema
- Return type defines output format

## Tool with Optional Parameters

```python
@mcp.tool()
def create_task(
    title: str,
    description: str = None,
    priority: str = "medium",
    due_date: str = None,
) -> dict:
    """Create a new task.

    Args:
        title: The task title (required)
        description: Optional task description
        priority: Task priority (low, medium, high)
        due_date: Optional due date in ISO format
    """
    return {
        "id": 1,
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "status": "created",
    }
```

## Async Tool

```python
@mcp.tool()
async def fetch_data(url: str) -> dict:
    """Fetch data from a URL asynchronously."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

## Tool with Context

The `Context` object provides access to MCP capabilities like logging and progress reporting.

```python
from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP("Context Server")

@mcp.tool()
async def process_items(items: list[str], ctx: Context) -> str:
    """Process a list of items with progress updates."""
    total = len(items)

    await ctx.info(f"Starting to process {total} items")

    for i, item in enumerate(items):
        # Report progress
        await ctx.report_progress(
            progress=(i + 1) / total,
            total=1.0,
            message=f"Processing item {i + 1}/{total}",
        )

        # Log debug info
        await ctx.debug(f"Processing: {item}")

        # Simulate work
        await asyncio.sleep(0.1)

    await ctx.info("Processing complete")
    return f"Processed {total} items"
```

**Context methods:**
- `ctx.info(message)` - Info level log
- `ctx.debug(message)` - Debug level log
- `ctx.warning(message)` - Warning level log
- `ctx.error(message)` - Error level log
- `ctx.report_progress(progress, total, message)` - Progress updates

## Tool with Database Access

```python
from mcp.server.fastmcp import Context, FastMCP
from sqlmodel import Session, select

@mcp.tool()
def list_tasks(user_id: str, status: str = None, ctx: Context) -> list[dict]:
    """List tasks for a user, optionally filtered by status."""
    app_ctx = ctx.request_context.lifespan_context

    with Session(app_ctx.engine) as session:
        statement = select(Task).where(Task.user_id == user_id)
        if status:
            statement = statement.where(Task.status == status)

        tasks = session.exec(statement).all()
        return [task.model_dump() for task in tasks]
```

## Tool with Validation

```python
from typing import Literal

@mcp.tool()
def update_task_status(
    task_id: int,
    status: Literal["pending", "in_progress", "completed"],
) -> dict:
    """Update a task's status.

    Args:
        task_id: The ID of the task to update
        status: New status (pending, in_progress, or completed)
    """
    # Literal type creates enum-like validation
    return {"task_id": task_id, "status": status, "updated": True}
```

## Tool with Complex Return Types

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class TaskResult:
    id: int
    title: str
    completed: bool
    error: Optional[str] = None

@mcp.tool()
def get_task(task_id: int) -> dict:
    """Get a task by ID."""
    # Return as dict for JSON serialization
    return {
        "id": task_id,
        "title": "Example Task",
        "completed": False,
        "error": None,
    }
```

## Tool with Error Handling

```python
@mcp.tool()
def delete_task(task_id: int, user_id: str) -> dict:
    """Delete a task by ID.

    Returns success status or error message.
    """
    try:
        # Verify ownership
        task = get_task_by_id(task_id)
        if not task:
            return {"success": False, "error": "Task not found"}

        if task.user_id != user_id:
            return {"success": False, "error": "Not authorized"}

        # Delete task
        delete_task_from_db(task_id)
        return {"success": True, "deleted_id": task_id}

    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Tool with Icons

```python
from mcp.server.fastmcp import FastMCP, Icon

icon = Icon(src="task-icon.png", mimeType="image/png", sizes="64x64")

@mcp.tool(icons=[icon])
def add_task(title: str) -> dict:
    """Add a task with a custom icon in UI."""
    return {"id": 1, "title": title}
```

## Best Practices

1. **Clear docstrings** - The docstring is shown to the AI agent
2. **Type hints** - Always use type hints for inputs
3. **Validation** - Validate inputs before processing
4. **Error handling** - Return structured errors, don't raise exceptions
5. **Idempotency** - Design tools to be safely retryable when possible
6. **Minimal side effects** - Be explicit about what changes
7. **Progress reporting** - Use context for long-running operations
