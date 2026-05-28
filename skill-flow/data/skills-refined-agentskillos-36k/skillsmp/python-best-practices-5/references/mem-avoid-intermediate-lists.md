---
title: Avoid Intermediate Lists in Pipelines
impact: HIGH
impactDescription: eliminates N intermediate allocations, O(1) vs O(n) memory
tags: mem, pipeline, intermediate-lists, chaining
---

## Avoid Intermediate Lists in Pipelines

Chaining list operations creates intermediate lists at each step. Use generator expressions or `itertools` to process data in a single pass without intermediate allocations.

**Incorrect (creates 3 intermediate lists):**

```python
def process_orders(orders: list[Order]) -> list[str]:
    pending = [o for o in orders if o.status == "pending"]  # List 1
    high_value = [o for o in pending if o.total > 1000]  # List 2
    emails = [o.customer_email for o in high_value]  # List 3
    return emails
```

**Correct (single pass, no intermediate lists):**

```python
def process_orders(orders: Iterable[Order]) -> Iterator[str]:
    return (
        order.customer_email
        for order in orders
        if order.status == "pending" and order.total > 1000
    )
```

**Note:** The return type changes from `list[str]` to `Iterator[str]`. If you need a concrete list, wrap with `list(process_orders(orders))`.

**Alternative (itertools for complex pipelines):**

```python
from itertools import filterfalse, islice

def process_orders(orders: Iterable[Order]) -> Iterator[str]:
    pending = (o for o in orders if o.status == "pending")
    high_value = (o for o in pending if o.total > 1000)
    return (o.customer_email for o in islice(high_value, 100))
```

Reference: [itertools documentation](https://docs.python.org/3/library/itertools.html)
