---
title: Use Generators for Lazy Evaluation
impact: HIGH
impactDescription: O(1) memory instead of O(n), processes any size dataset
tags: mem, generator, lazy-evaluation, iterator
---

## Use Generators for Lazy Evaluation

List comprehensions create the entire list in memory. Generator expressions yield items one at a time, using constant memory regardless of dataset size.

**Incorrect (creates entire list in memory):**

```python
def get_active_users(users: list[User]) -> list[User]:
    return [user for user in users if user.is_active]
    # 1M users with 100K active = 100K User objects in memory
```

**Correct (yields one at a time, O(1) memory):**

```python
def get_active_users(users: Iterable[User]) -> Iterator[User]:
    return (user for user in users if user.is_active)
    # Memory: 1 User object at a time

# Or with yield for complex logic
def get_active_users(users: Iterable[User]) -> Iterator[User]:
    for user in users:
        if user.is_active:
            yield user
```

**When to materialize:**

```python
# Only create list when you need random access or length
active_list = list(get_active_users(users))  # Explicit materialization
```

Reference: [Generator expressions](https://docs.python.org/3/howto/functional.html#generator-expressions-and-list-comprehensions)
