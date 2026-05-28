# Python Tooling

## Overview

Modern Python tooling landscape:

**Linting + Formatting:**
- **Ruff** - All-in-one linter and formatter (replaces black, isort, flake8, pylint, and more)
- Extremely fast (written in Rust)
- Drop-in replacement for multiple tools

**Type Checking:**
- **mypy** - Static type checker for Python
- **pyright** - Fast alternative from Microsoft

**Testing:**
- **pytest** - Industry standard testing framework

**Package Management:**
- **uv** - Modern, fast package manager (Rust-based)
- **poetry** - Popular alternative with good dependency management

---

## Ruff (Linting + Formatting)

### Installation

**Via uv (recommended):**
```bash
uv tool install ruff
```

**Via pip:**
```bash
pip install ruff
```

**Via Homebrew:**
```bash
brew install ruff
```

### Configuration

**pyproject.toml:**
```toml
[tool.ruff]
line-length = 100
target-version = "py311"

# Enable pycodestyle (E, W), Pyflakes (F), isort (I), and more
lint.select = [
    "E",     # pycodestyle errors
    "W",     # pycodestyle warnings
    "F",     # Pyflakes
    "I",     # isort
    "N",     # pep8-naming
    "UP",    # pyupgrade
    "B",     # flake8-bugbear
    "C4",    # flake8-comprehensions
    "SIM",   # flake8-simplify
    "ARG",   # flake8-unused-arguments
    "PTH",   # flake8-use-pathlib
    "RUF",   # Ruff-specific rules
]

lint.ignore = [
    "E501",  # Line too long (handled by formatter)
]

# Exclude common patterns
extend-exclude = [
    ".venv",
    "venv",
    ".eggs",
    "*.egg",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
]

# Formatting (replaces black)
format.quote-style = "double"
format.indent-style = "space"
format.line-ending = "auto"

# Docstring formatting
format.docstring-code-format = true

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Unused imports in __init__.py
"tests/*" = ["ARG", "S101"]  # Allow assert statements in tests

[tool.ruff.lint.isort]
known-first-party = ["myproject"]
force-single-line = false
lines-after-imports = 2
```

### Usage

**Format code:**
```bash
ruff format .
```

**Check formatting:**
```bash
ruff format --check .
```

**Lint code:**
```bash
ruff check .
```

**Lint and fix:**
```bash
ruff check --fix .
```

**Run both:**
```bash
ruff check --fix . && ruff format .
```

### Pre-commit Integration

**On staged files:**
```bash
ruff check --fix $(git diff --cached --name-only --diff-filter=ACM "*.py")
ruff format $(git diff --cached --name-only --diff-filter=ACM "*.py")
```

---

## Mypy (Type Checking)

### Installation

**Via uv:**
```bash
uv add --dev mypy
```

**Via pip:**
```bash
pip install mypy
```

### Configuration

**pyproject.toml:**
```toml
[tool.mypy]
python_version = "3.11"
strict = true

# Strict options (enable individually if `strict = true` is too aggressive)
warn_unused_configs = true
disallow_any_generics = true
disallow_subclassing_any = true
disallow_untyped_calls = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_return_any = true
no_implicit_reexport = true
strict_equality = true

# Output
show_error_codes = true
show_column_numbers = true
pretty = true

# Per-module options
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = "untyped_package.*"
ignore_missing_imports = true
```

**mypy.ini (alternative):**
```ini
[mypy]
python_version = 3.11
strict = True
warn_unused_configs = True
show_error_codes = True

[mypy-tests.*]
disallow_untyped_defs = False

[mypy-untyped_package.*]
ignore_missing_imports = True
```

### Usage

**Check all files:**
```bash
mypy .
```

**Check specific file:**
```bash
mypy src/module.py
```

**With coverage report:**
```bash
mypy --html-report mypy-report .
```

### Type Stubs

For libraries without type hints:

**Install stubs:**
```bash
uv add --dev types-requests types-redis
```

**Or let mypy find them:**
```bash
mypy --install-types
```

---

## Pytest (Testing)

### Installation

**Via uv:**
```bash
uv add --dev pytest pytest-cov pytest-xdist
```

### Configuration

**pyproject.toml:**
```toml
[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

# Output options
addopts = [
    "-ra",                    # Show all test summary info
    "--strict-config",        # Enforce config errors
    "--strict-markers",       # Enforce marker registration
    "--showlocals",           # Show local variables in tracebacks
    "--tb=short",             # Short traceback format
    "-v",                     # Verbose output
]

# Coverage
[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "**/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

### Usage

**Run all tests:**
```bash
pytest
```

**Run with coverage:**
```bash
pytest --cov=src --cov-report=html --cov-report=term
```

**Run in parallel:**
```bash
pytest -n auto  # Uses pytest-xdist
```

**Run specific test:**
```bash
pytest tests/test_example.py::test_function
```

**Run with markers:**
```bash
pytest -m "not slow"
```

### Example Test

```python
import pytest
from myproject import add

