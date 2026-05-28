---
name: template-test-e2e
description: "Generate Kailash end-to-end test template (Tier 3). Use when requesting 'e2e test template', 'Tier 3 test', 'end-to-end test', 'complete workflow test', or 'business scenario test'."
---

# End-to-End Test Template (Tier 3)

Complete business scenario test template with full infrastructure stack.

> **Skill Metadata**
> Category: `cross-cutting` (code-generation)
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`
> Related Skills: [`test-3tier-strategy`](../../4-operations/testing/test-3tier-strategy.md), [`template-test-integration`](template-test-integration.md)
> Related Subagents: `testing-specialist`, `tdd-implementer`

## Quick Reference

- **Purpose**: Test complete user workflows end-to-end
- **Speed**: <10 seconds per test
- **Dependencies**: Full Docker infrastructure
- **Location**: `tests/e2e/`
- **Mocking**: ❌ **FORBIDDEN** - complete real scenarios

## E2E Test Template

```python
"""End-to-end tests for [Business Scenario]"""

import pytest
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

@pytest.mark.e2e
@pytest.mark.timeout(10)
class Test[BusinessScenario]E2E:
    """End-to-end test for complete [scenario] workflow."""

    def test_complete_user_journey(self, test_database_url):
        """Test complete user journey from start to finish."""
        workflow = WorkflowBuilder()

        # Step 1: Data ingestion
        workflow.add_node("PythonCodeNode", "ingest", {
            "code": "result = {'data': [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]}"
        })

        # Step 2: Validation
        workflow.add_node("PythonCodeNode", "validate", {
            "code": """
items = input_data
valid_items = [item for item in items if 'id' in item and 'name' in item]
result = {'validated': valid_items, 'count': len(valid_items)}
"""
        })

        # Step 3: Database storage
        workflow.add_node("AsyncSQLDatabaseNode", "store", {
            "connection_string": test_database_url,
            "query": "INSERT INTO users (id, name) VALUES ($1, $2) ON CONFLICT DO NOTHING"
        })

        # Step 4: Verification
        workflow.add_node("AsyncSQLDatabaseNode", "verify", {
            "connection_string": test_database_url,
            "query": "SELECT COUNT(*) as count FROM users"
        })

        # Connect complete pipeline
        workflow.add_connection("ingest", "result.data", "validate", "input_data")
        workflow.add_connection("validate", "result.validated", "store", "batch_data")
        workflow.add_connection("store", "result", "verify", "trigger")

        # Execute complete workflow
        runtime = LocalRuntime()
        results, run_id = runtime.execute(workflow.build())

        # Verify end-to-end results
        assert results["ingest"]["result"]["data"] is not None
        assert results["validate"]["result"]["count"] == 2
        assert results["verify"]["data"][0]["count"] >= 2
```

## Related Patterns

- **Unit tests**: [`template-test-unit`](template-test-unit.md)
- **Integration tests**: [`template-test-integration`](template-test-integration.md)
- **Testing strategy**: [`test-3tier-strategy`](../../4-operations/testing/test-3tier-strategy.md)

## When to Escalate

Use `testing-specialist` when:
- Complex E2E scenario design
- Performance testing needed
- CI/CD integration

## Documentation References

### Primary Sources
- **Testing Specialist**: [`.claude/agents/testing-specialist.md` (lines 211-262)](../../../../.claude/agents/testing-specialist.md#L211-L262)
- **Production Testing**: [`sdk-users/3-development/12-testing-production-quality.md`](../../../../sdk-users/3-development/12-testing-production-quality.md)

## Quick Tips

- 💡 **Complete scenarios**: Test full user journeys
- 💡 **<10 seconds**: Keep reasonable execution time
- 💡 **Real infrastructure**: All services must be real
- 💡 **Business validation**: Verify business rules, not just technical

<!-- Trigger Keywords: e2e test template, Tier 3 test, end-to-end test, complete workflow test, business scenario test, e2e template, full workflow test -->
