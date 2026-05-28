---
name: fastapi-project-setup
description: Use this skill when you want to initialize a new FastAPI project with the necessary configurations and tooling.
---

# FastAPI Project Setup

## Overview

This skill covers initializing a new FastAPI project with the `uv` package manager, proper project configuration, and tooling setup.

## Step 1: Initialize Project with uv

```bash
uv init
```

## Step 2: Create `pyproject.toml`

```toml
[project]
name = "your-project-name"
version = "0.1.0"
description = "FastAPI backend application"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.7.0",
    "sqlalchemy[asyncio]>=2.0.36",
    "asyncpg>=0.30.0",
    "alembic>=1.14.0",
    "fastapi-pagination>=0.12.33",
    "fastapi-filter>=2.0.0",
    "python-json-logger>=3.2.1",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.8.0",
    "pytest>=8.3.0",
    "pytest-asyncio>=0.25.0",
    "httpx>=0.28.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/app"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
testpaths = ["tests"]
pythonpath = ["src"]
```

## Step 3: Create `.python-version`

```
3.12
```

## Step 4: Create `ruff.toml`

```toml
# Ruff configuration for FastAPI project

# Target Python 3.12
target-version = "py312"

# Line length
line-length = 100

# Exclude directories
exclude = [
    ".git",
    ".ruff_cache",
    ".venv",
    "venv",
    "__pycache__",
    "alembic/versions",
]

[lint]
# Enable rules
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "ARG",    # flake8-unused-arguments
    "SIM",    # flake8-simplify
    "TCH",    # flake8-type-checking
    "PTH",    # flake8-use-pathlib
    "ERA",    # eradicate (commented-out code)
    "PL",     # Pylint
    "RUF",    # Ruff-specific rules
]

# Ignore specific rules
ignore = [
    "E501",   # line too long (handled by formatter)
    "B008",   # do not perform function calls in argument defaults (needed for Depends)
    "PLR0913", # too many arguments
    "PLR2004", # magic value comparison
]

# Allow autofix for all enabled rules
fixable = ["ALL"]
unfixable = []

[lint.per-file-ignores]
# Tests can have unused arguments (fixtures)
```