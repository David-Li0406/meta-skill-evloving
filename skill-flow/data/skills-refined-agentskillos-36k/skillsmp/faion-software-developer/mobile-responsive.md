---
id: mobile-responsive
name: "Mobile Responsive"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Mobile Responsive

## Overview

Mobile responsive design ensures web applications provide optimal viewing experiences across all device sizes. This includes fluid layouts, flexible images, and CSS media queries to adapt content to different screen dimensions.

## When to Use

- All web development (should be default practice)
- Mobile-first design approach
- Cross-device user experiences
- E-commerce and content sites
- Web applications with diverse user bases

## Key Principles

- **Mobile first**: Design for mobile, enhance for larger screens
- **Fluid layouts**: Use relative units over fixed pixels
- **Breakpoints at content**: Break when content breaks, not device sizes
- **Touch-friendly**: Adequate tap targets and spacing
- **Performance**: Optimize for mobile networks and devices

## Best Practices

### Viewport Meta Tag

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <!-- Viewport for responsive design -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Prevent phone number detection on iOS -->
  <meta name="format-detection" content="telephone=no">

  <!-- Theme color for browser UI -->
  <meta name="theme-color" content="#0066cc">

  <title>Responsive App</title>
</head>
</html>
```

### Mobile-First CSS

```css
/* Base styles for mobile (no media query needed) */
.container {
  width: 100%;
  padding: 1rem;
  margin: 0 auto;
}

.grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr;
}

.card {
  padding: 1rem;
  border-radius: 0.5rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    max-width: 720px;
    padding: 1.5rem;
  }

  .grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container {
    max-width: 960px;
    padding: 2rem;
  }

  .grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }
}

