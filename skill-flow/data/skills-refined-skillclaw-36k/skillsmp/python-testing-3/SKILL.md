---
name: python-testing
description: Helps write pytest tests for Python code including Azure Functions, MCP tools, and API endpoints. Use this skill when creating unit tests, integration tests, fixtures, or mocking external services.
---

# Python Testing Skill

## Overview

This skill helps you write comprehensive tests using **pytest** for Azure Functions, MCP tools, and general Python code.

## Project Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_azure_functions.py  # Azure Functions tests
├── test_logic_apps.py       # Logic Apps tests
├── test_mcp_tools.py        # MCP tool tests
└── integration/
    └── test_e2e.py          # End-to-end tests
```

## Writing Tests

### Basic Test Pattern

```python
import pytest
from src.abstractions.azure_functions import analyze_data

def test_analyze_data_with_valid_input():
    """Test analyze_data returns correct statistics."""
    result = analyze_data([1, 2, 3, 4, 5])
    
    assert result["count"] == 5
    assert result["sum"] == 15
    assert result["mean"] == 3.0
    assert result["min"] == 1
    assert result["max"] == 5

def test_analyze_data_with_empty_list():
    """Test analyze_data handles empty input."""
    with pytest.raises(ValueError, match="No values provided"):
        analyze_data([])
```

### Testing MCP Tools

```python
import json
import pytest

def test_mcp_analyze_data_tool():
    """Test the MCP analyze_data tool."""
    from src.tool_registry.mcps.src.function_app import analyze_data
    
    # Simulate MCP context (how Azure Functions passes data)
    context = json.dumps({
        "arguments": {
            "values": "[10, 20, 30]"
        }
    })
    
    result = json.loads(analyze_data(context))
    
    assert result["count"] == 3
    assert result["mean"] == 20.0
    assert result["status"] != "error"

def test_mcp_tool_handles_invalid_json():
    """Test MCP tool handles malformed input gracefully."""
    context = json.dumps({
        "arguments": {
            "values": "not valid json"
        }
    })
    
    result = json.loads(analyze_data(context))
    assert "error" in result
```

## Fixtures (conftest.py)

```python
import pytest
from pathlib import Path

@pytest.fixture
def sample_numbers():
    """Provide sample data for tests."""
    return [10, 20, 30, 40, 50]

@pytest.fixture
def mcp_context():
    """Create a factory for MCP context objects."""
    def _create_context(arguments: dict):
        return json.dumps({"arguments": arguments})
    return _create_context

@pytest.fixture
def temp_config_dir(tmp_path):
    """Create a temporary directory with config files."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    return config_dir

@pytest.fixture(scope="session")
def azure_function_app():
    """Session-scoped fixture for expensive setup."""
    # Setup that runs once per test session
    app = create_test_app()
    yield app
    # Teardown
    app.cleanup()
```

## Mocking External Services

```python
from unittest.mock import Mock, patch, MagicMock
import pytest

@patch("src.abstractions.azure_functions.requests.post")
def test_function_calls_external_api(mock_post):
    """Test that function calls external API correctly."""
    # Arrange
    mock_post.return_value = Mock(
        status_code=200,
        json=lambda: {"result": "success"}
    )
    
    # Act
    result = call_external_api("test-data")
    
    # Assert
    mock_post.assert_called_once()
    assert result["status"] == "success"

@patch.dict("os.environ", {"API_KEY": "test-key"})
def test_function_uses_env_variable():
    """Test function reads environment variables."""
    result = get_api_key()
    assert result == "test-key"
```

## Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("input_values,expected_mean", [
    ([1, 2, 3], 2.0),
    ([10, 20], 15.0),
    ([100], 100.0),
    ([-5, 5], 0.0),
])
def test_analyze_data_mean_calculation(input_values, expected_mean):
    """Test mean calculation with various inputs."""
    result = analyze_data(input_values)
    assert result["mean"] == expected_mean

@pytest.mark.parametrize("invalid_input,error_message", [
    ([], "No values provided"),
    (None, "Invalid input type"),
    ("not a list", "Expected list"),
])
def test_analyze_data_error_cases(invalid_input, error_message):
    """Test error handling for invalid inputs."""
    with pytest.raises(ValueError, match=error_message):
        analyze_data(invalid_input)
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_azure_functions.py

# Run tests matching pattern
pytest -k "test_analyze"

# Run with coverage
pytest --cov=src --cov-report=html

# Run only fast tests (skip slow/integration)
pytest -m "not slow"
```

## Test Markers

```python
import pytest

@pytest.mark.slow
def test_large_data_processing():
    """This test takes a while."""
    pass

@pytest.mark.integration
def test_azure_connection():
    """Requires actual Azure connection."""
    pass

@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(
    condition=not os.environ.get("AZURE_KEY"),
    reason="Requires AZURE_KEY environment variable"
)
def test_with_azure_credentials():
    pass
```

## pytest.ini Configuration

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
markers =
    slow: marks tests as slow
    integration: marks tests requiring external services
addopts = -v --tb=short
```
