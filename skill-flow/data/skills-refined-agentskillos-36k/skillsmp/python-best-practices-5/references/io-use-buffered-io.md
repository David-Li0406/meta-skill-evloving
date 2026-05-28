---
title: Use Buffered I/O for Frequent Small Writes
impact: CRITICAL
impactDescription: reduces syscalls by 100-1000×, 10× throughput improvement
tags: io, buffering, writes, syscalls
---

## Use Buffered I/O for Frequent Small Writes

Each unbuffered write triggers a system call with kernel transition overhead. Buffered I/O batches writes, dramatically reducing syscall frequency.

**Incorrect (unbuffered writes, syscall per line):**

```python
def write_metrics(metrics: list[Metric], filepath: str):
    with open(filepath, "w", buffering=1) as f:  # Line buffered
        for metric in metrics:
            f.write(f"{metric.name},{metric.value}\n")
            # 10000 metrics = 10000 syscalls
```

**Correct (buffered writes, batched syscalls):**

```python
def write_metrics(metrics: list[Metric], filepath: str):
    with open(filepath, "w") as f:  # Default buffering ~8KB
        for metric in metrics:
            f.write(f"{metric.name},{metric.value}\n")
        # Writes batched into ~8KB chunks, ~100× fewer syscalls
```

**Alternative (explicit buffer size for large writes):**

```python
def write_large_dataset(records: list[dict], filepath: str):
    with open(filepath, "w", buffering=65536) as f:  # 64KB buffer
        for record in records:
            f.write(json.dumps(record) + "\n")
```

**Note:** Use `buffering=1` (line buffered) only when you need immediate line-by-line visibility, such as log files read by external tools in real-time.

Reference: [Python open() documentation](https://docs.python.org/3/library/functions.html#open)
