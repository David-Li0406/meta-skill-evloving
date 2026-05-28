# Python-Specific Rules

These rules apply when reviewing **Python** (`.py`, `.pyi`) files.

---

## 1. Type Hints

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| Function signatures | Warning | Add type hints to all public functions |
| Return types | Warning | Include return type annotations |
| Use modern syntax | Info | `list[str]` not `List[str]` (Python 3.9+) |
| Optional types | Warning | `str \| None` or `Optional[str]` for nullable |
| TypedDict for dicts | Info | Prefer TypedDict over `dict[str, Any]` |
| Dataclasses | Info | Prefer over plain classes for data containers |

### Check For

```python
# BAD: No type hints
def process(data):
    return data['value']

# GOOD: Typed function
def process(data: dict[str, Any]) -> str:
    return data['value']

# BAD: Old typing syntax (pre-3.9)
from typing import List, Dict, Optional
def get_names() -> List[str]: ...

# GOOD: Modern syntax (3.9+)
def get_names() -> list[str]: ...

# BAD: dict with Any
def get_user() -> dict[str, Any]: ...

# GOOD: TypedDict
class User(TypedDict):
    id: int
    name: str
    email: str | None

def get_user() -> User: ...

# GOOD: Dataclass
@dataclass
class User:
    id: int
    name: str
    email: str | None = None
```

### Red Flags

- Public functions without type hints
- `Any` used excessively
- `# type: ignore` comments (investigate why)
- Mixing old and new typing syntax

---

## 2. Pythonic Idioms

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| List comprehensions | Info | Prefer over map/filter for simple cases |
| Context managers | Warning | Use `with` for resource management |
| Unpacking | Info | Use tuple unpacking where appropriate |
| f-strings | Info | Prefer over .format() or % |
| Enumerate | Info | Use instead of range(len()) |
| Dictionary methods | Info | Use .get(), .setdefault(), .items() |

### Check For

```python
# BAD: Manual loop for transformation
result = []
for item in items:
    if item.active:
        result.append(item.name)

# GOOD: List comprehension
result = [item.name for item in items if item.active]

# BAD: Manual file handling
f = open('file.txt')
data = f.read()
f.close()

# GOOD: Context manager
with open('file.txt') as f:
    data = f.read()

# BAD: Index-based iteration
for i in range(len(items)):
    print(i, items[i])

# GOOD: Enumerate
for i, item in enumerate(items):
    print(i, item)

# BAD: String formatting
"Hello %s" % name
"Hello {}".format(name)

# GOOD: f-string
f"Hello {name}"

# BAD: Key check then access
if key in d:
    value = d[key]
else:
    value = default

# GOOD: .get()
value = d.get(key, default)
```

### Red Flags

- `range(len(...))` pattern
- String concatenation with `+` in loops
- Manual try/finally for cleanup (use context manager)
- Mutable default arguments: `def f(items=[]):`

---

## 3. Async/Await

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| Consistency | Warning | Don't mix sync and async in same module |
| Await all coroutines | Critical | Never leave coroutines unawaited |
| Use gather | Info | `asyncio.gather()` for parallel async ops |
| Async context managers | Info | `async with` for async resources |
| Cleanup | Warning | Ensure proper cleanup of async resources |

### Check For

```python
# BAD: Unawaited coroutine
async def main():
    fetch_data()  # Returns coroutine, doesn't execute!

# GOOD: Awaited
async def main():
    await fetch_data()

# BAD: Sequential when parallel possible
user = await get_user()
orders = await get_orders()

# GOOD: Parallel
user, orders = await asyncio.gather(get_user(), get_orders())

# BAD: sync call in async function
async def process():
    time.sleep(1)  # Blocks event loop!

# GOOD: async sleep
async def process():
    await asyncio.sleep(1)

# GOOD: Async context manager
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.json()
```

### Red Flags

- Coroutines called without `await`
- `time.sleep()` in async code (use `asyncio.sleep()`)
- Blocking I/O in async functions
- Missing `async` keyword on functions that await

---

## 4. Imports

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| Absolute imports | Info | Prefer over relative imports |
| No star imports | Warning | `from module import *` hides origins |
| Import order | Info | stdlib, third-party, local (use isort) |
| Lazy imports | Info | For heavy modules, import inside functions |
| Circular imports | Warning | Avoid; restructure if needed |

### Check For

```python
# BAD: Star import
from utils import *

# GOOD: Explicit imports
from utils import validate_email, format_date

# BAD: Deep relative import
from ...core.utils.helpers import validate

# GOOD: Absolute import
from myproject.core.utils.helpers import validate

# GOOD: Import order (PEP 8)
import os
import sys

import requests
import pandas as pd

from myproject.utils import helper
from myproject.models import User

# GOOD: Lazy import for heavy module
def generate_report():
    import pandas as pd  # Only loaded when function called
    return pd.DataFrame(data)
```

### Red Flags

- `from x import *` anywhere
- Circular import errors at runtime
- Mixing relative and absolute imports
- Unused imports (use a linter)

---

## 5. Structure

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| `__init__.py` | Info | Required for packages (can be empty) |
| `if __name__ == "__main__"` | Warning | Guard script execution |
| Module docstrings | Info | Describe module purpose |
| Class organization | Info | Public methods first, private after |
| Constants at top | Info | UPPER_CASE constants after imports |

### Check For

```python
# GOOD: Module structure
"""
User authentication module.

Handles login, logout, and session management.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from myproject.db import get_connection

# Constants
MAX_LOGIN_ATTEMPTS = 5
SESSION_TIMEOUT = 3600

# Public functions
def login(username: str, password: str) -> User | None:
    ...

def logout(user: User) -> None:
    ...

# Private helpers
def _validate_password(password: str) -> bool:
    ...

# Script guard
if __name__ == "__main__":
    main()
```

### Red Flags

- Code at module level that runs on import
- Missing `if __name__ == "__main__"` in scripts
- Private functions (`_func`) called from outside module
- Very long modules (>500 lines, consider splitting)

---

## 6. Common Patterns

### Prefer

```python
# Walrus operator (3.8+) for assign-and-test
if (match := pattern.search(text)):
    print(match.group())

# Structural pattern matching (3.10+)
match command:
    case ["quit"]:
        return
    case ["load", filename]:
        load(filename)

# Pydantic for validation
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int = Field(ge=0)

# Path over os.path
from pathlib import Path
config = Path.home() / ".config" / "app.json"

# Exceptions as context managers
from contextlib import suppress
with suppress(FileNotFoundError):
    os.remove(temp_file)
```

### Avoid

```python
# Bare except
try:
    ...
except:  # Catches SystemExit, KeyboardInterrupt!
    pass

# Use specific exceptions
try:
    ...
except ValueError:
    pass

# Mutable default arguments
def append(item, lst=[]):  # Bug! Same list reused
    lst.append(item)
    return lst

# Use None instead
def append(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

# os.path when pathlib works
os.path.join(base, "subdir", "file.txt")
# Use: Path(base) / "subdir" / "file.txt"

# String concatenation in loops
result = ""
for s in strings:
    result += s  # O(n²)!
# Use: result = "".join(strings)
```

---

## Summary Checklist

Before completing Python review:

- [ ] Type hints on public functions and methods
- [ ] Pythonic idioms used (comprehensions, f-strings, enumerate)
- [ ] Context managers for resource cleanup
- [ ] All coroutines properly awaited
- [ ] No star imports
- [ ] Import order follows PEP 8 / isort
- [ ] `if __name__ == "__main__"` guard on scripts
- [ ] No mutable default arguments
- [ ] Modern syntax (3.9+ types, pathlib, etc.)
