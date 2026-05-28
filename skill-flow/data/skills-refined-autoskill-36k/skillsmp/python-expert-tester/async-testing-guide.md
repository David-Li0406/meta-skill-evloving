# Async Testing Guide - Dynamic and Current

This guide adapts to your project's async setup and uses the latest async testing patterns. I'll analyze your project before providing recommendations.

## Project Analysis

I'll first examine your project to understand:
```python
# Check your async setup (I use Read/Glob tools)
async_frameworks = detect_async_frameworks()  # asyncio, trio, curio
http_clients = detect_http_clients()          # aiohttp, httpx
web_frameworks = detect_web_frameworks()     # FastAPI, Starlette, aioflask

# Get latest async testing documentation
latest_docs = fetch_latest_async_testing_info()
```

## Setup (Context-Aware)

### Dynamic Package Installation
I check your current setup before suggesting packages:

```bash
# I'll first check what you have
pip list | grep pytest  # Check existing pytest setup
pip list | grep asyncio  # Check async packages

# Then get latest compatible versions
# (I'll fetch current versions from PyPI)
```

### Configuration Adaptation

#### For `pyproject.toml` users:
```toml
[tool.pytest.ini_options]
# I'll check your existing config and add async support
asyncio_mode = "auto"  # I'll check if this is compatible with your setup
```

#### For `pytest.ini` users:
```ini
[tool:pytest]
# I'll add to your existing configuration
asyncio_mode = "auto"
```

## Core Async Testing Patterns (Current Best Practices)

### Basic Async Tests
I'll provide patterns based on your async framework:

```python
# Standard asyncio (I'll check if this matches your setup)
@pytest.mark.asyncio
async def test_async_function():
    result = await async_operation()
    assert result.success is True

# Trio (if I detect trio usage)
@pytest.mark.trio
async def test_trio_function():
    result = await trio_async_operation()
    assert result.success is True
```

### Async Fixtures (Framework-Adaptive)

```python
@pytest.fixture
async def async_client():
    # I'll detect your HTTP client framework
    if has_aiohttp():
        async with aiohttp.ClientSession() as client:
            yield client
    elif has_httpx():
        async with httpx.AsyncClient() as client:
            yield client
    else:
        # Suggest installing appropriate async HTTP client
        recommend_async_http_client()

@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    response = await async_client.get("/api")
    assert response.status_code == 200
```

### Database Async Testing (ORM-Specific)

```python
@pytest.fixture
async def async_db_session():
    # I'll detect your ORM and provide appropriate setup
    if has_sqlalchemy_async():
        # SQLAlchemy async setup
        engine = create_async_engine("sqlite+aiosqlite:///:memory:")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async_session = async_sessionmaker(engine, class_=AsyncSession)
        async with async_session() as session:
            yield session

    elif has_django_async():
        # Django async database setup
        # I'll check Django version and provide compatible setup
        pass

    elif has_tortoise_orm():
        # Tortoise ORM async setup
        await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["models"]})
        await Tortoise.generate_schemas()
        yield
        await Tortoise.close_connections()
```

## Framework-Specific Examples

### FastAPI Testing (Current Patterns)

```python
# I'll check your FastAPI version and provide current examples
@pytest.fixture
async def fastapi_client():
    # Check if you have FastAPI and get latest testing patterns
    fastapi_docs = get_library_docs("/tiangolo/fastapi", topic="testing")

    from fastapi.testclient import TestClient
    return TestClient(app)

@pytest.mark.asyncio
async def test_fastapi_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users", json={"name": "John"})
        assert response.status_code == 200
```

### Starlette Testing

```python
@pytest.mark.asyncio
async def test_starlette_endpoint():
    # I'll detect if you're using Starlette directly
    from httpx import AsyncClient
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/items/1")
        assert response.status_code == 200
```

### Aiohttp Testing

```python
@pytest.mark.asyncio
async def test_aiohttp_client():
    # I'll check if you're using aiohttp and provide current patterns
    from aiohttp.test import AioHTTPTestCase, unittest_run_loop
    from aiohttp import web

    async def handler(request):
        return web.json_response({"status": "ok"})

    app = web.Application()
    app.router.add_get("/test", handler)

    # Testing pattern based on your aiohttp version
    async with TestClient(app) as tc:
        resp = await tc.get("/test")
        assert resp.status == 200
        data = await resp.json()
        assert data["status"] == "ok"
```

