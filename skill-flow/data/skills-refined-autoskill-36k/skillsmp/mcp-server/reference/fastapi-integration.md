# FastAPI + MCP Integration Reference

Integrate MCP servers into existing FastAPI applications by mounting the MCP app as a sub-application.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Application                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐  │
│  │   /api/tasks    │  │   /api/users    │  │    /api/mcp    │  │
│  │   (REST API)    │  │   (REST API)    │  │  (MCP Server)  │  │
│  └─────────────────┘  └─────────────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Basic Integration

```python
import contextlib
from fastapi import FastAPI
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP

# Create FastAPI app
app = FastAPI(title="Todo API")

# Create MCP server
mcp = FastMCP("Todo MCP", stateless_http=True, json_response=True)
mcp.settings.streamable_http_path = "/"

# Define MCP tools
@mcp.tool()
def add_task(title: str, description: str = None) -> dict:
    """Add a new task."""
    return {"id": 1, "title": title, "description": description}

@mcp.tool()
def list_tasks() -> list:
    """List all tasks."""
    return []

# Lifespan manager
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp.session_manager.run():
        yield

app = FastAPI(title="Todo API", lifespan=lifespan)

# Mount MCP at /api/mcp
app.mount("/api/mcp", mcp.streamable_http_app())

# Regular FastAPI routes
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# Run with: uvicorn main:app --reload
# MCP endpoint: http://localhost:8000/api/mcp
```

## Shared Database Connection

```python
import contextlib
from dataclasses import dataclass
from fastapi import FastAPI, Depends
from sqlmodel import Session, create_engine, SQLModel
from mcp.server.fastmcp import Context, FastMCP

# Database setup
DATABASE_URL = "postgresql://user:pass@localhost/db"
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

# MCP Lifespan context
@dataclass
class MCPContext:
    engine: any

@contextlib.asynccontextmanager
async def mcp_lifespan(server: FastMCP):
    yield MCPContext(engine=engine)

# Create MCP server with database access
mcp = FastMCP("Todo MCP", lifespan=mcp_lifespan, stateless_http=True, json_response=True)
mcp.settings.streamable_http_path = "/"

@mcp.tool()
def add_task_mcp(title: str, user_id: str, ctx: Context) -> dict:
    """Add a task via MCP."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        task = Task(title=title, user_id=user_id)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task.model_dump()

# FastAPI app lifespan
@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    async with mcp.session_manager.run():
        yield

app = FastAPI(lifespan=app_lifespan)
app.mount("/api/mcp", mcp.streamable_http_app())

# Regular FastAPI routes with same database
@app.post("/api/tasks")
def create_task(title: str, user_id: str, session: Session = Depends(get_session)):
    task = Task(title=title, user_id=user_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

## With Authentication

```python
from fastapi import FastAPI, Depends, HTTPException, Header
from mcp.server.fastmcp import Context, FastMCP

# Auth dependency for FastAPI
async def get_current_user(authorization: str = Header(...)):
    # Verify JWT token
    user = verify_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

# MCP server
mcp = FastMCP("Authenticated MCP", stateless_http=True, json_response=True)

@mcp.tool()
def get_my_tasks(user_id: str, ctx: Context) -> list:
    """Get tasks for authenticated user.

    Note: user_id should be passed by the agent after authentication.
    """
    # In MCP, authentication is typically handled by the client
    # The agent passes user context to tools
    return fetch_tasks_for_user(user_id)

# FastAPI routes with auth
@app.get("/api/tasks")
async def get_tasks(user = Depends(get_current_user)):
    return fetch_tasks_for_user(user.id)
```

## CORS Configuration

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP("MCP Server", stateless_http=True, json_response=True)

# Add CORS middleware BEFORE mounting MCP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Mcp-Session-Id"],  # Required for MCP sessions
)

app.mount("/api/mcp", mcp.streamable_http_app())
```

## Complete Example: Todo App

```python
import contextlib
import os
from dataclasses import dataclass
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select
from mcp.server.fastmcp import Context, FastMCP

# Models
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

# MCP Context
@dataclass
class MCPAppContext:
    engine: any

@contextlib.asynccontextmanager
async def mcp_lifespan(server: FastMCP):
    yield MCPAppContext(engine=engine)

# MCP Server
mcp = FastMCP(
    "Todo MCP Server",
    lifespan=mcp_lifespan,
    stateless_http=True,
    json_response=True,
)
mcp.settings.streamable_http_path = "/"

# MCP Tools
@mcp.tool()
def add_task(user_id: str, title: str, description: str = None, ctx: Context) -> dict:
    """Add a new task for a user."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        task = Task(title=title, description=description, user_id=user_id)
        session.add(task)
        session.commit()
        session.refresh(task)
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
        }

@mcp.tool()
def list_tasks(user_id: str, completed: bool = None, ctx: Context) -> list:
    """List tasks for a user, optionally filtered by completion status."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        statement = select(Task).where(Task.user_id == user_id)
        if completed is not None:
            statement = statement.where(Task.completed == completed)
        tasks = session.exec(statement).all()
        return [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "completed": t.completed,
            }
            for t in tasks
        ]

@mcp.tool()
def complete_task(user_id: str, task_id: int, ctx: Context) -> dict:
    """Mark a task as completed."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return {"success": False, "error": "Task not found"}
        task.completed = True
        session.add(task)
        session.commit()
        return {"success": True, "task_id": task_id}

@mcp.tool()
def delete_task(user_id: str, task_id: int, ctx: Context) -> dict:
    """Delete a task."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return {"success": False, "error": "Task not found"}
        session.delete(task)
        session.commit()
        return {"success": True, "deleted_id": task_id}

# MCP Prompts
@mcp.prompt()
def task_assistant(user_name: str = "User") -> str:
    """System prompt for task management."""
    return f"""You are a helpful task management assistant for {user_name}.
Help them manage their tasks efficiently using the available tools."""

# App Lifespan
@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    async with mcp.session_manager.run():
        yield

# FastAPI App
app = FastAPI(title="Todo API", lifespan=app_lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Mcp-Session-Id"],
)

# Mount MCP
app.mount("/api/mcp", mcp.streamable_http_app())

# REST API Routes (optional, alongside MCP)
@app.get("/api/health")
def health():
    return {"status": "healthy"}

@app.get("/api/tasks/{user_id}")
def get_tasks_rest(user_id: str, session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks
```

## Testing

```python
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from mcp import ClientSession, streamablehttp_client

# Test REST endpoints
def test_health():
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200

# Test MCP endpoint
@pytest.mark.asyncio
async def test_mcp_tools():
    async with streamablehttp_client("http://localhost:8000/api/mcp") as (
        read, write, _
    ):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            tool_names = [t.name for t in tools.tools]
            assert "add_task" in tool_names
            assert "list_tasks" in tool_names
```

## Best Practices

1. **Use stateless mode** for production
2. **Share database connections** via lifespan context
3. **Configure CORS** before mounting MCP
4. **Mount at `/api/mcp`** for clear API organization
5. **Use `streamable_http_path = "/"** for cleaner URLs
6. **Handle errors gracefully** in MCP tools
7. **Document tools clearly** with docstrings
