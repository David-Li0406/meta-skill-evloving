---
name: performance-optimization
description: Optimize frontend and backend performance through profiling, caching strategies, database optimization, code splitting, and Core Web Vitals improvements. Build fast user experiences.
---

# Performance Optimization

Complete framework for identifying and fixing performance bottlenecks in web applications.

## When to Use

- Page load times are slow (>3 seconds)
- Core Web Vitals failing
- Database queries are slow
- API responses are slow
- High server costs due to inefficiency
- Poor user experience on mobile

## Core Principles

**Measure First:**
- Don't optimize without data
- Profile before changing
- Set performance budgets
- Monitor continuously

**User Perception > Actual Speed:**
- Time to Interactive matters most
- Progressive loading
- Provide feedback (spinners, skeleton screens)

**80/20 Rule:**
- 20% of code causes 80% of slowdowns
- Find the hot paths first
- Don't micro-optimize everything

---

## Workflow

### Step 1: Measure Current Performance

**Core Web Vitals:**
```markdown
## Performance Baseline

**LCP (Largest Contentful Paint)**
- Goal: <2.5 seconds
- Current: [X]s
- What: Time until largest content element renders

**FID (First Input Delay)**
- Goal: <100 milliseconds
- Current: [X]ms
- What: Time from first interaction to response

**CLS (Cumulative Layout Shift)**
- Goal: <0.1
- Current: [X]
- What: Unexpected layout movements

**Time to Interactive**
- Goal: <3 seconds
- Current: [X]s

**Total Page Weight**
- Goal: <1MB
- Current: [X]MB
```

**Tools:**
- Lighthouse (Chrome DevTools)
- WebPageTest.org
- Chrome DevTools Performance tab
- Real User Monitoring (RUM)

### Step 2: Frontend Optimization

**Image Optimization:**
```html
<!-- ❌ SLOW: Large unoptimized image -->
<img src="hero-5mb.jpg" alt="Hero" />

<!-- ✅ FAST: Responsive images with modern formats -->
<picture>
  <source srcset="hero.avif" type="image/avif" />
  <source srcset="hero.webp" type="image/webp" />
  <img
    srcset="hero-300.jpg 300w,
            hero-600.jpg 600w,
            hero-1200.jpg 1200w"
    sizes="(max-width: 600px) 300px,
           (max-width: 1200px) 600px,
           1200px"
    src="hero-600.jpg"
    alt="Hero"
    loading="lazy"
  />
</picture>
```

**Code Splitting:**
```javascript
// ❌ SLOW: Load everything upfront
import { HeavyComponent } from './HeavyComponent';
import { RarelyUsedFeature } from './RarelyUsedFeature';

// ✅ FAST: Lazy load on demand
const HeavyComponent = lazy(() => import('./HeavyComponent'));
const RarelyUsedFeature = lazy(() => import('./RarelyUsedFeature'));

// Route-based code splitting
const routes = {
  '/': () => import('./pages/Home'),
  '/dashboard': () => import('./pages/Dashboard'),
  '/settings': () => import('./pages/Settings'),
};
```

**JavaScript Optimization:**
```javascript
// ❌ SLOW: Blocking render
<script src="large-bundle.js"></script>

// ✅ FAST: Defer non-critical JS
<script src="critical.js"></script>
<script src="non-critical.js" defer></script>

// Debounce expensive operations
function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

const handleSearch = debounce(async (query) => {
  const results = await searchAPI(query);
  displayResults(results);
}, 300);

// Use web workers for heavy computation
const worker = new Worker('heavy-task.js');
worker.postMessage(largeDataset);
worker.onmessage = (e) => handleResults(e.data);
```

**CSS Optimization:**
```css
/* ❌ SLOW: Expensive selectors */
.container div span a { }

/* ✅ FAST: Specific selectors */
.nav-link { }

/* Critical CSS - inline in <head> */
.header, .hero { /* styles */ }

/* Non-critical CSS - load async */
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

**Resource Hints:**
```html
<!-- Preload critical resources -->
<link rel="preload" href="/critical.css" as="style" />
<link rel="preload" href="/hero.jpg" as="image" />

<!-- Prefetch next page resources -->
<link rel="prefetch" href="/next-page.js" />

<!-- DNS prefetch for external domains -->
<link rel="dns-prefetch" href="//api.example.com" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
```

### Step 3: Backend Optimization

**Database Query Optimization:**
```sql
-- ❌ SLOW: No index, SELECT *
SELECT * FROM orders WHERE user_id = 123;

-- ✅ FAST: Add index
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- ✅ FAST: Select only needed columns
SELECT id, total, created_at
FROM orders
WHERE user_id = 123;

-- Use EXPLAIN ANALYZE
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123;

-- Avoid N+1 queries
-- ❌ SLOW
const users = await User.findAll();
for (const user of users) {
  user.posts = await Post.findAll({ userId: user.id }); // N queries!
}

-- ✅ FAST: Use joins or eager loading
const users = await User.findAll({
  include: [Post]  // 1 query with JOIN
});
```

**Caching Strategy:**
```javascript
// Cache-aside pattern
async function getUser(id) {
  // 1. Check cache
  const cached = await redis.get(`user:${id}`);
  if (cached) {
    return JSON.parse(cached);
  }

  // 2. Cache miss: fetch from DB
  const user = await db.users.findById(id);

  // 3. Store in cache
  await redis.setex(
    `user:${id}`,
    JSON.stringify(user),
    3600  // TTL: 1 hour
  );

  return user;
}

