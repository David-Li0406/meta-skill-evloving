"""
FastAPI Router Template

Usage:
1. Copy this file to app/routers/your_resource.py
2. Rename the router and update the prefix
3. Import and include in main.py
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.dependencies.auth import User, get_current_user

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
)


# === LIST ===
@router.get("", response_model=List[TaskRead])
async def get_tasks(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    completed: bool | None = None,
):
    """Get all tasks for the current user."""
    statement = select(Task).where(Task.user_id == user.id)

    if completed is not None:
        statement = statement.where(Task.completed == completed)

    statement = statement.offset(skip).limit(limit)

    return session.exec(statement).all()


# === CREATE ===
@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Create a new task."""
    task = Task(**task_data.model_dump(), user_id=user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# === GET ONE ===
@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Get a single task by ID."""
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if task.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task",
        )

    return task


# === UPDATE ===
@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Update a task."""
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if task.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this task",
        )

    # Update only provided fields
    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# === DELETE ===
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Delete a task."""
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if task.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task",
        )

    session.delete(task)
    session.commit()


# === BULK OPERATIONS ===
@router.delete("", status_code=status.HTTP_200_OK)
async def delete_completed_tasks(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Delete all completed tasks for the current user."""
    statement = select(Task).where(
        Task.user_id == user.id,
        Task.completed == True,
    )
    tasks = session.exec(statement).all()

    count = len(tasks)
    for task in tasks:
        session.delete(task)

    session.commit()
    return {"deleted": count}
