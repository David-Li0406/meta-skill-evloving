# Optimization Patterns Reference

Comprehensive optimization patterns for different scenarios.

## Algorithm Optimizations

### Array/List Operations

```javascript
// Finding an item - O(n) to O(1)
// BAD: Linear search every time
function findUser(users, id) {
  return users.find(u => u.id === id);  // O(n)
}

// GOOD: Build index once, lookup O(1)
const userIndex = new Map(users.map(u => [u.id, u]));
function findUser(id) {
  return userIndex.get(id);  // O(1)
}
```

```javascript
// Deduplication - O(n²) to O(n)
// BAD: includes() is O(n), called n times
function dedupe(arr) {
  return arr.filter((item, index) => arr.indexOf(item) === index);
}

// GOOD: Set operations are O(1)
function dedupe(arr) {
  return [...new Set(arr)];
}
```

```javascript
// Intersection - O(n×m) to O(n+m)
// BAD: Nested loops
function intersection(arr1, arr2) {
  return arr1.filter(item => arr2.includes(item));
}

// GOOD: Use Set for O(1) lookups
function intersection(arr1, arr2) {
  const set2 = new Set(arr2);
  return arr1.filter(item => set2.has(item));
}
```

### String Operations

```javascript
// String concatenation in loops
// BAD: Creates new string each iteration
let result = '';
for (const item of items) {
  result += item + ', ';  // O(n²) total
}

// GOOD: Use array join
const result = items.join(', ');  // O(n)

// Or StringBuilder pattern in Java/C#
StringBuilder sb = new StringBuilder();
for (String item : items) {
  sb.append(item).append(", ");
}
String result = sb.toString();
```

### Sorting Optimizations

```javascript
// Sorting with expensive comparisons
// BAD: Compute on every comparison
items.sort((a, b) => expensiveCompute(a) - expensiveCompute(b));

// GOOD: Schwartzian transform (decorate-sort-undecorate)
items
  .map(item => [expensiveCompute(item), item])  // Compute once
  .sort((a, b) => a[0] - b[0])                   // Compare cached
  .map(pair => pair[1]);                         // Unwrap
```

## Database Optimizations

### Query Optimization

```sql
-- SLOW: Full table scan
SELECT * FROM orders WHERE YEAR(created_at) = 2024;

-- FAST: Use index-friendly range
SELECT * FROM orders
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';
```

```sql
-- SLOW: OR can prevent index usage
SELECT * FROM users WHERE email = 'a@b.com' OR name = 'John';

-- FAST: UNION uses indexes on both
SELECT * FROM users WHERE email = 'a@b.com'
UNION
SELECT * FROM users WHERE name = 'John';
```

```sql
-- SLOW: LIKE with leading wildcard
SELECT * FROM users WHERE name LIKE '%john%';

-- FAST: Full-text search (if available)
SELECT * FROM users WHERE MATCH(name) AGAINST('john');

-- Or use trigram indexes (PostgreSQL)
CREATE INDEX idx_users_name_trgm ON users USING gin (name gin_trgm_ops);
```

### Batch Operations

```python
# SLOW: Individual inserts
for user in users:
    db.execute("INSERT INTO users (name) VALUES (%s)", (user.name,))

# FAST: Batch insert
values = [(u.name,) for u in users]
db.executemany("INSERT INTO users (name) VALUES (%s)", values)

# FASTEST: Bulk insert with COPY (PostgreSQL)
with open('users.csv', 'w') as f:
    for user in users:
        f.write(f"{user.name}\n")
db.execute("COPY users(name) FROM '/path/to/users.csv' CSV")
```

### Connection Management

```python
# BAD: New connection per query
def get_user(id):
    conn = create_connection()  # Expensive!
    result = conn.query("SELECT * FROM users WHERE id = %s", id)
    conn.close()
    return result

# GOOD: Connection pooling
pool = create_pool(min=5, max=20)

def get_user(id):
    with pool.connection() as conn:  # Reuses connection
        return conn.query("SELECT * FROM users WHERE id = %s", id)
```

## Caching Patterns

### Memoization

```javascript
// Simple memoization
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);

    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

// With TTL
function memoizeWithTTL(fn, ttlMs) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    const cached = cache.get(key);

    if (cached && Date.now() < cached.expiry) {
      return cached.value;
    }

    const result = fn.apply(this, args);
    cache.set(key, { value: result, expiry: Date.now() + ttlMs });
    return result;
  };
}
```

