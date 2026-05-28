---
name: python-unit-testing
description: Write Python unit tests using pytest. Tests should be non-trivial, complete in under 30 seconds, and run with just "pytest". Covers conftest.py fixtures, test organization, parametrization, mocking, and temporary files. Use when adding unit tests to Python libraries or modules.
---

# Python Unit Testing Guide

Write unit tests for Python libraries using pytest. Unit tests verify individual functions and classes in isolation.

## Testing Terminology

| Type | What it tests | How to run | Skill |
|------|---------------|------------|-------|
| **Unit test** | Individual functions/classes in isolation | `pytest` | This skill |
| **CLI test** | Command-line interface via CliRunner | `pytest` | `python-cli-testing` |
| **Smoketest** | Full system with real services (AKA e2e, integration) | `RUN_INTEGRATION_TESTS=true pytest` | `smoketest-writing` |

## Core Principles

1. **Fast** - Full suite completes in under 30 seconds
2. **Simple to run** - Just type `pytest`, no flags or env vars needed
3. **Non-trivial** - Test behavior, not implementation details
4. **Isolated** - No network, no database, no filesystem side effects
5. **Deterministic** - Same result every time

## Directory Structure

```
project/
├── mypackage/
│   ├── __init__.py
│   ├── processing.py
│   └── utils.py
├── tests/
│   ├── conftest.py          # Shared fixtures
│   ├── test_processing.py   # Tests for processing.py
│   └── test_utils.py        # Tests for utils.py
└── pyproject.toml           # pytest configuration
```

## pytest Configuration

Add to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

## conftest.py - Shared Fixtures

```python
# tests/conftest.py

import pytest
from pathlib import Path


@pytest.fixture
def temp_dir(tmp_path):
    """Temporary directory for test files."""
    return tmp_path


@pytest.fixture
def sample_data():
    """Sample data structure for testing."""
    return {
        "name": "test",
        "values": [1, 2, 3],
        "nested": {"key": "value"}
    }


@pytest.fixture
def sample_file(tmp_path):
    """Create a temporary file with content."""
    f = tmp_path / "sample.txt"
    f.write_text("line1\nline2\nline3\n")
    return f
```

## Writing Tests

### Basic Test Structure

```python
# tests/test_processing.py

import pytest
from mypackage.processing import compute_digest, validate_input


class TestComputeDigest:
    """Tests for compute_digest function."""

    def test_returns_expected_format(self, sample_file):
        """Digest should be a 64-char hex string."""
        result = compute_digest(sample_file)

        assert isinstance(result, str)
        assert len(result) == 64
        assert all(c in "0123456789abcdef" for c in result)

    def test_same_input_same_output(self, sample_file):
        """Same file should produce same digest."""
        result1 = compute_digest(sample_file)
        result2 = compute_digest(sample_file)

        assert result1 == result2

    def test_different_input_different_output(self, tmp_path):
        """Different files should produce different digests."""
        file1 = tmp_path / "a.txt"
        file2 = tmp_path / "b.txt"
        file1.write_text("content A")
        file2.write_text("content B")

        assert compute_digest(file1) != compute_digest(file2)


class TestValidateInput:
    """Tests for validate_input function."""

    def test_valid_input_returns_true(self):
        assert validate_input({"name": "test", "value": 42}) is True

    def test_missing_required_field(self):
        assert validate_input({"name": "test"}) is False

    def test_empty_input(self):
        assert validate_input({}) is False
```

### Testing Exceptions

```python
def test_file_not_found_raises(self):
    """Missing file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        compute_digest(Path("/nonexistent/file.txt"))


def test_invalid_input_raises_with_message(self):
    """Invalid input should raise ValueError with helpful message."""
    with pytest.raises(ValueError, match="must be positive"):
        validate_input({"value": -1})
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input_val,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
    ("123", "123"),
])
def test_uppercase_conversion(input_val, expected):
    assert to_uppercase(input_val) == expected


@pytest.mark.parametrize("invalid_input", [
    None,
    123,
    [],
    {},
])
def test_rejects_non_string(invalid_input):
    with pytest.raises(TypeError):
        to_uppercase(invalid_input)
```

### Testing with Temporary Files

```python
def test_writes_output_file(self, tmp_path):
    """Function should create output file."""
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"
    input_file.write_text("test content")

    process_file(input_file, output_file)

    assert output_file.exists()
    assert output_file.read_text() == "processed: test content"


def test_handles_large_file(self, tmp_path):
    """Should handle files with many lines."""
    large_file = tmp_path / "large.txt"
    large_file.write_text("\n".join(f"line{i}" for i in range(10000)))

    result = count_lines(large_file)

    assert result == 10000
```

## Mocking

### Mock External Dependencies

```python
from unittest.mock import Mock, patch


def test_fetches_from_api(self):
    """Should call API and return parsed response."""
    mock_response = Mock()
    mock_response.json.return_value = {"data": "value"}
    mock_response.status_code = 200

    with patch("mypackage.client.requests.get", return_value=mock_response):
        result = fetch_data("http://example.com/api")

    assert result == {"data": "value"}


def test_handles_api_error(self):
    """Should raise on API error."""
    mock_response = Mock()
    mock_response.status_code = 500

    with patch("mypackage.client.requests.get", return_value=mock_response):
        with pytest.raises(APIError):
            fetch_data("http://example.com/api")
```

### Mock as Fixture

```python
# conftest.py
@pytest.fixture
def mock_api_client():
    """Mock API client for testing."""
    with patch("mypackage.client.APIClient") as mock:
        client = Mock()
        mock.return_value = client
        yield client


# test file
def test_uses_api_client(mock_api_client):
    mock_api_client.fetch.return_value = {"key": "value"}

    result = process_with_api()

    mock_api_client.fetch.assert_called_once()
    assert result == "value"
```

## Fixtures with Setup/Teardown

```python
@pytest.fixture
def database_connection():
    """In-memory SQLite for testing."""
    import sqlite3
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE items (id INTEGER, name TEXT)")
    yield conn
    conn.close()


@pytest.fixture
def populated_db(database_connection):
    """Database with test data."""
    database_connection.execute("INSERT INTO items VALUES (1, 'test')")
    database_connection.commit()
    return database_connection
```

## Test Organization

### Group by Feature

```python
class TestUserValidation:
    """All tests for user validation logic."""

    def test_valid_email(self): ...
    def test_invalid_email(self): ...
    def test_valid_password(self): ...
    def test_password_too_short(self): ...


class TestUserCreation:
    """All tests for user creation."""

    def test_creates_user(self): ...
    def test_duplicate_email_fails(self): ...
```

### Use Descriptive Names

```python
# Good - describes behavior
def test_empty_list_returns_none(self): ...
def test_single_item_returns_that_item(self): ...
def test_multiple_items_returns_first_match(self): ...

# Bad - describes implementation
def test_function_works(self): ...
def test_returns_correct_value(self): ...
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific file
pytest tests/test_processing.py

# Run specific class
pytest tests/test_processing.py::TestComputeDigest

# Run specific test
pytest tests/test_processing.py::TestComputeDigest::test_returns_expected_format

# Run with coverage
pytest --cov=mypackage

# Run matching pattern
pytest -k "digest"
```

## Checklist

- [ ] Tests in `tests/` directory
- [ ] `conftest.py` with shared fixtures
- [ ] `pyproject.toml` with pytest config
- [ ] Full suite runs in under 30 seconds
- [ ] `pytest` runs without flags or env vars
- [ ] No network calls (mock external APIs)
- [ ] No real database (use in-memory or mock)
- [ ] Descriptive test names
- [ ] Tests grouped by feature in classes
