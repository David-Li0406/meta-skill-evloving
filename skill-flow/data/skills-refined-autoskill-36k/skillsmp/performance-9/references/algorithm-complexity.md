# Algorithm Complexity & Optimization

Guide to identifying and fixing performance issues in code.

## Big O Quick Reference

| Complexity | Name | Example | 1K items | 1M items |
|------------|------|---------|----------|----------|
| O(1) | Constant | Hash lookup | 1 | 1 |
| O(log n) | Logarithmic | Binary search | 10 | 20 |
| O(n) | Linear | Array scan | 1,000 | 1,000,000 |
| O(n log n) | Linearithmic | Merge sort | 10,000 | 20,000,000 |
| O(n²) | Quadratic | Nested loops | 1,000,000 | 10¹² |
| O(2ⁿ) | Exponential | Recursive fib | 10³⁰⁰ | ∞ |

## Common Anti-Patterns

### N+1 Query Problem

```python
# ❌ O(n) queries - N+1 problem
def get_orders_with_customers():
    orders = db.query("SELECT * FROM orders")  # 1 query
    for order in orders:
        # N queries!
        order.customer = db.query(
            f"SELECT * FROM customers WHERE id = {order.customer_id}"
        )
    return orders

# ✅ O(1) queries - JOIN or eager load
def get_orders_with_customers():
    return db.query("""
        SELECT o.*, c.name as customer_name
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
    """)

# ✅ O(2) queries - batch load
def get_orders_with_customers():
    orders = db.query("SELECT * FROM orders")
    customer_ids = [o.customer_id for o in orders]
    customers = db.query(
        "SELECT * FROM customers WHERE id IN (%s)",
        customer_ids
    )
    customer_map = {c.id: c for c in customers}
    for order in orders:
        order.customer = customer_map[order.customer_id]
    return orders
```

### Nested Loop Search

```javascript
// ❌ O(n²) - nested loop for lookup
function findMatchingUsers(users, permissions) {
  const result = [];
  for (const user of users) {                    // O(n)
    for (const perm of permissions) {            // O(m)
      if (perm.userId === user.id) {
        result.push({ user, permission: perm });
      }
    }
  }
  return result;
}

// ✅ O(n + m) - use Map for O(1) lookup
function findMatchingUsers(users, permissions) {
  const permMap = new Map();
  for (const perm of permissions) {              // O(m)
    permMap.set(perm.userId, perm);
  }

  const result = [];
  for (const user of users) {                    // O(n)
    const perm = permMap.get(user.id);           // O(1)
    if (perm) {
      result.push({ user, permission: perm });
    }
  }
  return result;
}
```

### Repeated Computation

```javascript
// ❌ O(n × expensive) - recalculates every time
function processItems(items) {
  return items.map(item => {
    const config = loadConfig();  // Expensive! Called n times
    return transform(item, config);
  });
}

// ✅ O(1 + n) - compute once
function processItems(items) {
  const config = loadConfig();  // Once
  return items.map(item => transform(item, config));
}
```

### String Concatenation in Loop

```javascript
// ❌ O(n²) - string immutability creates copies
function buildReport(items) {
  let report = '';
  for (const item of items) {
    report += `${item.name}: ${item.value}\n`;  // New string each time
  }
  return report;
}

// ✅ O(n) - array join
function buildReport(items) {
  const lines = items.map(item => `${item.name}: ${item.value}`);
  return lines.join('\n');
}
```

### Array Operations Inside Loop

```javascript
// ❌ O(n²) - includes is O(n)
function removeDuplicates(arr) {
  const result = [];
  for (const item of arr) {
    if (!result.includes(item)) {  // O(n) inside O(n) loop!
      result.push(item);
    }
  }
  return result;
}

// ✅ O(n) - Set is O(1)
function removeDuplicates(arr) {
  return [...new Set(arr)];
}

// ❌ O(n²) - indexOf is O(n)
function findCommon(arr1, arr2) {
  return arr1.filter(x => arr2.indexOf(x) !== -1);
}

// ✅ O(n + m) - Set lookup is O(1)
function findCommon(arr1, arr2) {
  const set2 = new Set(arr2);
  return arr1.filter(x => set2.has(x));
}
```

## Optimization Techniques

### Memoization

```javascript
// ❌ O(2ⁿ) - exponential
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

// ✅ O(n) - memoized
function fibonacci(n, memo = {}) {
  if (n in memo) return memo[n];
  if (n <= 1) return n;
  memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo);
  return memo[n];
}

// Generic memoization
function memoize(fn) {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}
```

### Lazy Evaluation

```javascript
// ❌ Eager - processes all even if not needed
function getFirstMatchingUser(users, predicate) {
  const matching = users.filter(predicate);  // Processes ALL
  return matching[0];
}

// ✅ Lazy - stops at first match
function getFirstMatchingUser(users, predicate) {
  return users.find(predicate);  // Stops early
}

// Generators for lazy sequences
function* filterLazy(items, predicate) {
  for (const item of items) {
    if (predicate(item)) yield item;
  }
}

// Only processes until first 5 found
const first5Active = [];
for (const user of filterLazy(users, u => u.active)) {
  first5Active.push(user);
  if (first5Active.length >= 5) break;
}
```

### Batch Processing

```javascript
// ❌ One at a time
async function processUsers(userIds) {
  for (const id of userIds) {
    await updateUser(id);  // Sequential!
  }
}

// ✅ Batch with concurrency limit
async function processUsers(userIds, batchSize = 10) {
  for (let i = 0; i < userIds.length; i += batchSize) {
    const batch = userIds.slice(i, i + batchSize);
    await Promise.all(batch.map(id => updateUser(id)));
  }
}
```

### Index Usage

```sql
-- ❌ Full table scan
SELECT * FROM orders WHERE YEAR(created_at) = 2024;

-- ✅ Can use index on created_at
SELECT * FROM orders
WHERE created_at >= '2024-01-01'
  AND created_at < '2025-01-01';

-- ❌ Index on (a, b) won't help
SELECT * FROM orders WHERE b = 'value';

-- ✅ Uses composite index (a, b)
SELECT * FROM orders WHERE a = 'x' AND b = 'value';
```

## Data Structure Selection

| Operation | Array | Set | Map | Object |
|-----------|-------|-----|-----|--------|
| Access by index | O(1) | - | - | - |
| Access by key | O(n) | - | O(1) | O(1) |
| Search | O(n) | O(1) | O(1) | O(1) |
| Insert | O(1)* | O(1) | O(1) | O(1) |
| Delete | O(n) | O(1) | O(1) | O(1) |
| Ordered | Yes | No | Insertion | No |

*O(n) if inserting in middle

### When to Use What

```javascript
// Use Array when: order matters, numeric indices
const queue = [];
queue.push(item);
const next = queue.shift();

// Use Set when: unique values, fast lookup
const visited = new Set();
if (!visited.has(node)) {
  visited.add(node);
  process(node);
}

// Use Map when: key-value pairs, any key type
const cache = new Map();
cache.set(complexKey, value);

// Use Object when: string keys, JSON serialization
const config = { apiUrl: '...', timeout: 5000 };
```

## Profiling Checklist

1. **Measure first**: Don't optimize without data
2. **Profile production-like data**: Small data hides O(n²)
3. **Check the hot path**: Focus on frequently called code
4. **Verify improvement**: Measure after optimization

```javascript
// Simple timing
console.time('operation');
doSomething();
console.timeEnd('operation');

// More detailed
const start = performance.now();
doSomething();
const duration = performance.now() - start;
console.log(`Took ${duration.toFixed(2)}ms`);
```
