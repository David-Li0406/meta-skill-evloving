# Performance Code Review Checklist

## Algorithm Complexity

### 1. Time Complexity (Big O)
**Check:**
- [ ] Algorithm complexity appropriate for expected data size
- [ ] Avoid O(n²) or worse for large datasets
- [ ] Consider amortized complexity for variable workloads

**Common Complexities:**
- O(1) - Constant: Hash table lookup, array access
- O(log n) - Logarithmic: Binary search
- O(n) - Linear: Single loop, array scan
- O(n log n) - Linearithmic: Efficient sorting (merge sort, quicksort)
- O(n²) - Quadratic: Nested loops
- O(2ⁿ) - Exponential: Recursive fibonacci (avoid!)

**Examples:**
```typescript
// Bad - O(n²) for duplicate detection
function hasDuplicates(arr: number[]) {
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) return true;
    }
  }
  return false;
}

// Good - O(n) using Set
function hasDuplicates(arr: number[]) {
  return new Set(arr).size !== arr.length;
}
```

### 2. Nested Loops
**Check:**
- [ ] Avoid unnecessary nested iterations
- [ ] Can nested loops be replaced with hash maps?
- [ ] Early termination conditions present?

**Examples:**
```typescript
// Bad - O(n²)
for (const user of users) {
  for (const order of orders) {
    if (order.userId === user.id) {
      user.orders.push(order);
    }
  }
}

// Good - O(n) with Map
const ordersByUser = new Map();
for (const order of orders) {
  if (!ordersByUser.has(order.userId)) {
    ordersByUser.set(order.userId, []);
  }
  ordersByUser.get(order.userId).push(order);
}
for (const user of users) {
  user.orders = ordersByUser.get(user.id) || [];
}
```

---

## Data Structure Selection

### 3. Choose Appropriate Data Structures
**Check:**
- [ ] Map/Set for lookups (O(1)) vs Array (O(n))
- [ ] Array for ordered iteration vs Set for uniqueness
- [ ] Appropriate collection type for use case

**Data Structure Performance:**

| Operation | Array | Set | Map |
|-----------|-------|-----|-----|
| Add/Insert | O(1)* | O(1) | O(1) |
| Remove | O(n) | O(1) | O(1) |
| Search | O(n) | O(1) | O(1) |
| Iterate | O(n) | O(n) | O(n) |

*Array push is O(1), but insert at position is O(n)

**Examples:**
```typescript
// Bad - Array for lookups
const userIds = [1, 2, 3, 4, 5, ...]; // 10,000 IDs
if (userIds.includes(targetId)) { // O(n) scan every time
  // ...
}

// Good - Set for lookups
const userIds = new Set([1, 2, 3, 4, 5, ...]); // 10,000 IDs
if (userIds.has(targetId)) { // O(1) lookup
  // ...
}
```

---

## Memory Management

### 4. Memory Leaks
**Check:**
- [ ] Event listeners removed when no longer needed
- [ ] Timers/intervals cleared
- [ ] Large data structures released when done
- [ ] Circular references avoided or handled

**Examples:**
```typescript
// Bad - Memory leak
class Component {
  constructor() {
    window.addEventListener('resize', this.handleResize);
  }
  // No cleanup - listener persists after component destroyed
}

// Good - Cleanup
class Component {
  constructor() {
    this.handleResize = this.handleResize.bind(this);
    window.addEventListener('resize', this.handleResize);
  }

  destroy() {
    window.removeEventListener('resize', this.handleResize);
  }
}
```

### 5. Unnecessary Object Creation
**Check:**
- [ ] Objects not created in loops unnecessarily
- [ ] Reuse objects when possible
- [ ] Avoid creating temporary arrays/objects

**Examples:**
```typescript
// Bad - Creates new object every iteration
for (let i = 0; i < 1000; i++) {
  const config = { threshold: 100, enabled: true };
  processItem(items[i], config);
}

// Good - Reuse object
const config = { threshold: 100, enabled: true };
for (let i = 0; i < 1000; i++) {
  processItem(items[i], config);
}
```

### 6. Large Data Handling
**Check:**
- [ ] Streaming/pagination for large datasets
- [ ] Avoid loading entire dataset into memory
- [ ] Use cursors or generators for iteration

