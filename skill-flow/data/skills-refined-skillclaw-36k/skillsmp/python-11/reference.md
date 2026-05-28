# Reference Guide

## Data Structure Selection

| Need | Data Structure |
|------|----------------|
| Ordered, mutable sequence | `list` |
| Immutable sequence | `tuple` |
| Fast lookup by key | `dict` |
| Membership testing | `set` / `frozenset` |
| FIFO queue | `collections.deque` |
| Priority queue | `heapq` |
| Counting | `collections.Counter` |
| Ordered dict | `dict` (insertion order since 3.7) |
| Default values | `collections.defaultdict` |

### When to Use What

- **list**: Default mutable sequence. O(1) append, O(n) insert/delete.
- **tuple**: Immutable, hashable. Use for fixed data, dict keys, return values.
- **dict**: Key-value lookup. O(1) average access.
- **set**: Membership testing O(1), deduplication, set operations.
- **deque**: Fast append/pop from both ends. Use for queues.
- **namedtuple/dataclass**: Structured data with named fields.

## Naming Conventions (PEP 8)

```python
# snake_case for functions and variables
def calculate_total_price(items: list) -> float: ...
user_count = 42

# SCREAMING_SNAKE_CASE for constants
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT = 30

# PascalCase for classes
class UserRepository: ...
class HTTPClient: ...  # Acronyms capitalized

# _leading underscore for private
def _internal_helper(): ...
_cache = {}

# __dunder__ for magic methods
def __init__(self): ...
def __repr__(self): ...
```

## Best Practices

### Do

- **Use type hints**: Document intent, enable static analysis
- **Prefer immutability**: `frozen=True` dataclasses, tuples over lists
- **Write pure functions**: Same input, same output, no side effects
- **Use context managers**: `with` for resource cleanup
- **Leverage comprehensions**: Readable, Pythonic transformations
- **Validate at boundaries**: Check external input, trust internal data
- **Use Protocol for interfaces**: Structural typing, duck typing

### Don't

- **Avoid mutable default args**: `def f(lst=None)` not `def f(lst=[])`
- **Don't catch bare Exception**: Be specific about error types
- **Avoid global state**: Pass dependencies explicitly
- **Don't mutate function args**: Return new values instead
- **Avoid deep inheritance**: Composition over inheritance
- **Don't ignore type errors**: Fix them, they catch bugs

## Code Organization

```
my-project/
├── src/my_project/
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── config.py        # Configuration
│   ├── domain/          # Business entities
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── order.py
│   ├── services/        # Business logic
│   │   └── user_service.py
│   ├── adapters/        # External interfaces
│   │   ├── db.py
│   │   └── api.py
│   └── utils/           # Shared utilities
├── tests/
│   ├── unit/
│   └── integration/
├── pyproject.toml
└── uv.lock
```

## Error Handling

```python
# Custom exceptions with context
class UserNotFoundError(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")

# Catch specific exceptions
try:
    user = find_user(user_id)
except UserNotFoundError as e:
    logger.warning(f"User {e.user_id} not found")
    return None
except DatabaseError:
    logger.exception("Database error")
    raise

# Result types instead of exceptions
from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T")

@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T

@dataclass(frozen=True)
class Err:
    error: str

Result = Ok[T] | Err
```

## Performance Tips

### Prefer

- **Generator expressions**: `(x for x in items)` for large data
- **`dict.get()`**: Avoid KeyError, provide defaults
- **`set` for membership**: O(1) vs O(n) for lists
- **Local variables**: Faster than globals in tight loops
- **`itertools`**: Memory-efficient iteration
- **`__slots__`**: Reduce memory for many instances

### Avoid

- **Repeated attribute lookup**: Cache `obj.attr` in loops
- **String concatenation in loops**: Use `"".join(parts)`
- **Creating lists for iteration**: Use generators
- **`import` inside functions**: Move to module level

## Common Idioms

```python
# Unpacking
first, *rest = items
a, b = b, a  # Swap

# Dict comprehension with condition
{k: v for k, v in data.items() if v is not None}

# Defaultdict for grouping
from collections import defaultdict
groups = defaultdict(list)
for item in items:
    groups[item.category].append(item)

# Counter for frequencies
from collections import Counter
counts = Counter(["a", "b", "a", "c", "a"])
# Counter({'a': 3, 'b': 1, 'c': 1})

# Enumerate with start
for i, item in enumerate(items, start=1):
    print(f"{i}. {item}")

# Zip for parallel iteration
for name, age in zip(names, ages):
    print(f"{name} is {age}")

# any/all for conditions
if any(item.is_valid for item in items): ...
if all(x > 0 for x in numbers): ...

# Walrus operator
if (match := pattern.search(text)):
    print(match.group(0))
```

## Type Hints Quick Reference

