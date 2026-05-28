# Python Language Rules

Detailed reference from Google Python Style Guide Section 2. For quick lookup, see the main [SKILL.md](SKILL.md).

## 2.1 Lint

Run ruff on all code. Suppress warnings with line-level comments using rule codes, and document the reason.

```python
# Good
x = some_function()  # noqa: F841 - assigned for side effect, value unused

# Bad
x = some_function()  # noqa
```

## 2.2 Imports

Use `import x` for packages/modules. Use `from x import y` for specific items within modules. Use `import y as z` only with standard abbreviations.

```python
# Good
import os
import sys
from collections.abc import Mapping, Sequence
from typing import Any
import numpy as np  # Standard abbreviation

# Bad
from os import *  # Pollutes namespace
import tensorflow as t  # Non-standard abbreviation
from . import sibling  # Relative import
```

### Import What You Use

Import specific items you need, not entire modules when you only use one thing.

```python
# Good
from collections import defaultdict
counts = defaultdict(int)

# Acceptable for frequently-used modules
import os
os.path.join(base, filename)
```

## 2.3 Packages

Import each module using its full pathname location.

```python
# Good
from myproject.utils import helpers
from myproject.models import user

# Bad
import helpers  # Ambiguous without full path
```

## 2.4 Exceptions

Use built-in exception classes appropriately. Define custom exceptions when needed, inheriting from `Exception`.

### Exception Guidelines

1. Raise exceptions with clear, specific messages
2. Never use bare `except:`
3. Minimize code in `try` blocks
4. Use `finally` for cleanup or prefer `with` statements
5. Chain exceptions to preserve context

```python
# Good
class ConfigurationError(Exception):
    """Raised when configuration is invalid."""

def load_config(path: str) -> dict[str, Any]:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        raise ConfigurationError(f"Config file not found: {path}") from None
    except json.JSONDecodeError as e:
        raise ConfigurationError(f"Invalid JSON in {path}: {e}") from e

# Bad
def load_config(path: str) -> dict[str, Any]:
    try:
        f = open(path)
        data = json.load(f)
        process(data)
        validate(data)
        transform(data)  # Too much in try block
        return data
    except:  # Bare except
        return {}  # Silent failure
```

### Never Use Assert for Validation

`assert` statements are removed when Python runs with optimization (`-O`). Use them only for internal invariants during development.

```python
# Good
def process_age(age: int) -> None:
    if age < 0:
        raise ValueError(f"Age must be non-negative, got {age=}")

# Bad
def process_age(age: int) -> None:
    assert age >= 0, "Age must be non-negative"  # Removed with -O flag
```

## 2.5 Mutable Global State

Avoid mutable module-level variables. They break encapsulation and cause unpredictable behavior.

```python
# Good
_DEFAULT_TIMEOUT = 30  # Immutable constant

def get_timeout() -> int:
    return _DEFAULT_TIMEOUT

# Bad
timeout = 30  # Mutable global

def slow_operation() -> None:
    global timeout
    timeout = 60  # Modifies global state
```

### Module-Level Constants

Constants are encouraged. Use CAPS_WITH_UNDER naming.

```python
# Good
MAX_RETRIES = 3
DEFAULT_ENCODING = "utf-8"
SUPPORTED_FORMATS = frozenset({"json", "yaml", "toml"})  # Immutable
```

## 2.6 Nested/Local/Inner Classes and Functions

Use nested functions when closing over local variables. Avoid nesting merely to hide utilities—use `_` prefix at module level instead for testability.

```python
# Good - closure over local state
def make_counter(start: int = 0) -> Callable[[], int]:
    count = start
    def counter() -> int:
        nonlocal count
        count += 1
        return count
    return counter

# Good - module-level for testability
def _validate_input(data: dict) -> bool:
    ...

def process(data: dict) -> None:
    if not _validate_input(data):
        raise ValueError("Invalid input")
    ...

# Bad - hidden and untestable
def process(data: dict) -> None:
    def validate(d: dict) -> bool:  # Can't test this
        ...
    if not validate(data):
        raise ValueError("Invalid input")
```

## 2.7 Comprehensions & Generator Expressions

Use for simple transformations. Prohibit multiple `for` clauses or complex filters.

```python
# Good
squares = [x * x for x in numbers]
evens = [x for x in numbers if x % 2 == 0]
mapping = {k: v for k, v in pairs if v is not None}

# Bad - multiple for clauses
matrix = [[i * j for j in range(5)] for i in range(5)]  # Nested is OK
flat = [x for row in matrix for x in row]  # Multiple for - use explicit loop

# Bad - complex filter
result = [
    transform(x)
    for x in items
    if x.is_valid() and x.category in allowed and not x.is_deleted()
]  # Too complex - use explicit loop with early continue
```

### When to Use Explicit Loops

```python
# Good - explicit loop for complex logic
result = []
for x in items:
    if not x.is_valid():
        continue
    if x.category not in allowed:
        continue
    if x.is_deleted():
        continue
    result.append(transform(x))
```

## 2.8 Default Iterators and Operators

Use default iterators rather than explicit method calls.

```python
# Good
for key in dictionary:
    ...

for item in sequence:
    ...

if key in dictionary:
    ...

if item in sequence:
    ...

# Bad
for key in dictionary.keys():
    ...

for i in range(len(sequence)):
    item = sequence[i]
    ...
```