**Examples:**
```typescript
// Bad - Loads everything into memory
const allUsers = await db.users.findAll(); // 1 million users
return allUsers.filter(u => u.active);

// Good - Paginated query
const activeUsers = await db.users.find({ active: true })
  .limit(100)
  .skip(page * 100);
```

---

## Database Performance

### 7. N+1 Query Problem
**Check:**
- [ ] Queries batched or joined
- [ ] Eager loading used where appropriate
- [ ] No query in loop

**Examples:**
```typescript
// Bad - N+1 queries (1 + N queries for N users)
const users = await db.users.findAll();
for (const user of users) {
  user.posts = await db.posts.find({ userId: user.id }); // N queries!
}

// Good - Single query with join
const users = await db.users.findAll({
  include: [{ model: db.posts }]
});
```

### 8. Missing Database Indexes
**Check:**
- [ ] Indexes on frequently queried columns
- [ ] Indexes on foreign keys
- [ ] Composite indexes for multi-column queries
- [ ] Not over-indexing (indexes slow writes)

**Examples:**
```sql
-- Bad - No index on frequently queried column
SELECT * FROM orders WHERE customer_id = 123; -- Full table scan

-- Good - Add index
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

### 9. Inefficient Queries
**Check:**
- [ ] SELECT specific columns, not `SELECT *`
- [ ] Use appropriate WHERE clauses
- [ ] LIMIT results when possible
- [ ] Avoid functions in WHERE clause (prevents index use)

**Examples:**
```sql
-- Bad - Fetches all columns and rows
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- Good - Specific columns, indexed lookup
SELECT id, name, email FROM users WHERE email = 'user@example.com' LIMIT 1;
```

---

## Caching

### 10. Caching Opportunities
**Check:**
- [ ] Expensive computations cached
- [ ] Database query results cached when appropriate
- [ ] HTTP responses cached with proper headers
- [ ] CDN used for static assets

**Cache Levels:**
1. **In-memory**: Variables, class properties
2. **Application cache**: Redis, Memcached
3. **HTTP cache**: ETag, Cache-Control headers
4. **CDN cache**: CloudFlare, CloudFront

**Examples:**
```typescript
// Bad - Recalculates every time
function getMonthlyReport(userId: string) {
  const data = expensiveCalculation(userId); // Takes 5 seconds
  return data;
}

// Good - Cache results
const cache = new Map();
function getMonthlyReport(userId: string) {
  const cacheKey = `report:${userId}:${getCurrentMonth()}`;
  if (cache.has(cacheKey)) {
    return cache.get(cacheKey);
  }
  const data = expensiveCalculation(userId);
  cache.set(cacheKey, data);
  return data;
}
```

### 11. Memoization
**Check:**
- [ ] Pure functions with expensive computation memoized
- [ ] React components wrapped in `memo` when appropriate
- [ ] Use `useMemo`/`useCallback` for expensive operations

**Examples:**
```typescript
// Bad - Recalculates on every render
function Component({ data }) {
  const processed = expensiveOperation(data); // Runs every render
  return <div>{processed}</div>;
}

// Good - Memoized
import { useMemo } from 'react';
function Component({ data }) {
  const processed = useMemo(() => expensiveOperation(data), [data]);
  return <div>{processed}</div>;
}
```

---

## Network & I/O

### 12. Reduce Network Requests
**Check:**
- [ ] Batch multiple requests when possible
- [ ] Use connection pooling for databases
- [ ] Implement request coalescing/debouncing
- [ ] Use WebSockets for frequent updates

**Examples:**
```typescript
// Bad - Sequential requests
const user = await fetch('/api/user/1');
const posts = await fetch('/api/posts?userId=1');
const comments = await fetch('/api/comments?userId=1');

// Good - Parallel requests
const [user, posts, comments] = await Promise.all([
  fetch('/api/user/1'),
  fetch('/api/posts?userId=1'),
  fetch('/api/comments?userId=1')
]);
```

### 13. Payload Size
**Check:**
- [ ] Response payloads minimized
- [ ] Images compressed and optimized
- [ ] Gzip/Brotli compression enabled
- [ ] Unnecessary data not sent

---

## Async & Concurrency

### 14. Blocking Operations
**Check:**
- [ ] No synchronous I/O in async contexts
- [ ] Long operations don't block event loop
- [ ] Use async/await properly
- [ ] CPU-intensive work offloaded (workers, queues)

**Examples:**
```typescript
// Bad - Blocks event loop
const fs = require('fs');
const data = fs.readFileSync('large-file.txt'); // Blocks!

