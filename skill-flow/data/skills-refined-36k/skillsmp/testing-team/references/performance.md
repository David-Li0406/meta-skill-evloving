# Performance Profiling

## Core Web Vitals

### Metrics to Track

| Metric | Target | What It Measures |
|--------|--------|------------------|
| **LCP** (Largest Contentful Paint) | <2.5s | Loading performance |
| **INP** (Interaction to Next Paint) | <200ms | Responsiveness |
| **CLS** (Cumulative Layout Shift) | <0.1 | Visual stability |
| **FCP** (First Contentful Paint) | <1.8s | Initial render |
| **TTFB** (Time to First Byte) | <800ms | Server response |

### Measuring in Code

```typescript
// Use web-vitals library
import { onLCP, onINP, onCLS } from 'web-vitals';

function sendToAnalytics(metric: Metric) {
  console.log(metric.name, metric.value);
  // Send to your analytics service
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
```

## React Performance

### Identifying Re-renders

```typescript
// React DevTools Profiler
// 1. Open React DevTools
// 2. Go to Profiler tab
// 3. Click record, interact, stop
// 4. Look for components rendering often

// why-did-you-render for development
import React from 'react';

if (process.env.NODE_ENV === 'development') {
  const whyDidYouRender = require('@welldone-software/why-did-you-render');
  whyDidYouRender(React, {
    trackAllPureComponents: true,
  });
}

// Add to specific component
ResourceBar.whyDidYouRender = true;
```

### Common Re-render Causes

```typescript
// ❌ Bad: New object every render
function Parent() {
  return <Child style={{ color: 'red' }} />;  // New object each time!
}

// ✅ Good: Stable reference
const childStyle = { color: 'red' };  // Outside component

function Parent() {
  return <Child style={childStyle} />;
}

// ✅ Good: useMemo for computed styles
function Parent({ isActive }) {
  const style = useMemo(() => ({ 
    color: isActive ? 'green' : 'red' 
  }), [isActive]);
  
  return <Child style={style} />;
}
```

### Optimizing Expensive Components

```typescript
// Memoize component that renders often
const HexCell = memo(function HexCell({ hex, onClick }: HexCellProps) {
  return (
    <div onClick={() => onClick(hex.id)} className="hex-cell">
      {/* expensive rendering */}
    </div>
  );
});

// Custom comparison for complex props
const HexCell = memo(
  function HexCell({ hex, onClick }: HexCellProps) { ... },
  (prevProps, nextProps) => {
    return (
      prevProps.hex.id === nextProps.hex.id &&
      prevProps.hex.state === nextProps.hex.state &&
      prevProps.hex.growthStage === nextProps.hex.growthStage
    );
  }
);
```

