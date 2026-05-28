"""Google Tasks tools for managing task lists and tasks."""

import asyncio
import logging

from src.humcp.decorator import tool
from src.tools.google.auth import SCOPES, get_google_service

logger = logging.getLogger("humcp.tools.google.tasks")

TASKS_READONLY_SCOPES = [SCOPES["tasks_readonly"]]
TASKS_FULL_SCOPES = [SCOPES["tasks"]]


@tool()
async def google_tasks_list_task_lists(max_results: int = 100) -> dict:
    """List all task lists for the user.

    Returns all task lists including the default list.

    Args:
        max_results: Maximum number of task lists to return (default: 100).

    Returns:
        List of task lists with id, title, and updated timestamp.
    """
    try:

        def _list():
            service = get_google_service("tasks", "v1", TASKS_READONLY_SCOPES)
            results = service.tasklists().list(maxResults=max_results).execute()
            items = results.get("items", [])
            return {
                "task_lists": [
                    {
                        "id": tl["id"],
                        "title": tl.get("title", ""),
                        "updated": tl.get("updated", ""),
                    }
                    for tl in items
                ],
                "total": len(items),
            }

        logger.info("tasks_list_task_lists")
        result = await asyncio.to_thread(_list)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("tasks_list_task_lists failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_tasks_get_task_list(task_list_id: str) -> dict:
    """Get details of a specific task list.

    Args:
        task_list_id: ID of the task list.

    Returns:
        Task list details with id, title, and updated timestamp.
    """
    try:

        def _get():
            service = get_google_service("tasks", "v1", TASKS_READONLY_SCOPES)
            tl = service.tasklists().get(tasklist=task_list_id).execute()
            return {
                "id": tl["id"],
                "title": tl.get("title", ""),
                "updated": tl.get("updated", ""),
            }

        logger.info("tasks_get_task_list id=%s", task_list_id)
        result = await asyncio.to_thread(_get)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("tasks_get_task_list failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_tasks_create_task_list(title: str) -> dict:
    """Create a new task list.

    Args:
        title: Title for the new task list.

    Returns:
        Created task list with id, title, and updated timestamp.
    """
    try:

        def _create():
            service = get_google_service("tasks", "v1", TASKS_FULL_SCOPES)
            tl = service.tasklists().insert(body={"title": title}).execute()
            return {
                "id": tl["id"],
                "title": tl.get("title", ""),
                "updated": tl.get("updated", ""),
            }

        logger.info("tasks_create_task_list title=%s", title)
        result = await asyncio.to_thread(_create)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("tasks_create_task_list failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_tasks_delete_task_list(task_list_id: str) -> dict:
    """Delete a task list.

    Permanently removes the task list and all its tasks.

    Args:
        task_list_id: ID of the task list to delete.

    Returns:
        Confirmation with deleted_task_list_id.
    """
    try:

        def _delete():
            service = get_google_service("tasks", "v1", TASKS_FULL_SCOPES)
            service.tasklists().delete(tasklist=task_list_id).execute()
            return {"deleted_task_list_id": task_list_id}

        logger.info("tasks_delete_task_list id=%s", task_list_id)
        result = await asyncio.to_thread(_delete)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("tasks_delete_task_list failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_tasks_list_tasks(
    task_list_id: str = "@default",
    show_completed: bool = True,
    show_hidden: bool = False,
    max_results: int = 100,
) -> dict:
    """List tasks in a task list.

    Returns tasks with their status, due dates, and hierarchy information.

    Args:
        task_list_id: Task list ID (default: "@default" for the default list).
        show_completed: Include completed tasks (default: True).
        show_hidden: Include hidden tasks (default: False).
        max_results: Maximum number of tasks to return (default: 100).

    Returns:
        List of tasks with id, title, notes, status, due date, and parent info.
    """
    try:

        def _list():
            service = get_google_service("tasks", "v1", TASKS_READONLY_SCOPES)
            results = (
                service.tasks()
                .list(
                    tasklist=task_list_id,
                    showCompleted=show_completed,
                    showHidden=show_hidden,
                    maxResults=max_results,
                )
                .execute()
            )
            items = results.get("items", [])
            return {
                "tasks": [
                    {
                        "id": t["id"],
                        "title": t.get("title", ""),
                        "notes": t.get("notes", ""),
                        "status": t.get("status", ""),
                        "due": t.get("due", ""),
                        "completed": t.get("completed", ""),
                        "parent": t.get("parent", ""),
                        "position": t.get("position", ""),
                    }
                    for t in items
                ],
                "total": len(items),
            }

        logger.info("tasks_list_tasks list_id=%s", task_list_id)
        result = await asyncio.to_thread(_list)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("tasks_list_tasks failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_tasks_get_task(task_list_id: str, task_id: str) -> dict:
    """Get details of a specific task.

    Args:
        task_list_id: ID of the task list containing the task.
        task_id: ID of the task.

    Returns:
        Task details with id, title, notes, status, due, completed, parent, position, links.
    """
    try:

        def _get():
            service = get_google_service("tasks", "v1", TASKS_READONLY_SCOPES)
            t = service.tasks().get(tasklist=task_list_id, task=task_id).execute()
            return {
                "id": t["id"],
                "title": t.get("title", ""),
                "notes": t.get("notes", ""),
                "status": t.get("status", ""),
                "due": t.get("due", ""),
                "completed": t.get("completed", ""),
                "parent": t.get("parent", ""),
                "position": t.get("position", ""),
                "links": t.get("links", []),
            }

        logger.info("tasks_get_task list_id=%s task_id=%s", task_list_id, task_id)
        result = await asyncio.to_thread(_get)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("tasks_get_task failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_tasks_create_task(
    task_list_id: str = "@default",
    title: str = "",
    notes: str = "",
    due: str = "",
    parent: str = "",
) -> dict:
    """Create a new task.

    Creates a task in the specified task list.

    Args:
        task_list_id: Task list ID (default: "@default").
        title: Task title.
        notes: Optional task notes/description.
        due: Optional due date in RFC 3339 format.
        parent: Optional parent task ID for subtasks.

    Returns:
        Created task with id, title, notes, status, and due date.
    """
    try:

        def _create():
            service = get_google_service("tasks", "v1", TASKS_FULL_SCOPES)
            body = {"title": title}
            if notes:
                body["notes"] = notes
            if due:
                body["due"] = due

            kwargs = {"tasklist": task_list_id, "body": body}
            if parent:
                kwargs["parent"] = parent

            t = service.tasks().insert(**kwargs).execute()
            return {
                "id": t["id"],
                "title": t.get("title", ""),
                "notes": t.get("notes", ""),
                "status": t.get("status", ""),
                "due": t.get("due", ""),
            }

        logger.info("tasks_create_task title=%s", title)
        result = await asyncio.to_thread(_create)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("tasks_create_task failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_tasks_update_task(
    task_list_id: str,
    task_id: str,
    title: str = "",
    notes: str = "",
    status: str = "",
    due: str = "",
) -> dict:
    """Update an existing task.

    Updates the specified fields of a task. Only provided fields are changed.

    Args:
        task_list_id: ID of the task list containing the task.
        task_id: ID of the task to update.
        title: New title (optional).
        notes: New notes (optional).
        status: New status - "needsAction" or "completed" (optional).
        due: New due date in RFC 3339 format (optional).

    Returns:
        Updated task with id, title, notes, status, due, and completed.
    """
    try:

        def _update():
            service = get_google_service("tasks", "v1", TASKS_FULL_SCOPES)
            # Get current task first
            current = service.tasks().get(tasklist=task_list_id, task=task_id).execute()

            # Update only provided fields
            if title:
                current["title"] = title
            if notes:
                current["notes"] = notes
            if status:
                current["status"] = status
            if due:
                current["due"] = due

            t = (
                service.tasks()
                .update(tasklist=task_list_id, task=task_id, body=current)
                .execute()
            )
            return {
                "id": t["id"],
                "title": t.get("title", ""),
                "notes": t.get("notes", ""),
                "status": t.get("status", ""),
                "due": t.get("due", ""),
                "completed": t.get("completed", ""),
            }

        logger.info("tasks_update_task task_id=%s", task_id)
        result = await asyncio.to_thread(_update)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("tasks_update_task failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_tasks_delete_task(task_list_id: str, task_id: str) -> dict:
    """Delete a task.

    Permanently removes a task from the task list.

    Args:
        task_list_id: ID of the task list containing the task.
        task_id: ID of the task to delete.

    Returns:
        Confirmation with deleted_task_id.
    """
    try:

        def _delete():
            service = get_google_service("tasks", "v1", TASKS_FULL_SCOPES)
            service.tasks().delete(tasklist=task_list_id, task=task_id).execute()
            return {"deleted_task_id": task_id}

        logger.info("tasks_delete_task task_id=%s", task_id)
        result = await asyncio.to_thread(_delete)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("tasks_delete_task failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_tasks_complete_task(task_list_id: str, task_id: str) -> dict:
    """Mark a task as completed.

    Convenience function to set a task's status to completed.

    Args:
        task_list_id: ID of the task list containing the task.
        task_id: ID of the task to complete.

    Returns:
        Updated task with completion status.
    """
    return await google_tasks_update_task(task_list_id, task_id, status="completed")


@tool()
async def google_tasks_clear_completed(task_list_id: str = "@default") -> dict:
    """Clear all completed tasks from a task list.

    Removes all tasks marked as completed from the specified list.

    Args:
        task_list_id: Task list ID (default: "@default").

    Returns:
        Confirmation with cleared status and task_list_id.
    """
    try:

        def _clear():
            service = get_google_service("tasks", "v1", TASKS_FULL_SCOPES)
            service.tasks().clear(tasklist=task_list_id).execute()
            return {"cleared": True, "task_list_id": task_list_id}

        logger.info("tasks_clear_completed list_id=%s", task_list_id)
        result = await asyncio.to_thread(_clear)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("tasks_clear_completed failed")
        return {"success": False, "error": str(e)}
