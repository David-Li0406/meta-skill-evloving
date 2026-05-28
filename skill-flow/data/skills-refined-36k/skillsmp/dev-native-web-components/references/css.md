# CSS Best Practices

## What is it?

A comprehensive guide to writing modern, maintainable CSS using Baseline-supported features for native web components and web applications.

## Why follow these practices?

- **Browser Compatibility**: All features are Baseline-supported across Chrome, Edge, Firefox, Safari
- **Maintainability**: Design tokens and logical properties enable scalable CSS
- **Performance**: Modern layout and loading patterns optimize Core Web Vitals
- **Accessibility**: Built-in support for reduced motion, high contrast, and RTL

---

## CSS Custom Properties (Design Tokens)

### Token Architecture

```css
:root {
  /* Color tokens */
  --color-primary: oklch(55% 0.2 250);
  --color-surface: oklch(98% 0.01 250);
  --color-text: oklch(20% 0.02 250);
  --color-border: oklch(85% 0.02 250);
  
  /* Spacing scale */
  --space-xs: 0.25rem;   /* 4px */
  --space-sm: 0.5rem;    /* 8px */
  --space-md: 1rem;      /* 16px */
  --space-lg: 1.5rem;    /* 24px */
  --space-xl: 2rem;      /* 32px */
  
  /* Typography */
  --font-sans: system-ui, -apple-system, sans-serif;
  --font-mono: 'Menlo', 'Monaco', monospace;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.25rem;
  
  /* Borders & Shadows */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --shadow-sm: 0 1px 2px oklch(0% 0 0 / 0.1);
  
  /* Animation */
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --easing-default: cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Dark Mode with `light-dark()`

```css
:root {
  color-scheme: light dark;
  
  --color-bg: light-dark(oklch(98% 0 0), oklch(15% 0 0));
  --color-text: light-dark(oklch(20% 0 0), oklch(90% 0 0));
  --color-surface: light-dark(oklch(100% 0 0), oklch(20% 0 0));
  --color-border: light-dark(oklch(85% 0 0), oklch(35% 0 0));
}

body {
  background-color: var(--color-bg);
  color: var(--color-text);
}
```

### Registered Custom Properties (`@property`)

```css
/* Enable animation of custom properties */
@property --gradient-angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

.animated-gradient {
  background: linear-gradient(var(--gradient-angle), #f00, #00f);
  animation: rotate 3s linear infinite;
}

@keyframes rotate {
  to { --gradient-angle: 360deg; }
}
```

---

## CSS Logical Properties

Logical properties automatically adapt for RTL languages.

### Property Mapping

| Physical (Avoid) | Logical (Use) |
|-----------------|---------------|
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `padding-left` | `padding-inline-start` |
| `padding-right` | `padding-inline-end` |
| `text-align: left` | `text-align: start` |
| `text-align: right` | `text-align: end` |
| `left` / `right` | `inset-inline-start` / `inset-inline-end` |
| `top` / `bottom` | `inset-block-start` / `inset-block-end` |
| `width` | `inline-size` |
| `height` | `block-size` |
| `border-left` | `border-inline-start` |
| `border-right` | `border-inline-end` |

### Practical Example

```css
/* Component using logical properties */
.card {
  padding-block: var(--space-md);
  padding-inline: var(--space-lg);
  margin-block-end: var(--space-md);
  border-inline-start: 3px solid var(--color-primary);
  text-align: start;
}

/* Works correctly in both LTR and RTL */
```

---

## Layout with CSS Grid

### Basic Grid

```css
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  gap: var(--space-md);
}
```

### Named Grid Areas

```css
.page-layout {
  display: grid;
  grid-template-areas:
    "header header"
    "nav    main"
    "footer footer";
  grid-template-columns: 250px 1fr;
  grid-template-rows: auto 1fr auto;
  min-block-size: 100dvh;
}