## 2.9 Generators

Use generators for memory efficiency when processing large sequences.

```python
# Good
def read_large_file(path: str) -> Iterator[str]:
    """Yield lines from a large file without loading all into memory.

    Yields:
        Each line from the file, stripped of trailing newline.
    """
    with open(path) as f:
        for line in f:
            yield line.rstrip("\n")

# Process without loading entire file
for line in read_large_file("huge.txt"):
    process(line)
```

## 2.10 Lambda Functions

Use for simple one-liners only. Prefer `operator` module for common operations.

```python
# Good
from operator import attrgetter, itemgetter

users.sort(key=attrgetter("name"))
pairs.sort(key=itemgetter(1))

# Acceptable
button.on_click(lambda event: handle_click(event.target))

# Bad
process = lambda x: (  # Too complex for lambda
    x.strip()
    .lower()
    .replace("-", "_")
)
```

## 2.11 Conditional Expressions

Use for simple cases where the entire expression fits on one line.

```python
# Good
status = "active" if user.is_active else "inactive"
value = x if x is not None else default

# Bad
result = (  # Too complex
    value_if_true
    if some_long_condition_that_spans_multiple_words
    else value_if_false
)
```

## 2.12 Default Argument Values

Never use mutable objects as defaults. Evaluate defaults at definition time, not call time.

```python
# Good
def append_to(
    element: int,
    target: list[int] | None = None,
) -> list[int]:
    if target is None:
        target = []
    target.append(element)
    return target

# Bad - mutable default
def append_to(element: int, target: list[int] = []) -> list[int]:
    target.append(element)  # Modifies shared default!
    return target
```

### Why This Matters

```python
# Demonstration of the bug
def buggy(items: list[str] = []) -> list[str]:
    items.append("x")
    return items

print(buggy())  # ['x']
print(buggy())  # ['x', 'x'] - same list!
print(buggy())  # ['x', 'x', 'x']
```

## 2.13 Properties

Use `@property` for computed attributes that should look like simple access. Avoid properties with significant side effects.

```python
# Good
class Circle:
    def __init__(self, radius: float) -> None:
        self._radius = radius

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value < 0:
            raise ValueError("Radius must be non-negative")
        self._radius = value

    @property
    def area(self) -> float:
        return math.pi * self._radius ** 2

# Bad - property with side effects
class User:
    @property
    def profile(self) -> Profile:
        return self._fetch_from_database()  # Surprising I/O on attribute access
```

## 2.14 True/False Evaluations

Use implicit falsiness for sequences and mappings. Always check `None` explicitly.

### Falsy Values in Python

- `None`
- `False`
- Zero: `0`, `0.0`, `0j`
- Empty sequences: `""`, `[]`, `()`
- Empty mappings: `{}`
- Objects with `__bool__` returning `False` or `__len__` returning `0`

```python
# Good
if not users:  # Empty list
    return "No users"

if name:  # Non-empty string
    greet(name)

if count is None:  # Explicit None check
    count = 0

# Bad
if len(users) == 0:
    return "No users"

if name != "":
    greet(name)

if not count:  # Fails if count is legitimately 0
    count = default
```

## 2.16 Lexical Scoping

Understand that assignments create local variables. Use `nonlocal` for closures that modify enclosing scope.

```python
# Good
def make_incrementer(start: int) -> Callable[[], int]:
    value = start
    def increment() -> int:
        nonlocal value
        value += 1
        return value
    return increment

# Bad - creates local variable instead of modifying
def broken_incrementer(start: int) -> Callable[[], int]:
    value = start
    def increment() -> int:
        value = value + 1  # UnboundLocalError - value is local here
        return value
    return increment
```

## 2.17 Function and Method Decorators

Use decorators judiciously. They execute at import time.

```python
# Good
@functools.lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    ...

@contextlib.contextmanager
def temporary_directory() -> Iterator[Path]:
    ...

# Bad - staticmethod (use module function instead)
class Utilities:
    @staticmethod
    def format_date(d: date) -> str:
        ...

# Better
def format_date(d: date) -> str:
    ...
```

## 2.18 Threading

Use `queue.Queue` for inter-thread communication. Use `threading.Lock` or `threading.Condition` for synchronization.

```python
# Good
import queue
import threading

work_queue: queue.Queue[Task] = queue.Queue()

def worker() -> None:
    while True:
        task = work_queue.get()
        try:
            process(task)
        finally:
            work_queue.task_done()

# Bad - relying on "atomic" operations
counter = 0

def increment() -> None:
    global counter
    counter += 1  # Not actually atomic!
```

## 2.19 Power Features

Avoid metaclasses, `__del__`, dynamic inheritance, and bytecode manipulation unless absolutely necessary.

```python
# Usually Bad
class Meta(type):
    def __new__(mcs, name, bases, namespace):
        ...  # Magic that's hard to debug

# Usually Bad
class Resource:
    def __del__(self):
        self.cleanup()  # May never run, runs at unpredictable times
```

## 2.21 Type Annotated Code

Use type hints for all function signatures. mypy enforces correctness at build time.

```python
# Good
def greeting(name: str) -> str:
    return f"Hello, {name}"

def process_items(items: list[int]) -> dict[str, int]:
    return {"sum": sum(items), "count": len(items)}

# Python 3.12+ generics
def first[T](items: Sequence[T]) -> T | None:
    return items[0] if items else None
```
