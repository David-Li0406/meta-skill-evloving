---
title: Use str.join() for String Concatenation
impact: MEDIUM-HIGH
impactDescription: O(n) vs O(n²), eliminates quadratic string creation
tags: algo, string, join, concatenation
---

## Use str.join() for String Concatenation

String concatenation with `+=` in loops creates new string objects each iteration, resulting in O(n²) complexity. `str.join()` builds the result in a single pass.

**Incorrect (quadratic string concatenation):**

```python
def build_csv_row(values: list[str]) -> str:
    result = ""
    for i, value in enumerate(values):
        if i > 0:
            result += ","
        result += value  # Creates new string each iteration
    return result
```

**Correct (single-pass join):**

```python
def build_csv_row(values: list[str]) -> str:
    return ",".join(values)
```

**With transformation:**

```python
def build_user_summary(users: list[User]) -> str:
    return "\n".join(f"{user.name}: {user.email}" for user in users)
```

**Alternative (f-strings for fixed small concatenations):**

```python
# For 2-5 known values, f-strings are cleaner and fast
greeting = f"Hello, {first_name} {last_name}!"
```

Reference: [str.join documentation](https://docs.python.org/3/library/stdtypes.html#str.join)
