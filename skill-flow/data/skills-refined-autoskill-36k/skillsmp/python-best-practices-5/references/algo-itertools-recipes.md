---
title: Use itertools for Efficient Iteration Patterns
impact: MEDIUM-HIGH
impactDescription: 2-5× faster than Python equivalents
tags: algo, itertools, iteration, functional
---

## Use itertools for Efficient Iteration Patterns

The `itertools` module provides C-optimized iterators for common patterns. They're memory-efficient and faster than Python equivalents.

**Incorrect (manual batching):**

```python
def batch_items(items: list[Item], batch_size: int) -> list[list[Item]]:
    batches = []
    for i in range(0, len(items), batch_size):
        batches.append(items[i:i + batch_size])
    return batches
```

**Correct (itertools.batched, Python 3.12+):**

```python
from itertools import batched

def batch_items(items: Iterable[Item], batch_size: int) -> Iterator[tuple[Item, ...]]:
    return batched(items, batch_size)
```

**Common itertools patterns:**

```python
from itertools import chain, groupby, islice, takewhile

# Flatten nested iterables
all_orders = chain.from_iterable(user.orders for user in users)

# Group by key (requires sorted input)
by_status = groupby(sorted(orders, key=lambda o: o.status), key=lambda o: o.status)

# Take first N items lazily
first_10 = islice(large_iterator, 10)

# Take while condition is true
recent = takewhile(lambda o: o.created_at > cutoff, sorted_orders)
```

Reference: [itertools documentation](https://docs.python.org/3/library/itertools.html)
