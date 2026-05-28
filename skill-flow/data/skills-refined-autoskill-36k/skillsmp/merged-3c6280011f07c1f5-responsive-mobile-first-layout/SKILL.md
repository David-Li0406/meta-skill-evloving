---
name: responsive-mobile-first-layout
description: Use this skill to create responsive, mobile-first layouts that optimize user experience across all devices using modern CSS techniques.
---

# Responsive Mobile-First Layout

Create responsive layouts using a mobile-first approach with modern CSS techniques like Grid and Flexbox for optimal user experience across all devices.

## When to Apply

Reference these guidelines when:
- Building new page layouts from scratch
- Refactoring existing layouts for better responsiveness
- Implementing navigation systems
- Optimizing touch interactions for mobile
- Creating adaptive component layouts

## Core Principles

### 1. Mobile-First Methodology

```css
/* Start with mobile styles (no media query) */
.container {
  padding: 16px;
  font-size: 16px;
}

/* Then enhance for larger screens */
@media (min-width: 768px) {
  .container {
    padding: 24px;
    font-size: 18px;
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 32px;
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

### 2. Breakpoint Strategy

| Breakpoint | Target | Use Case |
|------------|--------|----------|
| Default | 320px+ | Mobile phones (portrait) |
| `sm` 640px | 640px+ | Large phones (landscape) |
| `md` 768px | 768px+ | Tablets (portrait) |
| `lg` 1024px | 1024px+ | Tablets (landscape), small laptops |
| `xl` 1280px | 1280px+ | Desktops |
| `2xl` 1536px | 1536px+ | Large desktops |

### 3. Touch Target Sizing

```css
/* Minimum touch target: 44x44px (WCAG) / 48x48px (Material) */
.touch-target {
  min-width: 44px;
  min-height: 44px;
  padding: 12px;
}

/* Adequate spacing between targets */
.touch-list > * + * {
  margin-top: 8px; /* Minimum 8px between touch targets */
}
```

## Layout Patterns

### Responsive Container

```css
.container {
  width: 100%;
  max-width: var(--content-max-width, 1280px);
  margin-inline: auto;
  padding-inline: var(--page-padding-x, 16px);
}

@media (min-width: 768px) {
  .container {
    --page-padding-x: 24px;
  }
}

@media (min-width: 1024px) {
  .container {
    --page-padding-x: 32px;
  }
}
```

### Responsive Grid

```css
/* Auto-fit grid that adapts to available space */
.grid-auto {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
  gap: 24px;
}