.header { grid-area: header; }
.nav { grid-area: nav; }
.main { grid-area: main; }
.footer { grid-area: footer; }
```

### Subgrid

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-lg);
}

.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3; /* header, content, footer */
}
```

---

## Container Queries

### Setup

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Query container width */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 150px 1fr;
  }
}

@container card (min-width: 600px) {
  .card {
    grid-template-columns: 200px 1fr;
    padding: var(--space-lg);
  }
}
```

### Container Query Units

```css
.card-title {
  /* Size relative to container, not viewport */
  font-size: clamp(1rem, 5cqi, 1.5rem);
}
```

| Unit | Description |
|------|-------------|
| `cqw` | 1% of container width |
| `cqh` | 1% of container height |
| `cqi` | 1% of container inline size |
| `cqb` | 1% of container block size |

---

## CSS Nesting

Native CSS nesting reduces repetition and improves organization.

```css
.button {
  padding: var(--space-sm) var(--space-md);
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  
  /* Nested hover state */
  &:hover {
    background: oklch(from var(--color-primary) calc(l - 0.1) c h);
  }
  
  &:focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
  }
  
  /* Nested variants */
  &.primary {
    background: var(--color-primary);
  }
  
  &.secondary {
    background: transparent;
    border: 1px solid var(--color-border);
    color: var(--color-text);
  }
  
  /* Nested media query */
  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }
}
```

---

## `@scope` for Component Styling

Limit selector reach to prevent style leakage.

```css
@scope (.card) to (.card-footer) {
  /* Styles apply inside .card but NOT inside .card-footer */
  a {
    color: var(--color-primary);
    text-decoration: underline;
  }
}

@scope (.component) {
  /* All styles scoped to .component */
  :scope {
    padding: var(--space-md);
  }
  
  .title {
    font-size: var(--text-lg);
  }
}
```

---

## `@layer` for Cascade Control

Organize styles with explicit cascade layers.

```css
/* Define layer order (first = lowest priority) */
@layer reset, base, components, utilities;

@layer reset {
  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
}

@layer base {
  body {
    font-family: var(--font-sans);
    line-height: 1.6;
  }
}

@layer components {
  .button { /* ... */ }
  .card { /* ... */ }
}

@layer utilities {
  .hidden { display: none !important; }
  .sr-only { /* screen reader only */ }
}
```

---

## Popover and Dialog Styling

### Popover

```css
[popover] {
  padding: var(--space-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  background: var(--color-surface);
  
  /* Remove default border */
  &::backdrop {
    background: transparent;
  }
}

/* Popover open state */
[popover]:popover-open {
  opacity: 1;
}
```

### Dialog with Backdrop

```css
dialog {
  padding: var(--space-lg);
  border: none;
  border-radius: var(--radius-md);
  box-shadow: 0 8px 32px oklch(0% 0 0 / 0.2);
  max-inline-size: min(90vw, 500px);
  
  &::backdrop {
    background: oklch(0% 0 0 / 0.5);
    backdrop-filter: blur(4px);
  }
}
```

### Entry/Exit Animations

```css
dialog {
  /* Allow discrete animations */
  transition: 
    opacity var(--duration-normal) var(--easing-default),
    transform var(--duration-normal) var(--easing-default),
    overlay var(--duration-normal) var(--easing-default) allow-discrete,
    display var(--duration-normal) var(--easing-default) allow-discrete;
  
  opacity: 0;
  transform: translateY(-20px);
  
  &[open] {
    opacity: 1;
    transform: translateY(0);
    
    @starting-style {
      opacity: 0;
      transform: translateY(-20px);
    }
  }
}
```

---

## View Transitions

### Same-Document Transitions

```css
/* Default crossfade */
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 300ms;
}

/* Named elements for custom transitions */
.hero-image {
  view-transition-name: hero;
}

