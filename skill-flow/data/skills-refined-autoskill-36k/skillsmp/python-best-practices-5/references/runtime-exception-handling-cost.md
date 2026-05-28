---
title: Minimize Exception Handling in Hot Paths
impact: LOW
impactDescription: exceptions are 100× slower than conditionals
tags: runtime, exceptions, performance, conditionals
---

## Minimize Exception Handling in Hot Paths

Exception handling is expensive compared to conditionals. In hot paths, use explicit checks instead of try/except for expected conditions.

**Incorrect (exception for expected case):**

```python
def get_value(data: dict, key: str) -> int:
    try:
        return data[key]
    except KeyError:
        return 0
    # KeyError raised and caught for every missing key
```

**Correct (conditional check):**

```python
def get_value(data: dict, key: str) -> int:
    return data.get(key, 0)
    # No exception overhead
```

**Incorrect (exception for type conversion):**

```python
def parse_int(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None
```

**Correct (pre-validation for expected failures):**

```python
def parse_int(value: str) -> int | None:
    if value.lstrip("-").isdigit():
        return int(value)
    return None
```

**When exceptions are appropriate:**
- Truly exceptional conditions (file not found, network errors)
- Rare error cases where conditional would be complex
- When the check would duplicate the operation's work

Reference: [Python exception handling performance](https://docs.python.org/3/faq/design.html#how-fast-are-exceptions)
