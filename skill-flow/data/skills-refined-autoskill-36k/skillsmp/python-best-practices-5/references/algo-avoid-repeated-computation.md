---
title: Cache Expensive Computations in Loops
impact: MEDIUM-HIGH
impactDescription: eliminates N redundant calculations
tags: algo, caching, loops, optimization
---

## Cache Expensive Computations in Loops

Repeated computation inside loops multiplies cost. Hoist invariant calculations outside the loop or cache intermediate results.

**Incorrect (repeated computation inside loop):**

```python
def filter_recent_orders(orders: list[Order], days: int) -> list[Order]:
    return [
        order for order in orders
        if order.created_at > datetime.now() - timedelta(days=days)
        # datetime.now() and timedelta() called for each order
    ]
```

**Correct (computation hoisted outside loop):**

```python
def filter_recent_orders(orders: list[Order], days: int) -> list[Order]:
    cutoff = datetime.now() - timedelta(days=days)  # Computed once
    return [order for order in orders if order.created_at > cutoff]
```

**Alternative (cache attribute access):**

```python
def process_config_items(items: list[Item], config: Config) -> list[Result]:
    # Cache frequently accessed nested attributes
    threshold = config.settings.processing.threshold
    multiplier = config.settings.processing.multiplier

    return [
        Result(item.value * multiplier)
        for item in items
        if item.value > threshold
    ]
```

Reference: [Python Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)