// Cache invalidation
async function updateUser(id, data) {
  await db.users.update(id, data);
  await redis.del(`user:${id}`);  // Invalidate
}
```

**API Optimization:**
```javascript
// Response compression
const compression = require('compression');
app.use(compression());

// Pagination (not loading all data)
app.get('/api/items', async (req, res) => {
  const { cursor, limit = 20 } = req.query;

  const items = await db.items.findMany({
    where: cursor ? { id: { gt: cursor } } : {},
    take: limit + 1,  // Fetch one extra to check if more
  });

  const hasMore = items.length > limit;
  if (hasMore) items.pop();

  res.json({
    items,
    nextCursor: hasMore ? items[items.length - 1].id : null,
  });
});

// Move heavy work to background
const emailQueue = new Queue('emails');

app.post('/api/orders', async (req, res) => {
  const order = await createOrder(req.body);

  // Queue email instead of sending inline
  await emailQueue.add({ orderId: order.id });

  res.json(order);  // Fast response
});
```

### Step 4: Profiling & Debugging

**Browser DevTools:**
```
PERFORMANCE TAB:
1. Click Record
2. Perform slow action
3. Stop recording
4. Look for:
   - Long tasks (>50ms)
   - Main thread blocking
   - Layout thrashing
   - Memory leaks

NETWORK TAB:
- Check request waterfall
- Look for slow/large requests
- Verify caching headers
- Check compression
```

**Node.js Profiling:**
```bash
# Built-in profiler
node --prof app.js

# Analyze profile
node --prof-process isolate-*.log > profile.txt

# Clinic.js for visualization
npx clinic doctor -- node app.js
npx clinic flame -- node app.js

# Memory profiling
node --inspect app.js
# Then open chrome://inspect
```

### Step 5: Performance Budget

```markdown
## Performance Budget

### Page Load
| Metric | Budget | Current | Status |
|--------|--------|---------|--------|
| LCP | <2.5s | 3.1s | ❌ |
| FID | <100ms | 85ms | ✅ |
| CLS | <0.1 | 0.05 | ✅ |
| TTI | <3s | 4.2s | ❌ |

### Assets
| Asset | Budget | Current |
|-------|--------|---------|
| Total JS | <200KB | 350KB |
| Total CSS | <50KB | 45KB |
| Images/page | <500KB | 800KB |
| Total weight | <1MB | 1.5MB |

### API
| Endpoint | P50 | P95 | P99 |
|----------|-----|-----|-----|
| GET /items | <50ms | <100ms | <200ms |
| POST /order | <100ms | <200ms | <500ms |

### Actions
1. ❌ Reduce JS bundle (200KB over budget)
2. ❌ Optimize images (300KB over budget)
3. ✅ CSS within budget
```

---

## Optimization Checklist

```markdown
## Performance Review: [Feature]

### Frontend
- [ ] Images optimized and lazy loaded
- [ ] JavaScript code split
- [ ] Critical CSS inlined
- [ ] No layout shifts (CLS <0.1)
- [ ] Long tasks broken up (<50ms)
- [ ] Resource hints used
- [ ] Fonts optimized

### Backend
- [ ] Database queries optimized (EXPLAIN ANALYZE)
- [ ] Appropriate caching
- [ ] Heavy work moved to background
- [ ] Response compression enabled
- [ ] N+1 queries eliminated
- [ ] Connection pooling configured

### Monitoring
- [ ] Performance metrics tracked
- [ ] Alerts set for regressions
- [ ] Real user monitoring (RUM)
- [ ] Synthetic monitoring
```

---

## Quick Wins

**Immediate Impact:**

1. **Enable Compression** (5 min)
   ```javascript
   const compression = require('compression');
   app.use(compression());
   ```

2. **Add Image Lazy Loading** (10 min)
   ```html
   <img src="image.jpg" loading="lazy" alt="..." />
   ```

3. **Add Database Index** (5 min)
   ```sql
   CREATE INDEX idx_users_email ON users(email);
   ```

4. **Cache Static Assets** (10 min)
   ```javascript
   res.setHeader('Cache-Control', 'public, max-age=31536000');
   ```

5. **Use CDN** (varies)
   - Move static assets to CDN
   - Reduces server load
   - Faster delivery globally

---

## Common Performance Killers

| Problem | Impact | Fix |
|---------|--------|-----|
| No database indexes | 100x slower queries | Add indexes on filtered columns |
| Loading all data | Memory + slow | Paginate results |
| Synchronous heavy work | Blocking | Move to background queue |
| No caching | Repeated expensive operations | Cache at multiple levels |
| Large images | Slow page load | Optimize, lazy load, responsive |
| Too much JavaScript | Slow TTI | Code split, lazy load |
| No compression | Large transfers | Enable gzip/brotli |
| N+1 queries | Database overload | Use joins or eager loading |

---

## Tools & Resources

**Measurement:**
- Lighthouse (Chrome DevTools)
- WebPageTest.org
- Chrome User Experience Report
- Google PageSpeed Insights

**Profiling:**
- Chrome DevTools Performance
- React DevTools Profiler
- Node.js --prof
- Clinic.js

**Monitoring:**
- New Relic
- Datadog
- Sentry Performance
- web-vitals library

---

## Related Skills

- `/security-review` - Security considerations for caching
- `/database-schema` - Optimizing schema design
- `/devops-cicd` - Performance testing in CI/CD

---

**Last Updated**: 2026-01-22
