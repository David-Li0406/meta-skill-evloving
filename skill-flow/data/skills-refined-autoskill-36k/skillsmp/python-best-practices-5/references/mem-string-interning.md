---
title: Leverage String Interning for Repeated Strings
impact: HIGH
impactDescription: eliminates duplicate string allocations
tags: mem, string-interning, sys-intern, deduplication
---

## Leverage String Interning for Repeated Strings

Python automatically interns some strings, but explicit interning with `sys.intern()` ensures repeated strings share the same memory location.

**Incorrect (duplicate strings consume memory):**

```python
def process_events(events: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for event in events:
        event_type = event["type"]  # Each "click" is a new string
        counts[event_type] = counts.get(event_type, 0) + 1
    return counts
    # 1M events with 10 types = 1M string allocations
```

**Correct (interned strings share memory):**

```python
import sys

def process_events(events: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for event in events:
        event_type = sys.intern(event["type"])  # Reuses existing string
        counts[event_type] = counts.get(event_type, 0) + 1
    return counts
    # 1M events with 10 types = 10 string allocations
```

**Alternative (pre-intern known values):**

```python
EVENT_TYPES = {
    sys.intern("click"): 0,
    sys.intern("scroll"): 0,
    sys.intern("submit"): 0,
}
```

**Note:** Python automatically interns string literals and identifiers. Use `sys.intern()` for dynamically created strings that repeat frequently.

Reference: [sys.intern documentation](https://docs.python.org/3/library/sys.html#sys.intern)
