---
name: frontend-performance
description: Provides performance optimization patterns for React applications. This skill should be used when optimizing bundle size, implementing code splitting, reducing re-renders, or improving web vitals.
---

# Frontend Performance

This skill provides patterns for optimizing React application performance.

## Performance Categories

### 1. Code Splitting and Lazy Loading

**What**: Split your bundle into smaller chunks and load them on demand.

**Benefits**:
- Faster initial page load
- Smaller bundle size
- Better caching

**Implementation** (React.lazy):

```typescript
import { lazy, Suspense } from 'react';
import { LoadingSpinner } from '@/components/LoadingSpinner';

// Lazy load route components
const Dashboard = lazy(() => import('@/routes/dashboard'));
const Settings = lazy(() => import('@/routes/settings'));
const Reports = lazy(() => import('@/routes/reports'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/reports" element={<Reports />} />
      </Routes>
    </Suspense>
  );
}
```

**Route-based code splitting** (TanStack Router):

```typescript
// TanStack Router automatically code-splits routes
// Each route file is a separate chunk
// src/routes/dashboard.tsx
export const Route = createFileRoute('/dashboard')({
  component: Dashboard,
});

function Dashboard() {
  return <div>Dashboard</div>;
}
```

**Component-based lazy loading**:

```typescript
// Lazy load heavy components
const HeavyChart = lazy(() => import('@/components/HeavyChart'));

function Dashboard() {
  const [showChart, setShowChart] = useState(false);

  return (
    <div>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      {showChart && (
        <Suspense fallback={<div>Loading chart...</div>}>
          <HeavyChart />
        </Suspense>
      )}
    </div>
  );
}
```

### 2. Memoization

**What**: Cache expensive computations and prevent unnecessary re-renders.

**Tools**:
- `React.memo` - Memoize components
- `useMemo` - Memoize values
- `useCallback` - Memoize functions

**React.memo** (Memoize Components):

```typescript
// Prevents re-render if props haven't changed
const UserCard = React.memo(function UserCard({ user }: { user: User }) {
  return (
    <div>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
});

// With custom comparison function
const UserCard = React.memo(
  function UserCard({ user }: { user: User }) {
    return <div>{user.name}</div>;
  },
  (prevProps, nextProps) => {
    // Only re-render if user.id changed
    return prevProps.user.id === nextProps.user.id;
  }
);
```

**useMemo** (Memoize Values):

```typescript
function ProductList({ products, filter }: Props) {
  // Expensive filtering operation - only recompute when dependencies change
  const filteredProducts = useMemo(() => {
    return products.filter((product) => {
      // Complex filtering logic
      return product.category === filter.category &&
             product.price >= filter.minPrice &&
             product.price <= filter.maxPrice;
    });
  }, [products, filter]);

  return (
    <ul>
      {filteredProducts.map((product) => (
        <li key={product.id}>{product.name}</li>
      ))}
    </ul>
  );
}
```

**useCallback** (Memoize Functions):

```typescript
function TodoList({ todos }: { todos: Todo[] }) {
  // Memoize callback to prevent child re-renders
  const handleToggle = useCallback((id: string) => {
    updateTodo(id, { completed: !todos.find((t) => t.id === id)?.completed });
  }, [todos]);

  return (
    <ul>
      {todos.map((todo) => (
        // TodoItem won't re-render if handleToggle reference doesn't change
        <TodoItem key={todo.id} todo={todo} onToggle={handleToggle} />
      ))}
    </ul>
  );
}
```

**When to use memoization**:
- ✅ Expensive computations
- ✅ Large lists
- ✅ Callbacks passed to memoized children
- ❌ Simple computations (overhead > benefit)
- ❌ Props that change frequently

### 3. Virtual Scrolling

**What**: Only render visible items in long lists.

**Benefits**:
- Handle thousands of items without performance issues
- Reduced memory usage
- Faster initial render

