"""Async batch task dispatch.

Pure async parallel execution using asyncio.Semaphore.
Delegates individual task execution to workflow.service.run_task().
"""

from __future__ import annotations

import asyncio
from typing import Callable, Optional

from orchestrator.base import ExecutionResult

from .models import TaskRequest
from .service import run_task


async def run_batch(
    requests: list[TaskRequest],
    max_parallel: int = 1,
    on_task_start: Optional[Callable[[TaskRequest], None]] = None,
    on_task_complete: Optional[Callable[[TaskRequest, ExecutionResult], None]] = None,
    on_task_error: Optional[Callable[[TaskRequest, Exception], None]] = None,
    continue_on_error: bool = True,
) -> list[tuple[TaskRequest, ExecutionResult | Exception]]:
    """Execute a batch of tasks with bounded concurrency.

    Args:
        requests: List of task requests to execute.
        max_parallel: Maximum concurrent tasks.
        on_task_start: Callback when a task starts.
        on_task_complete: Callback when a task completes.
        on_task_error: Callback when a task fails.
        continue_on_error: Keep going after a failure.

    Returns:
        List of (request, result_or_exception) tuples.
    """
    semaphore = asyncio.Semaphore(max_parallel)
    results: list[tuple[TaskRequest, ExecutionResult | Exception]] = []
    cancel_event = asyncio.Event()

    async def _run_one(req: TaskRequest) -> tuple[TaskRequest, ExecutionResult | Exception]:
        if cancel_event.is_set():
            return req, Exception("Cancelled due to earlier failure")

        async with semaphore:
            if cancel_event.is_set():
                return req, Exception("Cancelled due to earlier failure")

            if on_task_start:
                on_task_start(req)
            try:
                result = await run_task(req)
                if on_task_complete:
                    on_task_complete(req, result)
                return req, result
            except Exception as exc:
                if on_task_error:
                    on_task_error(req, exc)
                if not continue_on_error:
                    cancel_event.set()
                return req, exc

    tasks = [asyncio.create_task(_run_one(req)) for req in requests]
    done = await asyncio.gather(*tasks, return_exceptions=False)
    results.extend(done)
    return results