### Request Deduplication

```javascript
// Dedupe concurrent requests for same resource
const pending = new Map();

async function fetchWithDedupe(url) {
  if (pending.has(url)) {
    return pending.get(url);
  }

  const promise = fetch(url).then(r => r.json()).finally(() => {
    pending.delete(url);
  });

  pending.set(url, promise);
  return promise;
}

// Multiple concurrent calls to same URL = single fetch
await Promise.all([
  fetchWithDedupe('/api/user/1'),  // Fetches
  fetchWithDedupe('/api/user/1'),  // Reuses promise
  fetchWithDedupe('/api/user/1'),  // Reuses promise
]);
```

### Stale-While-Revalidate

```javascript
const cache = new Map();

async function fetchWithSWR(url, ttlMs = 60000) {
  const cached = cache.get(url);
  const now = Date.now();

  // Return stale data immediately, refresh in background
  if (cached && now < cached.staleAt) {
    // Fresh - just return
    return cached.data;
  }

  if (cached && now < cached.expireAt) {
    // Stale but valid - return and refresh
    refreshInBackground(url);
    return cached.data;
  }

  // Expired or missing - fetch and wait
  return fetchAndCache(url, ttlMs);
}

function refreshInBackground(url) {
  fetchAndCache(url).catch(console.error);
}

async function fetchAndCache(url, ttlMs = 60000) {
  const data = await fetch(url).then(r => r.json());
  cache.set(url, {
    data,
    staleAt: Date.now() + ttlMs,
    expireAt: Date.now() + ttlMs * 2
  });
  return data;
}
```

## Frontend Optimizations

### Virtualization

```javascript
// Only render visible items in long lists
import { VariableSizeList } from 'react-window';

function VirtualList({ items }) {
  const getItemSize = index => items[index].height || 50;

  return (
    <VariableSizeList
      height={600}
      itemCount={items.length}
      itemSize={getItemSize}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>
          <ListItem item={items[index]} />
        </div>
      )}
    </VariableSizeList>
  );
}
```

### Debouncing and Throttling

```javascript
// Debounce - wait until activity stops
function debounce(fn, delayMs) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn.apply(this, args), delayMs);
  };
}

// Use for: search input, resize handlers, form validation
const searchDebounced = debounce(search, 300);
input.addEventListener('input', e => searchDebounced(e.target.value));

// Throttle - limit execution rate
function throttle(fn, limitMs) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limitMs);
    }
  };
}

// Use for: scroll handlers, mouse move, API rate limiting
const scrollThrottled = throttle(handleScroll, 100);
window.addEventListener('scroll', scrollThrottled);
```

### Lazy Loading

```javascript
// Component lazy loading
const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <HeavyComponent />
    </Suspense>
  );
}

// Route-based code splitting
const routes = [
  { path: '/', component: lazy(() => import('./Home')) },
  { path: '/dashboard', component: lazy(() => import('./Dashboard')) },
  { path: '/settings', component: lazy(() => import('./Settings')) },
];
```

### Image Optimization

```javascript
// Intersection Observer for lazy loading
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.classList.remove('lazy');
      observer.unobserve(img);
    }
  });
}, { rootMargin: '50px' });

document.querySelectorAll('img.lazy').forEach(img => observer.observe(img));
```

## Async Optimizations

### Parallel Execution

```javascript
// BAD: Sequential (slow)
async function loadPageData(userId) {
  const user = await fetchUser(userId);       // 100ms
  const orders = await fetchOrders(userId);   // 150ms
  const reviews = await fetchReviews(userId); // 100ms
  return { user, orders, reviews };           // Total: 350ms
}

// GOOD: Parallel (fast)
async function loadPageData(userId) {
  const [user, orders, reviews] = await Promise.all([
    fetchUser(userId),
    fetchOrders(userId),
    fetchReviews(userId)
  ]);
  return { user, orders, reviews };  // Total: ~150ms (slowest)
}
```

### Streaming Responses

```javascript
// Process large data in chunks instead of loading all at once
async function processLargeFile(url) {
  const response = await fetch(url);
  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  let buffer = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    // Process complete lines
    const lines = buffer.split('\n');
    buffer = lines.pop(); // Keep incomplete line

    for (const line of lines) {
      await processLine(line);
    }
  }

  if (buffer) await processLine(buffer);
}
```

