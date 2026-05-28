# Code Quality Tools Reference

## Recommended Setup

```toml
# pyproject.toml

[tool.black]
line-length = 88
target-version = ['py39', 'py310', 'py311', 'py312']

[tool.isort]
profile = "black"
known_django = ["django", "rest_framework"]
sections = ["FUTURE", "STDLIB", "DJANGO", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]
exclude = [".git", "__pycache__", "migrations"]

[tool.mypy]
python_version = "3.10"
plugins = ["mypy_django_plugin.main"]
ignore_missing_imports = true
```

## Pre-commit Config

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.4.2
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.1.0
    hooks:
      - id: flake8
```

## Exception Handling

### NEVER use bare except

```python
# WRONG - hides all errors including bugs
try:
    do_something()
except:  # NEVER!
    pass

try:
    do_something()
except Exception:  # AVOID - too broad
    logger.error("Error occurred")
```

### CORRECT - catch specific exceptions

```python
# Django ORM
try:
    obj = MyModel.objects.get(pk=pk)
except MyModel.DoesNotExist:
    raise NotFoundError(f"Object {pk} not found")

# Multiple exceptions
try:
    validate_data(data)
except (ValidationError, ValueError) as e:
    return Response({'error': str(e)}, status=400)

# HTTP requests
import requests

try:
    response = requests.post(url, json=data, timeout=30)
    response.raise_for_status()
except requests.Timeout:
    logger.warning("Request timeout")
    raise ServiceTimeoutError("External service timeout")
except requests.HTTPError as e:
    logger.error(f"HTTP error: {e.response.status_code}")
    raise ExternalServiceError(f"Service returned {e.response.status_code}")
```

## Pre-commit Checklist

Before committing code:

- [ ] Type hints on all functions
- [ ] Imports organized (isort)
- [ ] Code formatted (black)
- [ ] No linting errors (flake8)
- [ ] Specific exception handling
- [ ] Tests written and passing
- [ ] Migrations created if models changed
- [ ] Documentation updated if API changed
