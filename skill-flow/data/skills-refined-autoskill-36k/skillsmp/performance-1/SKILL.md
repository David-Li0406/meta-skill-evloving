---
name: performance
description: Write performance-friendly HTML pages. Use when optimizing page load, adding resources, configuring caching, or improving Core Web Vitals scores.
allowed-tools: Read, Write, Edit
---

# Performance Skill

This skill ensures HTML pages are optimized for fast loading and good Core Web Vitals scores.

## Core Web Vitals

The three metrics Google uses for page experience:

| Metric | Target | Measures |
|--------|--------|----------|
| **LCP** (Largest Contentful Paint) | < 2.5s | Loading performance |
| **INP** (Interaction to Next Paint) | < 200ms | Interactivity |
| **CLS** (Cumulative Layout Shift) | < 0.1 | Visual stability |

## Resource Hints

### Preconnect (High Priority)

Establish early connections to critical third-party origins:

```html
<head>
  <!-- DNS + TCP + TLS handshake for critical origins -->
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://cdn.example.com" crossorigin/>

  <!-- DNS-only for less critical origins -->
  <link rel="dns-prefetch" href="https://analytics.example.com"/>
</head>
```

**When to use:**
- Font providers (Google Fonts, Adobe Fonts)
- CDNs serving critical assets
- API endpoints called early in page load

### Preload (Critical Resources)

Load resources needed for current page immediately:

```html
<head>
  <!-- Critical CSS -->
  <link rel="preload" href="/css/critical.css" as="style"/>

  <!-- Hero image (LCP candidate) -->
  <link rel="preload" href="/images/hero.webp" as="image" type="image/webp"/>

  <!-- Critical font -->
  <link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin/>

  <!-- Critical script -->
  <link rel="preload" href="/js/app.js" as="script"/>
</head>
```

**The `as` attribute values:**
| Value | Resource Type |
|-------|---------------|
| `style` | CSS stylesheets |
| `script` | JavaScript files |
| `font` | Font files (requires `crossorigin`) |
| `image` | Images |
| `fetch` | XHR/fetch requests |
| `document` | HTML documents (iframes) |

### Prefetch (Future Navigation)

Load resources for likely next pages:

```html
<head>
  <!-- Next page the user will likely visit -->
  <link rel="prefetch" href="/products/"/>

  <!-- Resources for next page -->
  <link rel="prefetch" href="/css/products.css" as="style"/>
</head>
```

### Prerender (Speculative Loading)

Fully render a page in the background:

```html
<head>
  <!-- Only for very likely navigations -->
  <script type="speculationrules">
  {
    "prerender": [
      {"source": "list", "urls": ["/checkout/"]}
    ]
  }
  </script>
</head>
```

## Fetch Priority

### Priority Hints

Control resource loading priority:

```html
<!-- High priority for LCP image -->
<img src="hero.jpg" alt="Hero" fetchpriority="high"/>

<!-- Low priority for below-fold images -->
<img src="footer-logo.jpg" alt="Logo" fetchpriority="low" loading="lazy"/>

<!-- High priority for critical script -->
<script src="critical.js" fetchpriority="high"></script>

<!-- Low priority for analytics -->
<script src="analytics.js" fetchpriority="low" defer></script>
```

**Priority values:**
| Value | Use For |
|-------|---------|
| `high` | LCP images, critical scripts, above-fold content |
| `low` | Below-fold images, analytics, non-critical resources |
| `auto` | Default browser behavior |

## Image Optimization

### Lazy Loading

Defer loading of below-fold images:

```html
<!-- Above the fold: load immediately -->
<img src="hero.jpg" alt="Hero" fetchpriority="high"/>

<!-- Below the fold: lazy load -->
<img src="product.jpg" alt="Product" loading="lazy" decoding="async"/>
```

### Responsive Images with Performance

```html
<picture>
  <!-- Modern format first (smallest) -->
  <source type="image/avif"
          srcset="photo-400.avif 400w, photo-800.avif 800w, photo-1200.avif 1200w"
          sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 600px"/>
  <source type="image/webp"
          srcset="photo-400.webp 400w, photo-800.webp 800w, photo-1200.webp 1200w"
          sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 600px"/>
  <!-- Fallback -->
  <img src="photo-800.jpg"
       srcset="photo-400.jpg 400w, photo-800.jpg 800w, photo-1200.jpg 1200w"
       sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 600px"
       alt="Description"
       width="800"
       height="600"
       loading="lazy"
       decoding="async"/>
</picture>
```

