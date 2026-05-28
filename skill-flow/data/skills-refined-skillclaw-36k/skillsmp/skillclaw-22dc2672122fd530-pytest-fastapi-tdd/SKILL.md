---
name: pytest-fastapi-tdd
description: Use this skill when you want to implement Test-Driven Development (TDD) for FastAPI applications using pytest.
---

# Skill body

## Overview

This skill combines the powerful features of pytest with Test-Driven Development (TDD) patterns specifically tailored for FastAPI applications. It guides you through writing tests before implementation, ensuring robust and maintainable code.

## Key Features
- Integration with FastAPI for seamless testing
- TDD cycle: RED, GREEN, REFACTOR
- Support for async testing with pytest-asyncio
- Mocking capabilities for database operations

## Installation

To get started, install pytest and the necessary plugins:

```bash
pip install pytest pytest-asyncio httpx
```

## The TDD Cycle

1. **RED**: Write a failing test
   - Ensure the test fails initially to confirm it tests something.
   - Keep the test minimal and focused on one behavior.

2. **GREEN**: Write minimal code to pass
   - Implement just enough code to make the test pass.
   - Avoid optimization at this stage.

3. **REFACTOR**: Improve the code
   - Clean up the code while ensuring all tests remain passing.
   - Focus on DRY principles, readability, and performance.

## Basic Testing Patterns

### Setting Up a Test Client

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)
```

### Testing Async Endpoints

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_create_todo_async(client):
    """Test async endpoint with httpx AsyncClient."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/todos/",
            json={"title": "Test Todo", "description": "Test"},
            headers={"Authorization": "Bearer fake_token"}
        )

    assert response.status_code == 201
    assert response.json()["title"] == "Test Todo"
```

### Mocking Database Operations

```python
from unittest.mock import patch, AsyncMock, MagicMock

@patch("app.routers.todo.request.app.todo")
def test_get_todos(mock_collection, client):
    """Mock MongoDB find() with cursor."""
    mock_cursor = MagicMock()
    mock_cursor.to_list = AsyncMock(return_value=[{"title": "Test Todo"}])
    mock_collection.find.return_value = mock_cursor

    response = client.get("/todos/")
    assert response.status_code == 200
    assert response.json() == [{"title": "Test Todo"}]
```

## Running Tests

To discover and run all tests, use:

```bash
pytest
```

For verbose output, run:

```bash
pytest -v
```

This skill provides a comprehensive approach to testing FastAPI applications using pytest, ensuring that you can confidently implement features with TDD principles.