## Mock Async Testing (Current Patterns)

### AsyncMock (Latest Patterns)

```python
@pytest.mark.asyncio
async def test_async_mock(mocker):
    # I'll check your Python version and provide compatible patterns
    # AsyncMock behavior changed in Python 3.8+

    mock_async_func = mocker.AsyncMock(return_value={"data": "test"})

    result = await process_async_data(mock_async_func)
    mock_async_func.assert_awaited_once()
    assert result == {"processed": "test"}

# For async context managers
@pytest.mark.asyncio
async def test_async_context_mock(mocker):
    mock_cm = mocker.AsyncMock()
    mock_cm.__aenter__.return_value = MockResource()

    async with mock_cm as resource:
        result = await resource.operation()
        assert result is not None
```

### Real-time Mock Documentation

I fetch the latest async mocking patterns:
```python
# Get current unittest.mock patterns for async
async_mock_docs = get_library_docs("/python/cpython", topic="unittest.mock AsyncMock")

# Get latest pytest-mock async patterns
pytest_mock_docs = get_library_docs("/pytest-dev/pytest-mock", topic="async")
```

## Performance Testing (Adaptive)

### Async Performance Testing

```python
@pytest.mark.asyncio
async def test_concurrent_performance():
    # I'll check your performance testing needs
    if needs_benchmarking():
        # Suggest pytest-benchmark with async support
        recommend_async_benchmarking()

    # Performance testing for async code
    start_time = time.perf_counter()

    tasks = [async_operation() for _ in range(10)]
    results = await asyncio.gather(*tasks)

    duration = time.perf_counter() - start_time
    assert duration < 1.0  # Adjust based on your requirements
    assert all(result.success for result in results)
```

## Error Handling (Current Best Practices)

### Async Exception Testing

```python
@pytest.mark.asyncio
async def test_async_exception_handling():
    # Current patterns for async exception testing
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_operation(), timeout=1.0)

@pytest.mark.asyncio
async def test_async_exception_groups():
    # Python 3.11+ exception groups
    if python_version >= "3.11":
        async def failing_operations():
            async with TaskGroup() as tg:
                tg.create_task(fast_failing_task())
                tg.create_task(slow_failing_task())

        with pytest.raises(ExceptionGroup):
            await failing_operations()
```

## Current Best Practices

### I use real-time sources to stay current:

```python
# Get latest asyncio testing patterns
asyncio_docs = get_library_docs("/python/cpython", topic="asyncio testing")

# Check current pytest-asyncio documentation
pytest_asyncio_docs = get_library_docs("/pytest-dev/pytest-asyncio")

# Get latest async framework testing guides
if has_fastapi():
    fastapi_testing = get_library_docs("/tiangolo/fastapi", topic="testing")
```

### Version-Specific Guidance

```python
# I'll check your Python version and provide appropriate patterns
python_version = get_python_version()

if python_version >= "3.11":
    # Suggest TaskGroup and exception groups
    recommend_modern_async_patterns()
elif python_version >= "3.7":
    # Use create_task and gather patterns
    recommend_standard_async_patterns()
else:
    # Suggest upgrading Python or using legacy patterns
    suggest_upgrade_paths()
```

## Troubleshooting (Dynamic)

### Common Issues (Current Solutions)

I check the latest documentation for solutions:

```python
# Get current pytest-asyncio troubleshooting
troubleshooting_docs = fetch_latest_troubleshooting()

# Check common async testing issues in your framework
if has_fastapi():
    fastapi_issues = get_fastapi_testing_issues()

if has_aiohttp():
    aiohttp_issues = get_aiohttp_testing_issues()
```

## Key Principles

1. **Adapt to your existing setup** - I'll analyze your current async framework and tools
2. **Use real-time information** - I fetch the latest async testing documentation
3. **Version-specific guidance** - I check your Python and package versions
4. **Framework-aware patterns** - I provide examples specific to your web framework
5. **Progressive enhancement** - I build on your existing async setup

Remember: I'll always analyze your current async setup before providing recommendations and use real-time tools to ensure you get the most current, compatible async testing patterns for your specific situation.