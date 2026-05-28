---
name: python-asyncio
description: Async/await patterns, asyncio/anyio, structured concurrency, async testing
license: MIT
compatibility: opencode
metadata:
  audience: python-developers
  focus: concurrency
---

## What I do

I provide guidance on asynchronous programming in Python, including:

- Async/await fundamentals and event loops
- asyncio vs anyio for cross-library compatibility
- Structured concurrency with TaskGroup
- Async context managers and iterators
- Managing async resources (streams, websockets)
- Testing async code with pytest-asyncio and anyio
- Common pitfalls (blocking calls, improper exception handling)
- Performance optimization for async code

## When to use me

Use me when:
- Implementing async/await patterns
- Working with async libraries (aiohttp, asyncpg, motor)
- Managing concurrent I/O operations (HTTP requests, database queries)
- Writing async web services or consumers
- Debugging async performance issues
- Testing asynchronous code
- Deciding between asyncio and threading

## Best Practices

### ✅ Use Structured Concurrency

```python
import asyncio
from typing import Any

async def fetch_multiple(urls: list[str]) -> list[Any]:
    """Fetch multiple URLs concurrently with structured concurrency."""
    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(fetch_url(session, url))
                for url in urls
            ]
        return [task.result() for task in tasks]

# Use anyio for cross-library compatibility
import anyio

async def process_with_anyio(urls: list[str]) -> list[Any]:
    """Process URLs using anyio for library-agnostic async."""
    async with anyio.create_task_group() as tg:
        results: list[Any] = []
        for url in urls:
            tg.start_soon(fetch_and_store, url, results)
        return results
```

### ✅ Proper Async Context Managers

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def database_connection(url: str):
    """Async context manager for database connections."""
    conn = await asyncpg.connect(url)
    try:
        yield conn
    finally:
        await conn.close()

async def process_data(url: str) -> None:
    """Use async context manager for resource management."""
    async with database_connection(url) as conn:
        result = await conn.fetch("SELECT * FROM users")
        process_results(result)
```

### ✅ Avoid Blocking the Event Loop

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

# ❌ BAD: Blocking call in async context
async def bad_async():
    time.sleep(1)  # Blocks the entire event loop
    result = heavy_computation()  # CPU-bound work blocks

# ✅ GOOD: Offload blocking operations
async def good_async():
    # Use asyncio.sleep for delays
    await asyncio.sleep(1)

    # Use run_in_executor for CPU-bound work
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool,
            heavy_computation
        )
    return result
```

### ✅ Proper Error Handling in Async Code

```python
import asyncio
from logging import getLogger

logger = getLogger(__name__)

async def process_items(items: list[str]) -> None:
    """Process items with proper error handling."""
    tasks = [process_item(item) for item in items]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for item, result in zip(items, results):
        if isinstance(result, Exception):
            logger.error(f"Failed to process {item}: {result}")
        else:
            logger.info(f"Processed {item} successfully")
```

### ✅ Async Iterators and Generators

```python
from typing import AsyncIterator

async def async_file_reader(path: str) -> AsyncIterator[str]:
    """Async iterator for reading files line by line."""
    async with aiofiles.open(path, mode='r') as f:
        async for line in f:
            yield line.strip()

# Usage
async def process_file(path: str) -> int:
    """Process file using async iterator."""
    count = 0
    async for line in async_file_reader(path):
        process_line(line)
        count += 1
    return count
```

### ✅ Testing Async Code

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_async_endpoint():
    """Test async endpoint with pytest-asyncio."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/users")
    assert response.status_code == 200

# Use anyio for library-agnostic tests
import anyio

@pytest.mark.anyio
async def test_with_anyio():
    """Test using anyio for cross-library compatibility."""
    result = await async_function()
    assert result is not None
```

## Common Pitfalls to Avoid

### ❌ Don't Mix Sync and Async indiscriminately

```python
# BAD: Mixing sync and async without care
def bad_mixed():
    result = await async_function()  # Syntax error

# GOOD: Proper mixing
async def good_mixed():
    # Call async from async
    async_result = await async_function()

    # Call sync from async (must be non-blocking)
    sync_result = sync_non_blocking_function()

    # Call sync blocking with executor
    blocking_result = await asyncio.to_thread(
        blocking_sync_function
    )
```

### ❌ Don't Forget to Close Connections

```python
# BAD: Unclosed connections
async def bad_cleanup():
    session = aiohttp.ClientSession()
    await session.get("https://example.com")
    # Session never closed!

# GOOD: Proper cleanup with context manager
async def good_cleanup():
    async with aiohttp.ClientSession() as session:
        await session.get("https://example.com")
    # Session automatically closed
```

### ❌ Don't Use asyncio.run in Already Running Loop

```python
# BAD: Nested event loops
async def bad_nested():
    result = asyncio.run(some_async_function())

# GOOD: Use asyncio.create_task or await
async def good_nested():
    task = asyncio.create_task(some_async_function())
    result = await task
```

## Performance Tips

1. **Use asyncio.gather for concurrent independent tasks**
2. **Limit concurrency with asyncio.Semaphore to avoid overwhelming resources**
3. **Use connection pooling (aiohttp, asyncpg) for database/network connections**
4. **Profile async code with py-spy to identify blocking operations**
5. **Consider uvloop for improved performance (Linux/macOS)**
6. **Use async/await consistently throughout the codebase**

## When to Use Asyncio vs Other Approaches

**Use asyncio when:**
- I/O-bound operations (HTTP requests, database queries, file I/O)
- Need to handle thousands of concurrent connections
- Working with async libraries (aiohttp, asyncpg, motor)
- Building real-time applications (websockets, streaming)

**Use threading when:**
- Dealing with blocking C extensions that don't support async
- Legacy code that cannot be easily converted to async
- I/O-bound operations on older Python versions (<3.5)

**Use multiprocessing when:**
- CPU-bound operations that require parallelism
- Tasks that need true parallelism (no GIL limitation)
- Heavy computation that benefits from multiple cores

## References

- Python asyncio documentation: https://docs.python.org/3/library/asyncio.html
- anyio documentation: https://anyio.readthedocs.io/
- Real Python async/await guide: https://realpython.com/async-io-python/
- aiohttp documentation: https://docs.aiohttp.org/
