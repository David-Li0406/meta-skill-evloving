---
name: performance
description: Core Web Vitals optimization and Lighthouse performance guidelines. Use when optimizing page speed, reducing bundle size, implementing caching, or diagnosing performance issues.
allowed-tools: Read, Edit, Bash(npm:*, npx:*, lighthouse:*)
---

# Performance Optimization (Core Web Vitals)

Domain knowledge for optimizing web performance in this Astro template.

## When to Use

Apply this knowledge when:
- Lighthouse scores drop below thresholds (90+ performance)
- Pages feel slow to load or interact
- Bundle sizes are growing
- Implementing images or media
- Adding third-party scripts
- Configuring caching strategies
- Debugging Core Web Vitals issues

## Key Concepts

### Core Web Vitals (2024)

| Metric | Good | Needs Work | Poor | Measures |
|--------|------|------------|------|----------|
| **LCP** | < 2.5s | 2.5-4s | > 4s | Loading performance |
| **INP** | < 200ms | 200-500ms | > 500ms | Interactivity |
| **CLS** | < 0.1 | 0.1-0.25 | > 0.25 | Visual stability |

**Note**: INP (Interaction to Next Paint) replaced FID in March 2024.

### This Template's Targets

```yaml
# Lighthouse CI thresholds (config/lighthouse.json)
performance: 90
accessibility: 95
best-practices: 90
seo: 90
```

## Largest Contentful Paint (LCP)

LCP measures how long the largest visible element takes to render.

### Common LCP Elements

1. `<img>` elements
2. `<video>` poster images
3. Background images via CSS
4. Block-level text elements

### Optimization Strategies

**1. Preload Critical Images**

```astro
---
// In BaseLayout.astro
---
<head>
  <link
    rel="preload"
    as="image"
    href="/hero.webp"
    fetchpriority="high"
  />
</head>
```

**2. Optimize Hero Images**

```astro
---
import { Image } from 'astro:assets';
import hero from '../assets/hero.jpg';
---

<Image
  src={hero}
  alt="Hero"
  width={1200}
  height={630}
  format="webp"
  quality={80}
  loading="eager"        <!-- Don't lazy-load LCP image -->
  fetchpriority="high"
/>
```

**3. Inline Critical CSS**

```javascript
// astro.config.mjs
export default defineConfig({
  build: {
    inlineStylesheets: 'auto', // Inlines small stylesheets
  },
});
```

**4. Avoid Render-Blocking Resources**

```astro
<!-- Defer non-critical JS -->
<script src="/analytics.js" defer></script>

<!-- Async load fonts -->
<link
  rel="preload"
  href="/fonts/inter.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>
```

## Interaction to Next Paint (INP)

INP measures responsiveness to user interactions.

### Optimization Strategies

**1. Break Up Long Tasks**

```javascript
// WRONG: Blocks main thread
function processLargeArray(items) {
  items.forEach(item => heavyComputation(item));
}

// CORRECT: Yield to main thread
async function processLargeArray(items) {
  for (const item of items) {
    heavyComputation(item);
    // Yield every 50ms
    if (performance.now() - start > 50) {
      await scheduler.yield(); // Or setTimeout(0)
      start = performance.now();
    }
  }
}
```

**2. Use requestIdleCallback for Non-Critical Work**

```javascript
// Defer non-essential initialization
requestIdleCallback(() => {
  initializeAnalytics();
  loadComments();
});
```

**3. Event Delegation**

```javascript
// WRONG: Many listeners
document.querySelectorAll('.card').forEach(card => {
  card.addEventListener('click', handleClick);
});

// CORRECT: Single listener
document.querySelector('.card-grid').addEventListener('click', (e) => {
  const card = e.target.closest('.card');
  if (card) handleClick(e);
});
```

**4. Debounce Input Handlers**

```javascript
function debounce(fn, delay) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
}

searchInput.addEventListener('input', debounce(handleSearch, 300));
```

## Cumulative Layout Shift (CLS)

CLS measures visual stability during loading.

### Common Causes

1. Images without dimensions
2. Ads/embeds without reserved space
3. Dynamically injected content
4. Web fonts causing FOUT/FOIT
5. Animations triggering layout

### Optimization Strategies

**1. Always Set Image Dimensions**

```astro
<!-- WRONG: No dimensions -->
<img src="photo.jpg" alt="Photo" />

<!-- CORRECT: Explicit dimensions -->
<img src="photo.jpg" alt="Photo" width="800" height="600" />

<!-- BEST: Use Astro Image -->
<Image src={photo} alt="Photo" width={800} height={600} />
```

