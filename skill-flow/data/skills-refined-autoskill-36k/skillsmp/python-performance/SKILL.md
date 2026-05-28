---
name: python-performance
description: Performance optimization, profiling, benchmarking, memory management
license: MIT
compatibility: opencode
metadata:
  audience: python-developers
  focus: performance
---

## What I do

I provide guidance on optimizing Python code performance, including:

- Profiling tools (cProfile, py-spy, memory_profiler)
- Performance profiling workflow
- Algorithm selection and data structures
- Vectorization with numpy/polars
- Caching strategies (functools.lru_cache, redis)
- Async vs threading vs multiprocessing
- Memory management and garbage collection
- Python interpreter optimizations (PyPy, CPython)
- Critical sections and bottlenecks
- Performance testing with pytest-benchmark

## When to use me

Use me when:
- Profiling slow code
- Optimizing performance-critical sections
- Choosing the right data structures
- Implementing caching strategies
- Deciding between async, threading, multiprocessing
- Reducing memory usage
- Benchmarking code changes
- Debugging performance issues

## Best Practices

### ✅ Profile Before Optimizing

```python
import cProfile
import pstats
from io import StringIO

def profile_function(func, *args, **kwargs):
    """Profile a function and display results."""
    pr = cProfile.Profile()
    pr.enable()
    result = func(*args, **kwargs)
    pr.disable()

    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(10)  # Top 10 functions
    print(s.getvalue())

    return result

# Usage
result = profile_function(process_large_dataset, data)
```

### ✅ Use Py-Spy for Real-Time Profiling

```bash
# Install py-spy
pip install py-spy

# Profile running Python process
py-spy top --pid <PID>

# Generate flamegraph
py-spy record -o profile.svg --pid <PID>

# Profile specific function
py-spy record -o profile.svg -- python script.py
```

### ✅ Choose the Right Data Structure

```python
from typing import List

# ❌ BAD: List for O(1) lookups
def find_in_list(items: List[str], target: str) -> bool:
    """O(n) lookup."""
    return target in items

# ✅ GOOD: Set for O(1) lookups
def find_in_set(items: set[str], target: str) -> bool:
    """O(1) lookup."""
    return target in items

# ✅ GOOD: Use deque for queue operations
from collections import deque

queue = deque()
queue.append(1)
queue.append(2)
item = queue.popleft()  # O(1)
```

### ✅ Use Vectorization with NumPy/Polars

```python
import numpy as np
import polars as pl

# ❌ BAD: Loop-based operations
def mean_squared_error_slow(y_true: list, y_pred: list) -> float:
    """Slow MSE calculation."""
    total = 0.0
    for true, pred in zip(y_true, y_pred):
        total += (true - pred) ** 2
    return total / len(y_true)

# ✅ GOOD: Vectorized operations
def mean_squared_error_fast(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Fast MSE calculation."""
    diff = y_true - y_pred
    return np.mean(diff ** 2)

# ✅ GOOD: Use polars for DataFrame operations
def process_data_fast(df: pl.DataFrame) -> pl.DataFrame:
    """Fast DataFrame processing."""
    return (
        df.lazy()
        .filter(pl.col("status") == "active")
        .with_columns([
            (pl.col("price") * pl.col("quantity")).alias("total")
        ])
        .collect()
    )
```

### ✅ Use Caching Strategies

```python
from functools import lru_cache
import hashlib
import pickle
from typing import Any

# In-memory caching with lru_cache
@lru_cache(maxsize=128)
def expensive_computation(x: int, y: int) -> int:
    """Cache expensive computation."""
    print(f"Computing {x}^{y}")
    return x ** y

# Custom disk cache
class DiskCache:
    """Disk-based cache for large results."""

    def __init__(self, cache_dir: str):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path."""
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{hash_key}.cache"

    def get(self, key: str) -> Any:
        """Get cached value."""
        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        return None

    def set(self, key: str, value: Any) -> None:
        """Set cached value."""
        cache_path = self._get_cache_path(key)
        with open(cache_path, 'wb') as f:
            pickle.dump(value, f)

# Redis cache (requires redis-py)
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_with_cache(key: str, ttl: int = 3600):
    """Get value from cache or compute and store."""
    cached = redis_client.get(key)
    if cached is not None:
        return pickle.loads(cached)

    # Compute and cache
    result = expensive_computation()
    redis_client.setex(key, ttl, pickle.dumps(result))
    return result
```

### ✅ Use Generators for Memory Efficiency

```python
# ❌ BAD: List stores all data in memory
def read_large_file_list(filename: str) -> list[str]:
    """Read entire file into memory."""
    with open(filename) as f:
        return [line.strip() for line in f]

# ✅ GOOD: Generator yields one item at a time
def read_large_file_generator(filename: str):
    """Read file line by line."""
    with open(filename) as f:
        for line in f:
            yield line.strip()

# Usage: Process large files efficiently
for line in read_large_file_generator("large_file.txt"):
    process_line(line)  # Low memory usage
```

### ✅ Optimize Database Queries

```python
# ❌ BAD: N+1 query problem
def get_users_with_posts_bad():
    users = User.objects.all()
    for user in users:
        posts = user.posts.all()  # N queries
        print(f"{user.name}: {posts.count()} posts")

# ✅ GOOD: Use select_related/prefetch_related
def get_users_with_posts_good():
    users = User.objects.prefetch_related('posts').all()
    for user in users:
        # No additional queries
        print(f"{user.name}: {user.posts.count()} posts")

# ✅ GOOD: Use count for efficient counting
def get_post_count():
    count = Post.objects.count()  # Efficient COUNT(*)
    return count
```

