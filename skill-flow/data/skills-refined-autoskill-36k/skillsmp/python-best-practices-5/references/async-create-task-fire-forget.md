---
title: Store References to Fire-and-Forget Tasks
impact: CRITICAL
impactDescription: prevents silent task cancellation via garbage collection
tags: async, create-task, fire-forget, garbage-collection
---

## Store References to Fire-and-Forget Tasks

Tasks created with `asyncio.create_task()` can be garbage collected if no reference is kept, causing silent cancellation. Always store task references.

**Incorrect (task may be garbage collected):**

```python
async def handle_request(request: Request) -> Response:
    asyncio.create_task(log_analytics(request))  # May be GC'd
    asyncio.create_task(update_metrics(request))  # May be GC'd
    return await process_request(request)
```

**Correct (store references to prevent GC):**

```python
background_tasks: set[asyncio.Task] = set()

async def handle_request(request: Request) -> Response:
    for coro in [log_analytics(request), update_metrics(request)]:
        task = asyncio.create_task(coro)
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

    return await process_request(request)
```

**Alternative (using TaskGroup for managed lifecycle):**

```python
async def run_server():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(start_http_server())
        tg.create_task(start_metrics_reporter())
        # All tasks cleaned up when context exits
```

Reference: [asyncio.create_task documentation](https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task)
