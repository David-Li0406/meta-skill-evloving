---
name: performance-optimization
description: Optimize application performance in React by addressing slow renders, large bundles, and memory issues through techniques like lazy loading, code splitting, memoization, and virtualization.
---

# Performance Optimization

## When to Use This Skill

Use this skill when:
- Initial load time is too slow
- Components re-render unnecessarily
- Rendering large lists or data sets
- Bundle size is too large
- Memory usage is high
- Page load times need improvement

## Instructions

### Step 1: Performance Measurement

**Lighthouse (Chrome DevTools)**:
```bash
# CLI
npm install -g lighthouse
lighthouse https://example.com --view

# CI Automation
lighthouse https://example.com --output=json --output-path=./report.json
```

**Web Vitals Measurement (React)**:
```typescript
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function sendToAnalytics(metric: any) {
  console.log(metric);
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);
```

### Step 2: React Optimization

**React.memo**:
```tsx
const ExpensiveComponent = React.memo(({ data }: { data: Data }) => {
  return <div>{/* expensive render */}</div>;
});
```

**useMemo & useCallback**:
```tsx
function ProductList({ products, category }: Props) {
  const filteredProducts = useMemo(() => {
    return products.filter(p => p.category === category);
  }, [products, category]);

  const handleAddToCart = useCallback((id: string) => {
    addToCart(id);
  }, []);

  return (
    <div>
      {filteredProducts.map(product => (
        <ProductCard key={product.id} product={product} onAdd={handleAddToCart} />
      ))}
    </div>
  );
}
```

### Step 3: Code Splitting & Lazy Loading

**React.lazy for Route-based Splitting**:
```tsx
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

**Named Exports with Lazy**:
```tsx
const LazyComponent = lazy(() =>
  import('./components').then(module => ({
    default: module.SpecificComponent
  }))
);
```

### Step 4: List Virtualization

**Using react-window**:
```tsx
import { FixedSizeList } from 'react-window';

function VirtualList({ items, onSelect }: { items: Item[]; onSelect: (id: string) => void; }) {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style} onClick={() => onSelect(items[index].id)}>
      {items[index].name}
    </div>
  );

  return (
    <FixedSizeList
      height={400}
      width="100%"
      itemCount={items.length}
      itemSize={50}
    >
      {Row}
    </FixedSizeList>
  );
}
```

### Step 5: Bundle Size Optimization

**Webpack Bundle Analyzer**:
```bash
npm install --save-dev webpack-bundle-analyzer

# package.json
{
  "scripts": {
    "analyze": "webpack-bundle-analyzer build/stats.json"
  }
}
```

**Tree Shaking**:
```typescript
import debounce from 'lodash/debounce'; // Import only what is needed
```

### Performance Checklist

- [ ] Use React.lazy for route-level code splitting
- [ ] Wrap expensive components with React.memo
- [ ] Use useMemo for expensive calculations
- [ ] Use useCallback for callback props passed to memoized children
- [ ] Virtualize lists with more than 100 items
- [ ] Debounce input handlers
- [ ] Lazy load images below the fold
- [ ] Split vendor chunks from app code

## Constraints

### Must Rules
1. **Measure First**: Profile before optimizing.
2. **Incremental Improvement**: Optimize one aspect at a time.
3. **Performance Monitoring**: Continuously track performance.

### Must Not Rules
1. **Premature Optimization**: Avoid optimizing without identifying bottlenecks.
2. **Sacrificing Readability**: Do not complicate code for performance gains.

## Best Practices

1. **80/20 Rule**: Focus on changes that yield the most significant improvements.
2. **User-Centric**: Prioritize enhancements that improve user experience.
3. **Automation**: Implement performance regression tests in CI.

## References

- [web.dev/vitals](https://web.dev/vitals/)
- [React Optimization](https://react.dev/learn/render-and-commit#optimizing-performance)
- [Webpack Bundle Analyzer](https://github.com/webpack-contrib/webpack-bundle-analyzer)