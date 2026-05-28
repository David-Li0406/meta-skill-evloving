---
name: performance-optimization
description: Use this skill for optimizing application performance through profiling, benchmarking, and memory management across various programming languages.
---

# Performance Optimization

You are **Performance Optimization**, the application performance specialist.

## Optimization Areas

- Code profiling
- Database query optimization
- Frontend performance
- API response times
- Memory optimization
- Algorithm selection and data structures
- Caching strategies
- Async vs threading vs multiprocessing

## Profiling Tools

### Node.js
```javascript
// CPU profiling
const profiler = require('v8-profiler-next');
profiler.startProfiling('CPU profile');
// ... code to profile
const profile = profiler.stopProfiling();
profile.export((error, result) => {
  fs.writeFileSync('profile.cpuprofile', result);
});
```

### Python
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
```

## Database Optimization

### Query Analysis
```sql
-- PostgreSQL
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id;

-- Add index
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_users_created_at ON users(created_at);
```

### N+1 Query Prevention
```typescript
// ❌ Bad - N+1 queries
const users = await User.findAll();
for (const user of users) {
  user.orders = await Order.findAll({ where: { userId: user.id } });
}

// ✅ Good - Single query with eager loading
const users = await User.findAll({
  include: [{ model: Order }]
});
```

## Frontend Optimization

### Code Splitting
```typescript
// React lazy loading
const Dashboard = lazy(() => import('./Dashboard'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Dashboard />
    </Suspense>
  );
}
```

### Image Optimization
```html
<!-- Responsive images -->
<picture>
  <source srcset="image.webp" type="image/webp">
  <source srcset="image.jpg" type="image/jpeg">
  <img src="image.jpg" alt="Description" loading="lazy">
</picture>
```

## Caching Strategies

```python
from functools import lru_cache
import redis

# In-memory caching with lru_cache
@lru_cache(maxsize=128)
def expensive_computation(x: int, y: int) -> int:
    """Cache expensive computation."""
    print(f"Computing {x}^{y}")
    return x ** y

# Redis cache (requires redis-py)
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

## Performance Metrics

### Web Vitals
```typescript
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

getCLS(console.log);  // Cumulative Layout Shift
getFID(console.log);  // First Input Delay
getFCP(console.log);  // First Contentful Paint
getLCP(console.log);  // Largest Contentful Paint
getTTFB(console.log); // Time to First Byte
```

## Memory Management

### Profile Memory Usage
```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    """Profile memory usage."""
    data = []
    for i in range(100000):
        data.append(i * i)
    return data
```

### Use Generators for Memory Efficiency
```python
# ✅ GOOD: Generator yields one item at a time
def read_large_file_generator(filename: str):
    """Read file line by line."""
    with open(filename) as f:
        for line in f:
            yield line.strip()
```

## Performance Testing

### Benchmark with pytest-benchmark
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