// Good - Non-blocking
const fs = require('fs').promises;
const data = await fs.readFile('large-file.txt');
```

### 15. Promise Management
**Check:**
- [ ] Promises resolved in parallel when possible
- [ ] Error handling for all promises
- [ ] No unhandled promise rejections
- [ ] Use `Promise.all` for independent operations

---

## Frontend Performance

### 16. React Re-renders
**Check:**
- [ ] Unnecessary re-renders avoided
- [ ] Component memoization used appropriately
- [ ] State updates batched
- [ ] Large lists virtualized

**Examples:**
```typescript
// Bad - Creates new object every render
function Component() {
  const style = { color: 'red' }; // New object each render
  return <Child style={style} />; // Child re-renders unnecessarily
}

// Good - Memoized or constant
const STYLE = { color: 'red' };
function Component() {
  return <Child style={STYLE} />;
}
```

### 17. Bundle Size
**Check:**
- [ ] Code splitting implemented
- [ ] Tree shaking enabled
- [ ] Unused dependencies removed
- [ ] Large libraries imported selectively

**Examples:**
```typescript
// Bad - Imports entire library
import _ from 'lodash';
const result = _.debounce(fn, 100);

// Good - Import only what's needed
import debounce from 'lodash/debounce';
const result = debounce(fn, 100);
```

### 18. Lazy Loading
**Check:**
- [ ] Routes lazy loaded
- [ ] Images lazy loaded
- [ ] Heavy components loaded on demand
- [ ] Critical CSS inlined, rest deferred

---

## General Optimization

### 19. Premature Optimization
**Avoid:**
- Optimizing before measuring
- Micro-optimizations that hurt readability
- Complex caching for rarely accessed data

**Do:**
- Profile first, optimize bottlenecks
- Measure impact of optimizations
- Optimize critical paths only

### 20. Resource Cleanup
**Check:**
- [ ] Database connections closed
- [ ] File handles closed
- [ ] WebSocket connections closed
- [ ] Resources released in finally blocks

**Examples:**
```typescript
// Bad - Connection not closed on error
const conn = await db.connect();
const result = await conn.query(sql); // May throw
conn.close();

// Good - Guaranteed cleanup
const conn = await db.connect();
try {
  const result = await conn.query(sql);
  return result;
} finally {
  await conn.close();
}
```

---

## Performance Measurement

### Tools & Techniques

**Browser DevTools:**
- Performance tab: Record and analyze runtime performance
- Network tab: Check request timing, payload sizes
- Lighthouse: Overall performance score and recommendations

**Node.js Profiling:**
```typescript
// Built-in profiler
node --prof app.js
node --prof-process isolate-*.log

// Chrome DevTools
node --inspect app.js
```

**Metrics to Track:**
- Time to First Byte (TTFB)
- First Contentful Paint (FCP)
- Largest Contentful Paint (LCP)
- Time to Interactive (TTI)
- API response times
- Database query times

---

## Quick Performance Audit

1. Are there nested loops over large datasets?
2. Are lookups using Maps/Sets instead of Arrays?
3. Are database queries optimized and indexed?
4. Is there an N+1 query problem?
5. Are expensive operations cached?
6. Are network requests batched or parallel?
7. Is the bundle size optimized?
8. Are resources properly cleaned up?
9. Are there unnecessary re-renders?
10. Have bottlenecks been profiled and measured?

---

## Performance Anti-Patterns

### 1. String Concatenation in Loops
```typescript
// Bad
let result = '';
for (let i = 0; i < 10000; i++) {
  result += items[i]; // Creates new string each iteration
}

// Good
const result = items.join('');
```

### 2. Regex in Tight Loops
```typescript
// Bad
for (const item of largeArray) {
  if (/pattern/.test(item)) { // Compiles regex every iteration
    // ...
  }
}

// Good
const pattern = /pattern/;
for (const item of largeArray) {
  if (pattern.test(item)) {
    // ...
  }
}
```

### 3. Unnecessary Cloning
```typescript
// Bad
function processItems(items) {
  const copy = JSON.parse(JSON.stringify(items)); // Expensive deep clone
  return copy.map(item => item.value);
}

// Good - No cloning needed
function processItems(items) {
  return items.map(item => item.value);
}
```
