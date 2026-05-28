# Python Idioms & Best Practices

Patterns for writing clean, efficient, Pythonic code.

## Pythonic Patterns

### List Comprehensions

```python
# ❌ Non-Pythonic
result = []
for item in items:
    if item.active:
        result.append(item.name)

# ✅ Pythonic
result = [item.name for item in items if item.active]

# Dictionary comprehension
user_map = {user.id: user for user in users}

# Set comprehension
unique_tags = {tag for item in items for tag in item.tags}

# Generator expression (for large datasets)
total = sum(item.price for item in items if item.in_stock)
```

### Unpacking

```python
# Tuple unpacking
first, *middle, last = [1, 2, 3, 4, 5]
# first=1, middle=[2, 3, 4], last=5

# Dictionary unpacking
defaults = {'timeout': 30, 'retries': 3}
config = {**defaults, 'timeout': 60}  # Override timeout

# Function argument unpacking
def greet(name, greeting='Hello'):
    return f'{greeting}, {name}!'

args = ['World']
kwargs = {'greeting': 'Hi'}
greet(*args, **kwargs)  # 'Hi, World!'
```

### Walrus Operator (Python 3.8+)

```python
# ❌ Without walrus
match = pattern.search(text)
if match:
    process(match)

# ✅ With walrus operator
if (match := pattern.search(text)):
    process(match)

# Useful in comprehensions
valid_items = [
    transformed
    for item in items
    if (transformed := transform(item)) is not None
]
```

### Context Managers

```python
# For resource management
with open('file.txt') as f:
    content = f.read()
# File automatically closed

# Custom context manager
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f'{name}: {elapsed:.2f}s')

with timer('Operation'):
    do_something()
```

### EAFP vs LBYL

```python
# LBYL (Look Before You Leap) - Less Pythonic
if key in dictionary:
    value = dictionary[key]
else:
    value = default

# EAFP (Easier to Ask Forgiveness) - Pythonic
try:
    value = dictionary[key]
except KeyError:
    value = default

# Even better: use .get()
value = dictionary.get(key, default)
```

## Data Classes & Named Tuples

### Dataclasses (Python 3.7+)

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class User:
    id: str
    name: str
    email: str
    active: bool = True
    tags: list[str] = field(default_factory=list)

# Frozen (immutable)
@dataclass(frozen=True)
class Point:
    x: float
    y: float

# With custom methods
@dataclass
class Order:
    items: list[Item]
    tax_rate: float = 0.1

    @property
    def subtotal(self) -> float:
        return sum(item.price for item in self.items)

    @property
    def total(self) -> float:
        return self.subtotal * (1 + self.tax_rate)
```

### Named Tuples

```python
from typing import NamedTuple

class Coordinate(NamedTuple):
    x: float
    y: float
    label: str = ''

point = Coordinate(1.0, 2.0, 'origin')
x, y, label = point  # Can unpack
print(point.x)       # Can access by name
```

## Type Hints

### Modern Type Hints (Python 3.10+)

```python
# Union with |
def process(value: int | str | None) -> str:
    ...

# Instead of Optional[X], use X | None
def get_user(id: str) -> User | None:
    ...

# Generic collections (no need for typing imports)
def process_items(items: list[Item]) -> dict[str, int]:
    ...

# TypeAlias for complex types
type UserMap = dict[str, User]
type Callback = Callable[[int, str], bool]
```

### Generic Types

```python
from typing import TypeVar, Generic

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class Cache(Generic[K, V]):
    def __init__(self) -> None:
        self._data: dict[K, V] = {}

    def get(self, key: K) -> V | None:
        return self._data.get(key)

    def set(self, key: K, value: V) -> None:
        self._data[key] = value

# Usage
cache: Cache[str, User] = Cache()
cache.set('user-1', user)
```

### Protocols (Structural Subtyping)

```python
from typing import Protocol

class Readable(Protocol):
    def read(self) -> str: ...

class Writable(Protocol):
    def write(self, data: str) -> None: ...

# Any class with a read() method satisfies Readable
def process(source: Readable) -> str:
    return source.read()

# Works with file objects, StringIO, custom classes, etc.
```

## Error Handling

### Custom Exceptions

```python
class AppError(Exception):
    """Base exception for application."""
    pass

class NotFoundError(AppError):
    def __init__(self, resource: str, id: str):
        self.resource = resource
        self.id = id
        super().__init__(f'{resource} not found: {id}')

class ValidationError(AppError):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f'{field}: {message}')
```

### Exception Chaining

```python
try:
    result = external_api.fetch(id)
