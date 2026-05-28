---
title: Preallocate Lists When Size is Known
impact: HIGH
impactDescription: eliminates reallocation overhead, 10-30% faster
tags: mem, preallocation, list, array
---

## Preallocate Lists When Size is Known

List append operations trigger periodic reallocations as the list grows. When the final size is known, preallocate to avoid reallocation overhead.

**Incorrect (multiple reallocations during growth):**

```python
def transform_values(source: list[int]) -> list[int]:
    result = []
    for value in source:
        result.append(value * 2)  # Triggers reallocations
    return result
```

**Correct (list comprehension, single allocation):**

```python
def transform_values(source: list[int]) -> list[int]:
    return [value * 2 for value in source]  # Single allocation
```

**Alternative (numpy for numeric data):**

```python
import numpy as np

def transform_values(source: np.ndarray) -> np.ndarray:
    result = np.empty(len(source), dtype=source.dtype)  # Preallocate
    np.multiply(source, 2, out=result)  # In-place operation
    return result
```

**Alternative (preallocate with None):**

```python
def transform_sparse_values(indices: list[int], values: list[int], size: int) -> list[int | None]:
    result = [None] * size  # Single allocation
    for idx, val in zip(indices, values):
        result[idx] = val
    return result
```

Reference: [Python list implementation](https://docs.python.org/3/faq/design.html#how-are-lists-implemented-in-cpython)