### Virtualizing Large Lists

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function LeaderboardList({ entries }: { entries: LeaderboardEntry[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  
  const virtualizer = useVirtualizer({
    count: entries.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 60,  // Estimated row height
    overscan: 5,             // Render 5 extra items
  });
  
  return (
    <div ref={parentRef} className="h-[400px] overflow-auto">
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map((virtualRow) => (
          <div
            key={virtualRow.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            <LeaderboardRow entry={entries[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Bundle Optimization

### Analyzing Bundle Size

```bash
# Vite bundle analyzer
npm install -D rollup-plugin-visualizer

# Add to vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer';

export default {
  plugins: [
    visualizer({
      open: true,
      filename: 'dist/stats.html',
    }),
  ],
};

# Build and analyze
bun run build  # Opens visualization
```

### Code Splitting

```typescript
// Route-based splitting (React Router)
import { lazy } from 'react';

const GameBoard = lazy(() => import('./pages/GameBoard'));
const Shop = lazy(() => import('./pages/Shop'));
const Leaderboard = lazy(() => import('./pages/Leaderboard'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/game" element={<GameBoard />} />
        <Route path="/shop" element={<Shop />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
      </Routes>
    </Suspense>
  );
}

// Component-level splitting
const CelebrationAnimation = lazy(() => 
  import('./components/CelebrationAnimation')
);

function WinScreen({ show }: { show: boolean }) {
  if (!show) return null;
  
  return (
    <Suspense fallback={null}>
      <CelebrationAnimation />
    </Suspense>
  );
}
```

### Tree Shaking

```typescript
// ❌ Bad: Imports entire library
import * as _ from 'lodash';
_.debounce(fn, 300);

// ✅ Good: Import only what you need
import debounce from 'lodash/debounce';
debounce(fn, 300);

// ✅ Best: Use native or lighter alternatives
function debounce<T extends (...args: any[]) => void>(
  fn: T,
  delay: number
): T {
  let timeoutId: ReturnType<typeof setTimeout>;
  return ((...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  }) as T;
}
```

## Animation Performance

### 60fps Checklist

```
□ Only animating transform and opacity
□ Using will-change sparingly
□ Animations are GPU-accelerated
□ No layout thrashing in animation loop
□ Using requestAnimationFrame (not setInterval)
□ Particle count is reasonable (<100 simultaneous)
```

### Debugging Jank

```javascript
// Chrome DevTools > Performance tab
// 1. Click record
// 2. Trigger animation
// 3. Stop recording
// 4. Look for long frames (>16.67ms)

// Check for forced synchronous layout
// Look for purple "Recalculate Style" followed by purple "Layout"
// in the same frame - this is layout thrashing

// Common causes:
// - Reading offsetHeight/offsetWidth after writes
// - Multiple DOM writes without batching
// - Animating top/left instead of transform
```

### GPU Acceleration

```css
/* Force GPU layer */
.animated-element {
  will-change: transform;  /* Apply before animating */
  transform: translateZ(0); /* Force GPU layer */
}

/* Remove after animation */
.animated-element.done {
  will-change: auto;
}
```

```typescript
// In React
function AnimatedCard({ isAnimating }: { isAnimating: boolean }) {
  return (
    <motion.div
      style={{ willChange: isAnimating ? 'transform' : 'auto' }}
      animate={{ x: isAnimating ? 100 : 0 }}
    />
  );
}
```

## Memory Profiling

### Finding Memory Leaks

```javascript
// Chrome DevTools > Memory tab
// 1. Take heap snapshot
// 2. Perform actions
// 3. Take another snapshot
// 4. Compare - look for objects that should be GC'd

// Common React leaks:
// - setInterval without cleanup
// - Event listeners without removal
// - Subscriptions without unsubscribe
// - Closures holding references
```

### Cleanup Patterns

```typescript
// ✅ Correct cleanup
useEffect(() => {
  const subscription = eventBus.subscribe('event', handler);
  const intervalId = setInterval(tick, 1000);
  
  return () => {
    subscription.unsubscribe();
    clearInterval(intervalId);
  };
}, []);

// ✅ Abort controller for fetch
useEffect(() => {
  const controller = new AbortController();
  
  fetch('/api/data', { signal: controller.signal })
    .then(res => res.json())
    .then(setData)
    .catch(err => {
      if (err.name !== 'AbortError') throw err;
    });
  
  return () => controller.abort();
}, []);
```

## Load Time Optimization

### Critical Rendering Path

```html
<!-- Preload critical assets -->
<link rel="preload" href="/fonts/main.woff2" as="font" crossorigin>
<link rel="preload" href="/sprites/main.webp" as="image">

<!-- Defer non-critical JS -->
<script src="/analytics.js" defer></script>

<!-- Inline critical CSS -->
<style>
  /* Only above-the-fold styles */
  .game-container { display: flex; }
  .hex-grid { position: relative; }
</style>
```

### Image Optimization

```typescript
// Use next-gen formats with fallback
<picture>
  <source srcset="/hero.avif" type="image/avif">
  <source srcset="/hero.webp" type="image/webp">
  <img src="/hero.png" alt="Game hero" loading="lazy">
</picture>

// Responsive images
<img
  srcset="/sprite-1x.webp 1x, /sprite-2x.webp 2x"
  src="/sprite-1x.webp"
  alt="Sprite"
  width={64}
  height={64}
  loading="lazy"
/>
```

## Performance Budget

```json
// bundlesize.config.json
{
  "files": [
    {
      "path": "dist/assets/index-*.js",
      "maxSize": "150 KB"
    },
    {
      "path": "dist/assets/index-*.css",
      "maxSize": "30 KB"
    },
    {
      "path": "dist/assets/vendor-*.js",
      "maxSize": "100 KB"
    }
  ]
}
```

```yaml
# CI check
- name: Check bundle size
  run: |
    bun run build
    npx bundlesize
```

## Quick Wins Checklist

```markdown
## Immediate Optimizations

### Bundle
- [ ] Enable gzip/brotli compression
- [ ] Split routes with lazy()
- [ ] Remove unused dependencies
- [ ] Use production builds

### Images
- [ ] Convert to WebP/AVIF
- [ ] Add width/height attributes
- [ ] Lazy load below-fold images
- [ ] Use appropriate sizes

### Fonts
- [ ] Use font-display: swap
- [ ] Preload critical fonts
- [ ] Subset fonts if possible
- [ ] Use system fonts where appropriate

### React
- [ ] Wrap expensive components in memo()
- [ ] Use callback refs over string refs
- [ ] Virtualize long lists
- [ ] Avoid inline objects in JSX

### CSS
- [ ] Purge unused CSS
- [ ] Avoid expensive selectors
- [ ] Use CSS containment
- [ ] Minimize layout shifts
```
