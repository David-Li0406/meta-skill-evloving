# Performance Checklist

Deep-dive performance review. Reference this when performance concerns are detected.

---

## 1. Database & Queries

### N+1 Query Problem

The most common performance issue. Occurs when fetching related data in a loop.

```python
# BAD: N+1 queries
users = db.query("SELECT * FROM users")
for user in users:
    orders = db.query(f"SELECT * FROM orders WHERE user_id = {user.id}")
    # 1 query for users + N queries for orders

# GOOD: Single query with JOIN or batch
users_with_orders = db.query("""
    SELECT u.*, o.*
    FROM users u
    LEFT JOIN orders o ON o.user_id = u.id
""")

# GOOD: Batch query
user_ids = [u.id for u in users]
orders = db.query("SELECT * FROM orders WHERE user_id IN (?)", user_ids)
```

### Check For

- [ ] Queries inside loops
- [ ] Missing indexes on frequently queried columns
- [ ] `SELECT *` when only specific columns needed
- [ ] Missing pagination on list queries
- [ ] Unbounded queries (`LIMIT` missing)

### ORM Pitfalls

```python
# BAD: Lazy loading in loop (SQLAlchemy)
for user in users:
    print(user.orders)  # Each triggers a query!

# GOOD: Eager loading
users = session.query(User).options(joinedload(User.orders)).all()
```

---

## 2. Memory

### Large Data in Memory

- [ ] Loading entire datasets when streaming possible
- [ ] Accumulating data in lists without bounds
- [ ] Large file reads into memory
- [ ] Caching without eviction policy

```python
# BAD: Load all into memory
data = list(huge_generator())  # Could be GBs!

# GOOD: Stream/iterate
for item in huge_generator():
    process(item)

# BAD: Unbounded cache
cache = {}
def get_user(id):
    if id not in cache:
        cache[id] = fetch_user(id)  # Grows forever!
    return cache[id]

# GOOD: Bounded cache
from functools import lru_cache
@lru_cache(maxsize=1000)
def get_user(id):
    return fetch_user(id)
```

### Memory Leaks

- [ ] Event listeners not removed
- [ ] Timers/intervals not cleared
- [ ] Subscriptions not unsubscribed
- [ ] Closures holding large objects
- [ ] Global state accumulating data

```typescript
// BAD: Listener never removed
element.addEventListener('click', handler);

// GOOD: Clean up
const handler = () => { ... };
element.addEventListener('click', handler);
// Later:
element.removeEventListener('click', handler);

// BAD: Interval never cleared
setInterval(tick, 1000);

// GOOD: Clear on cleanup
const intervalId = setInterval(tick, 1000);
// Later:
clearInterval(intervalId);
```

---

## 3. Algorithms & Data Structures

### Time Complexity

| Operation | Array | Set/Map | Consider When |
|-----------|-------|---------|---------------|
| Lookup by value | O(n) | O(1) | Frequent lookups |
| Insert | O(1) | O(1) | - |
| Remove by value | O(n) | O(1) | Frequent removals |
| Check existence | O(n) | O(1) | Membership tests |

```typescript
// BAD: O(n) lookup in loop = O(n²)
for (const item of items) {
    if (blocklist.includes(item.id)) { ... }  // O(n) each time
}

// GOOD: O(1) lookup with Set
const blockSet = new Set(blocklist);
for (const item of items) {
    if (blockSet.has(item.id)) { ... }  // O(1) each time
}
```

### Check For

- [ ] Array `.includes()` / `.find()` in loops
- [ ] Nested loops on large datasets
- [ ] String concatenation in loops
- [ ] Repeated expensive calculations

```python
# BAD: String concat in loop - O(n²)
result = ""
for s in strings:
    result += s

# GOOD: Join - O(n)
result = "".join(strings)
```

---

## 4. Network & I/O

### Parallel vs Sequential

```typescript
// BAD: Sequential (total time = sum of all)
const user = await getUser();
const orders = await getOrders();
const settings = await getSettings();

// GOOD: Parallel (total time = max of all)
const [user, orders, settings] = await Promise.all([
    getUser(),
    getOrders(),
    getSettings(),
]);
```

### Batching

```typescript
// BAD: Many small requests
for (const id of ids) {
    await api.getItem(id);
}

// GOOD: Batch request
await api.getItems(ids);
```

### Check For

