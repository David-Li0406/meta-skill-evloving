# python Research

Research document for the Python language specialist skill. This skill helps developers write idiomatic, type-safe, and maintainable Python code.

## Phase 1: Upstream Survey

### VoltAgent python-pro Subagent

Source: [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-language-specialists/python-pro.md)

#### Identity
"Senior Python developer with mastery of Python 3.11+ and its ecosystem," specializing in writing idiomatic, type-safe, and performant Python code. Expertise spans web development, data science, automation, and system programming with a focus on modern best practices and production-ready solutions.

#### Core Philosophy
"Always prioritize code readability, type safety, and Pythonic idioms while delivering performant and secure solutions."

#### Development Checklist
- [ ] Type hints with 100% coverage for public APIs
- [ ] Ruff linting and formatting compliance
- [ ] mypy strict mode passing
- [ ] Test coverage exceeding 95%
- [ ] Pydantic validation for external data
- [ ] Comprehensive error handling
- [ ] Security scanning passed

#### Specializations Covered

| Area | Topics |
|------|--------|
| Type Safety | Type hints, mypy, generics, Protocols, TypedDict |
| Async | asyncio, coroutines, TaskGroups, structured concurrency |
| Web Frameworks | FastAPI, Django, Flask, Pydantic |
| Data Science | pandas, numpy, polars, data validation |
| Testing | pytest, fixtures, mocking, parametrize, coverage |
| Packaging | pyproject.toml, uv, poetry, modern packaging |
| Performance | profiling, caching, lazy evaluation, slots |

#### Delivery Standards
- Async FastAPI services with 100% type coverage
- 95% test coverage
- Sub-50ms p95 response times
- SQLAlchemy async ORM integration
- No security vulnerabilities

### obra/superpowers

