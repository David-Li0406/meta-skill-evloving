# Responsive Breakpoints Guide

## Overview

Mobile-first responsive design means starting with mobile styles and progressively enhancing for larger screens. This approach ensures the smallest devices always work, and larger screens get enhanced experiences.

---

## Standard Breakpoints

### The Four Breakpoints

| Name | Min Width | Target Devices |
|------|-----------|----------------|
| **Mobile** | 0px (base) | Phones in portrait |
| **Tablet** | 641px | Tablets, large phones in landscape |
| **Desktop** | 1024px | Laptops, desktops |
| **Large Desktop** | 1280px | Large monitors, wide screens |

### CSS Implementation

```css
/*
   MOBILE FIRST - Base styles apply to all screens
   No media query needed for mobile
*/
.container {
  padding: var(--space-sm);
}

/* Tablet: 641px and up */
@media (min-width: 641px) {
  .container {
    padding: var(--space-md);
  }
}

/* Desktop: 1024px and up */
@media (min-width: 1024px) {
  .container {
    padding: var(--space-lg);
  }
}

/* Large Desktop: 1280px and up */
@media (min-width: 1280px) {
  .container {
    padding: var(--space-xl);
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

### As CSS Variables

```css
:root {
  --breakpoint-sm: 641px;    /* Tablet */
  --breakpoint-md: 1024px;   /* Desktop */
  --breakpoint-lg: 1280px;   /* Large Desktop */
}
```

Note: CSS variables can't be used directly in media query conditions, but they document the values.

---

## Why Mobile-First?

### The Principle

1. **Start small:** Write base styles for mobile (no media query)
2. **Add complexity:** Layer on styles for larger screens with `min-width`
3. **Progressive enhancement:** Smallest screens always work

### min-width vs max-width

```css
/* ✅ Mobile-first (min-width) - CORRECT */
.nav {
  flex-direction: column;  /* Mobile: vertical stack */
}

@media (min-width: 1024px) {
  .nav {
    flex-direction: row;   /* Desktop: horizontal */
  }
}

/* ❌ Desktop-first (max-width) - AVOID */
.nav {
  flex-direction: row;     /* Desktop: horizontal */
}

@media (max-width: 1023px) {
  .nav {
    flex-direction: column; /* Mobile: vertical stack */
  }
}
```

**Why min-width wins:**
- Base CSS is smaller (simpler mobile styles)
- Styles cascade naturally from simple → complex
- Edge cases default to simpler mobile experience
- Easier to maintain and debug

---

## Container Widths

### Max-Width Strategy

```css
.container {
  width: 100%;
  margin: 0 auto;
  padding: 0 var(--space-md);
}

/* Mobile: full width with padding */
/* No max-width needed */

/* Tablet */
@media (min-width: 641px) {
  .container {
    max-width: 640px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: 960px;
  }
}

/* Large Desktop */
@media (min-width: 1280px) {
  .container {
    max-width: 1200px;
  }
}
```

### Container Size Variants

```css
.container-sm {
  max-width: 640px;
}

.container-md {
  max-width: 960px;
}

.container-lg {
  max-width: 1200px;
}

.container-full {
  max-width: 100%;
}
```

---

## Common Responsive Patterns

### Navigation

```css
/* Mobile: Hidden menu with hamburger trigger */
.nav-menu {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--color-surface);
  flex-direction: column;
  padding: var(--space-xl);
}

.nav-menu.is-open {
  display: flex;
}

.nav-hamburger {
  display: block;
}

/* Desktop: Full horizontal nav */
@media (min-width: 1024px) {
  .nav-menu {
    display: flex;
    position: static;
    flex-direction: row;
    background: transparent;
    padding: 0;
    gap: var(--space-lg);
  }

  .nav-hamburger {
    display: none;
  }
}
```

### Grid Layouts

```css
/* Mobile: Single column */
.card-grid {
  display: grid;
  gap: var(--space-md);
  grid-template-columns: 1fr;
}

