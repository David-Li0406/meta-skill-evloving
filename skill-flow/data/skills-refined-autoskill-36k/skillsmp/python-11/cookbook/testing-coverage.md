# Testing Cookbook: Coverage and Organization

Coverage reports, exclusions, test layout, markers, and commands.

---
## Generate Coverage Reports

**Problem**: Need to know which lines of code are tested and identify gaps.

**Solution**:
```bash
# Basic coverage
uv run pytest --cov=src

# With missing lines
uv run pytest --cov=src --cov-report=term-missing

# HTML report
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html

# Fail if below threshold
uv run pytest --cov=src --cov-fail-under=80
```

**Tip**: Use `--cov-report=term-missing` during development to quickly see uncovered lines, and HTML reports for detailed analysis.

---

## Configure Coverage Exclusions

**Problem**: Some lines like debug code or type checking shouldn't count against coverage.

**Solution**:
```toml
# pyproject.toml
[tool.coverage.run]
source = ["src"]
branch = true
omit = ["tests/*", "*/__main__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]
fail_under = 80
```

**Tip**: Enable `branch = true` to measure branch coverage, not just line coverage, for more thorough testing.

---

## Organize Tests by Type

**Problem**: Large projects need structure to separate unit, integration, and end-to-end tests.

**Solution**:
```text
tests/
|-- conftest.py           # Shared fixtures
|-- unit/
|   |-- test_entities.py
|   `-- test_services.py
|-- integration/
|   `-- test_api.py
`-- e2e/
    `-- test_workflow.py
```

**Tip**: Place shared fixtures in `conftest.py` at each level to make them available to all tests in that directory and subdirectories.

---

## Mark Tests by Category

**Problem**: Need to selectively run slow tests, integration tests, or exclude certain categories.

**Solution**:
```python
import pytest

@pytest.mark.slow
def test_slow_operation():
    ...

@pytest.mark.integration
def test_database_integration():
    ...

# Run only fast tests
# uv run pytest -m "not slow"

# Run only integration tests
# uv run pytest -m integration
```

**Tip**: Define markers in `pyproject.toml` with descriptions to document what each marker means and enable `--strict-markers`.

---

## Common pytest Commands

**Problem**: Need quick reference for running tests in different ways during development.

**Solution**:
```bash
# Run all tests
uv run pytest

# Verbose output
uv run pytest -v

# Stop on first failure
uv run pytest -x

# Run specific test
uv run pytest tests/test_user.py::TestUser::test_creation

# Run tests matching pattern
uv run pytest -k "user and not slow"

# Show print statements
uv run pytest -s

# Run last failed
uv run pytest --lf

# Parallel execution (requires pytest-xdist)
uv run pytest -n auto
```

**Tip**: Use `pytest -x --lf` during development to quickly iterate: stop on first failure, then rerun only failures on next run.

---