- [ ] Sequential awaits that could be parallel
- [ ] Many small API calls instead of batched
- [ ] Missing request deduplication
- [ ] No request caching
- [ ] Synchronous file I/O blocking event loop

---

## 5. Rendering (Frontend)

### React-Specific

- [ ] Unnecessary re-renders (use React DevTools Profiler)
- [ ] Large lists without virtualization
- [ ] Expensive calculations in render
- [ ] Missing `key` props or using index as key
- [ ] Context causing cascade re-renders

```tsx
// BAD: Recalculates every render
function Component({ items }) {
    const sorted = items.sort((a, b) => a.name.localeCompare(b.name));
    return <List items={sorted} />;
}

// GOOD: Memoize expensive calculation
function Component({ items }) {
    const sorted = useMemo(
        () => [...items].sort((a, b) => a.name.localeCompare(b.name)),
        [items]
    );
    return <List items={sorted} />;
}

// BAD: Large list without virtualization
<ul>
    {items.map(item => <ListItem key={item.id} {...item} />)}
</ul>

// GOOD: Virtualized (react-window, react-virtualized)
<VirtualList
    height={400}
    itemCount={items.length}
    itemSize={50}
    itemData={items}
>
    {Row}
</VirtualList>
```

### General DOM

- [ ] Layout thrashing (read/write DOM in loop)
- [ ] Forced synchronous layouts
- [ ] Large DOM trees
- [ ] Unoptimized images

---

## 6. Caching

### Where to Cache

| Layer | What | How |
|-------|------|-----|
| Browser | Static assets | Cache headers, CDN |
| API | Responses | Redis, in-memory |
| Database | Query results | Query cache, materialized views |
| Application | Computed values | `lru_cache`, memoization |

### Cache Invalidation

- [ ] TTL (time-to-live) appropriate
- [ ] Invalidation strategy defined
- [ ] Cache stampede prevention
- [ ] Stale data acceptable?

```python
# Simple TTL cache
from functools import lru_cache
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=300)  # 5 min TTL

def get_user(id):
    if id in cache:
        return cache[id]
    user = fetch_user(id)
    cache[id] = user
    return user
```

---

## 7. Async & Concurrency

### Blocking Operations

- [ ] Sync I/O in async code
- [ ] CPU-intensive work blocking event loop
- [ ] Missing worker threads for heavy computation

```typescript
// BAD: Blocking in async context
app.get('/process', async (req, res) => {
    const result = heavyCpuWork(req.body);  // Blocks!
    res.json(result);
});

// GOOD: Offload to worker
import { Worker } from 'worker_threads';
app.get('/process', async (req, res) => {
    const result = await runInWorker(heavyCpuWork, req.body);
    res.json(result);
});
```

### Connection Pools

- [ ] Database connections pooled
- [ ] HTTP client reuses connections
- [ ] Pool size appropriate for workload

```python
# GOOD: Connection pooling
from sqlalchemy import create_engine
engine = create_engine(url, pool_size=10, max_overflow=20)
```

---

## 8. Bundle Size (Frontend)

### Check For

- [ ] Tree shaking enabled
- [ ] Code splitting for routes
- [ ] Dynamic imports for heavy components
- [ ] No duplicate dependencies
- [ ] Minification enabled

```typescript
// BAD: Import entire library
import _ from 'lodash';
_.debounce(fn, 300);

// GOOD: Import only what's needed
import debounce from 'lodash/debounce';
debounce(fn, 300);

// GOOD: Dynamic import
const HeavyComponent = lazy(() => import('./HeavyComponent'));
```

---

## Severity Guide

| Finding | Severity |
|---------|----------|
| N+1 query in hot path | Warning |
| Unbounded query (no LIMIT) | Warning |
| Memory leak | Warning |
| O(n²) algorithm on large data | Warning |
| Sequential network calls (could be parallel) | Info |
| Missing pagination | Warning |
| Large bundle size | Info |
| Missing caching opportunity | Info |
| Expensive render without memo | Info |
| Blocking I/O in async | Warning |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Database queries | EXPLAIN ANALYZE, query logging |
| Memory | Chrome DevTools, py-spy, heaptrack |
| CPU profiling | Chrome DevTools, cProfile, perf |
| Bundle analysis | webpack-bundle-analyzer, source-map-explorer |
| Network | Chrome DevTools Network tab, Lighthouse |
| React rendering | React DevTools Profiler |
