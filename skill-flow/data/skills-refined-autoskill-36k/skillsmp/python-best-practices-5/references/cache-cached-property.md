---
title: Use cached_property for Expensive Computed Attributes
impact: LOW-MEDIUM
impactDescription: computes once per instance, O(1) subsequent access
tags: cache, cached-property, functools, lazy-evaluation
---

## Use cached_property for Expensive Computed Attributes

`functools.cached_property` computes an attribute value once and caches it on the instance, avoiding repeated computation.

**Incorrect (recomputes on every access):**

```python
class Report:
    def __init__(self, data: list[DataPoint]):
        self.data = data

    @property
    def statistics(self) -> Statistics:
        # Expensive computation runs every time .statistics is accessed
        return compute_statistics(self.data)
```

**Correct (computed once, cached on instance):**

```python
from functools import cached_property

class Report:
    def __init__(self, data: list[DataPoint]):
        self.data = data

    @cached_property
    def statistics(self) -> Statistics:
        # Computed once, stored as instance attribute
        return compute_statistics(self.data)
```

**Invalidating cached value:**

```python
class Report:
    @cached_property
    def statistics(self) -> Statistics:
        return compute_statistics(self.data)

    def update_data(self, new_data: list[DataPoint]) -> None:
        self.data = new_data
        # Invalidate cached value
        if "statistics" in self.__dict__:
            del self.__dict__["statistics"]
```

Reference: [functools.cached_property documentation](https://docs.python.org/3/library/functools.html#functools.cached_property)
