# Performance Reference

> Target Core Web Vitals thresholds for optimal user experience.

---

## Core Web Vitals Targets

| Metric | Good    | Needs Improvement | Poor    |
| ------ | ------- | ----------------- | ------- |
| LCP    | < 2.5s  | 2.5s - 4s         | > 4s    |
| INP    | < 200ms | 200ms - 500ms     | > 500ms |
| CLS    | < 0.1   | 0.1 - 0.25        | > 0.25  |

---

## LCP (Largest Contentful Paint)

### Optimize Critical Resources

```html
<!-- Preload LCP image -->
<link rel="preload" as="image" href="hero.webp" fetchpriority="high" />

<!-- Preconnect to origins -->
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="dns-prefetch" href="https://cdn.example.com" />
```

### Priority Hints

```html
<!-- High priority for LCP -->
<img src="hero.webp" fetchpriority="high" alt="Hero" />

<!-- Low priority for below-fold -->
<img src="footer-logo.png" fetchpriority="low" loading="lazy" alt="Logo" />
```

---

## INP (Interaction to Next Paint)

### Keep Main Thread Free

```javascript
// ❌ WRONG: Long task blocks main thread
button.onclick = () => {
  heavyComputation(); // Blocks for 100ms+
};

// ✅ CORRECT: Break up work
button.onclick = async () => {
  await new Promise((r) => setTimeout(r, 0));
  heavyComputation();
};

// ✅ BETTER: Use scheduler
button.onclick = () => {
  scheduler.postTask(() => heavyComputation(), {
    priority: "background",
  });
};
```

### CSS for Interactivity

```css
/* Instant visual feedback */
button {
  transition: transform 0.1s, background 0.1s;

  &:active {
    transform: scale(0.98);
  }
}
```

---

## CLS (Cumulative Layout Shift)

### Reserve Space

```css
/* Always set dimensions */
img,
video,
iframe {
  width: 100%;
  height: auto;
  aspect-ratio: 16/9;
}

/* Reserve space for dynamic content */
.ad-slot {
  min-height: 250px;
}
```

### Fonts

```css
/* Prevent font swap layout shift */
@font-face {
  font-family: "Custom";
  src: url("font.woff2") format("woff2");
  font-display: optional; /* or swap with fallback metrics */
}

/* Size-adjust fallback */
body {
  font-family: "Custom", "Arial", sans-serif;
  font-size-adjust: 0.5;
}
```

---

## Loading Strategies

### Images

```html
<!-- Eager load above-fold -->
<img src="hero.webp" loading="eager" decoding="async" />

<!-- Lazy load below-fold -->
<img src="product.webp" loading="lazy" decoding="async" />
```

### Scripts

```html
<!-- Defer non-critical -->
<script src="analytics.js" defer></script>

<!-- Async for independent scripts -->
<script src="widget.js" async></script>

<!-- Module for modern code -->
<script type="module" src="app.js"></script>
```

---

## content-visibility (2025)

```css
/* Skip rendering off-screen content */
.section {
  content-visibility: auto;
  contain-intrinsic-size: auto 500px;
}
```

---

## CSS Performance

```css
/* Use transform/opacity for animations */
.animated {
  /* ✅ GPU accelerated */
  transform: translateX(100px);
  opacity: 0.5;

  /* ❌ Causes reflow */
  /* left: 100px; */
  /* width: 200px; */
}

/* Contain layout calculations */
.card {
  contain: layout style paint;
}
```

---

## Resource Hints

```html
<head>
  <!-- DNS prefetch -->
  <link rel="dns-prefetch" href="//api.example.com" />

  <!-- Preconnect (includes DNS + TLS) -->
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />

  <!-- Preload critical resources -->
  <link rel="preload" href="critical.css" as="style" />
  <link rel="preload" href="hero.webp" as="image" />

  <!-- Prefetch next page -->
  <link rel="prefetch" href="/next-page.html" />

  <!-- Module preload -->
  <link rel="modulepreload" href="/app.js" />
</head>
```

---

## Image Optimization

```html
<!-- Modern formats with fallback -->
<picture>
  <source srcset="image.avif" type="image/avif" />
  <source srcset="image.webp" type="image/webp" />
  <img src="image.jpg" alt="Description" />
</picture>
```

### Format Priority

1. AVIF (best compression)
2. WebP (wide support)
3. JPEG/PNG (fallback)

---

## Bundle Size

```javascript
// Dynamic imports for code splitting
const module = await import("./heavy-feature.js");

// Feature detection before loading
if ("IntersectionObserver" in window) {
  import("./lazy-images.js");
}
```

---

## Checklist

- [ ] LCP image has `fetchpriority="high"`
- [ ] Below-fold images have `loading="lazy"`
- [ ] All images have dimensions/aspect-ratio
- [ ] Fonts use `font-display: swap` or `optional`
- [ ] Scripts are `defer` or `async`
- [ ] `content-visibility: auto` for long pages
- [ ] Animations use `transform`/`opacity` only
- [ ] Resource hints for third-party origins

---

## Measurement

```javascript
// Web Vitals library
import { onLCP, onINP, onCLS } from "web-vitals";

onLCP(console.log);
onINP(console.log);
onCLS(console.log);
```

_Reference: [web.dev/vitals](https://web.dev/articles/vitals)_
