# Function Tools Reference

Define custom tools that agents can call during conversations.

## Basic Function Tool

```python
from agents import function_tool

@function_tool
def get_weather(city: str) -> str:
    """Get the weather for a city.

    Args:
        city: The name of the city
    """
    # Implementation
    return f"The weather in {city} is sunny."
```

## Tool with Multiple Parameters

```python
@function_tool
def create_task(
    title: str,
    description: str = None,
    priority: str = "medium",
) -> dict:
    """Create a new task.

    Args:
        title: Task title (required)
        description: Optional task description
        priority: Task priority (low, medium, high)
    """
    return {
        "id": 1,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "created",
    }
```

## Async Function Tool

```python
import httpx

@function_tool
async def fetch_data(url: str) -> dict:
    """Fetch data from a URL.

    Args:
        url: The URL to fetch
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

## Tool with Type Hints

```python
from typing import Literal, Optional, List

@function_tool
def search_tasks(
    user_id: str,
    status: Literal["pending", "completed", "all"] = "all",
    priority: Optional[Literal["low", "medium", "high"]] = None,
    tags: List[str] = None,
) -> dict:
    """Search tasks with filters.

    Args:
        user_id: User ID to search tasks for
        status: Filter by status (pending, completed, or all)
        priority: Optional priority filter
        tags: Optional list of tags to filter by
    """
    # Implementation
    return {"tasks": [], "count": 0}
```

## Tool with Database Access

```python
from sqlmodel import Session

# Pass database session via closure
def create_task_tools(engine):
    @function_tool
    def add_task(user_id: str, title: str) -> dict:
        """Add a new task."""
        with Session(engine) as session:
            task = Task(title=title, user_id=user_id)
            session.add(task)
            session.commit()
            session.refresh(task)
            return {"id": task.id, "title": task.title}

    @function_tool
    def list_tasks(user_id: str) -> list:
        """List all tasks for a user."""
        with Session(engine) as session:
            tasks = session.exec(
                select(Task).where(Task.user_id == user_id)
            ).all()
            return [t.model_dump() for t in tasks]

    return [add_task, list_tasks]

# Usage
tools = create_task_tools(engine)
agent = Agent(name="Assistant", tools=tools, ...)
```

## Register Tools with Agent

```python
from agents import Agent

@function_tool
def tool_one(param: str) -> str:
    """First tool."""
    return "result one"

@function_tool
def tool_two(param: str) -> str:
    """Second tool."""
    return "result two"

agent = Agent(
    name="Assistant",
    instructions="Use tools to help users.",
    tools=[tool_one, tool_two],
    model=model,
)
```

## Tool Error Handling

```python
@function_tool
def safe_operation(id: int) -> dict:
    """Perform a safe operation.

    Args:
        id: The ID to operate on
    """
    try:
        # Attempt operation
        result = perform_operation(id)
        return {"success": True, "result": result}
    except NotFoundError:
        return {"success": False, "error": "Item not found"}
    except PermissionError:
        return {"success": False, "error": "Not authorized"}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Tool Return Types

Tools should return JSON-serializable data:

```python
# Good - returns dict
@function_tool
def good_tool(param: str) -> dict:
    return {"key": "value"}

# Good - returns string
@function_tool
def string_tool(param: str) -> str:
    return "result string"

# Good - returns list
@function_tool
def list_tool(param: str) -> list:
    return [1, 2, 3]

# Avoid - complex objects (serialize first)
@function_tool
def serialized_tool(param: str) -> dict:
    obj = ComplexObject()
    return obj.model_dump()  # Convert to dict
```

## Docstring Best Practices

The docstring is used as the tool description for the LLM:

```python
@function_tool
def well_documented_tool(
    user_id: str,
    action: str,
    target_id: int = None,
) -> dict:
    """Perform an action on behalf of a user.

    This tool executes the specified action. Use it when the user
    wants to modify their data.

    Args:
        user_id: The ID of the user making the request (required)
        action: The action to perform - one of: create, update, delete
        target_id: The ID of the target item (required for update/delete)

    Returns:
        A dictionary with:
        - success: Boolean indicating if action succeeded
        - message: Description of what happened
        - data: Any relevant data from the action

    Example:
        well_documented_tool("user123", "create")
        well_documented_tool("user123", "delete", target_id=42)
    """
    # Implementation
    return {"success": True, "message": "Action completed"}
```

## Combining MCP Tools and Function Tools

```python
from agents import Agent, function_tool
from agents.mcp import MCPServerStreamableHttp

# Local function tool
@function_tool
def format_response(data: dict) -> str:
    """Format data for display."""
    return f"Formatted: {data}"

async with MCPServerStreamableHttp(...) as mcp_server:
    agent = Agent(
        name="Assistant",
        # Both MCP tools and function tools
        mcp_servers=[mcp_server],
        tools=[format_response],
        ...
    )
```

## Best Practices

1. **Clear docstrings** - They're shown to the LLM
2. **Type hints** - Improve tool discovery and validation
3. **Return dicts** - Structured data is easier for LLMs to use
4. **Error handling** - Return error info, don't raise exceptions
5. **Keep tools focused** - One tool = one action
6. **Validate inputs** - Check parameters before processing