**Implementation** (react-virtual):

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';
import { useRef } from 'react';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // Estimated item height
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            <ItemComponent item={items[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 4. Image Optimization

**What**: Optimize images for faster loading and better performance.

**Techniques**:

**Lazy loading images**:

```typescript
// Native lazy loading
<img src="/large-image.jpg" loading="lazy" alt="Description" />

// With intersection observer for more control
function LazyImage({ src, alt }: { src: string; alt: string }) {
  const [isLoaded, setIsLoaded] = useState(false);
  const imgRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsLoaded(true);
          observer.disconnect();
        }
      },
      { rootMargin: '100px' } // Start loading 100px before visible
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <img
      ref={imgRef}
      src={isLoaded ? src : '/placeholder.jpg'}
      alt={alt}
    />
  );
}
```

**Responsive images**:

```typescript
<img
  src="/image-800.jpg"
  srcSet="
    /image-400.jpg 400w,
    /image-800.jpg 800w,
    /image-1200.jpg 1200w
  "
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  alt="Description"
/>
```

**Modern image formats**:

```typescript
<picture>
  <source srcSet="/image.avif" type="image/avif" />
  <source srcSet="/image.webp" type="image/webp" />
  <img src="/image.jpg" alt="Description" />
</picture>
```

### 5. Bundle Size Optimization

**What**: Reduce the size of your JavaScript bundles.

**Techniques**:

**Analyze bundle size**:

```bash
# Install bundle analyzer
pnpm add -D vite-plugin-bundle-analyzer

# Add to vite.config.ts
import { visualizer } from 'vite-plugin-bundle-analyzer';

export default defineConfig({
  plugins: [
    visualizer({ open: true }),
  ],
});
```

**Tree shaking** (automatic with Vite):

```typescript
// ✅ GOOD: Named imports (tree-shakeable)
import { Button } from '@eridu/ui/components/button';

// ❌ BAD: Barrel imports (may include unused code)
import { Button } from '@eridu/ui';
```

**Dynamic imports for large dependencies**:

```typescript
// Only load when needed
async function exportToPDF() {
  const { jsPDF } = await import('jspdf');
  const doc = new jsPDF();
  // ...
}
```

**Remove unused dependencies**:

```bash
# Find unused dependencies
pnpm dlx depcheck
```

### 6. Web Vitals Monitoring

**What**: Monitor Core Web Vitals to track real-world performance.

**Metrics**:
- **LCP** (Largest Contentful Paint) - Loading performance
- **FID** (First Input Delay) - Interactivity
- **CLS** (Cumulative Layout Shift) - Visual stability

**Implementation**:

```typescript
// src/lib/web-vitals.ts
import { onCLS, onFID, onLCP } from 'web-vitals';

export function initWebVitals() {
  onCLS((metric) => {
    console.log('CLS:', metric.value);
    // Send to analytics
  });

  onFID((metric) => {
    console.log('FID:', metric.value);
    // Send to analytics
  });

  onLCP((metric) => {
    console.log('LCP:', metric.value);
    // Send to analytics
  });
}

// src/main.tsx
import { initWebVitals } from './lib/web-vitals';

if (import.meta.env.PROD) {
  initWebVitals();
}
```

## Performance Checklist

### Initial Load
- [ ] Routes are code-split (lazy loaded)
- [ ] Heavy components are lazy loaded
- [ ] Images use lazy loading
- [ ] Bundle size is analyzed and optimized
- [ ] Unused dependencies are removed

### Runtime Performance
- [ ] Expensive computations use useMemo
- [ ] Callbacks passed to children use useCallback
- [ ] Large lists use virtual scrolling
- [ ] Components use React.memo where appropriate
- [ ] Re-renders are minimized

### Images
- [ ] Images are optimized (compressed, correct format)
- [ ] Images use lazy loading
- [ ] Responsive images with srcSet
- [ ] Modern formats (WebP, AVIF) are used

### Monitoring
- [ ] Web Vitals are tracked
- [ ] Performance metrics are sent to analytics
- [ ] Bundle size is monitored in CI/CD

## Best Practices

1. **Measure before optimizing** - Use profiler and analytics to identify bottlenecks
2. **Start with code splitting** - Biggest impact for least effort
3. **Don't over-memoize** - Memoization has overhead, use judiciously
4. **Optimize images** - Often the largest assets
5. **Monitor in production** - Real-world performance matters most
6. **Use production builds** - Development builds are slower
7. **Lazy load below the fold** - Prioritize visible content

## Tools

- **React DevTools Profiler** - Identify unnecessary re-renders
- **Lighthouse** - Audit performance, accessibility, SEO
- **Bundle Analyzer** - Visualize bundle size
- **Web Vitals** - Track Core Web Vitals
- **Chrome DevTools Performance** - Detailed performance analysis
