---
name: python-project-scaffold
description: Scaffold Python projects with uv (package/Python version manager), hatchling (build tool), and pytest (testing). Generates onion architecture structure with domain, infrastructure, application, and presentation layers. Use when users request to create a new Python project, initialize Python codebases, set up Python package structure, or need project templates following clean architecture principles.
---

# Python Project Scaffold

Generate production-ready Python projects with modern tooling and clean architecture.

## Stack

- **uv** - Fast Python package and version manager
- **hatchling** - Modern build backend
- **pytest** - Test framework with coverage
- **pyright** - Static type checker
- **ruff** - Linting and formatting

## Quick Start

Run the scaffold script with project name:

```bash
python scripts/scaffold.py <project-name> [--path <output-dir>]
```

## Project Structure

Generated projects follow onion architecture:

```
project-name/
├── pyproject.toml
├── README.md
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── domain/           # Core business logic (innermost)
│       │   ├── __init__.py
│       │   ├── entities/     # Domain entities
│       │   ├── value_objects/# Immutable value types
│       │   ├── services/     # Domain services
│       │   └── repositories/ # Repository interfaces (ports)
│       ├── application/      # Use cases & orchestration
│       │   ├── __init__.py
│       │   ├── use_cases/    # Application services
│       │   └── dto/          # Data transfer objects
│       ├── infrastructure/   # External adapters (outermost)
│       │   ├── __init__.py
│       │   ├── persistence/  # Repository implementations
│       │   ├── external/     # External API clients
│       │   └── config/       # Configuration
│       └── presentation/     # Entry points
│           ├── __init__.py
│           ├── cli/          # CLI commands
│           └── api/          # REST/GraphQL endpoints
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── unit/
    │   ├── domain/
    │   └── application/
    └── integration/
        ├── infrastructure/
        └── presentation/
```

## Onion Architecture Layers

### Dependency Rule

Dependencies flow inward only:
- **Domain** - Zero external dependencies. Pure Python.
- **Application** - Depends only on Domain.
- **Infrastructure** - Depends on Domain and Application.
- **Presentation** - Depends on all layers.

### Layer Responsibilities

| Layer | Contains | Depends On |
|-------|----------|------------|
| Domain | Entities, Value Objects, Repository Interfaces, Domain Services | Nothing |
| Application | Use Cases, DTOs, Application Services | Domain |
| Infrastructure | Repository Implementations, External APIs, Config | Domain, Application |
| Presentation | CLI, REST API, GraphQL | All |

## Configuration

### pyproject.toml Structure

```toml
[project]
name = "project-name"
version = "0.1.0"
description = ""
readme = "README.md"
requires-python = ">=3.13"
dependencies = []

[dependency-groups]
dev = [
    "pyright>=1.1.407",
    "pytest>=9.0.2",
    "pytest-cov>=6.0",
    "ruff>=0.14.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/project_name"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[tool.pyright]
include = ["src"]
venv = ".venv"
typeCheckingMode = "standard"

[tool.ruff]
src = ["src"]
line-length = 88
```

## Commands After Setup

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Type check
uv run pyright

# Format code
uv run ruff format src tests

# Lint code
uv run ruff check src tests --fix
```

## Layer Guidelines

See `references/` for detailed patterns:
- **Domain Layer**: `references/domain-patterns.md`
- **Application Layer**: `references/application-patterns.md`
- **Infrastructure Layer**: `references/infrastructure-patterns.md`
- **Presentation Layer**: `references/presentation-patterns.md`
