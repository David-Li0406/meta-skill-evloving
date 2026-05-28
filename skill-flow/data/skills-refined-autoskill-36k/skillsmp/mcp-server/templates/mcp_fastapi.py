"""
FastAPI + MCP Integration Template

A complete template for integrating MCP server into an existing FastAPI application.
This allows both REST API endpoints and MCP tools to coexist and share resources.

Usage:
    uvicorn mcp_fastapi:app --reload

Endpoints:
    - REST API: http://localhost:8000/api/...
    - MCP Server: http://localhost:8000/api/mcp
"""

import contextlib
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from mcp.server.fastmcp import Context, FastMCP


# ============================================================================
# Configuration
# ============================================================================

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")


# ============================================================================
# Database Models
# ============================================================================

class Task(SQLModel, table=True):
    """Task model for todo application."""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    status: str = Field(default="pending", index=True)
    priority: str = Field(default="medium")
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Database Setup
# ============================================================================

engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI dependency for database session."""
    with Session(engine) as session:
        yield session


# ============================================================================
# Pydantic Models (for REST API)
# ============================================================================

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Literal["low", "medium", "high"] = "medium"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal["pending", "in_progress", "completed"]] = None
    priority: Optional[Literal["low", "medium", "high"]] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    user_id: str
    created_at: datetime
    updated_at: datetime


# ============================================================================
# MCP Server Setup
# ============================================================================

@dataclass
class MCPContext:
    """Context passed to MCP tools."""
    engine: any


@contextlib.asynccontextmanager
async def mcp_lifespan(server: FastMCP):
    """MCP server lifespan - provides database access to tools."""
    yield MCPContext(engine=engine)


# Create MCP server
mcp = FastMCP(
    name="Todo MCP Server",
    lifespan=mcp_lifespan,
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
    ctx: Context = None,
) -> dict:
    """Add a new task for a user."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        task = Task(
            title=title,
            description=description,
            priority=priority,
            user_id=user_id,
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "priority": task.priority,
            },
        }


@mcp.tool()
def list_tasks(
    user_id: str,
    status: Literal["pending", "in_progress", "completed", "all"] = "all",
    ctx: Context = None,
) -> dict:
    """List tasks for a user with optional status filter."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        statement = select(Task).where(Task.user_id == user_id)
        if status != "all":
            statement = statement.where(Task.status == status)
        tasks = session.exec(statement).all()
        return {
            "success": True,
            "count": len(tasks),
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "status": t.status,
                    "priority": t.priority,
                }
                for t in tasks
            ],
        }


@mcp.tool()
def complete_task(user_id: str, task_id: int, ctx: Context = None) -> dict:
    """Mark a task as completed."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return {"success": False, "error": "Task not found"}
        task.status = "completed"
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        return {"success": True, "message": f"Task '{task.title}' completed"}


@mcp.tool()
def delete_task(user_id: str, task_id: int, ctx: Context = None) -> dict:
    """Delete a task."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return {"success": False, "error": "Task not found"}
        session.delete(task)
        session.commit()
        return {"success": True, "deleted_id": task_id}


@mcp.tool()
def update_task(
    user_id: str,
    task_id: int,
    title: str = None,
    description: str = None,
    status: Literal["pending", "in_progress", "completed"] = None,
    priority: Literal["low", "medium", "high"] = None,
    ctx: Context = None,
) -> dict:
    """Update a task's details."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return {"success": False, "error": "Task not found"}

        if title:
            task.title = title
        if description:
            task.description = description
        if status:
            task.status = status
        if priority:
            task.priority = priority

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "priority": task.priority,
            },
        }


# ============================================================================
# MCP Prompts
# ============================================================================

@mcp.prompt()
def task_assistant(user_name: str = "User") -> str:
    """System prompt for task management assistant."""
    return f"""You are a helpful task management assistant for {user_name}.

Available tools:
- add_task: Create new tasks
- list_tasks: View existing tasks (can filter by status)
- complete_task: Mark tasks as completed
- delete_task: Remove tasks
- update_task: Modify task details

Be helpful, confirm actions, and suggest task organization."""


# ============================================================================
# FastAPI Application
# ============================================================================

@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI):
    """Application lifespan - init DB and MCP session manager."""
    init_db()
    async with mcp.session_manager.run():
        yield


app = FastAPI(
    title="Todo API with MCP",
    description="REST API and MCP Server for task management",
    version="1.0.0",
    lifespan=app_lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Mcp-Session-Id"],
)

# Mount MCP server
app.mount("/api/mcp", mcp.streamable_http_app())


# ============================================================================
# REST API Routes (alongside MCP)
# ============================================================================

@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "mcp_enabled": True}


@app.get("/api/tasks/{user_id}", response_model=list[TaskResponse])
def get_tasks(
    user_id: str,
    status: Optional[str] = None,
    session: Session = Depends(get_session),
):
    """Get all tasks for a user (REST API)."""
    statement = select(Task).where(Task.user_id == user_id)
    if status:
        statement = statement.where(Task.status == status)
    return session.exec(statement).all()


@app.post("/api/tasks/{user_id}", response_model=TaskResponse)
def create_task(
    user_id: str,
    task_data: TaskCreate,
    session: Session = Depends(get_session),
):
    """Create a new task (REST API)."""
    task = Task(
        **task_data.model_dump(),
        user_id=user_id,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.patch("/api/tasks/{user_id}/{task_id}", response_model=TaskResponse)
def update_task_rest(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
):
    """Update a task (REST API)."""
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/api/tasks/{user_id}/{task_id}")
def delete_task_rest(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
):
    """Delete a task (REST API)."""
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"success": True, "deleted_id": task_id}


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