### ✅ Use Context Managers for Resource Management

```python
# ❌ BAD: Resource not properly managed
def read_file_bad(filename: str) -> str:
    f = open(filename)
    content = f.read()
    # File might not close if exception occurs
    f.close()
    return content

# ✅ GOOD: Context manager ensures cleanup
def read_file_good(filename: str) -> str:
    with open(filename) as f:
        return f.read()

# Async context managers
async def fetch_data(session):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

### ✅ Benchmark with pytest-benchmark

```python
import pytest

def test_sorting(benchmark):
    """Benchmark sorting algorithms."""
    data = list(range(1000, 0, -1))

    def sort_data():
        return sorted(data)

    result = benchmark(sort_data)
    assert result == sorted(data)
```

### ✅ Use String Join Instead of Concatenation

```python
# ❌ BAD: O(n^2) complexity
def build_string_bad(items: list[str]) -> str:
    result = ""
    for item in items:
        result += item  # Creates new string each time
    return result

# ✅ GOOD: O(n) complexity
def build_string_good(items: list[str]) -> str:
    return "".join(items)

# ✅ GOOD: Use f-strings for formatting
def format_message(name: str, age: int) -> str:
    return f"Hello, {name}! You are {age} years old."
```

### ✅ Offload CPU-Bound Work to Processes

```python
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

def cpu_bound_task(data):
    """CPU-intensive computation."""
    return sum(x ** 2 for x in data)

# ❌ BAD: Sequential processing
def process_sequential(datasets):
    results = []
    for data in datasets:
        results.append(cpu_bound_task(data))
    return results

# ✅ GOOD: Parallel processing with multiprocessing
def process_parallel(datasets):
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(cpu_bound_task, datasets))
    return results

# ✅ GOOD: Use multiprocessing pool
def process_with_pool(datasets):
    with multiprocessing.Pool() as pool:
        results = pool.map(cpu_bound_task, datasets)
    return results
```

## Memory Profiling

### ✅ Profile Memory Usage

```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    """Profile memory usage."""
    data = []
    for i in range(100000):
        data.append(i * i)
    return data

# Run with memory profiler
# python -m memory_profiler script.py
```

### ✅ Use Generators to Reduce Memory

```python
# ❌ BAD: Creates large list in memory
def squares_list(n: int) -> list[int]:
    return [i ** 2 for i in range(n)]

# ✅ GOOD: Generator uses minimal memory
def squares_generator(n: int):
    for i in range(n):
        yield i ** 2

# Usage
for square in squares_generator(1000000):
    process(square)  # Low memory footprint
```

## Performance Testing

### ✅ Use pytest-benchmark

```python
import pytest
from typing import Callable

def benchmark_sorting(
    benchmark: Callable,
    sort_func: Callable
) -> None:
    """Benchmark sorting function."""
    data = list(range(1000, 0, -1))

    def sort():
        return sort_func(data)

    result = benchmark(sort)
    assert result == sorted(data)

def test_builtin_sort(benchmark):
    """Benchmark built-in sort."""
    benchmark_sorting(benchmark, sorted)

def test_custom_sort(benchmark):
    """Benchmark custom sort."""
    benchmark_sorting(benchmark, custom_sort)
```

## Common Pitfalls

### ❌ Don't Optimize Without Profiling

```python
# BAD: Premature optimization
def fast_function(data):
    # Complex optimizations before knowing bottleneck
    return sum(map(lambda x: x * 2, data))

# GOOD: Profile first, then optimize
def optimized_function(data):
    # After profiling, optimize actual bottleneck
    return sum(x * 2 for x in data)
```

### ❌ Don't Use Global Variables

```python
# BAD: Global variable causes cache misses
CACHE = {}

def get_value(key):
    if key in CACHE:
        return CACHE[key]
    return compute_value(key)

# GOOD: Pass data as arguments
def get_value(key, cache):
    if key in cache:
        return cache[key]
    return compute_value(key)
```

### ❌ Don't Use Strings for Accumulation

```python
# BAD: O(n^2) string concatenation
def build_html(elements):
    html = ""
    for el in elements:
        html += f"<div>{el}</div>"
    return html

# GOOD: O(n) with join
def build_html(elements):
    parts = [f"<div>{el}</div>" for el in elements]
    return "".join(parts)
```

## Performance Optimization Workflow

1. **Measure First**: Profile before optimizing
2. **Identify Bottlenecks**: Find hot paths
3. **Optimize Algorithms**: Choose better algorithms/data structures
4. **Vectorize**: Use numpy/polars for numerical operations
5. **Cache**: Use caching for expensive computations
6. **Parallelize**: Use multiprocessing for CPU-bound work
7. **Profile Again**: Verify improvements
8. **Iterate**: Repeat until satisfactory

## Choosing the Right Approach

| Use Case | Recommended Approach |
|----------|---------------------|
| I/O-bound operations | asyncio |
| CPU-bound operations | multiprocessing |
| Small data (< 1GB) | pandas |
| Large data (> 1GB) | polars |
| Numerical computing | numpy |
| Low-latency requirements | compiled extensions (cython, numba) |
| Memory-constrained | generators, lazy evaluation |

## References

- Python profiling docs: https://docs.python.org/3/library/profile.html
- py-spy documentation: https://github.com/benfred/py-spy
- NumPy performance guide: https://numpy.org/doc/stable/reference/performance.html
- Python optimization tips: https://wiki.python.org/moin/PythonSpeed/PerformanceTips
- pytest-benchmark: https://pytest-benchmark.readthedocs.io/
