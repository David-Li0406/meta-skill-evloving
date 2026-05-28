---
name: pytest-testing
description: Use this skill when you need to write comprehensive tests with pytest, including unit, integration, and end-to-end tests, utilizing fixtures, mocking, and async patterns.
---

# Pytest Testing Skill

This skill provides a comprehensive guide for writing maintainable tests using pytest, covering various test types, patterns, and best practices.

## Core Philosophy

| Principle | Application |
|-----------|-------------|
| **AAA Pattern** | Arrange-Act-Assert for every test |
| **Behavior over Implementation** | Test what code does, not how |
| **Isolation** | Tests must be independent |
| **Fast Tests** | Mock I/O, minimize database hits |
| **Descriptive Names** | Test name explains the scenario |
| **Coverage** | Test happy paths AND edge cases |

## Test Type Taxonomy

| Test Type | What It Tests | Location |
|-----------|---------------|----------|
| **Unit Tests** | Single function/class in isolation | `tests/unit/` |
| **Backend-Integration Tests** | Service orchestration, real DB/Redis | `tests/integration/` |
| **E2E Tests** | Browser + DB verification | `tests/e2e/` |
| **Smoke Tests** | Critical path quick validation | Marker-based (`-m smoke`) |

## Project Structure

```
tests/
├── conftest.py          # Shared fixtures
├── unit/                # Unit tests (fast, isolated)
│   ├── test_models.py
│   └── test_services.py
├── integration/         # Integration tests (real dependencies)
│   └── test_api.py
└── e2e/                 # E2E tests
    └── test_ui.py
```

## Running Tests

```bash
# All quality gates
just check

# Backend tests with coverage
docker compose exec backend pytest /tests/unit/ /tests/integration/ --cov=app --cov-report=term-missing

# Specific test file
docker compose exec backend pytest /tests/integration/api/test_signal_chains.py -v

# E2E tests (runs on HOST)
just test-e2e-quick      # Quick E2E (< 1 min, for commits)
just test-e2e-full       # Full E2E (for pre-PR)
pytest -m e2e tests/e2e/  # All E2E
```

## Essential Patterns

### Basic Test Structure

```python
import pytest
from myapp.services import UserService

class TestUserService:
    """Tests for UserService."""

    def test_create_user_with_valid_data(self, user_service):
        # Arrange
        user_data = {"email": "test@example.com", "name": "Test User"}

        # Act
        result = user_service.create(user_data)

        # Assert
        assert result.email == "test@example.com"
        assert result.id is not None
```

### Fixtures

```python
# conftest.py
import pytest
from myapp.database import get_db
from myapp.services import UserService

@pytest.fixture
def db():
    """Provide a clean database session."""
    session = get_db()
    yield session
    session.rollback()

@pytest.fixture
def user_service(db):
    """Provide UserService instance."""
    return UserService(db)
```

### Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("input_email,expected_valid", [
    ("valid@example.com", True),
    ("invalid-email", False),
])
def test_email_validation(input_email, expected_valid):
    from myapp.validators import is_valid_email
    assert is_valid_email(input_email) == expected_valid
```

### Mocking

```python
from unittest.mock import Mock, patch

def test_send_email_calls_smtp(user_service):
    with patch("myapp.services.smtp_client") as mock_smtp:
        mock_smtp.send.return_value = True
        user_service.send_welcome_email("test@example.com")
        mock_smtp.send.assert_called_once_with(
            to="test@example.com",
            subject="Welcome!",
        )
```

### Async Testing

```python
import pytest

@pytest.mark.asyncio
async def test_async_fetch_user(user_service):
    user_id = 1
    user = await user_service.get_by_id(user_id)
    assert user.id == user_id
```

## Coverage

Target: 80%+

```bash
docker compose exec backend pytest /tests/unit/ /tests/integration/ --cov=app --cov-fail-under=80 --cov-report=html
```

## Quality Checklist

- [ ] AAA pattern (Arrange-Act-Assert) in every test
- [ ] Descriptive test names explaining the scenario
- [ ] Fixtures for common setup
- [ ] Parametrized tests for multiple inputs
- [ ] Mocks for external dependencies
- [ ] Happy path tested
- [ ] Error cases tested
- [ ] Edge cases covered
- [ ] Async tests use `@pytest.mark.asyncio`
- [ ] No test interdependencies
- [ ] Coverage >90%

## Related

- [Testing Methodology](https://github.com/krazyuniks/guitar-tone-shootout/wiki/Testing-Methodology) - Full methodology (GitHub Wiki)