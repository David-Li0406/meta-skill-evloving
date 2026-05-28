---
name: python-flask-quality
description: Use this skill when you need to perform quality checks on Python or Flask projects using tools like pytest, mypy, and Black.
---

# Python and Flask Quality Check

This skill provides a comprehensive quality check for both Python and Flask projects.

## Commands

| Tool    | Command                  | Purpose                     |
|---------|-------------------------|-----------------------------|
| pytest  | `pytest`                | Run tests                   |
| mypy    | `mypy --strict`         | Type checking               |
| Black   | `black .`               | Code formatting             |
| isort   | `isort .`               | Organize imports            |

## Usage

### Running Tests

```bash
# Basic
pytest

# Verbose
pytest -v

# Specific file
pytest tests/test_user.py  # For Python
pytest tests/test_routes.py  # For Flask

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

# Code formatting
black .
isort .

# Check only
black --check .
isort --check-only .
```

## Quality Standards

| Item     | Goal   |
|----------|--------|
| mypy     | strict mode |
| Coverage | 90%+   |
| Linting  | No errors |

## Flask-specific Testing

### Fixtures (pytest-flask)

| Fixture        | Purpose                      |
|----------------|------------------------------|
| `client`       | test_client instance         |
| `app`          | Flask application            |
| `app_context`  | Application context          |

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

## Reference

- For more details, refer to `reference.md`.