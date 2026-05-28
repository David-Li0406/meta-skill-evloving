# Better Auth + SQLAlchemy Integration

Complete guide for using SQLAlchemy with Better Auth JWT verification in FastAPI.

## Installation

```bash
# pip
pip install sqlalchemy fastapi uvicorn pyjwt cryptography httpx psycopg2-binary

# poetry
poetry add sqlalchemy fastapi uvicorn pyjwt cryptography httpx psycopg2-binary

# uv
uv add sqlalchemy fastapi uvicorn pyjwt cryptography httpx psycopg2-binary

# For async
pip install asyncpg sqlalchemy[asyncio]
```

## File Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── auth.py              # JWT verification
│   ├── database.py          # SQLAlchemy setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   └── routes/
│       └── tasks.py
├── .env
└── requirements.txt
```

## Database Setup (Sync)

```python
# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Database Setup (Async)

```python
# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL").replace(
    "postgresql://", "postgresql+asyncpg://"
)

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
```

## Models

```python
# app/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    user_id = Column(String(255), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

## Pydantic Schemas

```python
# app/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskRead(TaskBase):
    id: int
    completed: bool
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
```

## Protected Routes (Sync)

```python
# app/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate, TaskRead
from app.auth import User, get_current_user

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=List[TaskRead])
def get_tasks(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """Get all tasks for the current user."""
    tasks = (
        db.query(Task)
        .filter(Task.user_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return tasks


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific task."""
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return task


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new task."""
    task = Task(**task_data.model_dump(), user_id=user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a task."""
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a task."""
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(task)
    db.commit()
```

## Protected Routes (Async)

```python
# app/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskRead
from app.auth import User, get_current_user

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=List[TaskRead])
async def get_tasks(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all tasks for the current user."""
    result = await db.execute(
        select(Task).where(Task.user_id == user.id)
    )
    return result.scalars().all()


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new task."""
    task = Task(**task_data.model_dump(), user_id=user.id)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task
```

## Main Application

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import tasks

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="My API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)
```

## Alembic Migrations

```bash
# Install
pip install alembic

# Initialize
alembic init alembic
```

```python
# alembic/env.py
from app.database import Base
from app.models import Task  # Import all models

target_metadata = Base.metadata
```

```bash
# Create migration
alembic revision --autogenerate -m "create tasks table"

# Run migration
alembic upgrade head
```

## Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
BETTER_AUTH_URL=http://localhost:3000
```

## Common Patterns

### Relationship with User Data

```python
# If you need to store user info locally
class UserCache(Base):
    __tablename__ = "user_cache"

    id = Column(String(255), primary_key=True)  # From JWT sub
    email = Column(String(255))
    name = Column(String(255))
    last_seen = Column(DateTime(timezone=True), server_default=func.now())

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"
    # ...
    owner = relationship("UserCache", back_populates="tasks")
```

### Soft Delete

```python
class Task(Base):
    __tablename__ = "tasks"
    # ...
    deleted_at = Column(DateTime(timezone=True), nullable=True)


# In queries
.filter(Task.deleted_at.is_(None))
```

### Audit Fields Mixin

```python
from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func


class AuditMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String(255))
    updated_by = Column(String(255))


class Task(Base, AuditMixin):
    __tablename__ = "tasks"
    # ...
```
