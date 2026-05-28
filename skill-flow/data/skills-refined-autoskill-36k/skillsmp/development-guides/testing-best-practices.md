# Testing Best Practices

Testing strategies for Kailash SDK including 3-tier testing, runtime testing patterns, and quality assurance.

## Source Documentation
- [`sdk-users/3-development/testing/TESTING_BEST_PRACTICES.md`](../../../sdk-users/3-development/testing/TESTING_BEST_PRACTICES.md)

## 3-Tier Testing Strategy

### Tier 1: Unit Tests
- Test individual nodes and components
- Fast execution (< 1s per test)
- Mocking allowed for external dependencies
- Uses LocalRuntime for synchronous execution

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

def test_workflow_creation():
    """Test workflow builder."""
    workflow = WorkflowBuilder()
    workflow.add_node("PythonCodeNode", "process", {
        "code": "result = {'value': input_value * 2}"
    })

    runtime = LocalRuntime()
    results, run_id = runtime.execute(workflow.build(), parameters={
        "process": {"input_value": 10}
    })

    assert results["process"]["result"]["value"] == 20
```

### Tier 2: Integration Tests (NO MOCKING)
- Test multi-node workflows with real infrastructure
- Use real Docker services (PostgreSQL, Redis, Ollama)
- Test both LocalRuntime and AsyncLocalRuntime
- Medium execution time (< 30s per test)

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime
from tests.utils.docker_config import get_postgres_connection_string

def test_database_workflow():
    """Test with real PostgreSQL - NO MOCKS."""
    conn_string = get_postgres_connection_string()

    workflow = WorkflowBuilder()
    workflow.add_node("SQLDatabaseNode", "db", {
        "connection_string": conn_string,
        "query": "SELECT 1 as value",
        "operation": "select"
    })

    runtime = LocalRuntime()
    results, run_id = runtime.execute(workflow.build())

    assert results["db"]["success"]
    assert len(results["db"]["data"]) > 0
```

### Tier 3: End-to-End Tests
- Complete workflows with full scenarios
- Real external services and Docker infrastructure
- Test production-like deployments
- Slower execution (minutes acceptable)

```python
import pytest
from kailash.runtime import AsyncLocalRuntime

@pytest.mark.e2e
@pytest.mark.requires_docker
async def test_complete_etl_pipeline():
    """Test full ETL pipeline with AsyncLocalRuntime."""
    workflow = build_etl_workflow()

    runtime = AsyncLocalRuntime()
    results = await runtime.execute_workflow_async(workflow.build(), inputs={})

    assert results["extract"]["status"] == "success"
    assert results["transform"]["rows_processed"] > 0
    assert results["load"]["rows_inserted"] > 0
```

## Runtime Testing Patterns

### Testing LocalRuntime (Sync)
```python
from kailash.runtime import LocalRuntime

def test_sync_execution():
    """Test synchronous runtime execution."""
    workflow = WorkflowBuilder()
    workflow.add_node("PythonCodeNode", "node", {
        "code": "result = {'status': 'completed'}"
    })

    runtime = LocalRuntime()
    results, run_id = runtime.execute(workflow.build())

    assert results["node"]["result"]["status"] == "completed"
    assert run_id is not None
```

### Testing AsyncLocalRuntime (Async)
```python
import pytest
from kailash.runtime import AsyncLocalRuntime

@pytest.mark.asyncio
async def test_async_execution():
    """Test asynchronous runtime execution."""
    workflow = WorkflowBuilder()
    workflow.add_node("PythonCodeNode", "node", {
        "code": "result = {'status': 'completed'}"
    })

    runtime = AsyncLocalRuntime()
    results = await runtime.execute_workflow_async(workflow.build(), inputs={})

    assert results["node"]["result"]["status"] == "completed"
```

