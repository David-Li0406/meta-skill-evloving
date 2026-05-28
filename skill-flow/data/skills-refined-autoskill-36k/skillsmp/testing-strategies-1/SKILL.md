---
name: testing-strategies
description: "Comprehensive testing strategies for Kailash applications including the 3-tier testing approach with NO MOCKING policy for Tiers 2-3. Use when asking about 'testing', 'test strategy', '3-tier testing', 'unit tests', 'integration tests', 'end-to-end tests', 'testing workflows', 'testing DataFlow', 'testing Nexus', 'NO MOCKING', 'real infrastructure', 'test organization', or 'testing best practices'."
---

# Kailash Testing Strategies

Comprehensive testing approach for Kailash applications using the 3-tier testing strategy with NO MOCKING policy.

## Overview

Kailash testing philosophy:
- **3-Tier Strategy**: Unit, Integration, End-to-End
- **NO MOCKING Policy**: Tiers 2-3 use real infrastructure
- **Real Database Testing**: Actual PostgreSQL/SQLite
- **Real API Testing**: Live HTTP calls
- **Real LLM Testing**: Actual model calls (with caching)

## Reference Documentation

### Core Strategy
- **[test-3tier-strategy](test-3tier-strategy.md)** - Complete 3-tier testing guide
  - Tier 1: Unit Tests (mocking allowed)
  - Tier 2: Integration Tests (NO MOCKING)
  - Tier 3: End-to-End Tests (NO MOCKING)
  - Test organization
  - Fixture patterns
  - CI/CD integration

## 3-Tier Testing Strategy

### Tier 1: Unit Tests
**Scope**: Individual functions and classes
**Mocking**: ✅ Allowed
**Speed**: Fast (< 1s per test)

```python
def test_workflow_builder():
    """Test workflow builder logic (no execution)."""
    workflow = WorkflowBuilder()
    workflow.add_node("PythonCodeNode", "node1", {})

    built = workflow.build()
    assert built.node_count() == 1
```

### Tier 2: Integration Tests
**Scope**: Component integration (workflows, database, APIs)
**Mocking**: ❌ NO MOCKING
**Speed**: Medium (1-10s per test)

```python
def test_dataflow_crud(db: DataFlow):
    """Test DataFlow CRUD with real database."""
    # Uses real PostgreSQL/SQLite
    workflow = db.create_workflow("User_Create", {...})
    results = runtime.execute(workflow.build())

    # Verify in actual database
    assert results["create"]["result"] is not None
```

### Tier 3: End-to-End Tests
**Scope**: Complete user workflows
**Mocking**: ❌ NO MOCKING
**Speed**: Slow (10s+ per test)

```python
def test_user_registration_flow(nexus: Nexus):
    """Test complete user flow via Nexus API."""
    # Real HTTP request to actual API
    response = requests.post("http://localhost:8000/api/register", json={
        "email": "test@example.com",
        "name": "Test User"
    })

    assert response.status_code == 200
    assert response.json()["user_id"] is not None
```

## NO MOCKING Policy

### Why No Mocking in Tiers 2-3?

**Real Issues Found**:
- Database constraint violations
- API timeout problems
- Race conditions
- Connection pool exhaustion
- Schema migration issues
- LLM token limits

**Mocking Hides**:
- Real-world latency
- Actual error conditions
- Integration bugs
- Performance issues

### What to Use Instead

**Real Infrastructure**:
- Test databases (Docker containers)
- Test API endpoints
- Test LLM accounts (with caching)
- Test file systems (temp directories)

## Test Organization

### Directory Structure
```
tests/
  tier1_unit/
    test_workflow_builder.py
    test_node_logic.py
  tier2_integration/
    test_dataflow_crud.py
    test_workflow_execution.py
    test_api_integration.py
  tier3_e2e/
    test_user_flows.py
    test_production_scenarios.py
  conftest.py  # Shared fixtures
```

### Fixture Patterns

