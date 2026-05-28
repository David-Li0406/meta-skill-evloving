# Async Testing with Pytest

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

## Basic Async Test

```python
import pytest
from mypackage.api import fetch_user

# No decorator needed with asyncio_mode = "auto"
async def test_fetch_user():
    user = await fetch_user(1)
    assert user["id"] == 1
    assert user["name"] == "John"
```

## Async Fixtures

```python
@pytest.fixture
async def async_client():
    """Async context manager."""
    async with httpx.AsyncClient() as client:
        yield client


@pytest.fixture
async def db_connection():
    """Async setup/teardown."""
    conn = await asyncpg.connect("postgresql://...")
    yield conn
    await conn.close()


async def test_with_fixtures(async_client, db_connection):
    await db_connection.execute("INSERT INTO users ...")
    response = await async_client.get("/users/1")
    assert response.status_code == 200
```

## Testing Async Generators

```python
async def test_async_generator():
    async def gen():
        for i in range(3):
            yield i
    
    result = []
    async for value in gen():
        result.append(value)
    
    assert result == [0, 1, 2]
```

## Testing with asyncio.gather

```python
async def test_concurrent_requests():
    async with httpx.AsyncClient() as client:
        tasks = [
            client.get(f"https://api.example.com/users/{i}")
            for i in range(1, 4)
        ]
        responses = await asyncio.gather(*tasks)
    
    assert len(responses) == 3
    assert all(r.status_code == 200 for r in responses)
```

## Mocking Async Functions

```python
from unittest.mock import AsyncMock

async def test_with_async_mock(mocker):
    """Using pytest-mock with async."""
    mock_fetch = mocker.patch("mypackage.api.fetch_data", new=AsyncMock())
    mock_fetch.return_value = {"data": "test"}
    
    result = await fetch_and_process()
    
    assert result["data"] == "test"
    mock_fetch.assert_awaited_once()


@pytest.fixture
def mock_async_client(mocker):
    """Mock httpx.AsyncClient."""
    mock = mocker.Mock()
    mock.get = AsyncMock(return_value=mocker.Mock(
        status_code=200,
        json=lambda: {"id": 1}
    ))
    return mock
```

## Testing Timeouts

```python
import pytest
import asyncio

async def test_timeout():
    """Test that operation completes within time limit."""
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_operation(), timeout=1.0)


async def test_no_timeout():
    """Ensure fast operation doesn't timeout."""
    result = await asyncio.wait_for(fast_operation(), timeout=1.0)
    assert result is not None
```

## Testing Event Loops

```python
@pytest.fixture
def event_loop():
    """Custom event loop for tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


async def test_with_custom_loop(event_loop):
    """Uses the custom event loop."""
    result = await asyncio.sleep(0, result="done")
    assert result == "done"
```

## Testing Async Context Managers

```python
class AsyncResource:
    async def __aenter__(self):
        self.conn = await connect()
        return self
    
    async def __aexit__(self, *args):
        await self.conn.close()


async def test_async_context_manager():
    async with AsyncResource() as resource:
        assert resource.conn is not None
    # Connection closed automatically
```

## Parametrized Async Tests

```python
@pytest.mark.parametrize("user_id,expected_name", [
    (1, "Alice"),
    (2, "Bob"),
    (3, "Charlie"),
])
async def test_fetch_users(user_id, expected_name):
    user = await fetch_user(user_id)
    assert user["name"] == expected_name
```

## Testing Async Errors

```python
async def test_api_error():
    """Test async exception handling."""
    with pytest.raises(httpx.HTTPError):
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.example.com/error")
            response.raise_for_status()


async def test_custom_error():
    """Test custom async exception."""
    with pytest.raises(CustomError, match="database connection failed"):
        await connect_to_database("invalid://url")
```

## Async Markers

```python
@pytest.mark.asyncio
async def test_explicit_marker():
    """Explicit async marker (not needed with asyncio_mode = 'auto')."""
    result = await async_function()
    assert result is not None


@pytest.mark.asyncio
@pytest.mark.slow
async def test_slow_async():
    """Combining markers."""
    result = await slow_async_operation()
    assert result is not None
```

## Best Practices

### DO:
- Use `asyncio_mode = "auto"` in pyproject.toml
- Mock external async calls with `AsyncMock`
- Test both success and error paths
- Use `pytest.raises` for async exceptions
- Set appropriate timeouts for slow operations

### DON'T:
- Mix sync and async code without proper bridging
- Forget to await async functions in tests
- Share async resources between tests without cleanup
- Use `time.sleep()` in async tests (use `asyncio.sleep()`)
