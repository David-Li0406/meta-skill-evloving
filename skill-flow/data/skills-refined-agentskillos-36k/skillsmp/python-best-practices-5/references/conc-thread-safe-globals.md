---
title: Use Thread-Safe Data Structures for Shared State
impact: MEDIUM
impactDescription: prevents race conditions and data corruption
tags: conc, threading, thread-safety, queue
---

## Use Thread-Safe Data Structures for Shared State

Regular Python data structures are not thread-safe. Use `queue.Queue`, `threading.Lock`, or thread-local storage for shared state.

**Incorrect (race condition on shared list):**

```python
results: list[Result] = []

def worker(task: Task) -> None:
    result = process(task)
    results.append(result)  # Race condition!

with ThreadPoolExecutor() as executor:
    executor.map(worker, tasks)
```

**Correct (thread-safe queue):**

```python
from queue import Queue

results: Queue[Result] = Queue()

def worker(task: Task) -> None:
    result = process(task)
    results.put(result)  # Thread-safe

with ThreadPoolExecutor() as executor:
    executor.map(worker, tasks)

# Collect results
all_results = [results.get() for _ in range(len(tasks))]
```

**Alternative (return values from executor):**

```python
def process_task(task: Task) -> Result:
    return process(task)

with ThreadPoolExecutor() as executor:
    results = list(executor.map(process_task, tasks))
```

Reference: [queue documentation](https://docs.python.org/3/library/queue.html)
