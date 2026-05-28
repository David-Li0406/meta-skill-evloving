---
id: python-poetry-setup
name: "Poetry Project Setup"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Poetry Project Setup

## Overview

Poetry is the modern standard for Python dependency management, providing deterministic builds through lock files, virtual environment management, and streamlined publishing. This methodology covers project setup, dependency management, and CI/CD integration.

## When to Use

- Starting any new Python project
- Managing complex dependency trees
- Projects requiring reproducible builds
- Publishing packages to PyPI
- Monorepo Python projects

## Key Principles

1. **Lock everything** - Always commit poetry.lock for reproducibility
2. **Separate dev dependencies** - Keep production deps minimal
3. **Use dependency groups** - Organize by purpose (dev, test, docs)
4. **Pin versions** - Explicit versions for critical dependencies
5. **Virtual environments** - Isolated per project

## Best Practices

### Project Initialization

```bash
# Create new project
poetry new my-project
cd my-project

# Or initialize in existing directory
cd existing-project
poetry init

# Project structure created:
# my-project/
# ├── pyproject.toml
# ├── README.md
# ├── my_project/
# │   └── __init__.py
# └── tests/
#     └── __init__.py
```

### pyproject.toml Configuration

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "A production-ready Python project"
authors = ["Your Name <you@example.com>"]
readme = "README.md"
license = "MIT"
repository = "https://github.com/you/my-project"
documentation = "https://my-project.readthedocs.io"
keywords = ["api", "web"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
packages = [{include = "my_project", from = "src"}]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.109.0"
uvicorn = {extras = ["standard"], version = "^0.27.0"}
pydantic = "^2.6.0"
sqlalchemy = {extras = ["asyncio"], version = "^2.0.25"}
asyncpg = "^0.29.0"
httpx = "^0.26.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
pytest-asyncio = "^0.23.0"
pytest-cov = "^4.1.0"
mypy = "^1.8.0"
black = "^24.1.0"
isort = "^5.13.0"
ruff = "^0.1.14"

[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
mkdocs = "^1.5.0"
mkdocs-material = "^9.5.0"

[tool.poetry.scripts]
my-cli = "my_project.cli:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

# Tool configurations
[tool.black]
line-length = 88
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --tb=short"

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W", "UP"]
ignore = ["E501"]
```

### Dependency Management

```bash
# Add production dependency
poetry add fastapi uvicorn sqlalchemy

# Add with extras
poetry add sqlalchemy[asyncio]
poetry add uvicorn[standard]

# Add dev dependency
poetry add --group dev pytest mypy black

# Add optional group
poetry add --group docs mkdocs

# Add from git
poetry add git+https://github.com/user/repo.git

# Add with version constraints
poetry add "fastapi>=0.100.0,<1.0.0"
poetry add "pydantic@^2.0"  # Same as >=2.0.0,<3.0.0

# Remove dependency
poetry remove httpx

# Update dependencies
poetry update              # All dependencies
poetry update fastapi      # Single package
poetry update --dry-run    # Preview changes

# Show dependency tree
poetry show --tree
poetry show --outdated
```

### Virtual Environment

```bash
# Create/activate virtual environment
poetry install              # Install all deps, create venv if needed
poetry shell               # Activate venv in new shell

# Run command in venv
poetry run python script.py
poetry run pytest
poetry run python -m my_project

# Environment info
poetry env info
poetry env info --path

# Use specific Python version
poetry env use python3.11
poetry env use /usr/bin/python3.12

# Remove environment
poetry env remove python3.11
poetry env remove --all

# Configure venv in project directory
poetry config virtualenvs.in-project true
```

### Lock File Management

```bash
# Generate/update lock file
poetry lock

# Install from lock file (production)
poetry install --no-dev

# Install only specific groups
poetry install --only main
poetry install --with dev,docs

# Export to requirements.txt
poetry export -f requirements.txt --output requirements.txt
poetry export -f requirements.txt --output requirements-dev.txt --with dev

# Check lock file is up to date
poetry check
```

### Project Structure

```
my-project/
├── pyproject.toml          # Project configuration
├── poetry.lock             # Locked dependencies (commit this!)
├── README.md
├── .env.example
├── .gitignore
│
├── src/                    # Source directory
│   └── my_project/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── models/
│       ├── services/
│       └── api/
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_*.py
│
├── docs/
│   └── index.md
│
└── Dockerfile
```

### Docker Integration

```dockerfile
# Dockerfile
FROM python:3.11-slim AS builder

WORKDIR /app

# Install poetry
RUN pip install poetry==1.7.1

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Export to requirements.txt (faster in Docker)
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Run application
CMD ["python", "-m", "my_project.main"]
```

### CI/CD Integration

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install Poetry
        uses: snok/install-poetry@v1
        with:
          version: 1.7.1
          virtualenvs-create: true
          virtualenvs-in-project: true

      - name: Load cached venv
        id: cached-poetry-dependencies
        uses: actions/cache@v4
        with:
          path: .venv
          key: venv-${{ runner.os }}-${{ matrix.python-version }}-${{ hashFiles('**/poetry.lock') }}

      - name: Install dependencies
        if: steps.cached-poetry-dependencies.outputs.cache-hit != 'true'
        run: poetry install --no-interaction

      - name: Run linting
        run: |
          poetry run black --check src/ tests/
          poetry run isort --check src/ tests/
          poetry run mypy src/

      - name: Run tests
        run: poetry run pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

### Publishing to PyPI

```bash
# Build package
poetry build

# Configure PyPI token
poetry config pypi-token.pypi your-token-here

# Publish to PyPI
poetry publish

# Publish to private repository
poetry config repositories.private https://pypi.example.com/simple/
poetry publish -r private

# Bump version
poetry version patch  # 0.1.0 -> 0.1.1
poetry version minor  # 0.1.1 -> 0.2.0
poetry version major  # 0.2.0 -> 1.0.0
```

## Anti-patterns

### Avoid: Not Committing Lock File

```bash
# BAD - .gitignore
poetry.lock

# GOOD - always commit lock file
# poetry.lock should be in version control
```

### Avoid: Installing Without Lock

```bash
# BAD - non-deterministic
poetry install --no-lock

# GOOD - always use lock
poetry install
```

### Avoid: Mixing pip and Poetry

```bash
# BAD - breaks Poetry's tracking
pip install some-package

# GOOD - use Poetry
poetry add some-package
```

## References

- [Poetry Documentation](https://python-poetry.org/docs/)
- [PEP 517 - Build System](https://peps.python.org/pep-0517/)
- [PEP 518 - pyproject.toml](https://peps.python.org/pep-0518/)
- [Poetry GitHub](https://github.com/python-poetry/poetry)
