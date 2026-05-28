---
name: python
description: "Python development process and code quality review. Use when writing Python code, reviewing Python PRs, adding type hints, debugging Python issues, or setting up Python project tooling with pyproject.toml. Also use when code is 'clever' but hard to read, type hints are missing, bare except clauses appear, mutable default arguments are used, or code could be more Pythonic. Essential for async/await patterns, dataclasses, comprehensions, context managers, and mypy configuration."
---

# Python Skill

## Overview

Python's readability is its strength. This skill guides writing idiomatic Python that's clear, maintainable, and follows community standards.

**Core principle:** Explicit is better than implicit. Readability counts. If the implementation is hard to explain, it's a bad idea.

## The Pythonic Development Process

### Phase 1: Design Pythonically

**Before writing implementation:**

1. **Consider the Zen of Python**
   - Is there one obvious way to do this?
   - Is simple better than complex here?
   - Will this be readable in 6 months?

2. **Design with Types**
   ```python
   def get_user(user_id: str) -> User | None:
       """Fetch user by ID, return None if not found."""
       ...
   ```

3. **Choose the Right Data Structure**
   - List for ordered sequences
   - Set for unique items and fast lookup
   - Dict for key-value mapping
   - Dataclass for structured data

### Phase 2: Implement Idiomatically

**Write Python, not Java-in-Python:**

1. **Use Built-in Features**
   ```python
   # ❌ Non-Pythonic
   result = []
   for item in items:
       if item.active:
           result.append(item.name)

   # ✅ Pythonic
   result = [item.name for item in items if item.active]
   ```

2. **Handle Errors Explicitly**
   ```python
   # ❌ Bare except
   try:
       process(data)
   except:
       pass

   # ✅ Specific exceptions
   try:
       process(data)
   except ValidationError as e:
       logger.warning(f"Invalid data: {e}")
       raise
   ```

3. **Use Context Managers**
   ```python
   # ❌ Manual resource management
   f = open('file.txt')
   content = f.read()
   f.close()

   # ✅ Context manager
   with open('file.txt') as f:
       content = f.read()
   ```

### Phase 3: Review for Quality

**Before approving:**

1. **Check Type Coverage**
   - Are all public functions typed?
   - Run `mypy` with strict mode

2. **Check for Anti-patterns**
   - Mutable default arguments?
   - Bare except clauses?
   - Global state mutation?

3. **Verify Tests**
   - Are edge cases covered?
   - Are exceptions tested?

## Red Flags - STOP and Fix

### Python Anti-patterns

```python
# Mutable default argument (bug!)
def add_item(item, items=[]):  # Same list reused!

# Bare except (hides bugs)
except:
    pass

# Star import (namespace pollution)
from module import *

# Type checking with type()
if type(x) == list:  # Doesn't handle subclasses

# String concatenation in loop
result = ""
for s in strings:
    result += s  # O(n²)
```

### Code Quality Red Flags

```
- Functions > 50 lines (break them up)
- Deeply nested code > 3 levels (simplify)
- Magic numbers without names
- No docstrings on public functions
- Commented-out code (delete it)
- print() for logging (use logging module)
```

### Type Hint Red Flags

```
- Any type used without justification
- Missing return type annotations
- # type: ignore without explanation
- Union of many unrelated types
- No type hints on public API
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "Duck typing means no type hints" | Type hints document intent and catch bugs. |
| "It's Pythonic to be dynamic" | Explicit is better than implicit. Add types. |
| "Performance doesn't matter" | Algorithmic complexity matters. O(n²) hurts. |
| "Exception handling is verbose" | Specific handling prevents hidden bugs. |
| "It works" | Working isn't enough. It must be readable. |
| "I'll add types later" | Later never comes. Add them now. |

## Python Quality Checklist

Before approving Python code:

- [ ] **Typed**: Public functions have type hints
- [ ] **Mypy clean**: No type errors
- [ ] **No bare except**: All exceptions are specific
- [ ] **No mutable defaults**: Default arguments are immutable
- [ ] **Context managers**: Resources properly managed
- [ ] **Docstrings**: Public API is documented
- [ ] **Tests**: Behavior is tested

## Quick Pythonic Patterns

### Use Dataclasses

```python
# ❌ Manual __init__, __repr__, __eq__
class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

# ✅ Dataclass
@dataclass
class User:
    id: str
    name: str
    email: str
```

### Use Comprehensions

```python
# ❌ Manual loop
squares = []
for x in range(10):
    squares.append(x ** 2)

# ✅ List comprehension
squares = [x ** 2 for x in range(10)]

# Dict comprehension
user_map = {u.id: u for u in users}

# Generator for large data
total = sum(x ** 2 for x in range(1000000))
```

### Handle Optional Values

```python
# ❌ None checks everywhere
if user is not None:
    if user.profile is not None:
        name = user.profile.name

# ✅ Early return or walrus operator
if user is None or user.profile is None:
    return None
name = user.profile.name

# Or use getattr with default
name = getattr(getattr(user, 'profile', None), 'name', 'Unknown')
```

## Quick Commands

```bash
# Type checking
mypy src/ --strict

# Linting and formatting
ruff check . --fix
ruff format .

# Testing
pytest -v --cov=src

# Security
bandit -r src/
pip-audit
```

## References

Detailed patterns and examples in `references/`:
- `python-idioms.md` - Pythonic patterns and common mistakes
- `async-patterns.md` - async/await best practices
- `project-setup.md` - pyproject.toml and tooling configuration
