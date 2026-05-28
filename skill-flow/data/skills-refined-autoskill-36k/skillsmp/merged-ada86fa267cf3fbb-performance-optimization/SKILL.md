---
name: performance-optimization
description: Use this skill to identify and resolve performance bottlenecks, optimize both front-end and back-end performance, and implement best practices for database queries and caching strategies.
---

# Performance Optimization Skill

> **Performance is part of functionality**
> The perceived response time by users determines the product experience.

## 🎯 Performance Metrics

### Front-end Metrics

| Metric | Target | Description |
|:---|:---|:---|
| **FCP** (First Contentful Paint) | < 1.8s | First content rendering |
| **LCP** (Largest Contentful Paint) | < 2.5s | Largest content rendering |
| **FID** (First Input Delay) | < 100ms | First input delay |
| **CLS** (Cumulative Layout Shift) | < 0.1 | Cumulative layout shift |
| **TTI** (Time to Interactive) | < 3.8s | Time to interactive |

### Back-end Metrics

| Metric | Target | Description |
|:---|:---|:---|
| **Response Time** | < 200ms | API response |
| **Throughput** | As needed | Queries per second (QPS) |
| **Error Rate** | < 0.1% | 5xx errors |
| **P99 Latency** | < 1s | 99th percentile latency |

## 🔍 Performance Issue Detection

### Front-end Checklist

```markdown
## Front-end Performance Check

### Rendering Performance
- [ ] Are there unnecessary re-renders?
- [ ] Is virtual scrolling used for lists?
- [ ] Is large data paginated?
- [ ] Are memo/useMemo/useCallback utilized?

### Resource Loading
- [ ] Are images compressed/lazy-loaded?
- [ ] Are JS/CSS files split?
- [ ] Is a CDN used?
- [ ] Is caching enabled?

### Bundle Size
- [ ] Are there unused dependencies?
- [ ] Is code loaded on demand?
- [ ] Is tree-shaking applied?
```

### Back-end Checklist

```markdown
## Back-end Performance Check

### Database
- [ ] Are there N+1 queries?
- [ ] Are indexes appropriate?
- [ ] Are there slow queries?
- [ ] Is a connection pool used?

### Caching
- [ ] Is hot data cached?
- [ ] Is the caching strategy reasonable?
- [ ] Is cache penetration handled?

### Concurrency
- [ ] Are there race conditions?
- [ ] Is lock granularity appropriate?
- [ ] Is there a risk of deadlocks?
```

## 🛠️ Common Optimization Strategies

### 1. N+1 Query Optimization

```javascript
// ❌ N+1 Problem
const users = await User.findAll();
for (const user of users) {
  user.orders = await Order.findByUserId(user.id);
}

// ✅ Batch Query
const users = await User.findAll();
const userIds = users.map(u => u.id);
const orders = await Order.findByUserIds(userIds);
const orderMap = groupBy(orders, 'userId');
users.forEach(u => u.orders = orderMap[u.id] || []);
```

### 2. Asynchronous Optimization in Loops

```javascript
// ❌ Serial Execution
for (const id of ids) {
  await processItem(id);
}

// ✅ Parallel Execution
await Promise.all(ids.map(id => processItem(id)));

// ✅ Control Concurrency
import pLimit from 'p-limit';
const limit = pLimit(5);
await Promise.all(ids.map(id => limit(() => processItem(id))));
```

### 3. React Rendering Optimization

```javascript
// ❌ Creating new objects each time
<Component style={{ color: 'red' }} />

// ✅ Extracting constants
const style = { color: 'red' };
<Component style={style} />

// ❌ Creating new functions each time
<Button onClick={() => handleClick(id)} />

// ✅ Using useCallback
const handleClick = useCallback(() => {
  // ...
}, [id]);
```

### 4. List Optimization

```javascript
// ❌ Rendering all items
{items.map(item => <Item key={item.id} {...item} />)}

// ✅ Virtual Scrolling (render only visible items)
import { FixedSizeList } from 'react-window';
<FixedSizeList
  height={400}
  itemCount={items.length}
  itemSize={50}
>
  {({ index, style }) => (
    <Item style={style} {...items[index]} />
  )}
</FixedSizeList>
```

### 5. Database Indexing

```sql
-- Analyze slow queries
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'xxx';

-- Add index
CREATE INDEX idx_users_email ON users(email);

-- Composite index
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
```

### 6. Caching Strategy

```javascript
// Read from cache
async function getUser(id) {
  // 1. Check cache
  let user = await cache.get(`user:${id}`);
  if (user) return user;
  
  // 2. Check database
  user = await db.query('SELECT * FROM users WHERE id = ?', [id]);
  
  // 3. Write to cache
  await cache.set(`user:${id}`, user, { ttl: 3600 });
  
  return user;
}
```

## 📊 Performance Analysis Tools

### Front-end

| Tool | Purpose |
|:---|:---|
| **Chrome DevTools** | Performance/Network/Memory |
| **Lighthouse** | Overall scoring |
| **Web Vitals** | Core Web Vitals |
| **Bundle Analyzer** | Bundle size analysis |

### Back-end

| Tool | Purpose |
|:---|:---|
| **Database EXPLAIN** | Query analysis |
| **APM Tools** | Full trace tracking |
| **Load Testing Tools** | Performance benchmarking |

## 📋 Performance Optimization Checklist

### During Development
- [ ] Avoid N+1 queries
- [ ] Do not use await in loops
- [ ] Use memo appropriately
- [ ] Add necessary indexes

### Before Deployment
- [ ] Images are compressed
- [ ] Resources are minified
- [ ] Gzip is enabled
- [ ] Cache headers are configured

### Regular Review
- [ ] Analyze slow queries
- [ ] Check memory usage
- [ ] Evaluate cache hit rates
- [ ] Monitor P99 latency

## ⚠️ Performance Anti-patterns

```javascript
// Record in Memory to avoid repetition
memory.add({
  category: "forbidden_action",
  content: "Avoid using separate await in loops",
  tags: ["performance", "async"]
})

memory.add({
  category: "forbidden_action",
  content: "Avoid SELECT * on large tables",
  tags: ["performance", "database"]
})
```

## 🎯 Optimization Priorities

```
1. Measure before optimizing
2. Optimize the most impactful bottlenecks
3. Avoid premature optimization
4. Weigh benefits against complexity
```

---

**Method**: Measure → Analyze → Optimize → Validate | **Tools**: DevTools + APM | **Principle**: Data-driven