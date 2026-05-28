---
name: performance-optimization
description: Use this skill when you need to optimize application performance through profiling, benchmarking, and memory management across various programming environments.
---

# Skill body

## Overview

This skill provides guidance on optimizing application performance, including profiling tools, caching strategies, and best practices for various programming languages.

## Optimization Areas

- Code profiling
- Database query optimization
- Frontend performance
- Memory management
- Caching strategies

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

### Redis Caching
```typescript
async function getUser(id: string) {
  const cacheKey = `user:${id}`;
  
  // Check cache
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);
  
  // Fetch from DB
  const user = await db.users.findById(id);
  
  // Store in cache (5 min TTL)
  await redis.setex(cacheKey, 300, JSON.stringify(user));
}
```

## Best Practices

### Profile Before Optimizing
Always profile your code before making optimizations to identify bottlenecks.

### Choose the Right Data Structure
Select appropriate data structures to improve performance, e.g., using sets for O(1) lookups instead of lists.

### Use Vectorization
Utilize libraries like NumPy or Polars for efficient data processing through vectorization.

### Async vs Threading vs Multiprocessing
Understand the differences and use cases for async programming, threading, and multiprocessing to optimize performance based on your application's needs.