### Prevent Layout Shift (CLS)

Always specify dimensions:

```html
<!-- GOOD: Dimensions prevent layout shift -->
<img src="photo.jpg" alt="Photo" width="800" height="600"/>

<!-- BAD: No dimensions cause layout shift -->
<img src="photo.jpg" alt="Photo"/>
```

For responsive images, use aspect-ratio:

```css
img {
  aspect-ratio: 4 / 3;
  width: 100%;
  height: auto;
}
```

## CSS Loading

### Critical CSS (Inline)

Inline critical above-the-fold styles:

```html
<head>
  <!-- Critical CSS inline -->
  <style>
    /* Only styles needed for above-fold content */
    :root { --color-primary: #0066cc; }
    body { margin: 0; font-family: system-ui, sans-serif; }
    header { background: var(--color-primary); }
    /* ... minimal critical styles ... */
  </style>

  <!-- Full CSS loaded async -->
  <link rel="preload" href="/css/main.css" as="style" onload="this.onload=null;this.rel='stylesheet'"/>
  <noscript><link rel="stylesheet" href="/css/main.css"/></noscript>
</head>
```

### Non-Blocking CSS

Load non-critical CSS without blocking render:

```html
<!-- Print styles: non-blocking by default -->
<link rel="stylesheet" href="/css/print.css" media="print"/>

<!-- Load async, then apply -->
<link rel="stylesheet" href="/css/non-critical.css" media="print" onload="this.media='all'"/>
```

### CSS Containment

Limit rendering scope with containment:

```css
/* Isolate components for better performance */
.card {
  contain: layout style paint;
}

/* Full containment for off-screen content */
.lazy-section {
  contain: strict;
  content-visibility: auto;
  contain-intrinsic-size: 0 500px;
}
```

## JavaScript Loading

### Script Loading Strategies

```html
<!-- Blocking (avoid): Stops HTML parsing -->
<script src="blocking.js"></script>

<!-- Async: Download parallel, execute when ready (order not guaranteed) -->
<script src="analytics.js" async></script>

<!-- Defer: Download parallel, execute after HTML parsed (order preserved) -->
<script src="app.js" defer></script>

<!-- Module: Deferred by default -->
<script type="module" src="app.mjs"></script>
```

**When to use each:**

| Strategy | Use For |
|----------|---------|
| No attribute | Scripts that must run immediately (rare) |
| `async` | Independent scripts (analytics, ads) |
| `defer` | Scripts that need DOM, maintain order |
| `type="module"` | ES modules (automatically deferred) |

### Inline Scripts

For critical small scripts, inline them:

```html
<head>
  <!-- Theme detection: must run before render -->
  <script>
    if (localStorage.theme === 'dark' ||
        (!localStorage.theme && matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.dataset.theme = 'dark';
    }
  </script>
</head>
```

## Font Loading

### Font Display Strategy

```css
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap; /* Show fallback, then swap */
}
```

**Font-display values:**

| Value | Behavior | Use For |
|-------|----------|---------|
| `swap` | Fallback immediately, swap when loaded | Body text |
| `optional` | Use if cached, skip if not | Non-critical text |
| `fallback` | Brief block, then fallback | Headings |
| `block` | Invisible until loaded (avoid) | Icon fonts only |

### Preload Critical Fonts

```html
<head>
  <link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin/>
  <link rel="preload" href="/fonts/heading.woff2" as="font" type="font/woff2" crossorigin/>
</head>
```

### System Font Stack

Use system fonts to avoid font loading entirely:

```css
body {
  font-family:
    system-ui,           /* Modern browsers */
    -apple-system,       /* Safari */
    'Segoe UI',          /* Windows */
    Roboto,              /* Android */
    'Helvetica Neue',    /* Older macOS */
    Arial,               /* Fallback */
    sans-serif;
}

code {
  font-family:
    ui-monospace,
    'SF Mono',
    Consolas,
    'Liberation Mono',
    Menlo,
    monospace;
}
```