```python
# Basic types
x: int = 1
s: str = "hello"
flag: bool = True

# Collections
items: list[str] = []
counts: dict[str, int] = {}
ids: set[int] = set()

# Optional (None possible)
name: str | None = None

# Union
value: int | str = 42

# Callable
from typing import Callable
fn: Callable[[int, str], bool]

# TypeVar for generics
from typing import TypeVar
T = TypeVar("T")
def first(items: list[T]) -> T: ...

# Protocol for structural typing
from typing import Protocol

class Printable(Protocol):
    def __str__(self) -> str: ...
```

## Core Patterns

### Pure Functions + Immutability

```python
from dataclasses import dataclass

@dataclass(frozen=True)  # Immutable
class Point:
    x: float
    y: float

    def translate(self, dx: float, dy: float) -> "Point":
        return Point(self.x + dx, self.y + dy)  # New instance
```

### Composition with Pipe

```python
from functools import reduce
from typing import Callable, Any

def pipe(*fns: Callable[[Any], Any]) -> Callable[[Any], Any]:
    return reduce(lambda f, g: lambda x: g(f(x)), fns)

# Usage: read left-to-right
process = pipe(parse, validate, transform, save)
result = process(data)
```

### Structural Typing with Protocol

```python
from typing import Protocol

class Persistable(Protocol):
    def save(self) -> None: ...
    def load(self) -> None: ...

def backup(store: Persistable) -> None:  # Duck typing!
    store.save()
```

## Itertools Patterns

```python
from itertools import chain, batched, pairwise, groupby, accumulate, takewhile

# chain: Flatten iterables
list(chain([1, 2], [3, 4]))  # [1, 2, 3, 4]

# batched: Chunk into groups (3.12+)
list(batched("ABCDEFG", 3))  # [('A','B','C'), ('D','E','F'), ('G',)]

# pairwise: Consecutive pairs
list(pairwise("ABCD"))  # [('A','B'), ('B','C'), ('C','D')]

# groupby: Group consecutive (requires sorted input!)
data = [("a", 1), ("a", 2), ("b", 3)]
{k: list(g) for k, g in groupby(data, key=lambda x: x[0])}
# {'a': [('a', 1), ('a', 2)], 'b': [('b', 3)]}

# accumulate: Running totals
list(accumulate([1, 2, 3, 4]))  # [1, 3, 6, 10]

# takewhile/dropwhile: Conditional slicing
list(takewhile(lambda x: x < 5, [1, 3, 6, 2]))  # [1, 3]

# combinations/permutations/product
from itertools import combinations, permutations, product
list(combinations("ABC", 2))  # [('A','B'), ('A','C'), ('B','C')]
list(product([0, 1], repeat=2))  # [(0,0), (0,1), (1,0), (1,1)]
```

## Functools Patterns

```python
from functools import reduce, partial, lru_cache

# reduce: Fold to single value
reduce(lambda acc, x: acc + x, [1, 2, 3, 4], 0)  # 10

# partial: Fix arguments
from operator import mul
double = partial(mul, 2)
double(5)  # 10

# lru_cache: Memoization
@lru_cache(maxsize=128)
def fib(n: int) -> int:
    return n if n < 2 else fib(n-1) + fib(n-2)
```

## Async Patterns

```python
import asyncio
import httpx

# TaskGroup: Structured concurrency (3.11+)
async def fetch_all(urls: list[str]) -> list[str]:
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(client.get(url)) for url in urls]
    return [t.result().text for t in tasks]

# Async generator
async def async_range(n: int):
    for i in range(n):
        await asyncio.sleep(0.01)
        yield i

async def consume():
    async for value in async_range(5):
        print(value)

# Gather with error handling
async def fetch_safe(urls: list[str]):
    results = await asyncio.gather(
        *[fetch(url) for url in urls],
        return_exceptions=True
    )
    successes = [r for r in results if not isinstance(r, Exception)]
    errors = [r for r in results if isinstance(r, Exception)]
    return successes, errors
```

## Project Structure

```
my-project/
├── src/my_project/
│   ├── __init__.py
│   ├── main.py
│   ├── domain/        # Types, entities
│   └── services/      # Business logic
├── tests/
├── pyproject.toml
└── uv.lock            # Always commit!
```

## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| Mutable default args `def f(lst=[])` | `def f(lst=None)` |
| `requests.get` in async | `httpx.AsyncClient` |
| Classes for data bags | `@dataclass(frozen=True)` |
| Inheritance hierarchies | Protocols + composition |
| Mutating function args | Return new values |
| `try/except Exception` | Specific exception types |
| Blocking in async | `await asyncio.to_thread(fn)` |

## Pitfalls and Fixes

| Pitfall | Fix |
|---------|-----|
| Async client leaks | Use `async with httpx.AsyncClient()` |
| Ruff vs formatter churn | Use `ruff format` as the only formatter |
| mypy narrowing pain | Use `isinstance`, `match`, or Protocols |
| Slow tests from real I/O | Use fixtures, `tmp_path`, and mocks |
| Shared mutable state | Prefer immutable data or copy-on-write |
