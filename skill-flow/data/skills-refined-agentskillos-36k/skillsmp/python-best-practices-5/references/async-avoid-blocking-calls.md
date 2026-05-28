---
title: Avoid Blocking Calls in Async Code
impact: CRITICAL
impactDescription: prevents event loop starvation, maintains concurrency
tags: async, blocking, event-loop, executor
---

## Avoid Blocking Calls in Async Code

Blocking calls (CPU-bound work, synchronous I/O, `time.sleep()`) block the entire event loop, preventing all other coroutines from running. Use `run_in_executor()` for unavoidable blocking operations.

**Incorrect (blocks event loop for 5 seconds):**

```python
async def generate_report(data: ReportData) -> Report:
    time.sleep(5)  # Blocks ALL coroutines
    result = compute_heavy_statistics(data)  # CPU-bound, blocks
    return Report(result)
```

**Correct (offload blocking work to thread pool):**

```python
async def generate_report(data: ReportData) -> Report:
    await asyncio.sleep(5)  # Non-blocking sleep
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        None,  # Default thread pool
        compute_heavy_statistics,
        data,
    )
    return Report(result)
```

**Alternative (for synchronous libraries):**

```python
async def sync_api_call(endpoint: str) -> dict:
    loop = asyncio.get_running_loop()
    # Wrap synchronous requests in executor
    response = await loop.run_in_executor(
        None,
        lambda: requests.get(endpoint).json()
    )
    return response
```

Reference: [asyncio event loop executors](https://docs.python.org/3/library/asyncio-eventloop.html#executing-code-in-thread-or-process-pools)