```python
# conftest.py
import pytest
from dataflow import DataFlow
from kailash.runtime import LocalRuntime

@pytest.fixture
def db():
    """Real database for testing (Docker)."""
    db = DataFlow("postgresql://test:test@localhost:5433/test_db")
    db.create_tables()
    yield db
    db.drop_tables()

@pytest.fixture
def runtime():
    """Real runtime instance."""
    return LocalRuntime()
```

## Testing Different Components

### Testing Workflows
```python
def test_workflow_execution(runtime):
    """Tier 2: Integration test with real execution."""
    workflow = WorkflowBuilder()
    workflow.add_node("PythonCodeNode", "calc", {
        "code": "result = 2 + 2"
    })

    results = runtime.execute(workflow.build())
    assert results["calc"]["result"] == 4
```

### Testing DataFlow
```python
def test_dataflow_operations(db: DataFlow):
    """Tier 2: Test with real database."""
    @db.model
    class User:
        id: str
        name: str

    # Real database operations
    workflow = db.create_workflow("User_Create", {
        "data": {"id": "1", "name": "Test"}
    })
    results = runtime.execute(workflow.build())

    # Verify in actual database
    user = db.query("SELECT * FROM users WHERE id = '1'")
    assert user["name"] == "Test"
```

### Testing Nexus
```python
def test_nexus_api(nexus_server):
    """Tier 3: E2E test with real HTTP."""
    import requests

    response = requests.post(
        "http://localhost:8000/api/workflow/test_workflow",
        json={"input": "data"}
    )

    assert response.status_code == 200
    assert "result" in response.json()
```

### Testing Kaizen Agents
```python
def test_agent_execution():
    """Tier 2: Test with real LLM (cached)."""
    agent = MyAgent()

    # Real LLM call (use caching to reduce costs)
    result = agent(input="Test query")

    assert result.output is not None
    assert isinstance(result.output, str)
```

## Critical Rules

- ✅ Tier 1: Mock external dependencies
- ✅ Tier 2-3: Use real infrastructure
- ✅ Use Docker for test databases
- ✅ Clean up resources after tests
- ✅ Cache LLM responses for cost
- ✅ Run Tier 1 in CI, Tier 2-3 optionally
- ❌ NEVER mock database in Tier 2-3
- ❌ NEVER mock HTTP calls in Tier 2-3
- ❌ NEVER skip resource cleanup
- ❌ NEVER commit test credentials

## Running Tests

### Local Development
```bash
# Run all tests
pytest

# Run by tier
pytest tests/tier1_unit/
pytest tests/tier2_integration/
pytest tests/tier3_e2e/

# Run with coverage
pytest --cov=app --cov-report=html
```

### CI/CD
```bash
# Fast CI (Tier 1 only)
pytest tests/tier1_unit/

# Full CI (all tiers)
docker-compose up -d  # Start test infrastructure
pytest
docker-compose down
```

## When to Use This Skill

Use this skill when you need to:
- Understand Kailash testing philosophy
- Set up test infrastructure
- Write integration tests
- Test workflows with real execution
- Test DataFlow with real databases
- Test Nexus APIs end-to-end
- Organize test suites
- Configure CI/CD testing

## Best Practices

### Test Quality
- Write descriptive test names
- Use AAA pattern (Arrange, Act, Assert)
- Test both success and failure cases
- Clean up resources properly
- Use fixtures for setup/teardown

### Performance
- Use test database containers
- Cache expensive operations
- Run tests in parallel (when safe)
- Skip slow tests in development (mark with @pytest.mark.slow)

### Maintenance
- Keep tests close to code
- Update tests with code changes
- Review test coverage regularly
- Remove obsolete tests

## Related Skills

- **[07-development-guides](../../07-development-guides/SKILL.md)** - Testing patterns
- **[17-gold-standards](../../17-gold-standards/SKILL.md)** - Testing best practices
- **[02-dataflow](../../02-dataflow/SKILL.md)** - DataFlow testing
- **[03-nexus](../../03-nexus/SKILL.md)** - API testing

## Support

For testing help, invoke:
- `testing-specialist` - Testing strategies and patterns
- `tdd-implementer` - Test-driven development
- `dataflow-specialist` - DataFlow testing patterns
