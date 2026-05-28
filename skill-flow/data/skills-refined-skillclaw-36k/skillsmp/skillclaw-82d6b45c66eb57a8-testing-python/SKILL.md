---
name: testing-python
description: Use this skill when writing and evaluating effective Python tests with pytest, including unit tests, integration tests, and test-driven development practices.
---

# Skill body

## Core Principles

- Every test should be **atomic**, **self-contained**, and test **single functionality**. A test that tests multiple things is harder to debug and maintain.

## Test Structure

### Atomic Unit Tests

Each test should verify a single behavior. The test name should clearly indicate what is broken when it fails. Multiple assertions are acceptable if they all verify the same behavior.

```python
# Good: Name tells you what's broken
def test_user_creation_sets_defaults():
    user = User(name="Alice")
    assert user.role == "member"
    assert user.id is not None
    assert user.created_at is not None

# Bad: If this fails, what behavior is broken?
def test_user():
    user = User(name="Alice")
    assert user.role == "member"
    user.promote()
    assert user.role == "admin"
    assert user.can_delete_others()
```

### Use Parameterization for Variations of the Same Concept

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
    ("123", "123"),
])
def test_uppercase_conversion(input, expected):
    assert input.upper() == expected
```

### Test Types

- **Unit Tests**: Test individual functions/classes in isolation.
- **Integration Tests**: Test interaction between components, such as services and databases.
- **Functional Tests**: Test complete features end-to-end.
- **Performance Tests**: Measure speed and resource usage.

## Project-Specific Rules

### Async Testing

This project uses `asyncio_mode = "auto"` globally. Write async tests without decorators:

```python
# Correct
async def test_async_operation():
    result = await some_async_function()
    assert result == expected

# Wrong - don't add this
@pytest.mark.asyncio
async def test_async_operation():
    ...
```

### Imports at Module Level

Put all imports at the top of the file:

```python
# Correct
import pytest
from fastmcp import FastMCP
from fastmcp.client import Client

async def test_something():
    mcp = FastMCP("test")
    ...

# Wrong - no local imports
async def test_something():
    from fastmcp import FastMCP  # Don't do this
    ...
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_example.py -v
```

## Debugging Failing Tests

- Use `pytest -v` for verbose output.
- Check the traceback to identify the source of the failure.
- Use print statements or logging to inspect variable states.

## Test Coverage

- Measure what code is exercised by tests.
- Identify untested code paths.
- Aim for meaningful coverage, not just high percentages.

## Quick Start Example

```python
# test_example.py
def add(a, b):
    return a + b

def test_add():
    """Basic test example."""
    result = add(2, 3)
    assert result == 5

def test_add_negative():
    """Test with negative numbers."""
    assert add(-1, 1) == 0

# Run with: pytest test_example.py
```