::view-transition-old(hero),
::view-transition-new(hero) {
  animation-duration: 400ms;
}
```

### JavaScript Trigger

```javascript
document.startViewTransition(() => {
  // Update DOM here
  updateContent();
});
```

---

## Scroll-Driven Animations

### Scroll Progress

```css
@keyframes reveal {
  from { opacity: 0; transform: translateY(50px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-on-scroll {
  animation: reveal linear;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}
```

### Scroll-Linked Header

```css
.header {
  animation: shrink linear;
  animation-timeline: scroll();
  animation-range: 0 200px;
}

@keyframes shrink {
  from { padding-block: 2rem; }
  to { padding-block: 0.5rem; }
}
```

---

## Modern Color

### OKLCH Color Space

```css
:root {
  /* OKLCH: Lightness, Chroma, Hue */
  --color-primary: oklch(55% 0.2 250);
  --color-primary-light: oklch(75% 0.15 250);
  --color-primary-dark: oklch(35% 0.2 250);
  
  /* Relative color syntax */
  --color-primary-hover: oklch(from var(--color-primary) calc(l - 0.1) c h);
}
```

### Why OKLCH?

| Advantage | Description |
|-----------|-------------|
| Perceptual uniformity | Equal lightness steps look equal |
| Predictable manipulation | Lightness changes are intuitive |
| Wide gamut | Access to P3 display colors |
| Better gradients | No muddy middle tones |

---

## Typography

### Fluid Typography

```css
:root {
  --text-base: clamp(1rem, 0.5rem + 1vw, 1.25rem);
  --text-lg: clamp(1.25rem, 1rem + 1vw, 1.75rem);
  --text-xl: clamp(1.5rem, 1rem + 2vw, 2.5rem);
}

h1 { font-size: var(--text-xl); }
h2 { font-size: var(--text-lg); }
body { font-size: var(--text-base); }
```

### Text Balancing

```css
h1, h2, h3 {
  text-wrap: balance; /* Balanced line lengths */
}

p {
  text-wrap: pretty; /* Avoid orphans */
}
```

---

## Focus Styles

```css
/* Modern focus styles */
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Remove focus ring on mouse click */
:focus:not(:focus-visible) {
  outline: none;
}

/* High contrast mode support */
@media (forced-colors: active) {
  :focus-visible {
    outline: 3px solid CanvasText;
  }
}
```

---

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## CSS Checklist

### Required Patterns

- [ ] Use custom properties for all design tokens
- [ ] Use logical properties for RTL support
- [ ] Use `light-dark()` for theme switching
- [ ] Use `:focus-visible` for focus styles
- [ ] Respect `prefers-reduced-motion`
- [ ] Respect `prefers-color-scheme`

### Layout Patterns

- [ ] Use CSS Grid for 2D layouts
- [ ] Use Flexbox for 1D layouts
- [ ] Use container queries for component-level responsiveness
- [ ] Use subgrid for aligned nested content
- [ ] Use `@scope` to prevent style leakage

### Modern Features (Baseline 2024+)

- [ ] CSS nesting for organization
- [ ] `@layer` for cascade control
- [ ] View transitions for page/state changes
- [ ] Entry/exit animations with `@starting-style`
- [ ] Scroll-driven animations where appropriate

---

## Baseline Status Reference

| Feature | Baseline Status |
|---------|-----------------|
| CSS Grid | Baseline 2017 |
| Custom Properties | Baseline 2017 |
| `:focus-visible` | Baseline 2022 |
| Container Queries | Baseline 2023 |
| CSS Nesting | Baseline 2023 |
| Subgrid | Baseline 2023 |
| `light-dark()` | Baseline 2024 |
| `@layer` | Baseline 2022 |
| `@scope` | Baseline 2024 |
| View Transitions (SPA) | Baseline 2024 |
| `@starting-style` | Baseline 2024 |
| `@property` | Baseline 2024 |
| Popover API | Baseline 2024 |
| OKLCH colors | Baseline 2023 |