/* Large desktop */
@media (min-width: 1280px) {
  .container {
    max-width: 1200px;
  }

  .grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### Fluid Typography

```css
:root {
  /* Fluid typography using clamp() */
  --font-size-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --font-size-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
  --font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --font-size-lg: clamp(1.125rem, 1rem + 0.625vw, 1.25rem);
  --font-size-xl: clamp(1.25rem, 1rem + 1.25vw, 1.5rem);
  --font-size-2xl: clamp(1.5rem, 1rem + 2.5vw, 2rem);
  --font-size-3xl: clamp(1.875rem, 1rem + 4.375vw, 3rem);
  --font-size-4xl: clamp(2.25rem, 1rem + 6.25vw, 4rem);

  /* Fluid spacing */
  --space-xs: clamp(0.25rem, 0.2rem + 0.25vw, 0.5rem);
  --space-sm: clamp(0.5rem, 0.4rem + 0.5vw, 0.75rem);
  --space-md: clamp(1rem, 0.8rem + 1vw, 1.5rem);
  --space-lg: clamp(1.5rem, 1rem + 2.5vw, 2.5rem);
  --space-xl: clamp(2rem, 1rem + 5vw, 4rem);
}

body {
  font-size: var(--font-size-base);
  line-height: 1.5;
}

h1 { font-size: var(--font-size-4xl); }
h2 { font-size: var(--font-size-3xl); }
h3 { font-size: var(--font-size-2xl); }
h4 { font-size: var(--font-size-xl); }

.section {
  padding: var(--space-lg) var(--space-md);
}
```

### Responsive Images

```html
<!-- Art direction with picture element -->
<picture>
  <!-- Desktop: wide hero image -->
  <source
    media="(min-width: 1024px)"
    srcset="hero-desktop.webp 1920w, hero-desktop-2x.webp 3840w"
    sizes="100vw"
    type="image/webp"
  >
  <!-- Tablet: medium crop -->
  <source
    media="(min-width: 768px)"
    srcset="hero-tablet.webp 1024w, hero-tablet-2x.webp 2048w"
    sizes="100vw"
    type="image/webp"
  >
  <!-- Mobile: square crop -->
  <source
    srcset="hero-mobile.webp 640w, hero-mobile-2x.webp 1280w"
    sizes="100vw"
    type="image/webp"
  >
  <!-- Fallback -->
  <img
    src="hero-mobile.jpg"
    alt="Hero image description"
    loading="lazy"
  >
</picture>

<!-- Resolution switching with srcset -->
<img
  srcset="
    product-400.jpg 400w,
    product-800.jpg 800w,
    product-1200.jpg 1200w
  "
  sizes="(max-width: 640px) 100vw,
         (max-width: 1024px) 50vw,
         33vw"
  src="product-800.jpg"
  alt="Product image"
  loading="lazy"
>
```

```css
/* Responsive image styles */
img {
  max-width: 100%;
  height: auto;
  display: block;
}

/* Object-fit for aspect ratio containers */
.image-container {
  position: relative;
  aspect-ratio: 16 / 9;
  overflow: hidden;
}

.image-container img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Different aspect ratios for different screens */
.hero-image {
  aspect-ratio: 1 / 1;
}

@media (min-width: 768px) {
  .hero-image {
    aspect-ratio: 16 / 9;
  }
}

@media (min-width: 1024px) {
  .hero-image {
    aspect-ratio: 21 / 9;
  }
}
```

### Touch-Friendly Interactions

```css
/* Minimum touch target size (44x44px recommended) */
.button,
.link,
.input,
.interactive {
  min-height: 44px;
  min-width: 44px;
  padding: 0.75rem 1rem;
}

/* Adequate spacing between interactive elements */
.button + .button {
  margin-left: 0.5rem;
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

@media (min-width: 768px) {
  .nav-list {
    flex-direction: row;
    gap: 0.25rem;
  }
}

/* Remove hover effects on touch devices */
@media (hover: none) {
  .button:hover {
    /* Remove hover state */
    background: var(--button-bg);
  }
}

/* Active states for touch */
.button:active {
  transform: scale(0.98);
}

/* Prevent text selection on interactive elements */
.button {
  user-select: none;
  -webkit-touch-callout: none;
  -webkit-tap-highlight-color: transparent;
}
```

### Responsive Navigation

```tsx
// components/Navigation.tsx
import { useState } from 'react';

export function Navigation() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <header className="header">
      <a href="/" className="logo">
        Logo
      </a>

      {/* Mobile menu button */}
      <button
        className="menu-toggle"
        aria-expanded={isOpen}
        aria-controls="main-nav"
        aria-label={isOpen ? 'Close menu' : 'Open menu'}
        onClick={() => setIsOpen(!isOpen)}
      >
        <span className="menu-icon" aria-hidden="true" />
      </button>

      {/* Navigation */}
      <nav
        id="main-nav"
        className={`nav ${isOpen ? 'nav--open' : ''}`}
        aria-label="Main navigation"
      >
        <ul className="nav-list">
          <li><a href="/products">Products</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/contact">Contact</a></li>
        </ul>
      </nav>

      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="nav-overlay"
          onClick={() => setIsOpen(false)}
          aria-hidden="true"
        />
      )}
    </header>
  );
}
```

```css
/* Navigation styles */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  position: relative;
}

.menu-toggle {
  display: block;
  padding: 0.5rem;
  background: none;
  border: none;
  cursor: pointer;
}

.menu-icon {
  display: block;
  width: 24px;
  height: 2px;
  background: currentColor;
  position: relative;
}

.menu-icon::before,
.menu-icon::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background: inherit;
}

.menu-icon::before { top: -8px; }
.menu-icon::after { bottom: -8px; }

/* Mobile nav - slide in from right */
.nav {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 80%;
  max-width: 300px;
  background: white;
  transform: translateX(100%);
  transition: transform 0.3s ease;
  z-index: 100;
  padding: 5rem 1.5rem 1.5rem;
}

.nav--open {
  transform: translateX(0);
}

.nav-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 99;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.nav-list a {
  display: block;
  padding: 0.75rem 0;
  font-size: 1.125rem;
}

/* Desktop nav */
@media (min-width: 768px) {
  .menu-toggle {
    display: none;
  }

  .nav {
    position: static;
    transform: none;
    width: auto;
    max-width: none;
    padding: 0;
    background: transparent;
  }

  .nav-overlay {
    display: none;
  }

  .nav-list {
    flex-direction: row;
    gap: 0.5rem;
  }

  .nav-list a {
    padding: 0.5rem 1rem;
    font-size: 1rem;
  }
}
```

### Responsive Tables

```tsx
// Responsive table patterns
function ResponsiveTable({ data, columns }) {
  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.key}>{col.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.id}>
              {columns.map((col) => (
                <td key={col.key} data-label={col.label}>
                  {row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

```css
/* Horizontal scroll pattern */
.table-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

table {
  width: 100%;
  min-width: 600px;
  border-collapse: collapse;
}

th, td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

/* Card pattern for mobile */
@media (max-width: 640px) {
  .table-responsive table,
  .table-responsive thead,
  .table-responsive tbody,
  .table-responsive tr {
    display: block;
  }

  .table-responsive thead {
    position: absolute;
    top: -9999px;
    left: -9999px;
  }

  .table-responsive tr {
    margin-bottom: 1rem;
    border: 1px solid #eee;
    border-radius: 0.5rem;
    padding: 1rem;
  }

  .table-responsive td {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border: none;
  }

  .table-responsive td::before {
    content: attr(data-label);
    font-weight: bold;
    margin-right: 1rem;
  }
}
```

### Container Queries

```css
/* Modern container queries */
.card-container {
  container-type: inline-size;
  container-name: card;
}

.card {
  display: grid;
  gap: 1rem;
  padding: 1rem;
}

/* Respond to container width, not viewport */
@container card (min-width: 400px) {
  .card {
    grid-template-columns: 150px 1fr;
  }
}

@container card (min-width: 600px) {
  .card {
    grid-template-columns: 200px 1fr auto;
    padding: 1.5rem;
  }
}
```

## Anti-patterns

- **Fixed widths**: Using px for layout dimensions
- **Desktop-first**: Leads to complex mobile overrides
- **Device-specific breakpoints**: Content should dictate breakpoints
- **Tiny touch targets**: Links and buttons too small for fingers
- **Hidden content on mobile**: Same content should be accessible
- **Horizontal scroll**: Except for intentional patterns like carousels

## References

- [MDN Responsive Design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [Google Mobile-Friendly Guidelines](https://developers.google.com/search/mobile-sites)
- [CSS Tricks - A Complete Guide to Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [CSS Tricks - A Complete Guide to Grid](https://css-tricks.com/snippets/css/complete-guide-grid/)
