---
title: Use __slots__ for Memory-Efficient Classes
impact: HIGH
impactDescription: 30-50% memory reduction per instance
tags: mem, slots, dataclass, memory-efficiency
---

## Use __slots__ for Memory-Efficient Classes

By default, Python stores instance attributes in a `__dict__`. Defining `__slots__` eliminates this dict, reducing memory by 30-50% per instance.

**Incorrect (dict overhead per instance):**

```python
@dataclass
class Point:
    x: float
    y: float
    z: float
    # Each instance carries a __dict__ (~100+ bytes overhead)
```

**Correct (slots eliminate dict overhead):**

```python
@dataclass(slots=True)
class Point:
    x: float
    y: float
    z: float
    # No __dict__, ~40% less memory per instance
```

**Alternative (manual slots for pre-3.10):**

```python
class Point:
    __slots__ = ("x", "y", "z")

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
```

**When NOT to use slots:**
- Classes requiring dynamic attribute assignment
- Classes using multiple inheritance (slots can conflict)
- Few instances where memory savings are negligible

Reference: [dataclass slots documentation](https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass)
