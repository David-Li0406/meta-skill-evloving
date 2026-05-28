---
name: dataflow-tdd-api
description: "DataFlow TDD fixtures and testing API. Use when asking 'test dataflow', 'dataflow fixtures', or 'dataflow testing api'."
---

# DataFlow TDD API

> **Skill Metadata**
> Category: `dataflow`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Test Fixtures

```python
import pytest
from dataflow import DataFlow

@pytest.fixture
def test_db():
    """In-memory SQLite for tests"""
    db = DataFlow("sqlite:///:memory:")

    @db.model
    class User:
        id: str
        email: str

    db.initialize_schema()
    yield db
    db.close()

def test_user_creation(test_db):
    from kailash.workflow.builder import WorkflowBuilder
    from kailash.runtime import LocalRuntime

    workflow = WorkflowBuilder()
    workflow.add_node("UserCreateNode", "create", {
        "id": "user_001",
        "email": "test@example.com"
    })

    runtime = LocalRuntime()
    results, run_id = runtime.execute(workflow.build())

    assert results["create"]["id"] == "user_001"
    assert results["create"]["email"] == "test@example.com"
```

## Isolation Patterns

```python
@pytest.fixture(scope="function")
def isolated_db():
    """Each test gets isolated database"""
    db = DataFlow("sqlite:///:memory:")
    db.initialize_schema()
    yield db
    db.close()  # Clean up

def test_isolation_1(isolated_db):
    # This test's data won't affect test_isolation_2
    pass

def test_isolation_2(isolated_db):
    # Clean slate - no data from test_isolation_1
    pass
```

## Documentation

- **Testing Guide**: [`sdk-users/apps/dataflow/09-testing.md`](../../../../sdk-users/apps/dataflow/09-testing.md)

<!-- Trigger Keywords: test dataflow, dataflow fixtures, dataflow testing api, dataflow unit tests -->
