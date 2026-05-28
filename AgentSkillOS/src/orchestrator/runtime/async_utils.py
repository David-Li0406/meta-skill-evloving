"""Shared async utilities."""
import asyncio
from loguru import logger


def create_tracked_task(
    coro,
    task_set: set[asyncio.Task],
) -> asyncio.Task:
    """Create a background task with proper lifecycle management."""
    task = asyncio.create_task(coro)
    task_set.add(task)

    def _on_done(t: asyncio.Task) -> None:
        task_set.discard(t)
        if not t.cancelled() and t.exception():
            logger.error(f"Background task failed: {t.exception()}")

    task.add_done_callback(_on_done)
    return task
