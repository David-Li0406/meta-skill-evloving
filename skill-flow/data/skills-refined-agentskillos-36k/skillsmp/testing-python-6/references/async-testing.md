# Async Testing Reference

## Setup

```bash
uv add --dev pytest-asyncio
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
```

## Basic Async Tests

```python
# With asyncio_mode = "auto", no decorator needed
async def test_async_function():
    result = await fetch_data()
    assert result is not None


# Explicit marker (if asyncio_mode != "auto")
import pytest

@pytest.mark.asyncio
async def test_async_explicit():
    result = await fetch_data()
    assert result is not None
```

## Async Fixtures

```python
@pytest.fixture
async def async_client():
    """Async context manager fixture."""
    async with AsyncClient() as client:
        yield client


@pytest.fixture
async def db_connection():
    """Async setup/teardown."""
    conn = await create_connection()
    yield conn
    await conn.close()


async def test_with_async_fixtures(async_client, db_connection):
    response = await async_client.get("/api")
    assert response.status_code == 200
```

## Async Mocking

```python
from unittest.mock import AsyncMock

async def test_async_mock(mocker):
    # Mock async function
    mock = mocker.patch("module.async_func", new_callable=AsyncMock)
    mock.return_value = {"data": "mocked"}

    result = await code_under_test()

    mock.assert_awaited_once()
    assert result["data"] == "mocked"


async def test_async_side_effect(mocker):
    mock = mocker.patch("module.fetch", new_callable=AsyncMock)
    mock.side_effect = [
        {"id": 1},
        {"id": 2},
        ConnectionError("failed"),
    ]

    r1 = await fetch(1)  # {"id": 1}
    r2 = await fetch(2)  # {"id": 2}

    with pytest.raises(ConnectionError):
        await fetch(3)
```

## HTTP Testing with httpx

### With respx

```python
import httpx
import respx

@respx.mock
async def test_api_call():
    respx.get("https://api.example.com/users/1").respond(
        json={"id": 1, "name": "John"}
    )

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/users/1")

    assert response.json()["name"] == "John"


@respx.mock
async def test_api_error():
    respx.get("https://api.example.com/users/999").respond(status_code=404)

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/users/999")

    assert response.status_code == 404
```

### With pytest-httpx

```python
import httpx
import pytest

async def test_with_httpx_mock(httpx_mock):
    httpx_mock.add_response(
        url="https://api.example.com/data",
        json={"result": "ok"}
    )

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")

    assert response.json()["result"] == "ok"
```

## HTTP Testing with aiohttp

```python
from aioresponses import aioresponses
import aiohttp

async def test_aiohttp_request():
    with aioresponses() as m:
        m.get("https://api.example.com/data", payload={"result": "ok"})

        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.example.com/data") as resp:
                data = await resp.json()

        assert data["result"] == "ok"
```

## Testing Async Generators

```python
async def test_async_generator():
    results = []
    async for item in async_iterator():
        results.append(item)

    assert len(results) == 10


async def test_async_generator_with_list():
    results = [item async for item in async_iterator()]
    assert len(results) == 10
```

## Testing Timeouts

```python
import asyncio
import pytest

async def test_timeout():
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_operation(), timeout=0.1)


async def test_with_timeout(mocker):
    # Mock to avoid actual delay
    mock = mocker.patch("module.slow_operation", new_callable=AsyncMock)
    mock.return_value = "fast result"

    result = await asyncio.wait_for(slow_operation(), timeout=1.0)
    assert result == "fast result"
```

## Testing Concurrent Tasks

```python
async def test_concurrent_tasks():
    results = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3),
    )

    assert len(results) == 3
    assert all(r is not None for r in results)


async def test_concurrent_with_exception():
    with pytest.raises(ValueError):
        await asyncio.gather(
            fetch_user(1),
            failing_operation(),  # Raises ValueError
            fetch_user(3),
        )


async def test_gather_return_exceptions():
    results = await asyncio.gather(
        fetch_user(1),
        failing_operation(),
        return_exceptions=True,
    )

    assert results[0] is not None
    assert isinstance(results[1], ValueError)
```

## Testing Event Loops

```python
async def test_create_task():
    task = asyncio.create_task(background_job())

    # Do other work
    await asyncio.sleep(0.01)

    # Wait for task
    result = await task
    assert result == "completed"


async def test_cancel_task():
    task = asyncio.create_task(long_running_job())

    await asyncio.sleep(0.01)
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task
```

## Fixture Scopes with Async

```python
@pytest.fixture(scope="module")
async def shared_connection():
    """Shared across module - use carefully."""
    conn = await create_connection()
    yield conn
    await conn.close()


@pytest.fixture(scope="session")
async def app():
    """Shared across session."""
    app = await create_app()
    yield app
    await app.shutdown()
```

## Common Patterns

### Test Async Context Manager

```python
async def test_async_context_manager():
    async with MyAsyncResource() as resource:
        result = await resource.do_something()
        assert result is not None
```

### Test Async Iterator with Limit

```python
async def test_paginated_fetch():
    pages = []
    async for page in fetch_all_pages(limit=3):
        pages.append(page)
        if len(pages) >= 3:
            break

    assert len(pages) == 3
```

### Test Websocket

```python
async def test_websocket(mocker):
    mock_ws = mocker.AsyncMock()
    mock_ws.recv.side_effect = ['{"type": "hello"}', '{"type": "bye"}']

    messages = []
    for _ in range(2):
        msg = await mock_ws.recv()
        messages.append(msg)

    assert len(messages) == 2
```