/* Fixed column grid with breakpoints */
.grid-cols {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

@media (min-width: 768px) {
  .grid-cols {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
}

@media (min-width: 1024px) {
  .grid-cols {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1280px) {
  .grid-cols {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### Sidebar Layout

```css
/* Mobile: stacked, Desktop: sidebar */
.layout-sidebar {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

@media (min-width: 1024px) {
  .layout-sidebar {
    grid-template-columns: 280px 1fr;
  }
}

/* Sticky sidebar on desktop */
@media (min-width: 1024px) {
  .sidebar {
    position: sticky;
    top: 80px; /* Account for fixed header */
    height: fit-content;
    max-height: calc(100vh - 100px);
    overflow-y: auto;
  }
}
```

## Navigation Patterns

### Mobile Hamburger Menu

```html
<header class="header">
  <a href="/" class="logo">Logo</a>

  <button
    class="menu-toggle"
    aria-expanded="false"
    aria-controls="nav-menu"
    aria-label="Toggle navigation"
  >
    <span class="hamburger"></span>
  </button>

  <nav id="nav-menu" class="nav" aria-hidden="true">
    <ul class="nav-list">
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/contact">Contact</a></li>
    </ul>
  </nav>
</header>
```

```css
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  position: sticky;
  top: 0;
  background: var(--surface-color);
  z-index: var(--z-sticky);
}

/* Mobile: Hidden by default */
.nav {
  position: fixed;
  inset: 0;
  top: 60px; /* Header height */
  background: var(--surface-color);
  padding: 24px;
  transform: translateX(100%);
  transition: transform 300ms var(--ease-out);
}

.nav[aria-hidden="false"] {
  transform: translateX(0);
}

.menu-toggle {
  display: flex;
  padding: 12px;
}

/* Desktop: Inline navigation */
@media (min-width: 768px) {
  .nav {
    position: static;
    transform: none;
    padding: 0;
    background: transparent;
  }

  .nav-list {
    display: flex;
    gap: 24px;
  }

  .menu-toggle {
    display: none;
  }
}
```

## Responsive Typography

### Fluid Type Scale

```css
:root {
  /* Fluid typography using clamp() */
  --font-size-sm: clamp(0.875rem, 0.8rem + 0.25vw, 0.9375rem);
  --font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --font-size-lg: clamp(1.125rem, 1rem + 0.5vw, 1.25rem);
  --font-size-xl: clamp(1.25rem, 1rem + 1vw, 1.5rem);
  --font-size-2xl: clamp(1.5rem, 1.25rem + 1.25vw, 2rem);
  --font-size-3xl: clamp(2rem, 1.5rem + 2vw, 3rem);
  --font-size-4xl: clamp(2.5rem, 2rem + 2.5vw, 4rem);
}

body {
  font-size: var(--font-size-base);
  line-height: 1.6;
}

h1 { font-size: var(--font-size-4xl); line-height: 1.1; }
h2 { font-size: var(--font-size-3xl); line-height: 1.2; }
h3 { font-size: var(--font-size-2xl); line-height: 1.3; }
h4 { font-size: var(--font-size-xl); line-height: 1.4; }
```

## Responsive Images

```html
<!-- Responsive image with art direction -->
<picture>
  <source
    media="(min-width: 1024px)"
    srcset="hero-desktop.webp"
  />
  <source
    media="(min-width: 768px)"
    srcset="hero-tablet.webp"
  />
  <img
    src="hero-mobile.webp"
    alt="Hero image"
    loading="lazy"
    decoding="async"
    width="800"
    height="600"
  />
</picture>
```

## Testing Checklist

### Mobile Testing (320px - 767px)

- [ ] Content readable without horizontal scroll
- [ ] Touch targets minimum 44x44px
- [ ] Adequate spacing between interactive elements
- [ ] Navigation accessible (hamburger menu works)
- [ ] Forms usable with virtual keyboard
- [ ] Images scale properly
- [ ] Text size minimum 16px (prevents zoom on iOS)

### Tablet Testing (768px - 1023px)

- [ ] Layout adapts appropriately (2-column, etc.)
- [ ] Navigation transition smooth
- [ ] Touch and mouse interactions both work
- [ ] Portrait and landscape orientations tested

### Desktop Testing (1024px+)

- [ ] Full navigation visible
- [ ] Content width constrained (max-width)
- [ ] Hover states present
- [ ] Large screen utilizes space well
- [ ] No excessive white space or cramped layouts

### Performance

- [ ] Images use srcset/sizes
- [ ] Lazy loading for below-fold content
- [ ] CSS animations use GPU-accelerated properties
- [ ] No layout shift during loading
- [ ] Fonts display properly (font-display: swap)

## Best Practices

1. **Design for content, not devices** - Breakpoints where layout breaks
2. **Use relative units** - rem, em, %, vw instead of px
3. **Flexible images** - max-width: 100% by default
4. **Test zoom levels** - Support 200% zoom minimum
5. **Consider orientation** - Landscape vs portrait modes
6. **Optimize performance** - Mobile has slower networks

## Notes

- Mobile traffic often exceeds 50% of web traffic
- Test on actual devices, not just browser emulators
- Consider Progressive Web App (PWA) for mobile
- Use device pixel ratio for high-DPI screens