# Performance Patterns

Detailed patterns for performance issues by category.

## Algorithmic Complexity

### O(n²) Nested Loops

**Pattern**: Nested loops over collections that could be O(n).

```javascript
// SLOW - O(n²)
for (const user of users) {
  for (const order of orders) {
    if (order.userId === user.id) {
      // process
    }
  }
}

// FAST - O(n)
const ordersByUser = new Map();
for (const order of orders) {
  if (!ordersByUser.has(order.userId)) {
    ordersByUser.set(order.userId, []);
  }
  ordersByUser.get(order.userId).push(order);
}
for (const user of users) {
  const userOrders = ordersByUser.get(user.id) || [];
  // process
}
```

**Severity**: Major (on large datasets), Minor (on small fixed datasets)

### Repeated Expensive Operations

**Pattern**: Same expensive operation called multiple times.

```javascript
// SLOW
function processItems(items) {
  return items.map(item => {
    const config = loadConfigFromDisk(); // Called for each item!
    return transform(item, config);
  });
}

// FAST
function processItems(items) {
  const config = loadConfigFromDisk(); // Called once
  return items.map(item => transform(item, config));
}
```

**Severity**: Major

## Database Performance

### N+1 Query Problem

**Pattern**: One query per item instead of batched query.

```javascript
// SLOW - N+1 queries
const users = await User.findAll();
for (const user of users) {
  user.orders = await Order.findByUserId(user.id); // N queries!
}

// FAST - 2 queries
const users = await User.findAll();
const userIds = users.map(u => u.id);
const orders = await Order.findByUserIds(userIds);
const ordersByUser = groupBy(orders, 'userId');
users.forEach(u => u.orders = ordersByUser[u.id] || []);
```

**.NET Example**:
```csharp
// SLOW
foreach (var user in users) {
  user.Orders = await _db.Orders.Where(o => o.UserId == user.Id).ToListAsync();
}

// FAST - Include
var users = await _db.Users.Include(u => u.Orders).ToListAsync();
```

**Severity**: Critical (in hot paths), Major (otherwise)

### Missing Indexes

**Pattern**: Queries filtering on non-indexed columns.

**Signs**:
- WHERE clauses on columns without indexes
- JOIN conditions on non-indexed foreign keys
- ORDER BY on non-indexed columns

**Severity**: Major

### Unbounded Queries

**Pattern**: SELECT without LIMIT on potentially large tables.

```javascript
// DANGEROUS
const allUsers = await db.query('SELECT * FROM users');

// SAFE
const users = await db.query('SELECT * FROM users LIMIT 100 OFFSET 0');
```

**Severity**: Major

## Memory Issues

### Memory Leaks

**Patterns**:
- Event listeners not removed
- Closures holding large objects
- Growing caches without eviction
- Timers not cleared

```javascript
// LEAK - listener never removed
class Component {
  constructor() {
    window.addEventListener('resize', this.onResize);
  }
  // Missing: removeEventListener in cleanup
}

// LEAK - growing Map
const cache = new Map();
function getCached(key) {
  if (!cache.has(key)) {
    cache.set(key, expensiveComputation(key)); // Never evicts!
  }
  return cache.get(key);
}
```

**Severity**: Critical

### Large Object Allocation

**Pattern**: Creating large objects unnecessarily.

```javascript
// SLOW - creates new array each call
function getDefaults() {
  return [1, 2, 3, 4, 5, /* ... 1000 items */];
}

// FAST - reuse constant
const DEFAULTS = Object.freeze([1, 2, 3, 4, 5, /* ... */]);
function getDefaults() {
  return DEFAULTS;
}
```

**Severity**: Minor to Major

## Async/Await Performance

### Sequential Awaits (Waterfall)

**Pattern**: Awaiting independent operations sequentially.

```javascript
// SLOW - sequential (3 seconds)
const users = await fetchUsers();     // 1s
const orders = await fetchOrders();   // 1s
const products = await fetchProducts(); // 1s

// FAST - parallel (1 second)
const [users, orders, products] = await Promise.all([
  fetchUsers(),
  fetchOrders(),
  fetchProducts()
]);
```

**Severity**: Major

### Blocking Event Loop (Node.js)

**Pattern**: CPU-intensive work blocking the event loop.

```javascript
// BLOCKING
function processLargeFile(data) {
  for (let i = 0; i < data.length; i++) {
    // CPU-intensive processing
  }
}

// NON-BLOCKING
async function processLargeFile(data) {
  const CHUNK_SIZE = 1000;
  for (let i = 0; i < data.length; i += CHUNK_SIZE) {
    const chunk = data.slice(i, i + CHUNK_SIZE);
    processChunk(chunk);
    await setImmediate(); // Yield to event loop
  }
}
```

**Severity**: Critical (in servers), Major (in scripts)

## String Operations

### String Concatenation in Loops

**Pattern**: Building strings with += in loops.

```javascript
// SLOW
let result = '';
for (const item of items) {
  result += item.toString(); // Creates new string each time
}

// FAST
const result = items.map(i => i.toString()).join('');
```

**.NET**:
```csharp
// SLOW
string result = "";
foreach (var item in items) {
  result += item.ToString(); // O(n²)
}

// FAST
var sb = new StringBuilder();
foreach (var item in items) {
  sb.Append(item);
}
var result = sb.ToString();
```

**Severity**: Major (large loops), Minor (small loops)

## .NET Specific

### Boxing/Unboxing

**Pattern**: Value types converted to reference types.

```csharp
// BOXING
int value = 42;
object boxed = value;  // Boxing
int unboxed = (int)boxed;  // Unboxing

// AVOID - ArrayList boxes ints
var list = new ArrayList();
list.Add(42);

// PREFER - List<int> no boxing
var list = new List<int>();
list.Add(42);
```

**Severity**: Minor (isolated), Major (in hot loops)

### LINQ in Hot Paths

**Pattern**: LINQ creating allocations in frequently called code.

```csharp
// ALLOCATES
var first = items.FirstOrDefault(x => x.Id == id);
var filtered = items.Where(x => x.Active).ToList();

// For hot paths, consider:
foreach (var item in items) {
  if (item.Id == id) return item;
}
```

**Severity**: Minor to Major

### Async Void

**Pattern**: async void instead of async Task.

```csharp
// BAD - exceptions lost, can't await
async void ProcessAsync() { ... }

// GOOD
async Task ProcessAsync() { ... }
```

**Severity**: Major (also a correctness issue)

## Caching Opportunities

### Repeated Computations

**Pattern**: Same computation performed multiple times.

```javascript
// SLOW
function render(items) {
  const sorted = items.sort((a, b) => a.name.localeCompare(b.name));
  // ... render sorted
  const filtered = items.filter(i => i.active);
  // Oops, sort mutated items, filter sees sorted array
}

// Consider memoization for expensive pure functions
const memoizedSort = memoize((items) => [...items].sort(...));
```

**Severity**: Suggestion to Major

## Quick Reference

| Issue | Typical Severity | Fix Difficulty |
|-------|-----------------|----------------|
| N+1 Queries | Critical/Major | Medium |
| O(n²) Loops | Major | Medium |
| Memory Leaks | Critical | High |
| Sequential Awaits | Major | Low |
| String Concat in Loop | Major | Low |
| Missing Indexes | Major | Low |
| Unbounded Queries | Major | Low |
| Boxing in Loops | Minor/Major | Low |
