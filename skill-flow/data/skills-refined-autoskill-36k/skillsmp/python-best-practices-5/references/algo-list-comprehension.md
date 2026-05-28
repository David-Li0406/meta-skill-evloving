---
title: Use List Comprehensions Over Manual Loops
impact: MEDIUM-HIGH
impactDescription: 2-3× faster than equivalent for loop
tags: algo, list-comprehension, loops, performance
---

## Use List Comprehensions Over Manual Loops

List comprehensions are optimized in CPython and run faster than equivalent `for` loops with `append()`. They also produce cleaner, more readable code.

**Incorrect (manual loop with append):**

```python
def get_order_totals(orders: list[Order]) -> list[float]:
    totals = []
    for order in orders:
        totals.append(order.quantity * order.unit_price)
    return totals
```

**Correct (list comprehension):**

```python
def get_order_totals(orders: list[Order]) -> list[float]:
    return [order.quantity * order.unit_price for order in orders]
```

**With conditional filtering:**

```python
def get_high_value_totals(orders: list[Order]) -> list[float]:
    return [
        order.quantity * order.unit_price
        for order in orders
        if order.quantity * order.unit_price > 1000
    ]
```

**When to use a regular loop:**
- Complex logic with multiple statements per iteration
- Need to break early or handle exceptions per item
- Side effects during iteration

Reference: [List comprehension documentation](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
