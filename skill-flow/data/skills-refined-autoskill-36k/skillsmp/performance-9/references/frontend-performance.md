# Frontend Performance

Core Web Vitals and client-side optimization.

## Core Web Vitals

| Metric | Good | Needs Work | Poor | What It Measures |
|--------|------|------------|------|------------------|
| LCP | < 2.5s | 2.5-4s | > 4s | Largest contentful paint |
| INP | < 200ms | 200-500ms | > 500ms | Interaction to next paint |
| CLS | < 0.1 | 0.1-0.25 | > 0.25 | Cumulative layout shift |

## Largest Contentful Paint (LCP)

### Common Causes & Fixes

```html
<!-- ❌ Slow: Render-blocking CSS -->
<link rel="stylesheet" href="huge.css">

<!-- ✅ Fast: Critical CSS inline, rest deferred -->
<style>/* Critical CSS here */</style>
<link rel="preload" href="styles.css" as="style" onload="this.rel='stylesheet'">

<!-- ❌ Slow: Unoptimized hero image -->
<img src="hero.jpg">

<!-- ✅ Fast: Optimized with modern formats -->
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" loading="eager" fetchpriority="high"
       width="1200" height="600" alt="Hero">
</picture>
```

### Resource Hints

```html
<!-- Preconnect to critical origins -->
<link rel="preconnect" href="https://api.example.com">
<link rel="dns-prefetch" href="https://cdn.example.com">

<!-- Preload critical resources -->
<link rel="preload" href="/fonts/main.woff2" as="font" crossorigin>
<link rel="preload" href="/hero.webp" as="image">
```

## Interaction to Next Paint (INP)

### Common Causes & Fixes

```javascript
// ❌ Slow: Long task blocks main thread
function processData(data) {
  for (let i = 0; i < 1000000; i++) {
    heavyComputation(data[i]);
  }
}

// ✅ Fast: Break into chunks
async function processData(data) {
  for (let i = 0; i < data.length; i++) {
    heavyComputation(data[i]);
    if (i % 1000 === 0) {
      await new Promise(r => setTimeout(r, 0));  // Yield to main thread
    }
  }
}

// ✅ Better: Use Web Worker
const worker = new Worker('processor.js');
worker.postMessage(data);
worker.onmessage = (e) => updateUI(e.data);
```

### Debounce User Input

```javascript
// ❌ Slow: Handler runs on every keystroke
input.addEventListener('input', (e) => {
  search(e.target.value);  // API call on every key
});

// ✅ Fast: Debounced
let timeout;
input.addEventListener('input', (e) => {
  clearTimeout(timeout);
  timeout = setTimeout(() => search(e.target.value), 300);
});
```

## Cumulative Layout Shift (CLS)

### Common Causes & Fixes

```html
<!-- ❌ CLS: Image without dimensions -->
<img src="photo.jpg">

<!-- ✅ No CLS: Explicit dimensions -->
<img src="photo.jpg" width="400" height="300">

<!-- ✅ No CLS: Aspect ratio box -->
<div style="aspect-ratio: 16/9;">
  <img src="photo.jpg" style="width: 100%; height: 100%; object-fit: cover;">
</div>

<!-- ❌ CLS: Dynamic content injection -->
<div id="ad-slot"></div>  <!-- Ad loads and pushes content down -->

<!-- ✅ No CLS: Reserve space -->
<div id="ad-slot" style="min-height: 250px;"></div>
```

### Font Loading

```css
/* ❌ CLS: Font swap causes text reflow */
@font-face {
  font-family: 'CustomFont';
  src: url('font.woff2');
}

/* ✅ No CLS: Optional swap + preload */
@font-face {
  font-family: 'CustomFont';
  src: url('font.woff2');
  font-display: optional;  /* Use fallback if not loaded quickly */
}
```

## JavaScript Bundle Optimization

```javascript
// ❌ Large initial bundle
import { everything } from 'huge-library';

// ✅ Code splitting with dynamic imports
const HeavyComponent = lazy(() => import('./HeavyComponent'));

// ✅ Tree-shaking friendly imports
import { specificFunction } from 'library';
```

## Measurement

```bash
# Lighthouse CLI
npx lighthouse https://example.com --view

# Web Vitals in code
import {onLCP, onINP, onCLS} from 'web-vitals';

onLCP(console.log);
onINP(console.log);
onCLS(console.log);
```
