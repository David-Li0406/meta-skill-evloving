# Modern Python: 3.11 to 3.12

Concurrency, typing, and stdlib upgrades.

---
## Exception Groups (3.11+)

**Problem**: You need to raise or handle multiple exceptions at once, common in concurrent code.

**Solution**:
```python
# Raise multiple exceptions
raise ExceptionGroup("errors", [
    ValueError("invalid value"),
    TypeError("wrong type"),
])

# Catch by type
try:
    async_operation()
except* ValueError as eg:
    print(f"Value errors: {eg.exceptions}")
except* TypeError as eg:
    print(f"Type errors: {eg.exceptions}")
```

**Tip**: Use `except*` (not `except`) to handle exception groups. Each handler processes all exceptions of that type.

---

## TaskGroup for Structured Concurrency (3.11+)

**Problem**: You want to run multiple async tasks and ensure all complete or all cancel together on error.

**Solution**:
```python
import asyncio

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch("url1"))
        task2 = tg.create_task(fetch("url2"))
    # All tasks complete or all cancelled on error
    return task1.result(), task2.result()
```

**Tip**: TaskGroup provides automatic cancellation of sibling tasks if any task fails, preventing orphaned tasks.

---

## TOML Parser (3.11+)

**Problem**: You need to parse TOML configuration files without external dependencies.

**Solution**:
```python
import tomllib

with open("pyproject.toml", "rb") as f:
    config = tomllib.load(f)

# Or from string
data = tomllib.loads('[section]\nkey = "value"')
```

**Tip**: Note that files must be opened in binary mode (`"rb"`). `tomllib` is read-only; use `tomli_w` for writing.

---

## Self Type (3.11+)

**Problem**: You want method return types to correctly refer to the current class, not the parent.

**Solution**:
```python
from typing import Self

class Builder:
    def with_name(self, name: str) -> Self:
        self.name = name
        return self

    def clone(self) -> Self:
        return type(self)()
```

**Tip**: `Self` is especially useful for builder patterns and methods that return the instance for chaining.

---

## Type Parameter Syntax (3.12+)

**Problem**: You want to write generic functions and classes without the boilerplate of `TypeVar`.

**Solution**:
```python
# Old way
from typing import TypeVar
T = TypeVar("T")
def first(items: list[T]) -> T: ...

# New way - cleaner!
def first[T](items: list[T]) -> T:
    return items[0]

# Generic classes
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# Constrained types
def add[T: (int, float)](a: T, b: T) -> T:
    return a + b
```

**Tip**: The new bracket syntax is more concise and puts type parameters directly in function/class signatures.

---

## Type Alias Statement (3.12+)

**Problem**: You want to create type aliases that are properly recognized as types, not runtime values.

**Solution**:
```python
# Old way
from typing import TypeAlias
Vector: TypeAlias = list[float]

# New way
type Vector = list[float]
type Point = tuple[float, float]
type Callback[T] = Callable[[T], None]
```

**Tip**: The `type` statement creates proper type aliases that support generic parameters cleanly.

---

## F-String Improvements (3.12+)

**Problem**: You need to use quotes inside f-strings or format complex multiline expressions.

**Solution**:
```python
# Nested quotes (any quote style)
print(f"User: {user["name"]}")  # Now works!
print(f'Status: {data['status']}')

# Multiline expressions
result = f"{
    some_long_function_call(
        arg1,
        arg2
    )
}"

# Comments inside f-strings
f"{x:=10}"  # This is a format spec, not walrus!
```

**Tip**: You can now use any quote style inside f-strings without escaping, making JSON and dict access much cleaner.

---

## Override Decorator (3.12+)

**Problem**: You want to catch typos or signature mismatches when overriding parent class methods.

**Solution**:
```python
from typing import override

class Parent:
    def greet(self) -> str:
        return "Hello"

class Child(Parent):
    @override
    def greet(self) -> str:  # Type checker verifies this exists in parent
        return "Hi"

    @override
    def great(self) -> str:  # Error: typo, no such method in parent
        return "Oops"
```

**Tip**: Use `@override` to make type checkers verify that you're actually overriding a parent method, catching typos early.

---

## Batched Iteration (3.12+)

**Problem**: You need to process data in fixed-size chunks.

**Solution**:
```python
from itertools import batched

list(batched("ABCDEFG", 3))
# [('A', 'B', 'C'), ('D', 'E', 'F'), ('G',)]

# Process in chunks
for batch in batched(large_dataset, 100):
    process_batch(batch)
```

**Tip**: `batched()` is more efficient than manual chunking and handles the final partial batch automatically.

