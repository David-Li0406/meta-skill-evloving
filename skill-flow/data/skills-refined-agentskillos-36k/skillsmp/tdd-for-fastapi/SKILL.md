---
name: TDD for FastAPI
description: Test-Driven Development patterns for FastAPI with pytest
---

# TDD for FastAPI/pytest

This skill provides patterns for writing tests BEFORE implementation in FastAPI projects using pytest.

## The TDD Cycle

```
┌─────────────────────────────────────────────────────────┐
│  1. RED: Write a failing test                           │
│     - Test must fail initially (proves it tests something)│
│     - Test should be minimal, focused on one behavior   │
│                                                         │
│  2. GREEN: Write minimal code to pass                   │
│     - Only enough code to make the test pass            │
│     - Don't optimize yet                                │
│                                                         │
│  3. REFACTOR: Improve the code                          │
│     - Clean up while keeping tests green                │
│     - DRY, readability, performance                     │
└─────────────────────────────────────────────────────────┘
```

---

## FastAPI Testing Patterns

### Basic Test Structure

```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_db():
    """Mock MongoDB collection."""
    mock = AsyncMock()
    return mock
```

### Testing Async Endpoints

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_create_todo_async():
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

### Mocking MongoDB Operations

```python
from unittest.mock import patch, AsyncMock, MagicMock
from bson import ObjectId


@patch("app.routers.todo.request.app.todo")
def test_get_todos(mock_collection, client):
    """Mock MongoDB find() with cursor."""
    # Create mock cursor that behaves like MongoDB cursor
    mock_cursor = MagicMock()
    mock_cursor.to_list = AsyncMock(return_value=[
        {"_id": ObjectId(), "title": "Todo 1", "user_id": "test_user"},
        {"_id": ObjectId(), "title": "Todo 2", "user_id": "test_user"},
    ])
    mock_collection.find.return_value = mock_cursor

    response = client.get("/todos/")

    assert response.status_code == 200
    assert len(response.json()) == 2
```

### Testing Authentication

```python
import pytest
from app.routers.auth import create_access_token, verify_password


class TestAuthentication:
    """TDD tests for authentication flow."""

    def test_password_verification_correct(self):
        """GREEN: Correct password should verify."""
        hashed = "$argon2id$..."  # Pre-computed hash
        assert verify_password("correct_password", hashed) is True

    def test_password_verification_incorrect(self):
        """RED first: Wrong password should fail."""
        hashed = "$argon2id$..."
        assert verify_password("wrong_password", hashed) is False

    def test_access_token_contains_user_id(self):
        """Token should contain user_id in payload."""
        token = create_access_token(user_id="user123", username="testuser")
        # Decode and verify payload
        # Note: decode_token would be a project utility you implement
        payload = decode_token(token)
        assert payload["user_id"] == "user123"
```

### Testing Error Cases

```python
def test_todo_not_found_returns_404(client, mock_db):
    """Specific error case for non-existent todo."""
    mock_db.find_one.return_value = None

    response = client.get("/todos/nonexistent_id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_unauthorized_returns_401(client):
    """Missing token should return 401."""
    response = client.get("/todos/")  # No Authorization header

    assert response.status_code == 401
```

### Testing with Fixtures (conftest.py patterns)

```python
# conftest.py
import pytest
from unittest.mock import patch, AsyncMock


@pytest.fixture
def authenticated_client(client):
    """Client with valid auth token."""
    with patch("app.main.decode_token") as mock_decode:
        mock_decode.return_value = {
            "user_id": "test_user_id",
            "username": "testuser"
        }
        yield client


@pytest.fixture
def mock_user_collection():
    """Pre-configured user collection mock."""
    mock = AsyncMock()
    mock.find_one.return_value = {
        "_id": ObjectId(),
        "username": "testuser",
        "email": "test@example.com"
    }
    return mock
```

---

## TDD Workflow for New Endpoint

### Example: Adding a "mark complete" endpoint

**Step 1: RED - Write failing test first**

```python
# app/tests/routers/test_todo.py

def test_mark_todo_complete(authenticated_client, mock_db):
    """PATCH /todos/{id}/complete should mark todo as completed."""
    todo_id = "507f1f77bcf86cd799439011"

    # Mock the update operation
    mock_db.update_one.return_value = MagicMock(modified_count=1)
    mock_db.find_one.return_value = {
        "_id": ObjectId(todo_id),
        "title": "Test",
        "completed": True  # After update
    }

    response = authenticated_client.patch(f"/todos/{todo_id}/complete")

    assert response.status_code == 200
    assert response.json()["completed"] is True
```

Run: `pytest app/tests/routers/test_todo.py::test_mark_todo_complete -v`
Expected: **FAILED** (endpoint doesn't exist yet)

**Step 2: GREEN - Implement minimal code**

```python
# app/routers/todo.py

@router.patch("/{todo_id}/complete")
async def mark_complete(todo_id: str, request: Request):
    """Mark a todo as completed."""
    result = await request.app.todo.update_one(
        {"_id": ObjectId(todo_id), "user_id": request.state.user_id},
        {"$set": {"completed": True}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo = await request.app.todo.find_one({"_id": ObjectId(todo_id)})
    return todo
```

Run: `pytest app/tests/routers/test_todo.py::test_mark_todo_complete -v`
Expected: **PASSED**

**Step 3: REFACTOR - Add edge case tests, clean up**

```python
def test_mark_nonexistent_todo_returns_404(authenticated_client, mock_db):
    """Cannot complete a todo that doesn't exist."""
    mock_db.update_one.return_value = MagicMock(modified_count=0)

    response = authenticated_client.patch("/todos/nonexistent/complete")

    assert response.status_code == 404
```

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Test passes without implementation | Make test more specific, check exact values |
| Mock not applied correctly | Use full import path in `@patch()` |
| Async tests not running | Add `@pytest.mark.asyncio` decorator |
| ObjectId comparison fails | Compare string representations |
| Test depends on execution order | Use fixtures for isolation |

---

## Testing Checklist

Before marking tests complete:

- [ ] Tests fail without implementation (Red verified)
- [ ] Tests pass with implementation (Green verified)
- [ ] Edge cases covered (nulls, empty, invalid input)
- [ ] Error responses tested (4xx, 5xx)
- [ ] Auth/permission tests if applicable
- [ ] Mocks properly reset between tests

---

*Skill created: 2026-01-18*
