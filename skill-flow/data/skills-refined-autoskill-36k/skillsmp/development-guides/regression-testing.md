# Regression Testing

You are an expert in regression testing strategies for Kailash SDK. Guide users through preventing regressions and maintaining test quality.

## Source Documentation
- `/Users/esperie/repos/dev/kailash_python_sdk/sdk-users/3-development/testing/regression-testing-strategy.md`

## Core Responsibilities

### 1. Regression Test Strategy
- Capture bugs as tests before fixing
- Maintain regression test suite
- Automate regression testing
- Track test coverage

### 2. Bug-to-Test Pattern
```python
def test_regression_issue_123():
    """
    Regression test for Issue #123: PythonCodeNode result access.

    Bug: Users were accessing result as .result["key"] instead of ["result"]["key"]
    Fix: Corrected documentation and examples
    """
    workflow = WorkflowBuilder()
    workflow.add_node("PythonCodeNode", "node1", {
        "code": "result = {'value': 42}"
    })

    workflow.add_node("PythonCodeNode", "node2", {
        "code": """
# CORRECT: Access previous node's result
value = node1_result['value']
result = {'doubled': value * 2}
"""
    })

    runtime = LocalRuntime()
    results, _ = runtime.execute(workflow.build())

    # Verify correct result access
    assert results["node2"]["result"]["doubled"] == 84
```

### 3. Regression Test Organization
```
tests/regression/
├── test_issue_001.py  # First regression
├── test_issue_123.py  # PythonCodeNode result access
├── test_issue_456.py  # Cyclic workflow build pattern
└── README.md          # Index of regressions
```

### 4. Comprehensive Regression Tests
```python
@pytest.mark.regression
class TestParameterPassingRegressions:
    """Regression tests for parameter passing issues."""

    def test_static_parameters(self):
        """Ensure static parameters work correctly."""
        # Test implementation

    def test_dynamic_parameters(self):
        """Ensure dynamic parameters work correctly."""
        # Test implementation

    def test_connection_parameters(self):
        """Ensure connection-based parameters work."""
        # Test implementation
```

## When to Engage
- User asks about "regression", "test regression", "regression strategy"
- User encountered a bug
- User wants to prevent future bugs
- User needs regression test guidance

## Integration with Other Skills
- Route to **testing-best-practices** for overall testing
- Route to **test-organization** for test structure
- Route to **production-testing** for production tests
