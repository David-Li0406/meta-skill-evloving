---
name: testing-strategy
description: Universal testing strategies and best practices for software projects
license: MIT
compatibility: opencode
metadata:
    related_python_guidelines: For Python-specific testing, use skill `python-guidelines`
    related_coding_principles: For overall quality standards, use skill `coding-principles`
---

# Testing Strategy

## What I Do

Provide universal testing strategies and best practices that apply across different programming languages and project types.

## Universal Testing Framework

### Test Organization

```text
# Universal test directory structure
tests/
├── unit/              # Unit tests
│   ├── core/          # Core functionality tests
│   └── utils/         # Utility function tests
├── integration/       # Integration tests
├── e2e/               # End-to-end tests
├── performance/       # Performance tests
├── conftest.py        # Shared fixtures
└── test_data/         # Test data files
```

### Test Coverage Standards

**Minimum Coverage Targets:**

- **Unit Tests**: 90%+ code coverage
- **Integration Tests**: 80%+ scenario coverage
- **End-to-End Tests**: Critical user journey coverage
- **Performance Tests**: Baseline performance metrics

```python
# Universal test coverage monitoring
import pytest
import coverage

def run_tests_with_coverage():
    """Run tests with coverage measurement"""
    cov = coverage.Coverage()
    cov.start()

    # Run pytest
    exit_code = pytest.main([
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-fail-under=90",
        "tests/"
    ])

    cov.stop()
    cov.save()
    return exit_code
```

## When to Use Me

Use this skill when:

- Setting up testing for new projects
- Standardizing testing across teams
- Creating reusable testing patterns
- Implementing quality assurance processes

## Universal Testing Examples

### Test Fixtures

```python
# Universal test fixture patterns
import pytest
from typing import Generator

@pytest.fixture(scope="module")
def database_connection() -> Generator:
    """Universal database fixture"""
    # Setup
    conn = create_test_database()
    yield conn
    # Teardown
    conn.close()
    cleanup_test_database()

@pytest.fixture
def sample_data():
    """Universal sample data fixture"""
    return {
        "valid_input": get_valid_input(),
        "edge_cases": get_edge_cases(),
        "invalid_input": get_invalid_input()
    }
```

### Parameterized Testing

```python
# Universal parameterized testing
import pytest

@pytest.mark.parametrize("input,expected", [
    ([1, 2, 3], 6),      # Normal case
    ([], 0),             # Empty input
    ([-1, 0, 1], 0),     # Mixed values
    ([1.5, 2.5], 4.0)    # Float values
])
def test_sum_function(input, expected):
    """Test sum function with various inputs"""
    assert sum(input) == expected
```

### Mocking and Isolation

```python
# Universal mocking patterns
from unittest.mock import patch, MagicMock
import requests

def test_api_call():
    """Test API calls with mocking"""
    # Mock external API
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "success"}

    with patch("requests.get", return_value=mock_response):
        result = make_api_call()
        assert result == {"status": "success"}
        requests.get.assert_called_once_with("https://api.example.com/data")
```

### Performance Testing

```python
# Universal performance testing
import time
import pytest

@pytest.mark.performance
def test_processing_speed():
    """Test processing speed meets requirements"""
    start_time = time.time()

    # Run the operation
    result = process_large_dataset()

    duration = time.time() - start_time
    assert duration < 5.0, f"Processing took {duration:.2f}s, expected <5.0s"
    assert result.is_valid()
```

## Best Practices

1. **Consistency**: Apply same testing patterns across projects
2. **Automation**: Integrate testing into CI/CD pipelines
3. **Isolation**: Test components in isolation
4. **Documentation**: Document testing approaches clearly

## Compatibility

Applies to:

- All programming languages
- Any software project type
- Cross-project testing standardization
- Organizational quality assurance
