# Better Auth + SQLModel Integration

Complete guide for using SQLModel with Better Auth JWT verification in FastAPI.

## Installation

```bash
# pip
pip install sqlmodel fastapi uvicorn pyjwt cryptography httpx

# poetry
poetry add sqlmodel fastapi uvicorn pyjwt cryptography httpx

# uv
uv add sqlmodel fastapi uvicorn pyjwt cryptography httpx
```

## File Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── auth.py              # JWT verification
│   ├── database.py          # SQLModel setup
│   ├── models.py            # SQLModel models
│   └── routes/
│       ├── __init__.py
│       └── tasks.py         # Protected routes
├── .env
└── requirements.txt
```

## Database Setup

```python
# app/database.py
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# For SQLite
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
```

## Models

```python
# app/models.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class Task(SQLModel, table=True):
    """Task model - user's tasks stored in your database."""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)  # From JWT 'sub' claim
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(SQLModel):
    """Request model for creating tasks."""
    title: str
    description: Optional[str] = None


class TaskUpdate(SQLModel):
    """Request model for updating tasks."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskRead(SQLModel):
    """Response model for tasks."""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    user_id: str
    created_at: datetime
    updated_at: datetime
```

## Protected Routes with User Isolation

```python
# app/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from app.database import get_session
from app.models import Task, TaskCreate, TaskUpdate, TaskRead
from app.auth import User, get_current_user

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=List[TaskRead])
async def get_tasks(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    completed: bool | None = None,
):
    """Get all tasks for the current user."""
    statement = select(Task).where(Task.user_id == user.id)

    if completed is not None:
        statement = statement.where(Task.completed == completed)

    tasks = session.exec(statement).all()
    return tasks


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Get a specific task (only if owned by user)."""
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return task


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Create a new task for the current user."""
    task = Task(
        **task_data.model_dump(),
        user_id=user.id,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Update a task (only if owned by user)."""
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Delete a task (only if owned by user)."""
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    session.delete(task)
    session.commit()
```

## Main Application

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import create_db_and_tables
from app.routes import tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown


app = FastAPI(
    title="My API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-domain.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)


@app.get("/api/health")
async def health():
    return {"status": "healthy"}
```

## PostgreSQL Configuration

```python
# app/database.py
from sqlmodel import SQLModel, create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# PostgreSQL async support
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)
```

## Async SQLModel (Optional)

```python
# app/database.py
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL").replace(
    "postgresql://", "postgresql+asyncpg://"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


# In routes, use async:
@router.get("")
async def get_tasks(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.exec(select(Task).where(Task.user_id == user.id))
    return result.all()
```

## Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
BETTER_AUTH_URL=http://localhost:3000
```

## Common Patterns

### Pagination

```python
@router.get("", response_model=List[TaskRead])
async def get_tasks(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
):
    statement = (
        select(Task)
        .where(Task.user_id == user.id)
        .offset(skip)
        .limit(limit)
    )
    return session.exec(statement).all()
```

### Search

```python
@router.get("/search")
async def search_tasks(
    q: str,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    statement = (
        select(Task)
        .where(Task.user_id == user.id)
        .where(Task.title.contains(q))
    )
    return session.exec(statement).all()
```

### Bulk Operations

```python
@router.post("/bulk", response_model=List[TaskRead])
async def create_tasks_bulk(
    tasks_data: List[TaskCreate],
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    tasks = [
        Task(**data.model_dump(), user_id=user.id)
        for data in tasks_data
    ]
    session.add_all(tasks)
    session.commit()
    for task in tasks:
        session.refresh(task)
    return tasks
```
