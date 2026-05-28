# Database Integration with MCP Server

Patterns for integrating MCP servers with databases using SQLModel and async sessions.

## SQLModel Integration Pattern

### Synchronous Database Access

```python
import contextlib
import os
from dataclasses import dataclass
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select
from mcp.server.fastmcp import Context, FastMCP

# ============================================================================
# Models
# ============================================================================

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)

class User(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)

# ============================================================================
# Database Engine
# ============================================================================

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

# ============================================================================
# MCP Context with Database
# ============================================================================

@dataclass
class AppContext:
    engine: any

@contextlib.asynccontextmanager
async def app_lifespan(server: FastMCP):
    """Initialize database on startup."""
    init_db()
    yield AppContext(engine=engine)

# ============================================================================
# MCP Server
# ============================================================================

mcp = FastMCP(
    "DB Server",
    lifespan=app_lifespan,
    stateless_http=True,
    json_response=True,
)

# ============================================================================
# Tools with Database Access
# ============================================================================

@mcp.tool()
def create_task(user_id: str, title: str, ctx: Context) -> dict:
    """Create a task in the database."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        task = Task(title=title, user_id=user_id)
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"id": task.id, "title": task.title}

@mcp.tool()
def get_tasks(user_id: str, ctx: Context) -> list:
    """Get all tasks for a user."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
        return [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]
```

## Async Database with SQLAlchemy

For high-concurrency applications, use async sessions:

```python
import contextlib
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, select
from mcp.server.fastmcp import Context, FastMCP

# Async engine
DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"
async_engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

@dataclass
class AsyncAppContext:
    session_factory: any

@contextlib.asynccontextmanager
async def async_lifespan(server: FastMCP):
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield AsyncAppContext(session_factory=AsyncSessionLocal)
    await async_engine.dispose()

mcp = FastMCP("Async DB Server", lifespan=async_lifespan)

@mcp.tool()
async def get_tasks_async(user_id: str, ctx: Context) -> list:
    """Get tasks using async database session."""
    app_ctx = ctx.request_context.lifespan_context
    async with app_ctx.session_factory() as session:
        result = await session.execute(
            select(Task).where(Task.user_id == user_id)
        )
        tasks = result.scalars().all()
        return [{"id": t.id, "title": t.title} for t in tasks]
```

## Neon Serverless PostgreSQL

For Neon database with connection pooling:

```python
import os
from sqlmodel import create_engine

# Neon connection with SSL
DATABASE_URL = os.getenv("DATABASE_URL")  # postgresql://user:pass@host/db?sslmode=require

# Connection pool settings for serverless
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
)
```

## Transaction Patterns

### Single Transaction

```python
@mcp.tool()
def transfer_task(from_user: str, to_user: str, task_id: int, ctx: Context) -> dict:
    """Transfer a task to another user in a single transaction."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != from_user:
            return {"success": False, "error": "Task not found or not authorized"}

        # Both operations in single transaction
        task.user_id = to_user
        session.add(task)
        session.commit()

        return {"success": True, "new_owner": to_user}
```

### Explicit Transaction Control

```python
@mcp.tool()
def bulk_complete_tasks(user_id: str, task_ids: list[int], ctx: Context) -> dict:
    """Complete multiple tasks in a single transaction."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        try:
            completed = []
            for task_id in task_ids:
                task = session.get(Task, task_id)
                if task and task.user_id == user_id:
                    task.completed = True
                    session.add(task)
                    completed.append(task_id)

            session.commit()
            return {"success": True, "completed": completed}

        except Exception as e:
            session.rollback()
            return {"success": False, "error": str(e)}
```

## Query Patterns

### Filtering

```python
@mcp.tool()
def search_tasks(
    user_id: str,
    query: str = None,
    completed: bool = None,
    limit: int = 50,
    ctx: Context = None,
) -> list:
    """Search tasks with multiple filters."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        statement = select(Task).where(Task.user_id == user_id)

        if query:
            statement = statement.where(Task.title.contains(query))
        if completed is not None:
            statement = statement.where(Task.completed == completed)

        statement = statement.limit(limit)
        tasks = session.exec(statement).all()
        return [t.model_dump() for t in tasks]
```

### Aggregation

```python
from sqlmodel import func

@mcp.tool()
def get_task_stats(user_id: str, ctx: Context) -> dict:
    """Get task statistics for a user."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        # Count total tasks
        total = session.exec(
            select(func.count(Task.id)).where(Task.user_id == user_id)
        ).one()

        # Count completed tasks
        completed = session.exec(
            select(func.count(Task.id)).where(
                Task.user_id == user_id,
                Task.completed == True
            )
        ).one()

        return {
            "total": total,
            "completed": completed,
            "pending": total - completed,
            "completion_rate": round(completed / total * 100, 1) if total > 0 else 0,
        }
```

### Pagination

```python
@mcp.tool()
def get_tasks_paginated(
    user_id: str,
    page: int = 1,
    page_size: int = 20,
    ctx: Context = None,
) -> dict:
    """Get tasks with pagination."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        # Get total count
        total = session.exec(
            select(func.count(Task.id)).where(Task.user_id == user_id)
        ).one()

        # Get page
        offset = (page - 1) * page_size
        tasks = session.exec(
            select(Task)
            .where(Task.user_id == user_id)
            .offset(offset)
            .limit(page_size)
        ).all()

        return {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
            "tasks": [t.model_dump() for t in tasks],
        }
```

## Error Handling

```python
from sqlalchemy.exc import IntegrityError

@mcp.tool()
def create_user(user_id: str, name: str, email: str, ctx: Context) -> dict:
    """Create a new user with proper error handling."""
    app_ctx = ctx.request_context.lifespan_context
    with Session(app_ctx.engine) as session:
        try:
            user = User(id=user_id, name=name, email=email)
            session.add(user)
            session.commit()
            return {"success": True, "user_id": user_id}

        except IntegrityError:
            session.rollback()
            return {"success": False, "error": "Email already exists"}

        except Exception as e:
            session.rollback()
            return {"success": False, "error": str(e)}
```

## Best Practices

1. **Use context for database access** - Pass engine via lifespan context
2. **Create sessions per request** - Don't share sessions across tool calls
3. **Handle transactions properly** - Use session.commit() and session.rollback()
4. **Return serializable data** - Use model_dump() or manual dict conversion
5. **Validate user authorization** - Check user_id before modifying data
6. **Use indexes** - Add Field(index=True) for frequently queried columns
7. **Pool connections** - Configure pool_size for production
8. **Handle errors gracefully** - Return error dicts instead of raising exceptions
