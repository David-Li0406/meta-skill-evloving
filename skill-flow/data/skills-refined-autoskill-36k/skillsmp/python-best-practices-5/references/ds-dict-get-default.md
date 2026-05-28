---
title: Use dict.get() with Default Instead of KeyError Handling
impact: HIGH
impactDescription: cleaner code, avoids exception overhead
tags: ds, dict, get, default-value
---

## Use dict.get() with Default Instead of KeyError Handling

Exception handling for missing keys is slower and more verbose than using `dict.get()` with a default value.

**Incorrect (exception overhead for missing keys):**

```python
def get_user_setting(user_id: int, settings: dict[int, Settings]) -> Settings:
    try:
        return settings[user_id]
    except KeyError:
        return Settings()  # Default settings
```

**Correct (no exception overhead):**

```python
def get_user_setting(user_id: int, settings: dict[int, Settings]) -> Settings:
    return settings.get(user_id, Settings())
```

**Alternative (setdefault for insert-if-missing):**

```python
def get_or_create_settings(user_id: int, settings: dict[int, Settings]) -> Settings:
    return settings.setdefault(user_id, Settings())
    # Inserts default and returns it if key missing
```

**Alternative (defaultdict for automatic defaults):**

```python
from collections import defaultdict

user_counts: defaultdict[int, int] = defaultdict(int)
user_counts[user_id] += 1  # No KeyError, auto-initializes to 0
```

Reference: [dict.get documentation](https://docs.python.org/3/library/stdtypes.html#dict.get)
