---
name: python-testing
description: Use this skill when writing and evaluating Python tests with pytest, including unit tests, integration tests, and best practices for test-driven development.
---

# Python Testing

Comprehensive guide to implementing robust testing strategies in Python using pytest, fixtures, mocking, parameterization, and test-driven development practices.

## Core Principles

Every test should be **atomic**, **self-contained**, and test **single functionality**. A test that tests multiple things is harder to debug and maintain.

## Test Types

- **Unit Tests**: Test individual functions/classes in isolation.
- **Integration Tests**: Test interaction between components.
- **Functional Tests**: Test complete features end-to-end.
- **Performance Tests**: Measure speed and resource usage.

## Test Structure

### Arrange-Act-Assert (AAA) Pattern

1. **Arrange**: Set up test data and preconditions.
2. **Act**: Execute the code under test.
3. **Assert**: Verify the results.

### Test Naming

Use descriptive names that explain the scenario:

```python
# Good
def test_login_fails_with_invalid_password():
def test_user_can_update_own_profile():
# Bad
def test_login():
def test_update():
```

## Writing Effective Tests

### Basic pytest Tests

```python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
```

### Parameterized Tests

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_addition_parameterized(a, b, expected):
    assert add(a, b) == expected
```

### Fixtures for Setup and Teardown

```python
import pytest

@pytest.fixture
def sample_user():
    return {"id": 1, "name": "Test User"}

def test_user_creation(sample_user):
    assert sample_user["name"] == "Test User"
```

## Mocking External Dependencies

```python
from unittest.mock import patch

def fetch_data(url):
    response = requests.get(url)
    return response.json()

@patch('requests.get')
def test_fetch_data(mock_get):
    mock_get.return_value.json.return_value = {"data": "test"}
    result = fetch_data("http://example.com")
    assert result["data"] == "test"
```

## Running Tests

```bash
pytest -v                     # Run all tests with verbose output
pytest -k "test_name"        # Run tests matching pattern
pytest --cov=myapp           # Run tests with coverage
```

## Best Practices

1. **Write tests first** (TDD) or alongside code.
2. **One assertion per test** when possible.
3. **Use descriptive test names** that explain behavior.
4. **Keep tests independent** and isolated.
5. **Use fixtures** for setup and teardown.
6. **Mock external dependencies** appropriately.
7. **Parametrize tests** to reduce duplication.
8. **Test edge cases** and error conditions.
9. **Measure coverage** but focus on quality.
10. **Run tests in CI/CD** on every commit.

## Resources

- **pytest documentation**: https://docs.pytest.org/
- **unittest.mock**: https://docs.python.org/3/library/unittest.mock.html
- **hypothesis**: Property-based testing
- **pytest-asyncio**: Testing async code
- **pytest-cov**: Coverage reporting