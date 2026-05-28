---
name: performance-engineering
description: Use when optimizing performance, profiling bottlenecks, or architecting for scale
---

# Performance Engineering

Guidelines for building high-performance systems and optimizing existing code.

## When to Use

- Performance bottleneck investigation
- System architecture for scale
- Database query optimization
- Memory and CPU profiling
- Load testing and benchmarking
- Concurrent programming optimization

## Core Principles

1. **Measure First** - Profile before optimizing
2. **Focus on Bottlenecks** - Optimize the slowest parts
3. **Scalability by Design** - Plan for growth from the start
4. **Trade-offs Are Inevitable** - Balance performance, maintainability, cost
5. **Real-World Testing** - Use production-like workloads
6. **Continuous Monitoring** - Performance is ongoing, not one-time

## Performance Methodology

### 1. Measurement and Profiling
```python
import time
import cProfile
from contextlib import contextmanager

@contextmanager
def timer(operation_name: str):
    """Context manager for timing operations."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{operation_name}: {elapsed:.4f}s")

# CPU profiling
def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()
    
    expensive_operation()  # Your code here
    
    profiler.disable()
    profiler.print_stats(sort='cumulative')
```

## Algorithm Optimization

### Time Complexity Optimization
```python
# ❌ O(n²) - Nested loops
def find_duplicates_slow(numbers: list[int]) -> list[int]:
    duplicates = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j] and numbers[i] not in duplicates:
                duplicates.append(numbers[i])
    return duplicates

# ✅ O(n) - Hash set lookup
def find_duplicates_fast(numbers: list[int]) -> list[int]:
    seen = set()
    duplicates = set()
    
    for num in numbers:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)
    
    return list(duplicates)
```

## Memory Optimization

### Python Memory Patterns
```python
from typing import Iterator

# ❌ Memory-heavy list comprehension
def load_large_dataset_bad():
    return [process_item(i) for i in range(1000000)]

# ✅ Memory-efficient generator
def load_large_dataset_good() -> Iterator:
    for i in range(1000000):
        yield process_item(i)

# ✅ Use __slots__ for memory-efficient classes
class Point:
    __slots__ = ['x', 'y']
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
```

## Concurrency and Parallelism

### Python Async Optimization
```python
import asyncio
import aiohttp
from concurrent.futures import ProcessPoolExecutor
from typing import List

# ❌ Sequential I/O operations
def fetch_urls_slow(urls: List[str]) -> List[str]:
    import requests
    results = []
    for url in urls:
        response = requests.get(url)
        results.append(response.text)
    return results

# ✅ Async I/O operations
async def fetch_urls_fast(urls: List[str]) -> List[str]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def fetch_url(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        return await response.text()
```

### Rust Concurrency
```rust
use std::sync::Arc;
use tokio::sync::Semaphore;
use futures::future::join_all;

// ✅ Efficient async processing with concurrency limits
async fn process_items_concurrent<T>(items: Vec<T>) -> Vec<ProcessedItem>
where
    T: Send + Sync + 'static,
{
    let semaphore = Arc::new(Semaphore::new(10)); // Limit concurrency
    
    let tasks: Vec<_> = items
        .into_iter()
        .map(|item| {
            let semaphore = semaphore.clone();
            tokio::spawn(async move {
                let _permit = semaphore.acquire().await.unwrap();
                process_item(item).await
            })
        })
        .collect();
    
    join_all(tasks)
        .await
        .into_iter()
        .map(|result| result.unwrap())
        .collect()
}
```

## Database Performance

### Query Optimization
```sql
-- ❌ Inefficient query
SELECT u.*, p.title, COUNT(*) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.created_at > '2023-01-01'
GROUP BY u.id;

-- ✅ Optimized query with proper indexing
-- Index: CREATE INDEX idx_users_created_at ON users(created_at);
-- Index: CREATE INDEX idx_posts_user_id ON posts(user_id);
SELECT 
    u.id, 
    u.name, 
    u.email,
    COALESCE(pc.post_count, 0) as post_count
FROM users u
LEFT JOIN (
    SELECT user_id, COUNT(*) as post_count
    FROM posts
    GROUP BY user_id
) pc ON u.id = pc.user_id
WHERE u.created_at > '2023-01-01';
```

## Caching Strategies

### Multi-Level Caching
```python
import redis
from functools import wraps
from typing import Any, Callable
import hashlib

class CacheManager:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.memory_cache = {}  # L1 cache
        self.max_memory_items = 1000
    
    def cache_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate consistent cache key."""
        key_data = f"{func_name}:{args}:{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()

def cached(ttl: int = 3600):
    """Decorator for caching function results."""
    def decorator(func: Callable) -> Callable:
        cache = CacheManager()
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = cache.cache_key(func.__name__, args, kwargs)
            
            # Try cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute and cache
            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        
        return wrapper
    return decorator
```

## Performance Best Practices Checklist

### Algorithm & Data Structure
- [ ] Choose appropriate time complexity (O(log n) > O(n) > O(n²))
- [ ] Use efficient data structures (dict for lookups, deque for queues)
- [ ] Implement caching for expensive operations
- [ ] Prefer iterators/generators for large datasets
- [ ] Batch operations when possible

### Memory Management
- [ ] Profile memory usage regularly
- [ ] Use object pools for frequently allocated objects
- [ ] Implement pagination for large result sets
- [ ] Use streaming for file processing
- [ ] Clear references to large objects promptly

### Concurrency
- [ ] Use async I/O for network operations
- [ ] Implement connection pooling
- [ ] Limit concurrent operations (semaphores)
- [ ] Use process pools for CPU-intensive work
- [ ] Avoid sharing mutable state across threads

### Database
- [ ] Add proper indexes for query patterns
- [ ] Use connection pooling
- [ ] Implement query result caching
- [ ] Batch database operations
- [ ] Monitor slow queries

## Performance Commands

```bash
# Python profiling
python -m cProfile -s cumulative script.py

# Memory profiling
python -m memory_profiler script.py

# Rust profiling
cargo build --release
cargo flamegraph --bin mybin

# Database analysis
EXPLAIN ANALYZE SELECT ...;

# Load testing
ab -n 1000 -c 10 http://localhost:8080/api/test
```

## Remember

> Performance optimization is about understanding your system's bottlenecks, not premature optimization. Always measure before and after changes to ensure improvements are real and significant.