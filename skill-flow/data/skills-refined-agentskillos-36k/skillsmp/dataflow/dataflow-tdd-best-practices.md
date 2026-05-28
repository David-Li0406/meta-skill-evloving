---
name: dataflow-tdd-best-practices
description: "DataFlow TDD best practices. Use when asking 'dataflow test practices', 'dataflow testing strategy', or 'test dataflow workflows'."
---

# DataFlow TDD Best Practices

> **Skill Metadata**
> Category: `dataflow`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`

## 3-Tier Testing Strategy

### Tier 1: Unit Tests (Fast, In-Memory)

```python
def test_user_create(test_db):
    """Test single node operation"""
    workflow = WorkflowBuilder()
    workflow.add_node("UserCreateNode", "create", {
        "id": "user_001",
        "email": "test@example.com"
    })

    runtime = LocalRuntime()
    results, run_id = runtime.execute(workflow.build())
    assert results["create"]["id"] == "user_001"
```

### Tier 2: Integration Tests (Real SQLite)

```python
def test_user_workflow():
    """Test full workflow with real SQLite database"""
    db = DataFlow("sqlite:///test.db")
    db.initialize_schema()

    # Run full CRUD workflow
    # Cleanup after
    os.remove("test.db")
```

### Tier 3: E2E Tests (Real PostgreSQL)

```python
@pytest.mark.e2e
def test_production_workflow():
    """Test with production-like PostgreSQL"""
    db = DataFlow(os.getenv("TEST_POSTGRES_URL"))
    # Test full system
```

## Best Practices

1. **Use `:memory:` for unit tests** - Fast, isolated
2. **Real databases for integration** - Catch SQL dialect issues
3. **Clean up after tests** - Remove test databases
4. **Test error cases** - Invalid data, constraints
5. **Test concurrent access** - For PostgreSQL

## Documentation

- **Testing Strategy**: [`sdk-users/apps/dataflow/09-testing.md#strategy`](../../../../sdk-users/apps/dataflow/09-testing.md)

<!-- Trigger Keywords: dataflow test practices, dataflow testing strategy, test dataflow workflows -->