except ExternalAPIError as e:
    # Chain the original exception
    raise NotFoundError('User', id) from e
```

### Specific Exception Handling

```python
# ❌ BAD: Catching everything
try:
    do_something()
except Exception:
    pass

# ✅ GOOD: Specific exceptions
try:
    do_something()
except FileNotFoundError:
    handle_missing_file()
except PermissionError:
    handle_permission_denied()
except (ValueError, TypeError) as e:
    handle_bad_input(e)
```

## Iteration Patterns

### Enumerate and Zip

```python
# Instead of range(len())
for i, item in enumerate(items):
    print(f'{i}: {item}')

# Start from different index
for i, item in enumerate(items, start=1):
    print(f'{i}: {item}')

# Parallel iteration
for name, score in zip(names, scores):
    print(f'{name}: {score}')

# Strict zip (Python 3.10+)
for name, score in zip(names, scores, strict=True):
    # Raises if lengths differ
    pass
```

### Itertools

```python
from itertools import chain, groupby, islice, batched

# Chain multiple iterables
all_items = chain(list1, list2, list3)

# Group consecutive items
sorted_items = sorted(items, key=lambda x: x.category)
for category, group in groupby(sorted_items, key=lambda x: x.category):
    print(f'{category}: {list(group)}')

# Slice iterators
first_10 = islice(infinite_generator(), 10)

# Batch processing (Python 3.12+)
for batch in batched(items, 100):
    process_batch(batch)
```

## Common Mistakes

### Mistake: Mutable Default Arguments

```python
# ❌ BAD: Mutable default is shared
def add_item(item, items=[]):
    items.append(item)
    return items

# ✅ GOOD: Use None and create new list
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# Or use dataclass field factory
@dataclass
class Container:
    items: list[str] = field(default_factory=list)
```

### Mistake: Late Binding Closures

```python
# ❌ BAD: All lambdas capture final value of i
funcs = [lambda: i for i in range(5)]
[f() for f in funcs]  # [4, 4, 4, 4, 4]

# ✅ GOOD: Capture value at creation time
funcs = [lambda i=i: i for i in range(5)]
[f() for f in funcs]  # [0, 1, 2, 3, 4]
```

### Mistake: String Concatenation in Loop

```python
# ❌ BAD: O(n²) - creates new string each time
result = ''
for item in items:
    result += str(item) + ', '

# ✅ GOOD: O(n) - use join
result = ', '.join(str(item) for item in items)
```

### Mistake: Using `type()` Instead of `isinstance()`

```python
# ❌ BAD: Doesn't handle inheritance
if type(obj) == MyClass:
    ...

# ✅ GOOD: Works with subclasses
if isinstance(obj, MyClass):
    ...

# Multiple types
if isinstance(obj, (str, bytes)):
    ...
```

### Mistake: Not Using `with` for Files

```python
# ❌ BAD: File may not be closed on error
f = open('file.txt')
content = f.read()
f.close()

# ✅ GOOD: Always properly closed
with open('file.txt') as f:
    content = f.read()
```

### Mistake: Modifying List While Iterating

```python
# ❌ BAD: Skips items
items = [1, 2, 3, 4, 5]
for item in items:
    if item % 2 == 0:
        items.remove(item)  # Modifies list during iteration

# ✅ GOOD: Create new list
items = [item for item in items if item % 2 != 0]

# Or iterate over copy
for item in items[:]:
    if item % 2 == 0:
        items.remove(item)
```

## Performance Tips

### Use `__slots__` for Many Instances

```python
# Without slots: each instance has __dict__
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# With slots: ~40% less memory
class Point:
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y
```

### Use Generators for Large Data

```python
# ❌ BAD: Loads everything into memory
def get_all_users():
    return [process(row) for row in fetch_millions_of_rows()]

# ✅ GOOD: Yields one at a time
def get_all_users():
    for row in fetch_millions_of_rows():
        yield process(row)
```

### Use `set` for Membership Testing

```python
# ❌ BAD: O(n) lookup
valid_ids = ['a', 'b', 'c', 'd', 'e']
if user_id in valid_ids:  # O(n)
    ...

# ✅ GOOD: O(1) lookup
valid_ids = {'a', 'b', 'c', 'd', 'e'}
if user_id in valid_ids:  # O(1)
    ...
```

### Use `lru_cache` for Expensive Functions

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    # Result is cached
    return fibonacci(n)

# Clear cache if needed
expensive_computation.cache_clear()
```