/* Tablet: Two columns */
@media (min-width: 641px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop: Three columns */
@media (min-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Large Desktop: Four columns */
@media (min-width: 1280px) {
  .card-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### Sidebar Layouts

```css
/* Mobile: Stacked (sidebar below main) */
.layout {
  display: flex;
  flex-direction: column;
}

.sidebar {
  order: 2;  /* Sidebar below main on mobile */
}

.main {
  order: 1;
}

/* Desktop: Side-by-side */
@media (min-width: 1024px) {
  .layout {
    flex-direction: row;
    gap: var(--space-xl);
  }

  .sidebar {
    order: 1;  /* Sidebar on left */
    width: 280px;
    flex-shrink: 0;
  }

  .main {
    order: 2;
    flex: 1;
  }
}
```

### Typography Scaling

```css
/* Mobile: Smaller text */
:root {
  --font-size-h1: 1.75rem;   /* 28px */
  --font-size-h2: 1.5rem;    /* 24px */
  --font-size-body: 1rem;    /* 16px */
}

/* Tablet */
@media (min-width: 641px) {
  :root {
    --font-size-h1: 2rem;    /* 32px */
    --font-size-h2: 1.75rem; /* 28px */
  }
}

/* Desktop */
@media (min-width: 1024px) {
  :root {
    --font-size-h1: 2.5rem;  /* 40px */
    --font-size-h2: 2rem;    /* 32px */
  }
}
```

### Tables

```css
/* Mobile: Stack table rows */
@media (max-width: 640px) {
  table, thead, tbody, th, td, tr {
    display: block;
  }

  thead {
    position: absolute;
    left: -9999px;
  }

  tr {
    margin-bottom: var(--space-md);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
  }

  td {
    position: relative;
    padding-left: 50%;
  }

  td::before {
    content: attr(data-label);
    position: absolute;
    left: var(--space-sm);
    font-weight: var(--font-weight-bold);
  }
}

/* Tablet+: Normal table */
@media (min-width: 641px) {
  /* Default table styles apply */
}
```

---

## Touch vs Pointer Considerations

### Pointer Media Query

```css
/* Fine pointer (mouse, trackpad) */
@media (pointer: fine) {
  .button {
    padding: var(--space-sm) var(--space-md);
  }

  /* Smaller hover targets are OK */
  .link:hover {
    text-decoration: underline;
  }
}

/* Coarse pointer (touch screens) */
@media (pointer: coarse) {
  .button {
    padding: var(--space-md) var(--space-lg);
    min-height: 44px;  /* iOS minimum touch target */
  }
}
```

### Hover Media Query

```css
/* Only show hover effects when device supports hover */
@media (hover: hover) {
  .card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
  }
}

/* No hover support (touch) - show always or on active */
@media (hover: none) {
  .card:active {
    transform: scale(0.98);
  }
}
```

---

## Device-Specific Considerations

### iOS Safe Areas

```css
/* Account for notches and home indicators */
.header {
  padding-top: env(safe-area-inset-top);
}

.footer {
  padding-bottom: env(safe-area-inset-bottom);
}

/* Full bleed with safe areas */
.full-bleed {
  padding-left: max(var(--space-md), env(safe-area-inset-left));
  padding-right: max(var(--space-md), env(safe-area-inset-right));
}
```

### High DPI Screens

```css
/* High-res images for retina displays */
.logo {
  background-image: url('logo.png');
}

@media (-webkit-min-device-pixel-ratio: 2),
       (min-resolution: 192dpi) {
  .logo {
    background-image: url('logo@2x.png');
    background-size: 100px 50px;  /* Original dimensions */
  }
}
```

### Landscape vs Portrait

```css
/* Portrait-specific adjustments */
@media (orientation: portrait) {
  .hero {
    min-height: 60vh;
  }
}

/* Landscape-specific adjustments */
@media (orientation: landscape) {
  .hero {
    min-height: 100vh;
  }
}
```

---

## Testing Checklist

### Manual Testing

- [ ] Test on real mobile device (not just browser emulation)
- [ ] Test on real tablet
- [ ] Test at each breakpoint boundary (640px, 1024px, 1280px)
- [ ] Test in both orientations (portrait/landscape)
- [ ] Test with zoom levels (100%, 150%, 200%)
- [ ] Test with browser width dragging (resize smoothly)

### Device Testing Matrix

| Device Type | Screen Size | Resolution | Test Priority |
|-------------|-------------|------------|---------------|
| iPhone SE | 375 × 667 | 2x | High |
| iPhone 14 | 390 × 844 | 3x | High |
| iPad | 768 × 1024 | 2x | Medium |
| iPad Pro | 1024 × 1366 | 2x | Medium |
| Laptop | 1366 × 768 | 1x | High |
| Desktop | 1920 × 1080 | 1x | High |

### Common Issues to Check

- [ ] Text doesn't overflow containers
- [ ] Images don't break layouts
- [ ] Touch targets are at least 44×44px on mobile
- [ ] Navigation is accessible on all sizes
- [ ] Forms are usable on small screens
- [ ] Tables don't cause horizontal scroll
- [ ] Modals are sized appropriately

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `max-width` queries | Desktop-first thinking | Use `min-width` (mobile-first) |
| Pixel-specific breakpoints | Fragile, device-dependent | Use standard breakpoints |
| Hiding content on mobile | Content parity issues | Prioritize, don't hide |
| Fixed widths | Break on small screens | Use max-width + 100% |
| Horizontal scroll | Poor mobile UX | Responsive layouts |
| Hover-only interactions | Unusable on touch | Provide touch alternatives |
