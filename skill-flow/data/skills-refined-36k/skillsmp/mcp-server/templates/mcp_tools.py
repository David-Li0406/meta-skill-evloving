"""
MCP Tools Template - Todo CRUD operations.

This template provides the 5 essential todo task tools:
- add_task
- list_tasks
- complete_task
- delete_task
- update_task

Copy and adapt for your MCP server implementation.
"""

from datetime import datetime
from typing import Literal, Optional

from sqlmodel import Session, select
from mcp.server.fastmcp import Context, FastMCP

# Assuming Task model and engine are defined elsewhere
# from models import Task
# from database import engine


def register_todo_tools(mcp: FastMCP):
    """Register all todo tools with the MCP server."""

    @mcp.tool()
    def add_task(
        user_id: str,
        title: str,
        description: str = None,
        priority: Literal["low", "medium", "high"] = "medium",
        due_date: str = None,
        ctx: Context = None,
    ) -> dict:
        """
        Add a new task to the todo list.

        Args:
            user_id: The ID of the user creating the task
            title: The task title (required)
            description: Optional detailed description of the task
            priority: Task priority level - low, medium, or high (default: medium)
            due_date: Optional due date in ISO format (YYYY-MM-DD)

        Returns:
            The created task with its assigned ID and details

        Example:
            add_task(
                user_id="user123",
                title="Review quarterly report",
                priority="high",
                due_date="2024-01-15"
            )
        """
        app_ctx = ctx.request_context.lifespan_context

        with Session(app_ctx.engine) as session:
            task = Task(
                title=title,
                description=description,
                priority=priority,
                user_id=user_id,
                status="pending",
                due_date=datetime.fromisoformat(due_date) if due_date else None,
            )
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "message": f"Task '{title}' created successfully",
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
        limit: int = 50,
        ctx: Context = None,
    ) -> dict:
        """
        List tasks for a user with optional filters.

        Args:
            user_id: The ID of the user
            status: Filter by status - pending, in_progress, completed, or all (default: all)
            priority: Filter by priority - low, medium, high, or all (default: all)
            limit: Maximum number of tasks to return (default: 50)

        Returns:
            List of matching tasks with count

        Example:
            list_tasks(user_id="user123", status="pending", priority="high")
        """
        app_ctx = ctx.request_context.lifespan_context

        with Session(app_ctx.engine) as session:
            statement = select(Task).where(Task.user_id == user_id)

            if status != "all":
                statement = statement.where(Task.status == status)
            if priority != "all":
                statement = statement.where(Task.priority == priority)

            statement = statement.order_by(Task.created_at.desc()).limit(limit)
            tasks = session.exec(statement).all()

            return {
                "success": True,
                "count": len(tasks),
                "filters": {"status": status, "priority": priority},
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
        """
        Mark a task as completed.

        Args:
            user_id: The ID of the user (for authorization check)
            task_id: The ID of the task to mark as completed

        Returns:
            Success status and confirmation message

        Example:
            complete_task(user_id="user123", task_id=42)
        """
        app_ctx = ctx.request_context.lifespan_context

        with Session(app_ctx.engine) as session:
            task = session.get(Task, task_id)

            if not task:
                return {
                    "success": False,
                    "error": f"Task with ID {task_id} not found",
                }

            if task.user_id != user_id:
                return {
                    "success": False,
                    "error": "Not authorized to modify this task",
                }

            if task.status == "completed":
                return {
                    "success": True,
                    "message": f"Task '{task.title}' was already completed",
                    "task_id": task_id,
                }

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
        """
        Delete a task from the todo list.

        Args:
            user_id: The ID of the user (for authorization check)
            task_id: The ID of the task to delete

        Returns:
            Success status and confirmation message

        Example:
            delete_task(user_id="user123", task_id=42)
        """
        app_ctx = ctx.request_context.lifespan_context

        with Session(app_ctx.engine) as session:
            task = session.get(Task, task_id)

            if not task:
                return {
                    "success": False,
                    "error": f"Task with ID {task_id} not found",
                }

            if task.user_id != user_id:
                return {
                    "success": False,
                    "error": "Not authorized to delete this task",
                }

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
        """
        Update an existing task's details.

        Args:
            user_id: The ID of the user (for authorization check)
            task_id: The ID of the task to update
            title: New title (optional, only updates if provided)
            description: New description (optional)
            status: New status - pending, in_progress, or completed (optional)
            priority: New priority - low, medium, or high (optional)
            due_date: New due date in ISO format YYYY-MM-DD (optional)

        Returns:
            Success status and updated task details

        Example:
            update_task(
                user_id="user123",
                task_id=42,
                priority="high",
                status="in_progress"
            )
        """
        app_ctx = ctx.request_context.lifespan_context

        with Session(app_ctx.engine) as session:
            task = session.get(Task, task_id)

            if not task:
                return {
                    "success": False,
                    "error": f"Task with ID {task_id} not found",
                }

            if task.user_id != user_id:
                return {
                    "success": False,
                    "error": "Not authorized to modify this task",
                }

            # Track what was updated
            updates = []

            if title is not None:
                task.title = title
                updates.append("title")
            if description is not None:
                task.description = description
                updates.append("description")
            if status is not None:
                task.status = status
                updates.append("status")
            if priority is not None:
                task.priority = priority
                updates.append("priority")
            if due_date is not None:
                task.due_date = datetime.fromisoformat(due_date)
                updates.append("due_date")

            if not updates:
                return {
                    "success": True,
                    "message": "No changes provided",
                    "task_id": task_id,
                }

            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "message": f"Task updated ({', '.join(updates)})",
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

    return {
        "add_task": add_task,
        "list_tasks": list_tasks,
        "complete_task": complete_task,
        "delete_task": delete_task,
        "update_task": update_task,
    }
