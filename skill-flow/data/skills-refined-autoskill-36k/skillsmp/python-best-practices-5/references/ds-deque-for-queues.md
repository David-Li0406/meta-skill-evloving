---
title: Use deque for O(1) Queue Operations
impact: HIGH
impactDescription: O(n) to O(1) for left operations
tags: ds, deque, queue, collections
---

## Use deque for O(1) Queue Operations

List `pop(0)` and `insert(0, x)` are O(n) operations requiring element shifting. `collections.deque` provides O(1) operations on both ends.

**Incorrect (O(n) for left operations):**

```python
def process_queue(tasks: list[Task]) -> None:
    while tasks:
        task = tasks.pop(0)  # O(n) - shifts all elements
        process(task)
        if task.spawn_subtask:
            tasks.insert(0, task.subtask)  # O(n) again
```

**Correct (O(1) for both ends):**

```python
from collections import deque

def process_queue(tasks: list[Task]) -> None:
    queue = deque(tasks)
    while queue:
        task = queue.popleft()  # O(1)
        process(task)
        if task.spawn_subtask:
            queue.appendleft(task.subtask)  # O(1)
```

**Alternative (bounded deque for fixed-size buffers):**

```python
# Automatically discards oldest items when full
recent_events: deque[Event] = deque(maxlen=1000)
recent_events.append(new_event)  # O(1), auto-evicts if full
```

Reference: [deque documentation](https://docs.python.org/3/library/collections.html#collections.deque)