def test_add():
    assert add(2, 2) == 4

def test_add_negative():
    assert add(-1, 1) == 0

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected

@pytest.fixture
def sample_data():
    return {"key": "value"}

def test_with_fixture(sample_data):
    assert sample_data["key"] == "value"
```

---

## Package Management

### UV (Modern, Recommended)

**Installation:**
```bash
brew install uv
```

**Create new project:**
```bash
uv init my-project
cd my-project
```

**Add dependencies:**
```bash
uv add requests pydantic
uv add --dev pytest mypy ruff
```

**Install dependencies:**
```bash
uv sync
```

**Run commands:**
```bash
uv run pytest
uv run python src/main.py
```

**pyproject.toml (generated):**
```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My project"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "mypy>=1.5.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Poetry (Alternative)

**Installation:**
```bash
brew install poetry
```

**Create new project:**
```bash
poetry new my-project
cd my-project
```

**Add dependencies:**
```bash
poetry add requests pydantic
poetry add --group dev pytest mypy ruff
```

**Install dependencies:**
```bash
poetry install
```

**Run commands:**
```bash
poetry run pytest
poetry run python src/main.py
```

---

## Project Structure

**Recommended layout:**
```
my-project/
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_utils.py
├── pyproject.toml
├── README.md
└── .gitignore
```

**pyproject.toml (complete example):**
```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My awesome project"
readme = "README.md"
requires-python = ">=3.11"
authors = [
    {name = "Your Name", email = "you@example.com"}
]
license = {text = "MIT"}
dependencies = [
    "requests>=2.31.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-xdist>=3.3.0",
    "mypy>=1.5.0",
    "ruff>=0.1.0",
]

[project.scripts]
my-cli = "my_project.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["-ra", "--strict-markers", "-v"]

[tool.coverage.run]
source = ["src"]
```

---

## Scripts in pyproject.toml

**Define common tasks:**
```toml
[project.scripts]
# Entry points (installed as CLI commands)
my-cli = "my_project.cli:main"

# Or use a task runner like invoke/just
```

**Alternative: Use Makefile or justfile**

**Makefile:**
```makefile
.PHONY: format lint test validate

format:
	ruff format .

lint:
	ruff check --fix .
	mypy .

test:
	pytest --cov=src

validate: format lint test
	@echo "✅ All checks passed"
```

**justfile:**
```just
format:
    ruff format .

lint:
    ruff check --fix .
    mypy .

test:
    pytest --cov=src --cov-report=html

validate: format lint test
    echo "✅ All checks passed"
```

---

## Monorepo Configuration

For Python monorepos:

**pyproject.toml (workspace root):**
```toml
[tool.ruff]
extend = "ruff.toml"  # Shared config
src = ["packages/*/src"]

[tool.mypy]
mypy_path = "packages/pkg-a/src:packages/pkg-b/src"
```

**packages/pkg-a/pyproject.toml:**
```toml
[project]
name = "pkg-a"
version = "0.1.0"
dependencies = []

[tool.ruff]
extend = "../../ruff.toml"
```

**Use uv workspaces:**
```toml
# Root pyproject.toml
[tool.uv.workspace]
members = ["packages/*"]

[tool.uv.sources]
pkg-a = { workspace = true }
```

---

## Pre-commit Hook Example

**For staged files only:**
```bash
#!/bin/bash
# Get staged Python files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM "*.py")

if [ -n "$STAGED_FILES" ]; then
    # Format
    ruff format $STAGED_FILES

    # Lint and fix
    ruff check --fix $STAGED_FILES

    # Type check
    mypy $STAGED_FILES

    # Re-add formatted files
    git add $STAGED_FILES
fi
```

---

## CI/CD Example

**GitHub Actions:**
```yaml
name: Python CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v1

      - name: Set up Python
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Format check
        run: uv run ruff format --check .

      - name: Lint
        run: uv run ruff check .

      - name: Type check
        run: uv run mypy .

      - name: Test
        run: uv run pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

---

## Quick Reference

**Installation:**
```bash
# Modern stack
brew install uv ruff
uv tool install mypy

# Traditional stack
pip install poetry ruff mypy pytest
```

**Common commands:**
```bash
# Formatting
ruff format .                    # Format code
ruff format --check .            # Check formatting

# Linting
ruff check .                     # Lint code
ruff check --fix .               # Lint and fix

# Type checking
mypy .                           # Type check all

# Testing
pytest                           # Run tests
pytest --cov=src                 # With coverage
pytest -n auto                   # Parallel execution

# All checks
ruff check --fix . && ruff format . && mypy . && pytest
```

**Config files:**
- `pyproject.toml` - All tool configuration
- `ruff.toml` - Alternative Ruff config
- `mypy.ini` - Alternative mypy config
