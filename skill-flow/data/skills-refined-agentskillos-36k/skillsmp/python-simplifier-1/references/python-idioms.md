# Python Idioms Reference

Modern Python patterns for cleaner code.

## Unpacking

```python
# Swap values
a, b = b, a

# Unpack with ignore
first, *_, last = items
_, important, _ = get_triple()

# Dict unpacking
defaults = {'timeout': 30, 'retries': 3}
config = {**defaults, **user_config}
```

## Walrus Operator (3.8+)

```python
# Assign and test
if match := pattern.search(text):
    process(match)

# In comprehensions
[y for x in data if (y := expensive(x)) > 0]
```

## Dataclasses

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

# With defaults and immutability
@dataclass(frozen=True)
class Config:
    host: str = 'localhost'
    port: int = 8080
```

## Enums

```python
from enum import Enum, auto

class Status(Enum):
    PENDING = auto()
    APPROVED = auto()
    REJECTED = auto()

status = Status.PENDING
```

## Functional Tools

```python
# any/all
found = any(item.valid for item in items)
all_valid = all(item.valid for item in items)

# zip
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# enumerate with start
for i, item in enumerate(items, start=1):
    print(f"{i}. {item}")
```

## String Formatting

```python
# f-strings
f"Hello {name}"
f"Total: {price * quantity:.2f}"
f"{value=}"  # Debug: prints "value=42"

# Join for building strings
result = ", ".join(str(item) for item in items)
```

## Path Handling

```python
from pathlib import Path

path = Path(base) / 'subdir' / 'file.txt'
content = path.read_text()
path.write_text(data)
```

## Context Managers

```python
from contextlib import contextmanager

@contextmanager
def timer(name):
    start = time.time()
    yield
    print(f"{name}: {time.time() - start:.2f}s")

with timer("operation"):
    do_work()
```

## Exception Handling

```python
# Exception chaining
try:
    process(data)
except ValueError as e:
    raise ProcessingError("Invalid") from e

# Suppress specific exceptions
from contextlib import suppress
with suppress(FileNotFoundError):
    os.remove('temp.txt')
```

## Collections

```python
from collections import Counter, defaultdict, namedtuple

counts = Counter(words)
graph = defaultdict(list)
Point = namedtuple('Point', ['x', 'y'])
```

## Itertools

```python
from itertools import chain, groupby, islice

flat = list(chain.from_iterable(nested))
first_ten = list(islice(iterator, 10))
```
