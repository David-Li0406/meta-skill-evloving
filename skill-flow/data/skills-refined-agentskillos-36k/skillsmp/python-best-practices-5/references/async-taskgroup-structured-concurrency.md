---
title: Use TaskGroup for Structured Concurrency
impact: CRITICAL
impactDescription: automatic cleanup on failure, prevents orphaned tasks
tags: async, taskgroup, structured-concurrency, python311
---

## Use TaskGroup for Structured Concurrency

`asyncio.TaskGroup` (Python 3.11+) provides structured concurrency with automatic exception handling and cleanup. Unlike `gather()`, it cancels all tasks when one fails.

**Incorrect (unstructured tasks, potential orphans):**

```python
async def process_batch(items: list[Item]) -> list[Result]:
    tasks = [asyncio.create_task(process_item(item)) for item in items]
    try:
        return await asyncio.gather(*tasks)
    except Exception:
        # Some tasks may continue running as orphans
        for task in tasks:
            task.cancel()
        raise
```

**Correct (structured concurrency, automatic cleanup):**

```python
async def process_batch(items: list[Item]) -> list[Result]:
    results = []
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(process_item(item)) for item in items]
    # All tasks complete or all cancelled on any exception
    return [task.result() for task in tasks]
```

**Benefits:**
- Automatic cancellation of remaining tasks on exception
- No orphaned tasks or resource leaks
- Clear task lifetime boundaries
- Better exception propagation via ExceptionGroup

Reference: [asyncio.TaskGroup documentation](https://docs.python.org/3/library/asyncio-task.html#asyncio.TaskGroup)
