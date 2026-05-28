# Python Core Principles

## The Zen of Python

```python
import this
```

1. Beautiful is better than ugly
2. Explicit is better than implicit
3. Simple is better than complex
4. Flat is better than nested
5. Readability counts

## PEP 8 Style Guide

### Naming Conventions
- `snake_case` for functions and variables
- `PascalCase` for classes
- `UPPER_CASE` for constants
- `_leading_underscore` for private

### Code Layout
```python
# Good
def calculate_total(items: list[Item]) -> float:
    """Calculate total price of items."""
    return sum(item.price for item in items)

# Bad
def calculateTotal(items):
    return sum([item.price for item in items])
```

## Type Hints

Always use type hints for public APIs:

```python
from typing import Protocol

class Serializable(Protocol):
    def to_dict(self) -> dict: ...

def save_data(obj: Serializable, path: str) -> None:
    with open(path, 'w') as f:
        json.dump(obj.to_dict(), f)
```

## Context Managers

Prefer context managers for resource management:

```python
# Good
with open('file.txt') as f:
    data = f.read()

# Better - custom context manager
from contextlib import contextmanager

@contextmanager
def database_connection(url: str):
    conn = connect(url)
    try:
        yield conn
    finally:
        conn.close()
```

## Comprehensions

Use comprehensions for clarity:

```python
# Good
squares = [x**2 for x in range(10)]
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# Dict comprehension
word_lengths = {word: len(word) for word in words}
```

## Error Handling

```python
# Specific exceptions
try:
    value = int(user_input)
except ValueError as e:
    logger.error(f"Invalid input: {e}")
    raise

# Never bare except
# except:  # Bad!
```

## Best Practices

1. Use type hints
2. Follow PEP 8
3. Write docstrings
4. Prefer composition over inheritance
5. EAFP: Easier to Ask Forgiveness than Permission
6. Use dataclasses for data containers
7. Leverage standard library
8. Test your code
