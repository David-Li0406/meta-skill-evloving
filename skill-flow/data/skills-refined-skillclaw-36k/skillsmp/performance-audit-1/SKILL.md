---
name: performance-audit
description: Comprehensive performance audit workflow for web applications
license: MIT
---

# Performance Audit Skill

Use this skill when analyzing and optimizing application performance.

## When to Use

- Before major releases
- After performance complaints
- Regular performance reviews
- Optimizing slow pages/features
- Setting performance budgets

## Core Web Vitals

| Metric | Good | Needs Work | Poor | What It Measures |
|--------|------|------------|------|------------------|
| LCP | < 2.5s | < 4s | > 4s | Loading performance |
| FID | < 100ms | < 300ms | > 300ms | Interactivity |
| CLS | < 0.1 | < 0.25 | > 0.25 | Visual stability |
| INP | < 200ms | < 500ms | > 500ms | Responsiveness |
| TTFB | < 800ms | < 1.8s | > 1.8s | Server response |

## Audit Workflow

### Step 1: Establish Baseline

```bash
# Lighthouse CLI
npx lighthouse https://example.com --output=json --output-path=baseline.json

# WebPageTest
# Use https://webpagetest.org for real-world testing

# Chrome DevTools
# Performance tab → Record → Interact → Stop
```

### Step 2: Analyze Bundle Size

```bash
# Webpack bundle analyzer
npx webpack-bundle-analyzer stats.json

# Source map explorer
npx source-map-explorer 'dist/**/*.js'

# Next.js
ANALYZE=true npm run build

# Package size check
npx package-phobia lodash moment axios
```

### Step 3: Profile Runtime

```javascript
// Console timing
console.time('operation');
await expensiveOperation();
console.timeEnd('operation');

// Performance API
performance.mark('start');
await expensiveOperation();
performance.mark('end');
performance.measure('operation', 'start', 'end');
console.log(performance.getEntriesByName('operation'));

// React Profiler
import { Profiler } from 'react';

<Profiler id="Component" onRender={onRenderCallback}>
  <Component />
</Profiler>

function onRenderCallback(id, phase, actualDuration) {
  console.log({ id, phase, actualDuration });
}
```

## Optimization Techniques

### Bundle Size

```typescript
// ❌ Bad: Import entire library
import _ from 'lodash';
import moment from 'moment';

// ✅ Good: Import specific functions
import debounce from 'lodash/debounce';
import { format } from 'date-fns';

// ✅ Good: Dynamic imports
const Chart = dynamic(() => import('./Chart'), {
  loading: () => <Skeleton />,
  ssr: false,
});

// ✅ Good: Tree-shakeable imports
import { Button, Input } from '@/components';
// Not: import * as Components from '@/components';
```

### Images

```tsx
// ✅ Next.js Image optimization
import Image from 'next/image';

<Image
  src="/hero.jpg"
  width={1200}
  height={600}
  priority  // For above-the-fold
  placeholder="blur"
  blurDataURL={blurHash}
  sizes="(max-width: 768px) 100vw, 50vw"
/>

// ✅ Lazy loading for below-fold
<Image
  src="/product.jpg"
  loading="lazy"
  // ... other props
/>
```

### Code Splitting

```typescript
// Route-based splitting (automatic in Next.js)
// pages/dashboard.tsx → separate chunk

// Component-based splitting
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyComponent />
    </Suspense>
  );
}

// Conditional loading
const AdminPanel = React.lazy(() => 
  user.isAdmin ? import('./AdminPanel') : import('./UserPanel')
);
```

### React Optimization

```typescript
// ✅ Memoize expensive computations
const sortedItems = useMemo(
  () => items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// ✅ Memoize callbacks
const handleClick = useCallback(
  (id: string) => setSelected(id),
  []
);

// ✅ Memoize components
const MemoizedList = React.memo(ItemList);

// ✅ Virtualize long lists
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={400}
  itemCount={10000}
  itemSize={50}
>
  {({ index, style }) => (
    <div style={style}>{items[index].name}</div>
  )}
</FixedSizeList>
```

