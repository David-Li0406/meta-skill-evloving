# Performance Optimization

Performance is critical for user experience. This guide covers proven techniques for optimizing React applications, from initial load to runtime performance.

## Table of Contents

- [Code Splitting](#code-splitting)
- [Component Optimization](#component-optimization)
- [List Virtualization](#list-virtualization)
- [Image Optimization](#image-optimization)
- [Bundle Optimization](#bundle-optimization)
- [Web Vitals](#web-vitals)
- [Data Prefetching](#data-prefetching)
- [Performance Monitoring](#performance-monitoring)

## Code Splitting

Split your bundle into smaller chunks that load on demand.

### Route-Based Splitting

Split at route boundaries:

```tsx
import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// Lazy load route components
const Home = lazy(() => import('./routes/Home'));
const Dashboard = lazy(() => import('./routes/Dashboard'));
const Settings = lazy(() => import('./routes/Settings'));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          <route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
```

### Component-Based Splitting

Split large components:

```tsx
// Heavy chart library - only load when needed
const ChartComponent = lazy(() => import('./Chart'));

function Dashboard() {
  const [showChart, setShowChart] = useState(false);

  return (
    <div>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      {showChart && (
        <Suspense fallback={<Spinner />}>
          <ChartComponent />
        </Suspense>
      )}
    </div>
  );
}
```

### Named Exports

Lazy load named exports:

```tsx
// utils/charts.ts
export const LineChart = () => { /* ... */ };
export const BarChart = () => { /* ... */ };

// App.tsx - only loads the specific chart
const LineChart = lazy(() =>
  import('./utils/charts').then(module => ({ default: module.LineChart }))
);
```

## Component Optimization

### React Compiler (React 19+)

React 19's compiler automatically memoizes components - remove manual `React.memo`, `useMemo`, `useCallback` when using the compiler.

**Without compiler** (React 18 and below):

#### `React.memo`

Prevent re-renders when props haven't changed:

```tsx
// ❌ Bad - re-renders on every parent render
function ExpensiveComponent({ data }) {
  return <div>{/* expensive rendering */}</div>;
}

// ✅ Good - only re-renders when data changes
const ExpensiveComponent = React.memo(({ data }) => {
  return <div>{/* expensive rendering */}</div>;
});

// Custom comparison function
const ExpensiveComponent = React.memo(
  ({ user, onUpdate }) => {
    return <div>{user.name}</div>;
  },
  (prevProps, nextProps) => {
    // Only re-render if user.id changed
    return prevProps.user.id === nextProps.user.id;
  }
);
```

#### `useMemo`

Memoize expensive computations:

```tsx
function DataTable({ data, filters }) {
  // ❌ Bad - filters data on every render
  const filteredData = data.filter(item =>
    filters.every(filter => filter(item))
  );

  // ✅ Good - only recomputes when dependencies change
  const filteredData = useMemo(
    () => data.filter(item => filters.every(filter => filter(item))),
    [data, filters]
  );

  return <Table data={filteredData} />;
}
```

**When to use `useMemo`:**
- Expensive computations (array operations, filtering, sorting)
- Creating objects/arrays passed to memoized children
- NOT for cheap operations (simple math, string concatenation)

#### `useCallback`

Memoize function references:

```tsx
function ParentComponent() {
  // ❌ Bad - new function on every render, breaks memoization
  const handleClick = () => console.log('clicked');

  return <MemoizedChild onClick={handleClick} />;
}

// ✅ Good - stable function reference
function ParentComponent() {
  const handleClick = useCallback(() => {
    console.log('clicked');
  }, []); // No dependencies

  return <MemoizedChild onClick={handleClick} />;
}

// With dependencies
function ParentComponent({ userId }) {
  const handleClick = useCallback(() => {
    trackEvent('click', { userId });
  }, [userId]); // Recreates when userId changes

  return <MemoizedChild onClick={handleClick} />;
}
```

**When to use `useCallback`:**
- Passing callbacks to memoized children
- Function used in dependency arrays
- NOT for every function (overhead not worth it)

### State Colocation

Keep state close to where it's used to minimize re-renders:

```tsx
// ❌ Bad - entire component re-renders on input change
function Form() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  return (
    <div>
      <ExpensiveComponent /> {/* Re-renders unnecessarily */}
      <input value={name} onChange={e => setName(e.target.value)} />
      <input value={email} onChange={e => setEmail(e.target.value)} />
    </div>
  );
}

// ✅ Good - isolate state to minimize re-renders
function Form() {
  return (
    <div>
      <ExpensiveComponent /> {/* Never re-renders */}
      <NameInput />
      <EmailInput />
    </div>
  );
}

function NameInput() {
  const [name, setName] = useState('');
  return <input value={name} onChange={e => setName(e.target.value)} />;
}
```

## List Virtualization

Render only visible items for long lists.

### react-window

Lightweight virtualization:

```tsx
import { FixedSizeList } from 'react-window';

function VirtualizedList({ items }) {
  const Row = ({ index, style }) => (
    <div style={style}>
      {items[index].name}
    </div>
  );

  return (
    <FixedSizeList
      height={600}         // Viewport height
      itemCount={items.length}
      itemSize={50}        // Row height
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
}
```

### Tanstack Virtual

More flexible, modern virtualization:

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualizedList({ items }) {
  const parentRef = useRef(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
    overscan: 5, // Render 5 items above/below viewport
  });

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map(virtualItem => (
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
            {items[virtualItem.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

**Benefits:**
- 1000+ items: 50ms → 5ms render time
- Smooth scrolling
- Lower memory usage

## Image Optimization

### Lazy Loading

Native lazy loading:

```tsx
<img
  src="/large-image.jpg"
  loading="lazy" // Native lazy load
  alt="Description"
/>
```

With Intersection Observer for custom behavior:

```tsx
function LazyImage({ src, alt }) {
  const [imageSrc, setImageSrc] = useState(null);
  const imgRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setImageSrc(src);
          observer.disconnect();
        }
      },
      { rootMargin: '100px' } // Load 100px before visible
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, [src]);

  return (
    <img
      ref={imgRef}
      src={imageSrc || '/placeholder.jpg'}
      alt={alt}
    />
  );
}
```

### Modern Formats

Use WebP/AVIF with fallbacks:

```tsx
<picture>
  <source srcSet="/image.avif" type="image/avif" />
  <source srcSet="/image.webp" type="image/webp" />
  <img src="/image.jpg" alt="Fallback" />
</picture>
```

### Responsive Images

Serve appropriate sizes:

```tsx
<img
  src="/image-800w.jpg"
  srcSet="
    /image-400w.jpg 400w,
    /image-800w.jpg 800w,
    /image-1200w.jpg 1200w
  "
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  alt="Responsive image"
/>
```

## Bundle Optimization

### Tree Shaking

Import only what you need:

```tsx
// ❌ Bad - imports entire lodash
import _ from 'lodash';
const result = _.debounce(fn, 300);

// ✅ Good - only imports debounce
import debounce from 'lodash/debounce';
const result = debounce(fn, 300);

// Even better - use modern alternatives
import { debounce } from 'es-toolkit';
```

### Analyze Bundle

```bash
# Vite
npx vite-bundle-visualizer

# Webpack
npx webpack-bundle-analyzer
```

Target actions:
- Remove unused dependencies
- Replace heavy libraries (moment → date-fns)
- Code split large modules

## Web Vitals

Monitor Core Web Vitals:

### Largest Contentful Paint (LCP)

Target: < 2.5s

**Optimize:**
- Preload critical resources
- Optimize images (WebP, lazy load)
- Use CDN for static assets
- Server-side render above-the-fold content

```tsx
// Preload critical resources
<link rel="preload" href="/hero-image.jpg" as="image" />
<link rel="preload" href="/critical.css" as="style" />
```

### First Input Delay (FID)

Target: < 100ms

**Optimize:**
- Break up long tasks
- Use web workers for heavy computation
- Defer non-critical JavaScript

```tsx
// ❌ Bad - blocks main thread
function processLargeData(data) {
  // 500ms synchronous operation
  return data.map(heavyComputation);
}

// ✅ Good - web worker
const worker = new Worker('/data-processor.worker.js');
worker.postMessage(data);
worker.onmessage = (e) => setProcessedData(e.data);
```

### Cumulative Layout Shift (CLS)

Target: < 0.1

**Optimize:**
- Set explicit dimensions for images/videos
- Reserve space for dynamic content
- Avoid inserting content above existing content

```tsx
// ❌ Bad - causes layout shift
<img src="/image.jpg" alt="Unsized image" />

// ✅ Good - dimensions prevent shift
<img
  src="/image.jpg"
  width={800}
  height={600}
  alt="Sized image"
/>

// Or with aspect ratio
<div style={{ aspectRatio: '16/9' }}>
  <img src="/image.jpg" alt="Aspect ratio image" />
</div>
```

## Data Prefetching

### Route Prefetching

Prefetch routes user is likely to visit:

```tsx
import { useEffect } from 'react';

function HomePage() {
  useEffect(() => {
    // Prefetch likely next routes
    import('./routes/Dashboard');
    import('./routes/Products');
  }, []);

  return <div>Home</div>;
}
```

### React Query Prefetching

```tsx
import { useQueryClient } from '@tanstack/react-query';

function ProductList() {
  const queryClient = useQueryClient();

  const prefetchProduct = (productId) => {
    queryClient.prefetchQuery({
      queryKey: ['product', productId],
      queryFn: () => fetchProduct(productId),
    });
  };

  return (
    <ul>
      {products.map(product => (
        <li
          key={product.id}
          onMouseEnter={() => prefetchProduct(product.id)}
        >
          <Link to={`/products/${product.id}`}>{product.name}</Link>
        </li>
      ))}
    </ul>
  );
}
```

## Performance Monitoring

### React DevTools Profiler

Profile component renders:

```tsx
import { Profiler } from 'react';

function onRenderCallback(
  id,
  phase,
  actualDuration,
  baseDuration,
  startTime,
  commitTime
) {
  console.log(`${id} (${phase}) took ${actualDuration}ms`);
}

<Profiler id="App" onRender={onRenderCallback}>
  <App />
</Profiler>
```

### Web Vitals Library

```tsx
import { onCLS, onFID, onLCP } from 'web-vitals';

onCLS(console.log);
onFID(console.log);
onLCP(console.log);
```

### Performance Observer

```tsx
// Monitor long tasks
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.duration > 50) {
      console.warn('Long task detected:', entry);
    }
  }
});

observer.observe({ entryTypes: ['longtask'] });
```

## Quick Wins Checklist

- [ ] Enable code splitting at routes
- [ ] Lazy load heavy components (charts, editors)
- [ ] Add lazy loading to images
- [ ] Virtualize lists > 100 items
- [ ] Use React Query for all server data
- [ ] Memoize expensive computations with `useMemo`
- [ ] Use `React.memo` for expensive pure components
- [ ] Analyze and reduce bundle size
- [ ] Prefetch likely user actions
- [ ] Monitor Web Vitals in production

Performance optimization is iterative - measure, optimize, and measure again.
