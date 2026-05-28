---
name: dataflow-tdd-mode
description: "DataFlow TDD mode for fast isolated tests. Use when DataFlow TDD, test isolation, savepoint, fast tests, or <100ms tests DataFlow."
---

# DataFlow TDD Mode

Lightning-fast isolated tests (<100ms) using savepoint-based rollback for DataFlow.

> **Skill Metadata**
> Category: `dataflow`
> Priority: `HIGH`
> SDK Version: `0.9.25+ / DataFlow 0.6.0`
> Related Skills: [`test-3tier-strategy`](#), [`dataflow-models`](#)
> Related Subagents: `dataflow-specialist`, `testing-specialist`

## Quick Reference

- **TDD Mode**: Savepoint isolation - each test rollsback
- **Speed**: <100ms per test (no cleanup needed)
- **Isolation**: Tests don't affect each other
- **Pattern**: Use in-memory SQLite or transaction wrappers

## Core Pattern

```python
import pytest
from dataflow import DataFlow

@pytest.fixture
def db():
    """TDD mode - savepoint isolation."""
    db = DataFlow(
        database_url=":memory:",  # In-memory for speed
        auto_migrate=True,
        tdd_mode=True  # Enable savepoint isolation
    )

    @db.model
    class User:
        name: str
        email: str

    yield db
    # Automatic rollback via savepoint

def test_user_creation(db):
    """Test runs in <100ms with isolation."""
    workflow = WorkflowBuilder()
    workflow.add_node("UserCreateNode", "create", {
        "name": "Test User",
        "email": "test@example.com"
    })

    runtime = LocalRuntime()
    results, run_id = runtime.execute(workflow.build())

    assert results["create"]["result"]["name"] == "Test User"
    # Automatic rollback - no cleanup needed
```

## TDD Mode Features

### Savepoint Isolation

```python
@pytest.fixture
def isolated_db():
    db = DataFlow(":memory:", tdd_mode=True)

    @db.model
    class Product:
        name: str
        price: float

    yield db
    # Changes rolled back automatically

def test_product_1(isolated_db):
    # Create product
    # ... test logic ...
    pass  # Rolled back

def test_product_2(isolated_db):
    # Fresh state - no data from test_product_1
    pass
```

### Fast Test Execution

```python
def test_suite_performance(db):
    """100 tests in <10 seconds."""
    for i in range(100):
        workflow = WorkflowBuilder()
        workflow.add_node("UserCreateNode", f"create_{i}", {
            "name": f"User {i}",
            "email": f"user{i}@test.com"
        })
        runtime = LocalRuntime()
        results, run_id = runtime.execute(workflow.build())
        # Each test <100ms with rollback
```

## Common Mistakes

### Mistake 1: Not Using TDD Mode

```python
# SLOW - Full cleanup needed
@pytest.fixture
def db():
    db = DataFlow(":memory:")
    yield db
    # Manual cleanup - slow!
    db.drop_all_tables()
```

**Fix: Enable TDD Mode**

```python
@pytest.fixture
def db():
    db = DataFlow(":memory:", tdd_mode=True)
    yield db
    # Automatic savepoint rollback - fast!
```

## Documentation References

### Primary Sources
- **TDD Quick Start**: [`sdk-users/apps/dataflow/docs/tdd/quick-start.md`](../../../../sdk-users/apps/dataflow/docs/tdd/quick-start.md)
- **Best Practices**: [`sdk-users/apps/dataflow/docs/tdd/best-practices.md`](../../../../sdk-users/apps/dataflow/docs/tdd/best-practices.md)
- **Performance Guide**: [`sdk-users/apps/dataflow/docs/tdd/performance-guide.md`](../../../../sdk-users/apps/dataflow/docs/tdd/performance-guide.md)

### Related Documentation
- **DataFlow Specialist**: [`.claude/skills/dataflow-specialist.md`](../../dataflow-specialist.md#L893-L940)
- **Test Strategy**: [`test-3tier-strategy`](#)

## Quick Tips

- Use `:memory:` SQLite for maximum speed
- tdd_mode=True enables savepoint isolation
- Each test <100ms with rollback
- No manual cleanup needed
- Perfect for unit tests (Tier 1)

## Keywords for Auto-Trigger

<!-- Trigger Keywords: DataFlow TDD, test isolation, savepoint, fast tests, DataFlow testing, <100ms tests, test mode, isolated tests -->