**2. Reserve Space for Dynamic Content**

```astro
<!-- DynamicContent handles this automatically -->
<DynamicContent
  endpoint="/api/comments"
  minHeight="200px"      <!-- Reserves space -->
  skeleton="shimmer"     <!-- Visual placeholder -->
/>
```

**3. Font Loading Strategy**

```css
/* Use font-display: swap for FOUT (preferred for performance) */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter.woff2') format('woff2');
  font-display: swap;
}

/* Or optional to prevent layout shift (may show fallback longer) */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter.woff2') format('woff2');
  font-display: optional;
}
```

**4. Aspect Ratio Boxes**

```css
/* For responsive containers */
.video-container {
  aspect-ratio: 16 / 9;
  width: 100%;
}

/* Or old method for wider support */
.video-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 */
}
```

**5. Avoid Layout-Triggering Animations**

```css
/* WRONG: Triggers layout */
.animate {
  animation: slide 0.3s;
}
@keyframes slide {
  from { margin-left: -100px; }
  to { margin-left: 0; }
}

/* CORRECT: Uses transform (GPU-accelerated) */
.animate {
  animation: slide 0.3s;
}
@keyframes slide {
  from { transform: translateX(-100px); }
  to { transform: translateX(0); }
}
```

## Image Optimization

### Format Selection

| Format | Use Case | Browser Support |
|--------|----------|-----------------|
| **WebP** | General purpose | 97%+ |
| **AVIF** | Best compression | 92%+ |
| **JPEG** | Fallback for photos | 100% |
| **PNG** | Transparency needed | 100% |
| **SVG** | Icons, logos | 100% |

### Astro Image Component

```astro
---
import { Image, Picture } from 'astro:assets';
import hero from '../assets/hero.jpg';
---

<!-- Single format (WebP) -->
<Image
  src={hero}
  alt="Hero"
  width={1200}
  quality={80}
  format="webp"
/>

<!-- Multiple formats with Picture -->
<Picture
  src={hero}
  formats={['avif', 'webp']}
  widths={[400, 800, 1200]}
  sizes="(max-width: 800px) 100vw, 800px"
  alt="Hero"
/>
```

### Lazy Loading

```astro
<!-- Lazy load below-fold images -->
<Image
  src={photo}
  alt="Photo"
  loading="lazy"
  decoding="async"
/>

<!-- Eager load LCP image -->
<Image
  src={hero}
  alt="Hero"
  loading="eager"
  fetchpriority="high"
/>
```

## Code Splitting

### Dynamic Imports

```astro
---
// Only load heavy component when needed
---

<div id="chart-container"></div>

<script>
  // Load Chart.js only when visible
  const observer = new IntersectionObserver(async (entries) => {
    if (entries[0].isIntersecting) {
      const { Chart } = await import('chart.js');
      // Initialize chart
      observer.disconnect();
    }
  });

  observer.observe(document.getElementById('chart-container'));
</script>
```

### Client Directives in Astro

```astro
<!-- Load and hydrate immediately -->
<Counter client:load />

<!-- Load when visible -->
<Comments client:visible />

<!-- Load when idle -->
<Analytics client:idle />

<!-- Load on specific media query -->
<Sidebar client:media="(min-width: 768px)" />
```

### Bundle Analysis

```bash
# Build with stats
npm run build -- --stats

# Or use rollup-plugin-visualizer
# Add to astro.config.mjs vite.plugins
```

## Caching Strategies

### Static Assets (Long Cache)

```
# In your CDN/server config
Cache-Control: public, max-age=31536000, immutable

# Applies to:
/_assets/*     # Hashed assets
/fonts/*       # Web fonts
```

### HTML Pages (Short Cache with Revalidation)

```
Cache-Control: public, max-age=0, must-revalidate

# Or with stale-while-revalidate
Cache-Control: public, max-age=60, stale-while-revalidate=86400
```

### Service Worker (This Template)

```javascript
// Basic caching strategy
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cached) => {
      // Return cached or fetch
      return cached || fetch(event.request);
    })
  );
});
```

## Third-Party Scripts

### Loading Strategies

