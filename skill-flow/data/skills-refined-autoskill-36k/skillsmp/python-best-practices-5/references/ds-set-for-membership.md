---
title: Use Set for O(1) Membership Testing
impact: HIGH
impactDescription: O(n) to O(1) lookups
tags: ds, set, membership, lookup
---

## Use Set for O(1) Membership Testing

List membership testing (`in`) is O(n). Set membership testing is O(1). Convert lists to sets when performing repeated lookups.

**Incorrect (O(n) per lookup, O(n×m) total):**

```python
def filter_allowed_users(users: list[User], allowed_ids: list[int]) -> list[User]:
    return [user for user in users if user.id in allowed_ids]
    # 10K users × 1K allowed = 10M comparisons
```

**Correct (O(1) per lookup, O(n) total):**

```python
def filter_allowed_users(users: list[User], allowed_ids: list[int]) -> list[User]:
    allowed_set = set(allowed_ids)  # O(m) one-time cost
    return [user for user in users if user.id in allowed_set]
    # 10K users × O(1) = 10K comparisons
```

**Note:** Set creation is O(m). Use sets when lookup count exceeds set size, or when the set can be reused.

Reference: [Time complexity of Python operations](https://wiki.python.org/moin/TimeComplexity)