Source: [obra/superpowers](https://github.com/obra/superpowers)

The superpowers framework provides a software development workflow for coding agents with composable skills. While not Python-specific, it includes:
- Support for interactive Python REPLs
- TDD-focused development methodology
- Skills for systematic debugging

Key principles: Red/green TDD, YAGNI (You Aren't Gonna Need It), DRY.

---

## Phase 2: Research Findings

### 1. Official Python Style Guides

#### PEP 8 - Style Guide for Python Code
Source: [peps.python.org/pep-0008](https://peps.python.org/pep-0008/)

Core principles:
- Code is read more often than written — prioritize readability
- Consistency within a project is more important than strict PEP 8 adherence
- Use 4 spaces per indentation level
- Limit lines to 79 characters (72 for docstrings/comments)
- Use blank lines to separate functions and classes

**Naming Conventions:**

| Type | Style | Example |
|------|-------|---------|
| Modules | lowercase_with_underscores | `my_module` |
| Classes | CapWords | `MyClass` |
| Functions | lowercase_with_underscores | `my_function` |
| Constants | UPPERCASE_WITH_UNDERSCORES | `MAX_VALUE` |
| Private | _single_leading_underscore | `_internal` |

**Imports:**
```python
# Good: separate lines, grouped
import os
import sys

from collections import defaultdict
from typing import Optional

from mypackage import mymodule

# Bad: multiple imports on one line
import os, sys
```

#### PEP 257 - Docstring Conventions
Source: [peps.python.org/pep-0257](https://peps.python.org/pep-0257/)

**One-line docstrings:**
```python
def square(x):
    """Return the square of x."""
    return x * x
```

**Multi-line docstrings:**
```python
def complex_function(arg1, arg2):
    """
    Summary line.

    Extended description of function behavior.

    Args:
        arg1: Description of arg1.
        arg2: Description of arg2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When invalid input provided.
    """
    pass
```

Key rules:
- Always use triple double quotes (`"""`)
- Summary line on same line as opening quotes for one-liners
- Blank line after summary for multi-line docstrings
- Document all public modules, functions, classes, and methods

---

### 2. Python Type Hints and mypy

Sources: [docs.python.org/3/library/typing](https://docs.python.org/3/library/typing.html), [mypy.readthedocs.io](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)

#### Modern Type Hint Syntax (Python 3.9+)

```python
# Modern syntax (Python 3.9+)
def process(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Collections
names: list[str] = []
mapping: dict[str, int] = {}
coordinates: tuple[float, float] = (0.0, 0.0)
unique: set[int] = set()

# Optional values
from typing import Optional
name: Optional[str] = None  # equivalent to str | None

# Python 3.10+ union syntax
def get_value() -> int | None:
    return None
```

#### Duck Types for Flexibility

```python
from collections.abc import Iterable, Sequence, Mapping

# Accept broad types, be specific in return
def process_items(items: Iterable[str]) -> list[str]:
    return [item.upper() for item in items]

def get_item(seq: Sequence[int], index: int) -> int:
    return seq[index]

def lookup(data: Mapping[str, int], key: str) -> int | None:
    return data.get(key)
```

#### Type Aliases and TypeVar

```python
from typing import TypeVar, TypeAlias

# Type alias (Python 3.12+)
type Vector = list[float]

# Pre-3.12 alias
Vector: TypeAlias = list[float]

# Generic functions
T = TypeVar('T')

def first(items: list[T]) -> T | None:
    return items[0] if items else None
```

#### Recommended mypy Configuration

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
```

Key practices:
- Use gradual typing — start with critical code paths
- Prefer `Iterable`, `Sequence`, `Mapping` over concrete types for parameters
- Use `unknown` when you don't know the type (avoid `Any`)
- Run mypy in CI with strict mode

---

### 3. Python Linters: Ruff (Modern Choice)

Source: [docs.astral.sh/ruff](https://docs.astral.sh/ruff/)

Ruff is an extremely fast Python linter and formatter written in Rust, 10-100x faster than Flake8 and Black. It can replace Flake8, Black, isort, pydocstyle, pyupgrade, and autoflake.

#### Basic Commands

```bash
ruff check .                 # Lint
ruff check --fix .           # Lint and auto-fix
ruff format .                # Format (Black replacement)
```

#### Recommended Configuration

```toml
# pyproject.toml
[tool.ruff]
line-length = 88
target-version = "py311"
indent-width = 4

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "UP",     # pyupgrade
    "S",      # flake8-bandit (security)
    "C4",     # flake8-comprehensions
    "SIM",    # flake8-simplify
    "ARG",    # flake8-unused-arguments
    "PTH",    # flake8-use-pathlib
    "RUF",    # Ruff-specific rules
]
ignore = [
    "E501",   # line too long (handled by formatter)
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101"]  # Allow assert in tests

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

#### Pre-commit Integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.12.8
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

#### VS Code Integration

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit",
      "source.fixAll": "explicit"
    }
  }
}
```

#### Pylint vs Flake8 vs Ruff

| Tool | Speed | Rule Coverage | Configuration |
|------|-------|---------------|---------------|
| Ruff | Fastest (Rust) | 800+ rules | pyproject.toml |
| Flake8 | Fast | Extensible via plugins | setup.cfg/.flake8 |
| Pylint | Slowest | Most comprehensive | pyproject.toml |

Recommendation: Use Ruff for most projects. Add mypy for type checking. Consider Pylint for legacy codebases requiring deeper analysis.

---

### 4. Common Python Mistakes and Anti-Patterns

Sources: [docs.quantifiedcode.com/python-anti-patterns](https://docs.quantifiedcode.com/python-anti-patterns/), [deepsource.com/blog/8-new-python-antipatterns](https://deepsource.com/blog/8-new-python-antipatterns)

#### Mutable Default Arguments

```python
# Bad: mutable default is shared across calls
def append_to(item, target=[]):
    target.append(item)
    return target

append_to(1)  # [1]
append_to(2)  # [1, 2] — unexpected!

# Good: use None as sentinel
def append_to(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```

#### Empty or Overly Broad Exception Handling

```python
# Bad: swallows all errors
try:
    do_something()
except:
    pass

# Bad: catches too much
try:
    value = data["key"]
except Exception:
    value = default

# Good: catch specific exceptions
try:
    value = data["key"]
except KeyError:
    value = default
```

#### Inconsistent Return Types

```python
# Bad: returns different types
def find_user(user_id):
    user = db.get(user_id)
    if user:
        return user
    return False  # Should return None or raise

# Good: consistent return type
def find_user(user_id) -> User | None:
    return db.get(user_id)

# Or raise an exception
def get_user(user_id) -> User:
    user = db.get(user_id)
    if user is None:
        raise UserNotFoundError(user_id)
    return user
```

#### Wildcard Imports

```python
# Bad: pollutes namespace, hides dependencies
from module import *

# Good: explicit imports
from module import specific_function, SpecificClass
```

#### Using `type()` Instead of `isinstance()`

```python
# Bad: doesn't work with inheritance
if type(obj) == MyClass:
    pass

# Good: works with subclasses
if isinstance(obj, MyClass):
    pass
```

#### Not Using Context Managers

```python
# Bad: may leak resources
f = open("file.txt")
data = f.read()
f.close()

# Good: automatic cleanup
with open("file.txt") as f:
    data = f.read()
```

#### String Concatenation in Loops

```python
# Bad: O(n^2) complexity
result = ""
for s in strings:
    result += s

# Good: O(n) complexity
result = "".join(strings)
```

#### Using Lists When Generators Suffice

```python
# Bad: creates full list in memory
total = sum([x * x for x in range(1000000)])

# Good: generator expression (lazy evaluation)
total = sum(x * x for x in range(1000000))
```

---

### 5. Python Testing with pytest

Sources: [docs.pytest.org](https://docs.pytest.org/en/stable/), [emimartin.me/pytest_best_practices](https://emimartin.me/pytest_best_practices)

#### Basic Test Structure

```python
# test_example.py
import pytest

def test_simple():
    assert 1 + 1 == 2

def test_exception():
    with pytest.raises(ValueError):
        int("not a number")
```

#### Fixtures

```python
import pytest

@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return User(name="Alice", email="alice@example.com")

@pytest.fixture
def db_session():
    """Provide a database session with cleanup."""
    session = create_session()
    yield session
    session.rollback()
    session.close()

def test_user_creation(sample_user, db_session):
    db_session.add(sample_user)
    assert db_session.query(User).count() == 1
```

#### Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default: new for each test
def func_fixture():
    pass

@pytest.fixture(scope="class")     # Shared within a test class
def class_fixture():
    pass

@pytest.fixture(scope="module")    # Shared within a module
def module_fixture():
    pass

@pytest.fixture(scope="session")   # Shared across all tests
def session_fixture():
    pass
```

#### Parametrization

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("world", 5),
    ("", 0),
    ("python", 6),
])
def test_string_length(input, expected):
    assert len(input) == expected

# Multiple parameters
@pytest.mark.parametrize("x,y,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_addition(x, y, expected):
    assert x + y == expected
```

#### Mocking

```python
from unittest.mock import Mock, patch, MagicMock

def test_with_mock():
    mock_api = Mock()
    mock_api.get_data.return_value = {"key": "value"}

    result = process_data(mock_api)

    mock_api.get_data.assert_called_once()

@patch("mymodule.external_api")
def test_with_patch(mock_api):
    mock_api.fetch.return_value = "mocked"

    result = my_function()

    assert result == "mocked"
```

#### Recommended pytest Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = [
    "-ra",                    # Show extra test summary
    "-q",                     # Quiet mode
    "--strict-markers",       # Error on unknown markers
    "--strict-config",        # Error on config issues
    "-x",                     # Stop on first failure (optional)
]
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
]
filterwarnings = [
    "error",                  # Treat warnings as errors
]
```

#### Coverage Configuration

```toml
# pyproject.toml
[tool.coverage.run]
source = ["src"]
branch = true
omit = ["tests/*", "*/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
]
fail_under = 90
```

---

### 6. Python Packaging with pyproject.toml

Sources: [packaging.python.org/guides/writing-pyproject-toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/), [realpython.com/python-pyproject-toml](https://realpython.com/python-pyproject-toml/)

#### Modern Package Structure

```
my_project/
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── core.py
├── tests/
│   ├── __init__.py
│   └── test_core.py
├── pyproject.toml
└── README.md
```

#### Complete pyproject.toml Example

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "1.0.0"
description = "A sample Python package"
readme = "README.md"
license = "MIT"
requires-python = ">=3.11"
authors = [
    { name = "Your Name", email = "you@example.com" }
]
keywords = ["sample", "package"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "requests>=2.28.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
]
docs = [
    "mkdocs>=1.4.0",
]

[project.urls]
Homepage = "https://github.com/you/my-package"
Documentation = "https://my-package.readthedocs.io"

[project.scripts]
my-cli = "my_package.cli:main"

# Tool configurations
[tool.setuptools.packages.find]
where = ["src"]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

#### Dependency Management Tools

| Tool | Lock File | Speed | Features |
|------|-----------|-------|----------|
| pip + pip-tools | requirements.txt | Medium | Standard, widely supported |
| Poetry | poetry.lock | Medium | All-in-one, good DX |
| uv | uv.lock | Fastest | Rust-based, pip-compatible |

**uv Example:**
```bash
# Install uv
pip install uv

# Create virtual environment
uv venv

# Install dependencies
uv pip install -r requirements.txt

# Generate lock file
uv pip compile requirements.in -o requirements.txt
```

---

### 7. Python Idioms and Patterns

Sources: [python-3-patterns-idioms-test.readthedocs.io](https://python-3-patterns-idioms-test.readthedocs.io/en/latest/), [pythondeck.com/understanding_python_idioms](https://pythondeck.com/understanding_python_idioms.html)

#### The Zen of Python

```python
>>> import this
# Key principles:
# - Explicit is better than implicit
# - Simple is better than complex
# - Readability counts
# - Errors should never pass silently
# - There should be one obvious way to do it
```

#### List Comprehensions

```python
# Good: concise and readable
squares = [x**2 for x in range(10)]
evens = [x for x in numbers if x % 2 == 0]

# With multiple conditions
filtered = [x for x in data if x > 0 if x < 100]

# Dict comprehension
word_lengths = {word: len(word) for word in words}

# Set comprehension
unique_lengths = {len(word) for word in words}

# Rule: if comprehension spans multiple lines, use a loop
# Bad: too complex
result = [
    transform(x)
    for x in data
    if condition1(x)
    if condition2(x)
    if condition3(x)
]

# Good: use a loop for complex logic
result = []
for x in data:
    if condition1(x) and condition2(x) and condition3(x):
        result.append(transform(x))
```

#### Context Managers

```python
# Built-in context managers
with open("file.txt") as f:
    data = f.read()

# Multiple context managers
with open("in.txt") as fin, open("out.txt", "w") as fout:
    fout.write(fin.read())

# Custom context manager with contextlib
from contextlib import contextmanager

@contextmanager
def timer(label):
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"{label}: {elapsed:.2f}s")

with timer("operation"):
    do_work()
```

#### Generator Expressions (Lazy Evaluation)

```python
# Generator: lazy, memory-efficient
gen = (x**2 for x in range(1000000))

# Use for large datasets or when you don't need all values
def process_large_file(filename):
    with open(filename) as f:
        for line in f:  # File iterator is lazy
            yield process_line(line)

# Chain generators
filtered = (x for x in data if x > 0)
transformed = (x * 2 for x in filtered)
```

#### EAFP (Easier to Ask Forgiveness than Permission)

```python
# LBYL (Look Before You Leap) - less Pythonic
if key in dictionary:
    value = dictionary[key]
else:
    value = default

# EAFP - more Pythonic
try:
    value = dictionary[key]
except KeyError:
    value = default

# Even better: use dict.get()
value = dictionary.get(key, default)
```

#### Walrus Operator (Python 3.8+)

```python
# Without walrus
match = pattern.search(text)
if match:
    process(match)

# With walrus operator
if (match := pattern.search(text)):
    process(match)

# In while loops
while (line := file.readline()):
    process(line)

# In list comprehensions
results = [y for x in data if (y := expensive_compute(x)) > threshold]
```

#### Dataclasses

```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    email: str
    age: int = 0
    tags: list[str] = field(default_factory=list)

# Immutable dataclass
@dataclass(frozen=True)
class Point:
    x: float
    y: float

# Memory-optimized dataclass (Python 3.10+)
@dataclass(slots=True)
class OptimizedUser:
    name: str
    email: str
```

#### Properties

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius must be non-negative")
        self._radius = value

    @property
    def area(self):
        return 3.14159 * self._radius ** 2
```

---

### 8. Async/Await Best Practices

Sources: [docs.python.org/3/library/asyncio-task](https://docs.python.org/3/library/asyncio-task.html), [realpython.com/async-io-python](https://realpython.com/async-io-python/)

#### Basic Async Patterns

```python
import asyncio

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

asyncio.run(main())
```

#### Concurrent Execution with TaskGroup (Python 3.11+)

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_data(url1))
        task2 = tg.create_task(fetch_data(url2))
        task3 = tg.create_task(fetch_data(url3))

    # All tasks complete when context exits
    results = [task1.result(), task2.result(), task3.result()]
```

#### Semaphores for Rate Limiting

```python
async def fetch_with_limit(url: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        return await fetch_data(url)

async def main():
    semaphore = asyncio.Semaphore(10)  # Max 10 concurrent requests
    tasks = [fetch_with_limit(url, semaphore) for url in urls]
    results = await asyncio.gather(*tasks)
```

#### Key Async Principles

1. **Coroutines vs Tasks**: Awaiting a coroutine doesn't yield to the event loop. Only tasks create concurrency.
2. **No blocking calls**: Don't call blocking I/O in async functions. Use `run_in_executor` for CPU-bound or blocking code.
3. **Context cancellation**: Always handle cancellation gracefully.

```python
async def cancellable_work(ctx: asyncio.CancelledError):
    try:
        while True:
            await asyncio.sleep(1)
            do_work()
    except asyncio.CancelledError:
        cleanup()
        raise
```

---

### 9. Security Best Practices

Sources: [snyk.io/blog/python-security-best-practices-cheat-sheet](https://snyk.io/blog/python-security-best-practices-cheat-sheet/), [corgea.com/Learn/python-security-best-practices](https://corgea.com/Learn/python-security-best-practices-a-comprehensive-guide-for-engineers)

#### Bandit Security Scanner

```bash
# Install
pip install bandit

# Run on codebase
bandit -r src/

# With configuration
bandit -r src/ -c bandit.yaml
```

#### Common Security Issues

**SQL Injection:**
```python
# Bad: string formatting
query = f"SELECT * FROM users WHERE name = '{name}'"

# Good: parameterized queries
cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
```

**Command Injection:**
```python
# Bad: shell=True with user input
subprocess.run(f"ls {user_input}", shell=True)

# Good: use list arguments
subprocess.run(["ls", user_input])
```

**Unsafe Deserialization:**
```python
# Bad: pickle with untrusted data
import pickle
data = pickle.loads(untrusted_data)  # Code execution risk!

# Good: use JSON for untrusted data
import json
data = json.loads(untrusted_data)
```

**Hardcoded Secrets:**
```python
# Bad: hardcoded credentials
API_KEY = "sk-1234567890abcdef"

# Good: environment variables
import os
API_KEY = os.environ["API_KEY"]
```

#### Security Checklist
- [ ] Run Bandit in CI pipeline
- [ ] Use parameterized queries for databases
- [ ] Validate and sanitize all user input
- [ ] Never use `eval()` or `exec()` with user data
- [ ] Keep dependencies updated (`pip-audit`, `safety`)
- [ ] Use environment variables for secrets
- [ ] Avoid `pickle` for untrusted data

---

## Audit Checklist Summary

### Critical (Must Have)
- [ ] Type hints for all public functions and methods
- [ ] mypy passing with strict mode (or core rules enabled)
- [ ] Ruff linting and formatting configured
- [ ] No `# type: ignore` without explanatory comment
- [ ] No bare `except:` clauses
- [ ] No mutable default arguments
- [ ] Tests exist for core functionality

### Important (Should Have)
- [ ] pyproject.toml for all configuration
- [ ] pytest with fixtures and parametrization
- [ ] Test coverage above 80%
- [ ] Docstrings for public APIs (PEP 257)
- [ ] Security scanning with Bandit
- [ ] Pre-commit hooks configured
- [ ] Consistent import ordering (isort/ruff)
- [ ] No wildcard imports

### Recommended (Nice to Have)
- [ ] `@dataclass(slots=True)` for data containers
- [ ] Pydantic for external data validation
- [ ] Generator expressions for large datasets
- [ ] Context managers for resource management
- [ ] `asyncio.TaskGroup` for structured concurrency
- [ ] Lock file for reproducible builds (uv.lock, poetry.lock)
- [ ] Type coverage approaching 100%
- [ ] Walrus operator for cleaner conditionals

---

## Sources

### Official Documentation
- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [PEP 572 - Assignment Expressions](https://peps.python.org/pep-0572/)
- [Python typing module](https://docs.python.org/3/library/typing.html)
- [Python asyncio](https://docs.python.org/3/library/asyncio-task.html)

### Tools
- [Ruff](https://docs.astral.sh/ruff/)
- [mypy](https://mypy.readthedocs.io/)
- [pytest](https://docs.pytest.org/en/stable/)
- [Bandit](https://bandit.readthedocs.io/)
- [uv](https://docs.astral.sh/uv/)

### Best Practices Guides
- [Real Python - PEP 8 Guide](https://realpython.com/python-pep8/)
- [Real Python - Type Hints](https://realpython.com/python-type-checking/)
- [Real Python - pytest](https://realpython.com/pytest-python-testing/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [Python Anti-Patterns](https://docs.quantifiedcode.com/python-anti-patterns/)
- [Snyk Python Security Best Practices](https://snyk.io/blog/python-security-best-practices-cheat-sheet/)

### Style Guides
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

### Upstream
- [VoltAgent python-pro](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-language-specialists/python-pro.md)
- [obra/superpowers](https://github.com/obra/superpowers)
