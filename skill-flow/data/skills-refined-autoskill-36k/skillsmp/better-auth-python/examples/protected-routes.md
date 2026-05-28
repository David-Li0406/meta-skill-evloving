# Protected Routes Examples

Complete examples for protecting FastAPI routes with Better Auth JWT verification.

## Basic Protected Route

```python
from fastapi import APIRouter, Depends, HTTPException
from app.auth import User, get_current_user

router = APIRouter(prefix="/api", tags=["protected"])


@router.get("/me")
async def get_current_user_info(user: User = Depends(get_current_user)):
    """Get current user information from JWT."""
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
    }
```

## Resource Ownership Pattern

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models import Task
from app.auth import User, get_current_user

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/{task_id}")
async def get_task(
    task_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Get a task - only if owned by current user."""
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Ownership check
    if task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Delete a task - only if owned by current user."""
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    session.delete(task)
    session.commit()
```

## List with Filtering

```python
@router.get("", response_model=list[TaskRead])
async def get_tasks(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    completed: bool | None = None,
    skip: int = 0,
    limit: int = 100,
):
    """Get all tasks for the current user with optional filtering."""
    statement = select(Task).where(Task.user_id == user.id)

    if completed is not None:
        statement = statement.where(Task.completed == completed)

    statement = statement.offset(skip).limit(limit)

    return session.exec(statement).all()
```

## Create Resource

```python
from datetime import datetime
from app.models import TaskCreate, TaskRead


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
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

## Update Resource

```python
from app.models import TaskUpdate


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Update a task - only if owned by current user."""
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Only update provided fields
    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

## Optional Authentication

```python
from typing import Optional


async def get_optional_user(
    authorization: str | None = Header(None),
) -> Optional[User]:
    """Get user if authenticated, None otherwise."""
    if not authorization:
        return None

    try:
        # Reuse your existing verification logic
        from app.auth import verify_token
        return await verify_token(authorization)
    except:
        return None


@router.get("/public")
async def public_endpoint(user: Optional[User] = Depends(get_optional_user)):
    """Endpoint accessible to both authenticated and anonymous users."""
    if user:
        return {"message": f"Hello, {user.name}!"}
    return {"message": "Hello, anonymous user!"}
```

## Role-Based Access

```python
from functools import wraps
from typing import Callable


def require_role(required_role: str):
    """Dependency factory for role-based access."""
    async def role_checker(user: User = Depends(get_current_user)):
        # Assumes user has a 'role' field from JWT claims
        if not hasattr(user, 'role') or user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail=f"Role '{required_role}' required"
            )
        return user
    return role_checker


@router.get("/admin/users")
async def list_all_users(
    user: User = Depends(require_role("admin")),
    session: Session = Depends(get_session),
):
    """Admin-only endpoint to list all users."""
    # Your admin logic here
    pass
```

## Bulk Operations

```python
@router.post("/bulk", response_model=list[TaskRead])
async def create_tasks_bulk(
    tasks_data: list[TaskCreate],
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Create multiple tasks at once."""
    tasks = [
        Task(**data.model_dump(), user_id=user.id)
        for data in tasks_data
    ]
    session.add_all(tasks)
    session.commit()
    for task in tasks:
        session.refresh(task)
    return tasks


@router.delete("/bulk")
async def delete_completed_tasks(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Delete all completed tasks for the current user."""
    statement = select(Task).where(
        Task.user_id == user.id,
        Task.completed == True
    )
    tasks = session.exec(statement).all()

    for task in tasks:
        session.delete(task)

    session.commit()
    return {"deleted": len(tasks)}
```