```astro
<!-- 1. Defer: Load after HTML parse, before DOMContentLoaded -->
<script src="https://example.com/script.js" defer></script>

<!-- 2. Async: Load in parallel, execute when ready -->
<script src="https://example.com/script.js" async></script>

<!-- 3. Lazy load on interaction -->
<script>
  document.getElementById('chat-button').addEventListener('click', () => {
    const script = document.createElement('script');
    script.src = 'https://chat-widget.com/embed.js';
    document.body.appendChild(script);
  }, { once: true });
</script>
```

### Facade Pattern

```astro
<!-- Show static placeholder, load real widget on interaction -->
<div id="youtube-embed" data-video-id="abc123">
  <img src="/youtube-thumbnail.jpg" alt="Video thumbnail" />
  <button aria-label="Play video">Play</button>
</div>

<script>
  document.getElementById('youtube-embed').addEventListener('click', () => {
    // Replace with actual iframe
    this.innerHTML = `<iframe src="https://youtube.com/embed/abc123" ...></iframe>`;
  }, { once: true });
</script>
```

## Monitoring and Testing

### Lighthouse CI

```bash
# Run Lighthouse audit
npm run lighthouse

# Or manually
npx lighthouse https://localhost:4321 --view
```

### Web Vitals Measurement

```javascript
// Add to your analytics
import { onCLS, onINP, onLCP } from 'web-vitals';

onCLS(console.log);
onINP(console.log);
onLCP(console.log);
```

### Performance Budget

```javascript
// config/lighthouse.json
{
  "ci": {
    "collect": {
      "url": ["http://localhost:4321/"]
    },
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "total-blocking-time": ["error", { "maxNumericValue": 200 }]
      }
    }
  }
}
```

## Project-Specific Optimizations

### DynamicContent Performance

```astro
<!-- Good: Load when visible with skeleton -->
<DynamicContent
  endpoint="/api/comments"
  trigger="revealed"
  skeleton="shimmer"
  minHeight="200px"
/>

<!-- Bad: Load everything immediately -->
<DynamicContent
  endpoint="/api/comments"
  trigger="load"
/>
```

### YAML-Driven Asset Loading

```yaml
# {domain}.yaml
design:
  fonts:
    heading: Inter       # Will be preloaded
    body: system-ui      # Uses system fonts (fastest)
```

### Build Configuration

```javascript
// astro.config.mjs
export default defineConfig({
  build: {
    inlineStylesheets: 'auto',
    assets: '_assets',  // Enables hashing for caching
  },
  vite: {
    build: {
      chunkSizeWarningLimit: 100, // Alert on large chunks
    },
  },
});
```

## Common Mistakes

### 1. Not Setting Image Dimensions

```html
<!-- WRONG: Causes CLS -->
<img src="photo.jpg" />

<!-- CORRECT -->
<img src="photo.jpg" width="800" height="600" />
```

### 2. Loading Everything Eagerly

```astro
<!-- WRONG: Loads all frameworks immediately -->
<HeavyChart client:load />

<!-- CORRECT: Load when visible -->
<HeavyChart client:visible />
```

### 3. Blocking Render with JS

```html
<!-- WRONG: Blocks parsing -->
<script src="app.js"></script>

<!-- CORRECT: Defer non-critical -->
<script src="app.js" defer></script>
```

### 4. Ignoring Font Loading

```css
/* WRONG: No font-display */
@font-face {
  font-family: 'Custom';
  src: url('/font.woff2');
}

/* CORRECT */
@font-face {
  font-family: 'Custom';
  src: url('/font.woff2');
  font-display: swap;
}
```

### 5. Using Layout Animations

```css
/* WRONG: Animates layout properties */
.animate {
  transition: width 0.3s, height 0.3s;
}

/* CORRECT: Use transform and opacity */
.animate {
  transition: transform 0.3s, opacity 0.3s;
}
```

## Quick Checklist

### Before Launch

- [ ] Run Lighthouse (target: 90+ performance)
- [ ] Check Core Web Vitals in Chrome DevTools
- [ ] Verify LCP image is preloaded
- [ ] All images have width/height
- [ ] Fonts use `font-display: swap`
- [ ] Third-party scripts deferred/lazy
- [ ] Bundle size under budget

### Debug Tools

```bash
# Lighthouse
npm run lighthouse

# Bundle analysis
npm run build -- --stats

# Web Vitals
# Chrome DevTools > Performance > Web Vitals
```

## Related

- Config: `config/lighthouse.json`
- CI: `.github/workflows/ci.yml`
- Image component: `src/components/DynamicContent.astro`
- web.dev/vitals: https://web.dev/vitals/
- Lighthouse: https://developer.chrome.com/docs/lighthouse/