### Worker Threads

```javascript
// Offload CPU-intensive work to worker
// main.js
const worker = new Worker('worker.js');

worker.postMessage({ data: largeArray, operation: 'sort' });
worker.onmessage = (e) => {
  console.log('Sorted:', e.data);
};

// worker.js
self.onmessage = (e) => {
  const { data, operation } = e.data;
  if (operation === 'sort') {
    const sorted = data.sort((a, b) => a - b);  // CPU-intensive
    self.postMessage(sorted);
  }
};
```

## Memory Optimizations

### Object Pooling

```javascript
// Reuse objects instead of creating new ones
class ObjectPool {
  constructor(factory, initialSize = 10) {
    this.factory = factory;
    this.pool = Array(initialSize).fill(null).map(() => factory());
  }

  acquire() {
    return this.pool.pop() || this.factory();
  }

  release(obj) {
    this.reset(obj);  // Clear state
    this.pool.push(obj);
  }

  reset(obj) {
    // Override to reset object state
  }
}

// Usage for game entities, particles, etc.
const bulletPool = new ObjectPool(() => new Bullet(), 100);
const bullet = bulletPool.acquire();
// ... use bullet
bulletPool.release(bullet);  // Reuse instead of GC
```

### Weak References

```javascript
// Allow GC of cached items when memory is needed
const cache = new WeakMap();

function getCachedData(key) {
  if (cache.has(key)) {
    return cache.get(key);
  }

  const data = computeExpensiveData(key);
  cache.set(key, data);
  return data;
}

// When key object is no longer referenced elsewhere,
// both key and cached data can be garbage collected
```

### Avoiding Memory Leaks

```javascript
// Common leak: Forgotten intervals
class Component {
  startPolling() {
    this.interval = setInterval(() => this.fetch(), 1000);
  }

  // ALWAYS clean up
  destroy() {
    clearInterval(this.interval);
  }
}

// Common leak: Event listeners
class View {
  constructor() {
    this.handleClick = this.handleClick.bind(this);
    document.addEventListener('click', this.handleClick);
  }

  handleClick(e) { /* ... */ }

  // ALWAYS remove listeners
  destroy() {
    document.removeEventListener('click', this.handleClick);
  }
}

// Common leak: Closures holding references
function createHandler(element, data) {
  const hugeData = processData(data);  // 100MB

  // BAD: Closure holds hugeData forever
  element.onclick = () => {
    console.log(hugeData.summary);
  };

  // GOOD: Only capture what's needed
  const summary = hugeData.summary;
  element.onclick = () => {
    console.log(summary);
  };
}
```

## Network Optimizations

### Request Batching

```javascript
// Batch multiple requests into one
class RequestBatcher {
  constructor(batchFn, delayMs = 50) {
    this.batchFn = batchFn;
    this.delay = delayMs;
    this.pending = new Map();
    this.timeout = null;
  }

  async get(id) {
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.scheduleBatch();
    });
  }

  scheduleBatch() {
    if (this.timeout) return;
    this.timeout = setTimeout(() => this.executeBatch(), this.delay);
  }

  async executeBatch() {
    this.timeout = null;
    const batch = new Map(this.pending);
    this.pending.clear();

    try {
      const ids = [...batch.keys()];
      const results = await this.batchFn(ids);
      ids.forEach((id, i) => batch.get(id).resolve(results[i]));
    } catch (err) {
      batch.forEach(({ reject }) => reject(err));
    }
  }
}

// Usage
const userBatcher = new RequestBatcher(ids => fetchUsers(ids));

// These three calls become one batch request
const [user1, user2, user3] = await Promise.all([
  userBatcher.get(1),
  userBatcher.get(2),
  userBatcher.get(3)
]);
```

### Compression

```javascript
// Enable compression on Express
import compression from 'compression';
app.use(compression());

// Configure Nginx
gzip on;
gzip_types text/plain application/json application/javascript text/css;
gzip_min_length 1000;
```

### HTTP/2 and Resource Hints

```html
<!-- Preconnect to required origins -->
<link rel="preconnect" href="https://api.example.com">

<!-- Prefetch resources needed for next navigation -->
<link rel="prefetch" href="/next-page.js">

<!-- Preload critical resources -->
<link rel="preload" href="/fonts/main.woff2" as="font" crossorigin>
```
