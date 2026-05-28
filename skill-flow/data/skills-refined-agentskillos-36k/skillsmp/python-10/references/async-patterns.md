# Python Async/Await Patterns

Effective patterns for asynchronous Python code.

## Basic Async Pattern

```python
import asyncio

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    data = await fetch_data("https://api.example.com")
    print(data)

asyncio.run(main())
```

## Concurrent Execution

### gather - Run multiple tasks concurrently

```python
async def main():
    # Run all concurrently, wait for all
    results = await asyncio.gather(
        fetch_data("/users"),
        fetch_data("/posts"),
        fetch_data("/comments"),
    )
    users, posts, comments = results
```

### TaskGroup - Better error handling (Python 3.11+)

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_data("/users"))
        task2 = tg.create_task(fetch_data("/posts"))
    # All tasks complete when exiting context
    users = task1.result()
    posts = task2.result()
```

### as_completed - Process as they finish

```python
async def main():
    tasks = [fetch_data(url) for url in urls]
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"Got result: {result}")
```

## Timeout Handling

```python
async def with_timeout():
    try:
        result = await asyncio.wait_for(
            slow_operation(),
            timeout=5.0
        )
    except asyncio.TimeoutError:
        print("Operation timed out")
```

## Async Context Managers

```python
class AsyncDBConnection:
    async def __aenter__(self):
        self.conn = await create_connection()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()

async def main():
    async with AsyncDBConnection() as conn:
        await conn.execute("SELECT 1")
```

## Async Generators

```python
async def fetch_pages(url: str):
    page = 1
    while True:
        data = await fetch_data(f"{url}?page={page}")
        if not data["items"]:
            break
        for item in data["items"]:
            yield item
        page += 1

async def main():
    async for item in fetch_pages("/api/items"):
        process(item)
```

## Semaphore - Limit Concurrency

```python
async def fetch_with_limit(urls: list[str], limit: int = 10):
    semaphore = asyncio.Semaphore(limit)

    async def fetch_one(url: str):
        async with semaphore:
            return await fetch_data(url)

    return await asyncio.gather(*[fetch_one(url) for url in urls])
```

## Common Anti-Patterns

```python
# ❌ Blocking call in async function
async def bad():
    time.sleep(1)  # Blocks entire event loop!

# ✅ Use async sleep
async def good():
    await asyncio.sleep(1)

# ❌ Creating tasks without awaiting
async def bad():
    asyncio.create_task(work())  # Fire and forget = lost errors

# ✅ Track tasks
async def good():
    task = asyncio.create_task(work())
    await task  # Or store for later await

# ❌ Sync file I/O in async code
async def bad():
    with open("file.txt") as f:  # Blocks!
        return f.read()

# ✅ Use aiofiles
async def good():
    async with aiofiles.open("file.txt") as f:
        return await f.read()
```

## Testing Async Code

```python
import pytest

@pytest.mark.asyncio
async def test_fetch_data():
    result = await fetch_data("/test")
    assert result["status"] == "ok"

# With fixtures
@pytest.fixture
async def db_connection():
    conn = await create_connection()
    yield conn
    await conn.close()
```
