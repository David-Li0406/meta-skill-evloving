---
name: howto-code-in-python
description: Use when writing or reviewing Python code. Covers Google Python Style Guide language rules and style conventions for Python 3.12+.
---

# Python Development Guide

## Overview

This skill provides opinionated guidance for writing and reviewing Python 3.12+ code following Google's Python Style Guide. The toolchain uses ruff for linting and formatting, mypy for type checking, and uv for dependency and environment management.

## When to Use

- Writing new Python code
- Reviewing Python code for style and correctness
- Refactoring existing Python code
- Debugging Python style or language issues

## Core Pattern

### When Writing Python Code

- [ ] Absolute imports only (`from x import y`), no relative imports
- [ ] Specific exception types with clear messages using `{value=}` syntax
- [ ] `None` as default for mutable arguments, initialize inside function
- [ ] Implicit falsiness for sequences, explicit `is None` for None checks
- [ ] Comprehensions only for simple single-clause transformations
- [ ] `with` statements for all file and resource handling
- [ ] f-strings for formatting, `%s` placeholders for logging
- [ ] Functions under ~40 lines; split when logic has distinct phases
- [ ] Naming: `module_name`, `ClassName`, `function_name`, `CONSTANT_NAME`
- [ ] 4-space indent, 80-char lines, parentheses for continuation

### When Reviewing Python Code

- [ ] No mutable default arguments (`def foo(x=[])` is a bug)
- [ ] No bare `except:` or overly broad exception handling
- [ ] `if x is None` not `if x == None`
- [ ] No f-strings in logging calls
- [ ] No `@staticmethod` (should be module-level function)
- [ ] No multi-clause comprehensions (use explicit loops)
- [ ] No backslash line continuation (use parentheses)
- [ ] Resources managed with `with` statements
- [ ] Naming conventions followed consistently
- [ ] Functions focused and reasonably sized
- [ ] **No `Any` type** — defeats type checking entirely (see examples below)

## Examples

### Imports

```python
# Good
from sound.effects import echo

# Bad — relative imports break when package structure changes
from . import sibling
```

### Exceptions

```python
# Good
raise ValueError(f"Age must be non-negative, got {age=}")

# Bad — silent failure prevents tracing error origins
except:
    pass
```

### Mutable Defaults

```python
# Good
def append_to(element: int, target: list[int] | None = None) -> list[int]:
    if target is None:
        target = []
    target.append(element)
    return target

# Bad — list is shared across all calls, causes subtle bugs
def append_to(element: int, target: list[int] = []) -> list[int]:
    target.append(element)
    return target
```

### None Checks

```python
# Good
if value is None:
    value = default

# Bad — use `is None` for explicit None checks, not falsiness
if not value:
    value = default
```

### Falsiness

```python
# Good
if not users:
    return "No users"

# Bad — verbose, non-idiomatic
if len(users) == 0:
    return "No users"
```

### Comprehensions

```python
# Good
squares = [x * x for x in numbers if x > 0]

# Bad — multiple for-clauses are hard to read and debug
result = [(x, y) for x in range(10) for y in range(5) if x * y > 10]
```

### Resources

```python
# Good
with open("data.txt") as f:
    content = f.read()

# Bad — manual cleanup is error-prone, prefer context managers
f = open("data.txt")
content = f.read()
f.close()
```

### Logging

```python
# Good
logger.info("Processing user %s with %d items", user_id, item_count)

# Bad — defeats lazy evaluation, breaks log aggregation
logger.info(f"Processing user {user_id} with {item_count} items")
```

### Decorators

```python
# Good
def add(a: int, b: int) -> int:
    return a + b

# Bad — staticmethod has no benefit over module-level function
class Math:
    @staticmethod
    def add(a: int, b: int) -> int:
        return a + b
```

### Line Continuation

```python
# Good
result = function_with_long_name(
    argument_one,
    argument_two,
)

# Bad — backslash continuation is fragile and error-prone
result = function_with_long_name(argument_one, \
    argument_two)
```

### Avoiding `Any` Type

```python
# Good — use specific types
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Good — use TypeVar for generic code
T = TypeVar("T")
def first(items: list[T]) -> T | None:
    return items[0] if items else None

# Good — use Protocol for structural typing
class Drawable(Protocol):
    def draw(self) -> None: ...

def render(obj: Drawable) -> None:
    obj.draw()

# Good — use object if truly accepting anything (but can't do much with it)
def log_value(value: object) -> None:
    print(str(value))

# Bad — Any opts out of type checking entirely
def process(data: Any) -> Any:  # mypy can't catch errors here
    return data.foo.bar.baz  # no error even if this is wrong

# Bad — hiding type information
def get_config() -> dict[str, Any]:  # what's actually in here?
    ...
```

**When you see `Any`**, ask: what type should this actually be? Common fixes:
- JSON data → use `TypedDict` or Pydantic models
- Generic containers → use `TypeVar`
- Callable with unknown signature → use `Callable[..., ReturnType]`
- Truly dynamic data → use `object` (safer, can't call arbitrary methods)

## Quick Reference

```
Imports:      from x import y, not relative imports
Exceptions:   Specific types, never bare except
Defaults:     Never mutable (use None + initialize)
Truthiness:   if not seq: (implicit), if x is None: (explicit)
Lines:        80 chars max, parentheses for continuation
Indent:       4 spaces, never tabs
Strings:      f-strings, consistent quotes
Logging:      logger.info("msg %s", val) not f-strings
Resources:    Always use with statements
Names:        module_name, ClassName, function_name, CONSTANT
Types:        No Any — use specific types, TypeVar, Protocol, or object
```

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| Mutable default arguments | Shared state across calls | Use `None` and initialize inside |
| Bare `except:` | Catches KeyboardInterrupt, SystemExit | Catch specific exceptions |
| Multiple for-clauses in comprehension | Unreadable, hard to debug | Use explicit loops |
| f-strings in logging | Defeats lazy evaluation, breaks log aggregation | Use `%s` placeholders |
| `staticmethod` | No benefit over module function | Use module-level function |
| Backslash line continuation | Fragile, error-prone | Use parentheses |
| `if x == None:` | Fails for objects overriding `__eq__` | Use `if x is None:` |
| Using `Any` type | Opts out of type checking entirely | Use specific types, TypeVar, Protocol, or object |
| `dict[str, Any]` for config/JSON | Hides structure, no IDE completion | Use TypedDict or Pydantic models |

## Anti-Rationalizations

- "This comprehension is readable enough" — If it has multiple `for` clauses or complex filters, it isn't. Use explicit loops.
- "I'll remember the mutable default" — You won't. Neither will the next developer. Use `None`.
- "f-strings in logging are fine here" — Log aggregation tools depend on patterns. Use placeholders.
- "staticmethod documents intent" — Module-level functions are clearer and more Pythonic.
- "80 characters is too restrictive" — It forces better naming and decomposition. Embrace it.
- "Any is fine for this dynamic data" — No. Define the shape with TypedDict, Protocol, or Pydantic. `Any` means mypy can't help you.
- "I'll fix the types later" — You won't. Type debt compounds. Fix it now or it spreads.

## Supporting References

- [language-rules.md](language-rules.md) — Detailed language rules with examples from Google Python Style Guide Section 2
- [style-rules.md](style-rules.md) — Detailed style rules with examples from Google Python Style Guide Sections 3.1-3.18