### Network Optimization

```typescript
// ✅ Prefetch critical resources
<link rel="prefetch" href="/api/user" />
<link rel="preload" href="/fonts/inter.woff2" as="font" crossOrigin />

// ✅ Cache API responses
const CACHE_TIME = 5 * 60 * 1000; // 5 minutes

async function fetchWithCache(url: string) {
  const cached = cache.get(url);
  if (cached && Date.now() - cached.timestamp < CACHE_TIME) {
    return cached.data;
  }
  
  const data = await fetch(url).then(r => r.json());
  cache.set(url, { data, timestamp: Date.now() });
  return data;
}

// ✅ Use SWR or React Query
import useSWR from 'swr';

function Profile() {
  const { data, error, isLoading } = useSWR('/api/user', fetcher, {
    revalidateOnFocus: false,
    dedupingInterval: 60000,
  });
}
```

### Database Optimization

```sql
-- ✅ Add indexes for frequent queries
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);

-- ✅ Use EXPLAIN to analyze
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;

-- ✅ Avoid N+1 queries
-- Bad: Query per user
SELECT * FROM users;
-- Then for each user: SELECT * FROM orders WHERE user_id = ?;

-- Good: Single query with JOIN
SELECT u.*, o.* FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.id IN (1, 2, 3);
```

## Performance Budget

```javascript
// performance-budget.json
{
  "bundles": [
    { "name": "main", "maxSize": "100 KB" },
    { "name": "vendor", "maxSize": "150 KB" }
  ],
  "metrics": {
    "LCP": "2500",
    "FID": "100",
    "CLS": "0.1",
    "TTFB": "800"
  },
  "resourceSizes": {
    "script": "300 KB",
    "image": "500 KB",
    "font": "100 KB"
  }
}
```

```yaml
# Lighthouse CI
# lighthouserc.js
module.exports = {
  ci: {
    assert: {
      assertions: {
        'first-contentful-paint': ['error', { maxNumericValue: 2000 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['error', { maxNumericValue: 300 }],
      },
    },
  },
};
```

## Audit Report Template

```markdown
## Performance Audit Report

### Summary
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| LCP | 3.2s | < 2.5s | ⚠️ |
| FID | 85ms | < 100ms | ✅ |
| CLS | 0.05 | < 0.1 | ✅ |
| Bundle Size | 450KB | < 300KB | ❌ |

### Top Issues

#### 1. Large JavaScript Bundle (450KB)
**Impact**: +1.2s load time on 3G
**Cause**: Full lodash import, unoptimized images
**Fix**: Tree-shake lodash, lazy load charts

#### 2. Slow LCP (3.2s)
**Impact**: Poor user experience, SEO penalty
**Cause**: Hero image not optimized, render-blocking CSS
**Fix**: Add priority to hero image, inline critical CSS

### Optimization Roadmap

| Priority | Task | Impact | Effort |
|----------|------|--------|--------|
| 1 | Tree-shake lodash | -45KB | Low |
| 2 | Lazy load charts | -80KB | Medium |
| 3 | Optimize images | -0.8s LCP | Low |
| 4 | Add caching | -200ms | Medium |

### Expected Results
- Bundle size: 450KB → 280KB (-38%)
- LCP: 3.2s → 2.1s (-34%)
- Lighthouse score: 65 → 90
```

## Tools Reference

| Tool | Purpose | Command |
|------|---------|---------|
| Lighthouse | Full audit | `npx lighthouse URL` |
| Bundle Analyzer | Bundle composition | `npx webpack-bundle-analyzer` |
| Source Map Explorer | Module sizes | `npx source-map-explorer` |
| WebPageTest | Real-world testing | webpagetest.org |
| Chrome DevTools | Profiling | Performance tab |
