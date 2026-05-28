---
name: performance
description:
  Optimize code for speed and efficiency. Use this skill when profiling, identifying bottlenecks, or
  improving performance. Covers profiling tools, common patterns, and optimization strategies.
---

# Performance Optimization

Guidance for identifying and fixing performance bottlenecks.

## Core Principle

**Measure first, optimize second.** Never optimize without profiling data.

## Profiling Tools

### JavaScript/Node.js

```bash
# Node.js built-in profiler
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Chrome DevTools
node --inspect app.js
# Open chrome://inspect

# Clinic.js (recommended)
npx clinic doctor -- node app.js
npx clinic flame -- node app.js
```

### Python

```bash
# cProfile
python -m cProfile -s cumtime app.py

# py-spy (sampling profiler, low overhead)
py-spy record -o profile.svg -- python app.py

# line_profiler for line-by-line
kernprof -l -v script.py
```

### Go

```bash
# CPU profile
go test -cpuprofile=cpu.prof -bench=.
go tool pprof cpu.prof

# Memory profile
go test -memprofile=mem.prof -bench=.

# Built-in pprof server
import _ "net/http/pprof"
# Then: go tool pprof http://localhost:6060/debug/pprof/profile
```

### Rust

```bash
# Flamegraph
cargo install flamegraph
cargo flamegraph

# Criterion for benchmarks
# Add criterion to dev-dependencies
cargo bench
```

## Common Bottlenecks

### 1. N+1 Queries

```python
# Bad: N+1 queries
for user in users:
    posts = db.query(f"SELECT * FROM posts WHERE user_id = {user.id}")

# Good: Single query with join or batch
posts = db.query("SELECT * FROM posts WHERE user_id IN (...)")
```

### 2. Unnecessary Allocations

```javascript
// Bad: Creates new array each iteration
items
  .map((x) => x)
  .filter((x) => x.active)
  .map((x) => x.name);

// Good: Single pass
items.reduce((acc, x) => {
  if (x.active) acc.push(x.name);
  return acc;
}, []);
```

### 3. Blocking I/O

```python
# Bad: Sequential requests
for url in urls:
    response = requests.get(url)

# Good: Concurrent requests
import asyncio
import aiohttp

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*[session.get(url) for url in urls])
```

### 4. Missing Indexes

```sql
-- Check slow queries
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'x@y.com';

-- Add index
CREATE INDEX idx_users_email ON users(email);
```

### 5. Memory Leaks

```javascript
// Bad: Event listener never removed
element.addEventListener("click", handler);

// Good: Clean up
element.addEventListener("click", handler);
// Later:
element.removeEventListener("click", handler);
```

## Optimization Strategies

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(n):
    # ...
```

### Lazy Loading

```javascript
// Load on demand
const HeavyComponent = lazy(() => import("./HeavyComponent"));
```

### Pagination

```sql
-- Don't load everything
SELECT * FROM items LIMIT 20 OFFSET 40;

-- Or cursor-based for large datasets
SELECT * FROM items WHERE id > :last_id LIMIT 20;
```

### Connection Pooling

```python
# Reuse database connections
from sqlalchemy import create_engine
engine = create_engine(url, pool_size=10, max_overflow=20)
```

### Batching

```javascript
// Bad: Individual inserts
for (const item of items) {
  await db.insert(item);
}

// Good: Batch insert
await db.insertMany(items);
```

## Performance Checklist

- [ ] Profiled before optimizing
- [ ] Identified actual bottleneck (not guessing)
- [ ] Database queries have appropriate indexes
- [ ] No N+1 query problems
- [ ] Heavy computations are cached where appropriate
- [ ] Large lists are paginated
- [ ] I/O operations are concurrent when possible
- [ ] Memory usage is bounded
- [ ] Benchmarks exist for critical paths
