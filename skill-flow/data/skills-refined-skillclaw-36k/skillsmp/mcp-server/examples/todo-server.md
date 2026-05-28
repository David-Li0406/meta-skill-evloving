# Todo MCP Server Example

A complete MCP server implementation for task management with all CRUD operations.

## Full Implementation

```python
"""
Todo MCP Server - Complete implementation with all task management tools.

Run standalone: python todo_mcp_server.py
Run with uvicorn: uvicorn todo_mcp_server:app --reload
"""

import contextlib
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal

from sqlmodel import Field, Session, SQLModel, create_engine, select
from mcp.server.fastmcp import Context, FastMCP

# ============================================================================
# Database Models
# ============================================================================

class Task(SQLModel, table=True):
    """Task model for the todo application."""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    status: str = Field(default="pending", index=True)  # pending, in_progress, completed
    priority: str = Field(default="medium")  # low, medium, high
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = None

# ============================================================================
# Database Setup
# ============================================================================

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

# ============================================================================
# MCP Context
# ============================================================================

@dataclass
class AppContext:
    """Application context with database engine."""
    engine: any

@contextlib.asynccontextmanager
async def app_lifespan(server: FastMCP):
    """Manage application lifecycle."""
    init_db()
    yield AppContext(engine=engine)

# ============================================================================
# MCP Server
# ============================================================================

mcp = FastMCP(
    "Todo MCP Server",
    lifespan=app_lifespan,
    stateless_http=True,
    json_response=True,
)
mcp.settings.streamable_http_path = "/"

# ============================================================================
# MCP Tools
# ============================================================================

@mcp.tool()
def add_task(
    user_id: str,
    title: str,
    description: str = None,
    priority: Literal["low", "medium", "high"] = "medium",
    due_date: str = None,
    ctx: Context = None,
) -> dict:
    """Add a new task to the todo list.

    Args:
        user_id: The ID of the user creating the task
        title: The task title (required)
        description: Optional detailed description
        priority: Task priority - low, medium, or high
        due_date: Optional due date in ISO format (YYYY-MM-DD)

    Returns:
        The created task with its assigned ID
    """
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        task = Task(
            title=title,
            description=description,
            priority=priority,
            user_id=user_id,
            due_date=datetime.fromisoformat(due_date) if due_date else None,
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat(),
            },
        }


@mcp.tool()
def list_tasks(
    user_id: str,
    status: Literal["pending", "in_progress", "completed", "all"] = "all",
    priority: Literal["low", "medium", "high", "all"] = "all",
    ctx: Context = None,
) -> dict:
    """List tasks for a user with optional filters.

    Args:
        user_id: The ID of the user
        status: Filter by status (pending, in_progress, completed, or all)
        priority: Filter by priority (low, medium, high, or all)

    Returns:
        List of matching tasks
    """
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        statement = select(Task).where(Task.user_id == user_id)

        if status != "all":
            statement = statement.where(Task.status == status)
        if priority != "all":
            statement = statement.where(Task.priority == priority)

        statement = statement.order_by(Task.created_at.desc())
        tasks = session.exec(statement).all()

        return {
            "success": True,
            "count": len(tasks),
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "status": t.status,
                    "priority": t.priority,
                    "due_date": t.due_date.isoformat() if t.due_date else None,
                    "created_at": t.created_at.isoformat(),
                }
                for t in tasks
            ],
        }


@mcp.tool()
def complete_task(
    user_id: str,
    task_id: int,
    ctx: Context = None,
) -> dict:
    """Mark a task as completed.

    Args:
        user_id: The ID of the user (for authorization)
        task_id: The ID of the task to complete

    Returns:
        Success status and updated task info
    """
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        task = session.get(Task, task_id)

        if not task:
            return {"success": False, "error": "Task not found"}

        if task.user_id != user_id:
            return {"success": False, "error": "Not authorized to modify this task"}

        task.status = "completed"
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()

        return {
            "success": True,
            "message": f"Task '{task.title}' marked as completed",
            "task_id": task_id,
        }


@mcp.tool()
def delete_task(
    user_id: str,
    task_id: int,
    ctx: Context = None,
) -> dict:
    """Delete a task from the todo list.

    Args:
        user_id: The ID of the user (for authorization)
        task_id: The ID of the task to delete

    Returns:
        Success status
    """
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        task = session.get(Task, task_id)

        if not task:
            return {"success": False, "error": "Task not found"}

        if task.user_id != user_id:
            return {"success": False, "error": "Not authorized to delete this task"}

        title = task.title
        session.delete(task)
        session.commit()

        return {
            "success": True,
            "message": f"Task '{title}' deleted",
            "deleted_id": task_id,
        }


@mcp.tool()
def update_task(
    user_id: str,
    task_id: int,
    title: str = None,
    description: str = None,
    status: Literal["pending", "in_progress", "completed"] = None,
    priority: Literal["low", "medium", "high"] = None,
    due_date: str = None,
    ctx: Context = None,
) -> dict:
    """Update an existing task.

    Args:
        user_id: The ID of the user (for authorization)
        task_id: The ID of the task to update
        title: New title (optional)
        description: New description (optional)
        status: New status (optional)
        priority: New priority (optional)
        due_date: New due date in ISO format (optional)

    Returns:
        Success status and updated task
    """
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        task = session.get(Task, task_id)

        if not task:
            return {"success": False, "error": "Task not found"}

        if task.user_id != user_id:
            return {"success": False, "error": "Not authorized to modify this task"}

        # Update fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if priority is not None:
            task.priority = priority
        if due_date is not None:
            task.due_date = datetime.fromisoformat(due_date)

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "updated_at": task.updated_at.isoformat(),
            },
        }

# ============================================================================
# MCP Resources
# ============================================================================

@mcp.resource("tasks://{user_id}")
def get_user_tasks_resource(user_id: str) -> str:
    """Get all tasks for a user as a resource."""
    import json
    with Session(engine) as session:
        tasks = session.exec(
            select(Task).where(Task.user_id == user_id)
        ).all()
        return json.dumps([
            {
                "id": t.id,
                "title": t.title,
                "status": t.status,
                "priority": t.priority,
            }
            for t in tasks
        ])


@mcp.resource("tasks://{user_id}/stats")
def get_user_stats_resource(user_id: str) -> str:
    """Get task statistics for a user."""
    import json
    with Session(engine) as session:
        total = len(session.exec(
            select(Task).where(Task.user_id == user_id)
        ).all())
        completed = len(session.exec(
            select(Task).where(Task.user_id == user_id, Task.status == "completed")
        ).all())
        pending = len(session.exec(
            select(Task).where(Task.user_id == user_id, Task.status == "pending")
        ).all())

        return json.dumps({
            "total": total,
            "completed": completed,
            "pending": pending,
            "in_progress": total - completed - pending,
            "completion_rate": round(completed / total * 100, 1) if total > 0 else 0,
        })

# ============================================================================
# MCP Prompts
# ============================================================================

@mcp.prompt()
def task_assistant(user_name: str = "User") -> str:
    """System prompt for the task management assistant."""
    return f"""You are a helpful task management assistant for {user_name}.

Your available tools are:
- add_task: Create new tasks with title, description, priority, and due date
- list_tasks: View tasks filtered by status or priority
- complete_task: Mark tasks as completed
- delete_task: Remove tasks
- update_task: Modify existing tasks

Guidelines:
1. Always confirm actions with clear summaries
2. Suggest task organization when you notice patterns
3. Remind about overdue or high-priority tasks
4. Be concise but friendly
5. Ask for clarification if task details are unclear"""


@mcp.prompt()
def daily_review() -> str:
    """Prompt for daily task review."""
    return """Let's review your tasks for today. I'll help you:

1. Check what tasks are pending
2. Identify any overdue items
3. Prioritize what to focus on
4. Plan your day effectively

What would you like to start with?"""

# ============================================================================
# Run Server
# ============================================================================

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
    # Accessible at http://localhost:8000/mcp
```

## Usage Examples

### Add a Task
```
User: "Add a task to review the quarterly report by Friday"
Agent: Calls add_task(user_id="user123", title="Review quarterly report", due_date="2024-01-12", priority="high")
```

### List Tasks
```
User: "Show my pending high priority tasks"
Agent: Calls list_tasks(user_id="user123", status="pending", priority="high")
```

### Complete a Task
```
User: "I finished the report review"
Agent: Calls complete_task(user_id="user123", task_id=1)
```

### Update a Task
```
User: "Change task 1 priority to low"
Agent: Calls update_task(user_id="user123", task_id=1, priority="low")
```

## Running the Server

```bash
# Standalone with streamable-http
python todo_mcp_server.py

# With uvicorn for production
uvicorn todo_mcp_server:mcp.streamable_http_app() --reload

# As part of FastAPI app (see fastapi-integration.md)
```

## Client Connection

```python
from mcp import streamablehttp_client, ClientSession

async def main():
    async with streamablehttp_client("http://localhost:8000/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print([t.name for t in tools.tools])

            # Call add_task tool
            result = await session.call_tool(
                "add_task",
                arguments={
                    "user_id": "user123",
                    "title": "Test task",
                    "priority": "high",
                }
            )
            print(result)
```
