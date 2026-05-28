---
title: Stream Large Files Instead of Loading Into Memory
impact: CRITICAL
impactDescription: O(1) memory instead of O(n), prevents OOM errors
tags: io, streaming, memory, large-files
---

## Stream Large Files Instead of Loading Into Memory

Loading entire files into memory for processing causes memory spikes and potential OOM errors. Stream files line-by-line or in chunks to maintain constant memory usage.

**Incorrect (loads entire file into memory):**

```python
def process_log_file(filepath: str) -> int:
    with open(filepath, "r") as f:
        lines = f.readlines()  # 10GB file = 10GB+ memory
    return sum(1 for line in lines if "ERROR" in line)
```

**Correct (streams line by line, O(1) memory):**

```python
def process_log_file(filepath: str) -> int:
    error_count = 0
    with open(filepath, "r") as f:
        for line in f:  # File object is an iterator
            if "ERROR" in line:
                error_count += 1
    return error_count
```

**Alternative (chunked binary reading):**

```python
def calculate_checksum(filepath: str) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):  # 8KB chunks
            hasher.update(chunk)
    return hasher.hexdigest()
```

Reference: [Python I/O documentation](https://docs.python.org/3/tutorial/inputoutput.html)
