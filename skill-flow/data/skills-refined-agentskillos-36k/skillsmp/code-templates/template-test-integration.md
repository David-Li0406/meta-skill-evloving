---
name: template-test-integration
description: "Generate Kailash integration test template (Tier 2). Use when requesting 'integration test template', 'Tier 2 test', 'real infrastructure test', 'NO MOCKING test', or 'integration test example'."
---

# Integration Test Template (Tier 2)

Integration test template with real Docker services (NO MOCKING policy).

> **Skill Metadata**
> Category: `cross-cutting` (code-generation)
> Priority: `HIGH`
> SDK Version: `0.9.25+`
> Related Skills: [`test-3tier-strategy`](../../4-operations/testing/test-3tier-strategy.md), [`template-test-unit`](template-test-unit.md), [`template-test-e2e`](template-test-e2e.md)
> Related Subagents: `testing-specialist` (NO MOCKING policy), `tdd-implementer`

## Quick Reference

- **Purpose**: Test component interactions with real services
- **Speed**: <5 seconds per test
- **Dependencies**: Real Docker services (PostgreSQL, Redis, etc.)
- **Location**: `tests/integration/`
- **Mocking**: ❌ **FORBIDDEN** - use real services only

## Integration Test Template

```python
"""Integration tests for [Component] with real infrastructure"""

import pytest
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

@pytest.mark.integration
class Test[Component]Integration:
    """Integration tests with real Docker services."""

    def test_database_integration(self, test_database_url):
        """Test workflow with real database operations."""
        workflow = WorkflowBuilder()

        # Use real database node
        workflow.add_node("AsyncSQLDatabaseNode", "db_write", {
            "connection_string": test_database_url,
            "query": "INSERT INTO test_table (name, value) VALUES ($1, $2)",
            "params": ["test_name", 42]
        })

        workflow.add_node("AsyncSQLDatabaseNode", "db_read", {
            "connection_string": test_database_url,
            "query": "SELECT * FROM test_table WHERE name = $1",
            "params": ["test_name"]
        })

        workflow.add_connection("db_write", "result", "db_read", "trigger")

        # Execute with real database
        runtime = LocalRuntime()
        results, run_id = runtime.execute(workflow.build())

        # Verify real database operations
        assert results["db_read"]["data"] is not None
        assert len(results["db_read"]["data"]) > 0

    def test_node_interaction(self):
        """Test multiple nodes working together."""
        workflow = WorkflowBuilder()

        # Node 1: Data source
        workflow.add_node("PythonCodeNode", "source", {
            "code": "result = {'items': [1, 2, 3, 4, 5]}"
        })

        # Node 2: Processor
        workflow.add_node("PythonCodeNode", "process", {
            "code": """
items = input_data
filtered = [x for x in items if x > 2]
result = {'filtered': filtered, 'count': len(filtered)}
"""
        })

        # Node 3: Validator
        workflow.add_node("PythonCodeNode", "validate", {
            "code": """
data = input_data
valid = data['count'] > 0 and len(data['filtered']) == data['count']
result = {'valid': valid, 'data': data}
"""
        })

        # Connect nodes
        workflow.add_connection("source", "result.items", "process", "input_data")
        workflow.add_connection("process", "result", "validate", "input_data")

        # Execute
        runtime = LocalRuntime()
        results, run_id = runtime.execute(workflow.build())

        # Validate integration
        assert results["validate"]["result"]["valid"] is True
        assert results["validate"]["result"]["data"]["count"] == 3
```

## Docker Setup Required

```bash
# MUST run before integration tests
./tests/utils/test-env up && ./tests/utils/test-env status
```

## Fixtures for Real Services

```python
import pytest

@pytest.fixture(scope="session")
def test_database_url():
    """Provide real test database URL."""
    return "postgresql://test:test@localhost:5433/test_db"

@pytest.fixture(scope="session")
def test_redis_url():
    """Provide real Redis URL."""
    return "redis://localhost:6380/0"

@pytest.fixture(autouse=True)
def cleanup_database(test_database_url):
    """Clean database before each test."""
    import psycopg2
    conn = psycopg2.connect(test_database_url)
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE test_table CASCADE")
    conn.commit()
    conn.close()

    yield

    # Cleanup after test
    conn = psycopg2.connect(test_database_url)
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE test_table CASCADE")
    conn.commit()
    conn.close()
```

## NO MOCKING Policy

### ❌ FORBIDDEN in Tier 2
```python
# ❌ Don't mock databases
@patch('database.connect')
def test_database_integration(mock_db):
    mock_db.return_value = fake_connection

# ❌ Don't mock SDK components
@patch('kailash.nodes.CSVReaderNode')
def test_workflow(mock_node):
    mock_node.execute.return_value = fake_data
```

### ✅ USE REAL SERVICES
```python
# ✅ Use real database from Docker
def test_database_integration(test_database_url):
    # Uses actual PostgreSQL from Docker
    workflow.add_node("AsyncSQLDatabaseNode", "db", {
        "connection_string": test_database_url,
        "query": "SELECT * FROM users"
    })
```

## Related Patterns

- **Unit tests**: [`template-test-unit`](template-test-unit.md)
- **E2E tests**: [`template-test-e2e`](template-test-e2e.md)
- **Testing strategy**: [`test-3tier-strategy`](../../4-operations/testing/test-3tier-strategy.md)
- **NO MOCKING policy**: [`gold-mocking-policy`](../../17-gold-standards/gold-mocking-policy.md)

## When to Escalate

Use `testing-specialist` when:
- Complex test infrastructure needed
- Custom Docker setup required
- CI/CD integration

Use `tdd-implementer` when:
- Test-first development approach
- Complete test suite design

## Documentation References

### Primary Sources
- **Testing Specialist**: [`.claude/agents/testing-specialist.md` (lines 178-209)](../../../../.claude/agents/testing-specialist.md#L178-L209)
- **Test Organization**: [`sdk-users/3-development/testing/test-organization-policy.md`](../../../../sdk-users/3-development/testing/test-organization-policy.md)
- **NO MOCKING**: [`sdk-users/7-gold-standards/mock-directives-for-testing.md`](../../../../sdk-users/7-gold-standards/mock-directives-for-testing.md)

## Quick Tips

- 💡 **Real services**: Use Docker for databases, Redis, etc.
- 💡 **<5 seconds**: Keep tests fast
- 💡 **NO MOCKING**: Absolute rule for Tier 2
- 💡 **Cleanup**: Always clean test data before/after

<!-- Trigger Keywords: integration test template, Tier 2 test, real infrastructure test, NO MOCKING test, integration test example, integration test boilerplate, Docker test template -->