### Parametrized Runtime Testing
```python
import pytest
from kailash.runtime import LocalRuntime, AsyncLocalRuntime

@pytest.mark.parametrize("runtime_class", [LocalRuntime, AsyncLocalRuntime])
def test_both_runtimes(runtime_class):
    """Test pattern works with both runtimes."""
    workflow = WorkflowBuilder()
    workflow.add_node("PythonCodeNode", "node", {
        "code": "result = {'value': 42}"
    })

    runtime = runtime_class()

    if isinstance(runtime, AsyncLocalRuntime):
        import asyncio
        results = asyncio.run(runtime.execute_workflow_async(workflow.build(), inputs={}))
    else:
        results, run_id = runtime.execute(workflow.build())

    assert results["node"]["result"]["value"] == 42
```

## Testing with Real Infrastructure

### Docker Services Setup
```bash
# Start test services
cd tests/utils
docker-compose -f docker-compose.test.yml up -d

# Verify services
docker-compose -f docker-compose.test.yml ps
```

### Available Test Services
- PostgreSQL: `localhost:5434`
- Redis: `localhost:6380`
- Ollama: `localhost:11435`
- MySQL: `localhost:3307`
- MongoDB: `localhost:27017`
- Mock API: `localhost:8888`

### Using Docker Config
```python
from tests.utils.docker_config import (
    get_postgres_connection_string,
    get_redis_url,
    OLLAMA_CONFIG,
    MOCK_API_CONFIG
)

def test_with_postgres():
    """Use real PostgreSQL from Docker."""
    conn_string = get_postgres_connection_string()
    # Test with real database...

def test_with_redis():
    """Use real Redis from Docker."""
    redis_url = get_redis_url()
    # Test with real cache...
```

## Test Organization

### Directory Structure
```
tests/
├── unit/              # Tier 1: Fast, isolated tests
│   ├── nodes/
│   ├── runtime/
│   └── workflow/
├── integration/       # Tier 2: Real infrastructure tests
│   ├── database/
│   ├── api/
│   └── workflows/
├── e2e/              # Tier 3: Complete scenario tests
│   ├── pipelines/
│   └── production/
└── conftest.py       # Shared fixtures
```

### Running Tests by Tier
```bash
# Tier 1 - Unit tests (ALL unit tests)
pytest tests/unit/

# Tier 2 - Integration tests (ALL integration tests)
pytest tests/integration/

# Tier 3 - E2E tests (ALL e2e tests)
pytest tests/e2e/
```

## Critical Testing Policies

### 1. NO MOCKING in Tiers 2-3
```python
# ❌ NEVER in integration/e2e tests
from unittest.mock import patch

@patch('requests.get')
def test_api_integration(mock_get):
    mock_get.return_value.status_code = 200
    # BAD - mocking hides real issues

# ✅ ALWAYS use real services
def test_api_integration():
    response = requests.get('http://localhost:8888/v1/users')
    assert response.status_code == 200
```

### 2. Zero Skip Tolerance
```python
# ❌ NEVER skip tests
@pytest.mark.skip("Redis not available")
def test_redis_operations():
    pass

# ✅ Let tests fail naturally
def test_redis_operations():
    redis_client = redis.Redis(host='localhost', port=6380)
    redis_client.ping()  # Fails with clear error if Redis down
```

### 3. Test Isolation
```python
@pytest.fixture
def clean_database():
    """Each test gets clean database."""
    db = setup_test_db()
    yield db
    cleanup_test_db(db)

def test_one(clean_database):
    # Isolated test data
    pass

def test_two(clean_database):
    # Fresh database
    pass
```

## Related Patterns

- **Test organization**: [`test-organization`](test-organization.md)
- **Gold standard**: [`gold-testing`](../../17-gold-standards/gold-testing.md)
- **Runtime patterns**: [`runtime-execution`](../../01-core-sdk/runtime-execution.md)

## When to Escalate

Use `testing-specialist` subagent when:
- Complex test infrastructure setup needed
- Performance testing strategy required
- CI/CD integration issues
- Test coverage optimization needed

<!-- Trigger Keywords: testing best practices, test strategy, testing guide, runtime testing, how to test -->
