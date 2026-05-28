---
title: Use Built-in Functions Over Manual Implementation
impact: MEDIUM-HIGH
impactDescription: 5-20× faster, C-optimized implementations
tags: algo, builtins, sum, max, min, any, all
---

## Use Built-in Functions Over Manual Implementation

Built-in functions like `sum()`, `max()`, `min()`, `any()`, `all()` are implemented in C and significantly outperform Python loop equivalents.

**Incorrect (manual sum implementation):**

```python
def calculate_total_revenue(orders: list[Order]) -> float:
    total = 0
    for order in orders:
        total += order.total
    return total
```

**Correct (built-in sum):**

```python
def calculate_total_revenue(orders: list[Order]) -> float:
    return sum(order.total for order in orders)
```

**More built-in examples:**

```python
# Max/min with key function
highest_order = max(orders, key=lambda o: o.total)
oldest_user = min(users, key=lambda u: u.created_at)

# any/all for boolean checks (short-circuit)
has_admin = any(user.is_admin for user in users)  # Stops at first True
all_verified = all(user.verified for user in users)  # Stops at first False

# sorted with key
by_date = sorted(orders, key=lambda o: o.created_at, reverse=True)
```

Reference: [Built-in functions](https://docs.python.org/3/library/functions.html)
