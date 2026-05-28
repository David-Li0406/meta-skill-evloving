# Pytest Optimization Patterns

## pyproject.toml Configuration

```toml
[tool.pytest.ini_options]
# Async mode - auto-detect async tests
asyncio_mode = "auto"

# Test discovery
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]

# Performance options
addopts = [
    "-v",                    # Verbose output
    "--tb=short",            # Shorter tracebacks
    "-x",                    # Stop on first failure (fast feedback)
    "--strict-markers",      # Enforce marker registration
    "-p", "no:warnings",     # Disable warnings (cleaner output)
]

# Markers
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks integration tests",
    "unit: marks unit tests",
]

# Async configuration
asyncio_default_fixture_loop_scope = "function"
```

## Requirements (Optimized Versions)

```txt
# requirements-test.txt
pytest>=8.0.0
pytest-asyncio>=0.23.0
pytest-cov>=4.1.0
httpx>=0.27.0
aiosqlite>=0.19.0
```

## Why AsyncClient Over TestClient

| Aspect | TestClient (sync) | AsyncClient |
|--------|-------------------|-------------|
| **Speed** | Sync-to-async bridge overhead | Native async, ~20% faster |
| **Memory** | Thread pool for async | Single event loop |
| **Compatibility** | May cause event loop issues | Works with async fixtures |
| **Recommended** | Simple sync endpoints | Async endpoints (standard) |

```python
# AVOID: Sync TestClient with async endpoints
from fastapi.testclient import TestClient
client = TestClient(app)  # Creates new event loop, bridge overhead

# PREFER: AsyncClient
from httpx import AsyncClient, ASGITransport
async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
    response = await client.get("/")  # Native async
```

## Transaction Rollback vs Schema Recreation

```python
# SLOW: Recreate schema per test
@pytest.fixture(scope="function")
async def db_session(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Slow!

    async_session = async_sessionmaker(async_engine)
    async with async_session() as session:
        yield session

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Slow!

# FAST: Transaction rollback per test
@pytest.fixture(scope="function")
async def db_session(async_engine):  # Engine created once at session scope
    async_session = async_sessionmaker(async_engine, class_=AsyncSession)
    async with async_session() as session:
        async with session.begin():
            yield session
            await session.rollback()  # Fast! Just rollback
```

**Performance Comparison:**
| Approach | 100 tests | 1000 tests |
|----------|-----------|------------|
| Schema recreation | ~60s | ~600s |
| Transaction rollback | ~5s | ~50s |

## Parallel Test Execution

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel (auto-detect CPU cores)
pytest -n auto

# Run with specific worker count
pytest -n 4
```

```toml
# pyproject.toml for parallel
[tool.pytest.ini_options]
addopts = ["-n", "auto"]
```

**Note:** Requires isolated database per worker for parallel execution.

## Selective Test Running

```bash
# Run specific test
pytest tests/test_items.py::test_create_item -v

# Run tests matching pattern
pytest -k "test_create" -v

# Run by marker
pytest -m "not slow" -v

# Stop on first failure
pytest -x

# Run last failed tests only
pytest --lf

# Run failed first, then rest
pytest --ff
```

## Coverage Configuration

```toml
# pyproject.toml
[tool.coverage.run]
source = ["app"]
branch = true
omit = ["*/tests/*", "*/__pycache__/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
fail_under = 80
show_missing = true
```

```bash
# Run with coverage
pytest --cov=app --cov-report=term-missing --cov-report=html
```

## Fixture Caching

```python
# Expensive fixture - cache at session level
@pytest.fixture(scope="session")
async def expensive_resource():
    """Created once, cached for entire test session."""
    resource = await create_expensive_resource()
    yield resource
    await resource.cleanup()

# Use lru_cache for non-fixture helpers
from functools import lru_cache

@lru_cache(maxsize=1)
def get_test_settings():
    return Settings(_env_file=".env.test")
```

## Async Fixture Best Practices

```python
# Correct: async generator fixture
@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session

# Correct: async fixture with cleanup
@pytest.fixture
async def temp_file():
    path = Path("/tmp/test_file.txt")
    path.write_text("test")
    yield path
    path.unlink()  # Cleanup

# Avoid: Mixing sync and async improperly
@pytest.fixture
def bad_fixture():  # Sync fixture
    return asyncio.run(async_operation())  # Creates new event loop!
```

## Performance Monitoring

```python
# conftest.py - Add timing to slow tests
import time

@pytest.fixture(autouse=True)
def test_timing(request):
    start = time.perf_counter()
    yield
    duration = time.perf_counter() - start
    if duration > 1.0:  # Log tests taking > 1 second
        print(f"\n[SLOW] {request.node.name}: {duration:.2f}s")
```

```bash
# Show test durations
pytest --durations=10  # Show 10 slowest tests
pytest --durations=0   # Show all test durations
```