## Resource Budgets

Keep resources within budget:

| Resource | Budget |
|----------|--------|
| Total page weight | < 1.5 MB |
| JavaScript | < 200 KB (compressed) |
| CSS | < 100 KB (compressed) |
| Images (above fold) | < 200 KB total |
| Fonts | < 100 KB total |
| Third-party scripts | < 100 KB |

Check with: `npm run lint:budget`

## Caching Headers

Recommend caching strategy in comments:

```html
<!--
  Recommended caching:
  - HTML: Cache-Control: no-cache (always revalidate)
  - CSS/JS (hashed): Cache-Control: max-age=31536000, immutable
  - Images: Cache-Control: max-age=86400, stale-while-revalidate=604800
  - Fonts: Cache-Control: max-age=31536000, immutable
-->
```

## HTML Optimization

### Minimal Document Structure

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>

  <!-- Preconnect to critical origins -->
  <link rel="preconnect" href="https://fonts.googleapis.com"/>

  <!-- Preload critical resources -->
  <link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin/>
  <link rel="preload" href="/images/hero.webp" as="image"/>

  <title>Page Title</title>

  <!-- Critical CSS inline -->
  <style>/* critical styles */</style>

  <!-- Non-critical CSS async -->
  <link rel="stylesheet" href="/css/main.css" media="print" onload="this.media='all'"/>
</head>
<body>
  <!-- Content -->

  <!-- Deferred scripts at end -->
  <script src="/js/app.js" defer></script>
</body>
</html>
```

### Reduce HTML Size

- Remove unnecessary whitespace in production
- Avoid deeply nested elements
- Use semantic elements (smaller than div with classes)
- Minimize inline SVG complexity

## Third-Party Scripts

### Load Third-Party Async

```html
<!-- Analytics: async, low priority -->
<script src="https://analytics.example.com/script.js" async fetchpriority="low"></script>

<!-- Or defer loading until after page load -->
<script>
  window.addEventListener('load', () => {
    const script = document.createElement('script');
    script.src = 'https://analytics.example.com/script.js';
    document.body.appendChild(script);
  });
</script>
```

### Facade Pattern

Load heavy embeds on interaction:

```html
<!-- YouTube facade: show thumbnail, load on click -->
<div class="youtube-facade" data-video-id="abc123">
  <img src="https://i.ytimg.com/vi/abc123/hqdefault.jpg"
       alt="Video thumbnail"
       loading="lazy"/>
  <button aria-label="Play video">Play</button>
</div>
```

## Performance Checklist

Before finalizing:

- [ ] LCP image has `fetchpriority="high"`
- [ ] Below-fold images have `loading="lazy"`
- [ ] All images have `width` and `height` (prevent CLS)
- [ ] Critical CSS is inlined or preloaded
- [ ] Non-critical CSS loads async
- [ ] Scripts use `defer` or `async` appropriately
- [ ] Fonts use `font-display: swap` or `optional`
- [ ] Critical fonts are preloaded
- [ ] Third-party origins use `preconnect`
- [ ] Resource budgets are met (`npm run lint:budget`)
- [ ] Web Vitals are instrumented (`npm run lint:vitals`)

## Validation Commands

```bash
# Check resource budgets
npm run lint:budget

# Check Web Vitals readiness
npm run lint:vitals

# Full performance audit
npm run lighthouse
```

## Common Mistakes

| Mistake | Impact | Solution |
|---------|--------|----------|
| No image dimensions | CLS (layout shift) | Add `width` and `height` |
| Render-blocking CSS | Slow LCP | Inline critical, async rest |
| Sync third-party | Blocks main thread | Use `async` or `defer` |
| No font-display | FOIT (invisible text) | Use `font-display: swap` |
| Everything preloaded | Wastes bandwidth | Only preload critical |
| No lazy loading | Slow initial load | Add `loading="lazy"` |
| Large hero image | Slow LCP | Optimize, use modern formats |

## Related Skills

- **css-author** - Modern CSS organization with native @import, @layer casca...
- **responsive-images** - Modern responsive image techniques using picture element,...
- **build-tooling** - Configure Vite for development and production builds
- **service-worker** - Service worker patterns for offline support, caching stra...
