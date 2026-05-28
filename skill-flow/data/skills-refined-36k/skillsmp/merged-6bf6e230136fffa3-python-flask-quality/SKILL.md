---
name: python-flask-quality
description: Use this skill for quality checks in Python and Flask projects, including testing, static analysis, and code formatting.
---

# Python and Flask Quality Check

This skill provides tools for quality checks in both Python and Flask projects.

## Commands

| Tool    | Command               | Purpose                     |
|---------|----------------------|-----------------------------|
| pytest  | `pytest`             | Run tests                   |
| mypy    | `mypy --strict`      | Type checking               |
| Black   | `black .`            | Code formatting             |
| isort   | `isort .`            | Organize imports            |

## Usage

### Test Execution

```bash
# Basic
pytest

# Verbose
pytest -v

# Specific file
pytest tests/test_user.py  # or tests/test_routes.py for Flask

# Coverage
pytest --cov=src --cov-report=html
```

### Static Analysis

```bash
# Type checking (recommended: strict)
mypy --strict src/

# Linting
ruff check .
ruff check --fix .

# Formatting
black .
isort .

# Check only
black --check .
isort --check-only .
```

## Quality Standards

| Item      | Goal    |
|-----------|---------|
| mypy      | strict mode |
| Coverage   | 90%+    |
| ruff/black | 0 errors |

## Flask-specific Testing

### Fixtures (pytest-flask)

| Fixture        | Purpose                     |
|----------------|-----------------------------|
| `client`       | test_client instance        |
| `app`          | Flask application           |
| `app_context`  | Application context         |

### App Factory Pattern

```python
# conftest.py
import pytest
from myapp import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    yield app

@pytest.fixture
def client(app):
    return app.test_client()
```

### API Test Examples

```python
def test_get_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200
    assert response.json is not None

def test_create_user(client):
    response = client.post('/api/users', json={
        'name': 'Test User',
        'email': 'test@example.com'
    })
    assert response.status_code == 201
```

## Reference

- 詳細: `reference.md`