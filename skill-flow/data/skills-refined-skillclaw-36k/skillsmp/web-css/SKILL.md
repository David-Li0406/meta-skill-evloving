---
name: web-css
description: CSS architecture for vanilla CSS - organization, design tokens, responsive patterns
user-invocable: false
---

# Web CSS Skill

**Version:** 1.0
**Stack:** Vanilla CSS with CSS Variables

> Clean, maintainable CSS without preprocessors or utility frameworks. Design tokens via CSS variables.

---

## Core Principles

1. **Design Tokens First** — All values come from CSS variables.
2. **Component-Scoped** — CSS lives with its component.
3. **Mobile-First** — Base styles for mobile, enhance up.
4. **No Magic Numbers** — Every value has a purpose and comes from the system.
5. **Readable Over Clever** — Obvious code beats clever code.

---

## Design Tokens

### Single Source of Truth

All design values live in a global CSS file (e.g., `styles/tokens.css` or `global.css`).

```css
:root {
  /* Colors - Semantic naming */
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;
  --color-secondary: #64748b;
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;

  /* Neutrals - Numbered scale */
  --color-neutral-50: #f8fafc;
  --color-neutral-100: #f1f5f9;
  --color-neutral-200: #e2e8f0;
  --color-neutral-300: #cbd5e1;
  --color-neutral-400: #94a3b8;
  --color-neutral-500: #64748b;
  --color-neutral-600: #475569;
  --color-neutral-700: #334155;
  --color-neutral-800: #1e293b;
  --color-neutral-900: #0f172a;

  /* Typography */
  --font-sans: system-ui, -apple-system, sans-serif;
  --font-mono: ui-monospace, monospace;

  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg: 1.125rem;   /* 18px */
  --font-size-xl: 1.25rem;    /* 20px */
  --font-size-2xl: 1.5rem;    /* 24px */
  --font-size-3xl: 1.875rem;  /* 30px */

  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;

  /* Spacing - 4px base, 8px scale */
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */

  /* Borders */
  --radius-sm: 0.25rem;   /* 4px */
  --radius-md: 0.375rem;  /* 6px */
  --radius-lg: 0.5rem;    /* 8px */
  --radius-xl: 0.75rem;   /* 12px */
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15);

  /* Animations */
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 350ms;
  --easing-default: cubic-bezier(0.4, 0, 0.2, 1);
  --easing-in: cubic-bezier(0.4, 0, 1, 1);
  --easing-out: cubic-bezier(0, 0, 0.2, 1);

  /* Z-index layers */
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-modal-backdrop: 300;
  --z-modal: 400;
  --z-tooltip: 500;
  --z-toast: 600;

  /* Breakpoint values (for reference in JS) */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
}
```

### Using Tokens

```css
/* ✅ Good - Uses design tokens */
.button {
  padding: var(--space-2) var(--space-4);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  background-color: var(--color-primary);
  border-radius: var(--radius-md);
  transition: background-color var(--duration-fast) var(--easing-default);
}

.button:hover {
  background-color: var(--color-primary-hover);
}

/* ❌ Bad - Hardcoded values */
.button {
  padding: 8px 16px;
  font-size: 14px;
  background-color: #3b82f6;
  border-radius: 6px;
  transition: background-color 0.15s ease;
}
```

---

## Dark Mode

### CSS Variables for Theming

```css
:root {
  /* Light theme (default) */
  --color-bg: var(--color-neutral-50);
  --color-surface: white;
  --color-text: var(--color-neutral-900);
  --color-text-muted: var(--color-neutral-600);
  --color-border: var(--color-neutral-200);
}

[data-theme="dark"] {
  --color-bg: var(--color-neutral-900);
  --color-surface: var(--color-neutral-800);
  --color-text: var(--color-neutral-50);
  --color-text-muted: var(--color-neutral-400);
  --color-border: var(--color-neutral-700);
}

/* Components automatically adapt */
.card {
  background-color: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}
```

### System Preference Detection

```css
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-bg: var(--color-neutral-900);
    --color-surface: var(--color-neutral-800);
    /* ... dark theme values */
  }
}
```

---

## File Organization

### Component-Scoped CSS

```
src/
├── styles/
│   ├── tokens.css       # Design tokens (import first)
│   ├── reset.css        # CSS reset/normalize
│   ├── base.css         # Base element styles
│   └── utilities.css    # Utility classes (sparingly)
├── components/
│   ├── Button/
│   │   ├── Button.jsx
│   │   └── Button.css   # Button-specific styles
│   └── Modal/
│       ├── Modal.jsx
│       └── Modal.css
└── App.css              # App layout only
```

### Import Order

```css
/* In main entry (App.jsx or index.jsx) */
import './styles/tokens.css';    /* 1. Design tokens first */
import './styles/reset.css';     /* 2. Reset */
import './styles/base.css';      /* 3. Base element styles */
import './styles/utilities.css'; /* 4. Utilities (if any) */
import './App.css';              /* 5. App layout */
```

---

## Naming Conventions

### BEM-Inspired (Simplified)

```css
/* Block */
.product-card { }

/* Element (child of block) */
.product-card__image { }
.product-card__title { }
.product-card__price { }
.product-card__actions { }

/* Modifier (variation) */
.product-card--featured { }
.product-card--sold-out { }

/* State (JS-toggled) */
.product-card.is-loading { }
.product-card.is-selected { }
```

### Naming Rules

| Type | Convention | Example |
|------|------------|---------|
| Block | kebab-case | `.user-profile` |
| Element | `__element` | `.user-profile__avatar` |
| Modifier | `--modifier` | `.user-profile--compact` |
| State | `.is-state` | `.is-active`, `.is-loading` |
| Utility | `u-utility` | `.u-visually-hidden` |

---

## Responsive Design

### Mobile-First Breakpoints

```css
/* Base styles = mobile (no media query) */
.grid {
  display: grid;
  gap: var(--space-4);
  grid-template-columns: 1fr;
}

/* Tablet: 768px+ */
@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop: 1024px+ */
@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Large: 1280px+ */
@media (min-width: 1280px) {
  .grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### Container Pattern

```css
.container {
  width: 100%;
  max-width: 1280px;
  margin-inline: auto;
  padding-inline: var(--space-4);
}

@media (min-width: 768px) {
  .container {
    padding-inline: var(--space-6);
  }
}
```

### Never Use max-width Queries

```css
/* ❌ Bad - Desktop-first */
@media (max-width: 768px) {
  .sidebar { display: none; }
}

/* ✅ Good - Mobile-first */
.sidebar {
  display: none;
}

@media (min-width: 768px) {
  .sidebar { display: block; }
}
```

---

## Layout Patterns

### Grid for Structure

```css
/* Page layout with named areas */
.page-layout {
  display: grid;
  grid-template-areas:
    "header"
    "main"
    "footer";
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

@media (min-width: 1024px) {
  .page-layout {
    grid-template-areas:
      "header header"
      "sidebar main"
      "footer footer";
    grid-template-columns: 250px 1fr;
  }
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }
```

### Flexbox for Flow

```css
/* Navigation items */
.nav {
  display: flex;
  gap: var(--space-4);
  align-items: center;
}

/* Card gallery */
.card-gallery {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-6);
}

.card-gallery > * {
  flex: 1 1 300px; /* Grow, shrink, min 300px */
}
```

---

## Component States

All interactive elements must have these states:

```css
.button {
  /* Default */
  background-color: var(--color-primary);
  color: white;
  transition: all var(--duration-fast) var(--easing-default);
}

.button:hover {
  /* Hover */
  background-color: var(--color-primary-hover);
}

.button:active {
  /* Active/Pressed */
  transform: scale(0.98);
}

.button:focus-visible {
  /* Focus (keyboard) */
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.button:disabled {
  /* Disabled */
  opacity: 0.5;
  cursor: not-allowed;
}
```

---

## Accessibility

### Focus Indicators

```css
/* Remove default, add custom */
:focus {
  outline: none;
}

:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Skip link */
.skip-link {
  position: absolute;
  top: -100%;
  left: var(--space-4);
  z-index: var(--z-tooltip);
  padding: var(--space-2) var(--space-4);
  background: var(--color-surface);
}

.skip-link:focus {
  top: var(--space-4);
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Screen Reader Only

```css
.u-visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Hardcoded values** | No consistency, hard to theme | Use design tokens |
| **!important everywhere** | Specificity wars | Fix selector specificity |
| **Deep nesting** | Hard to override, specificity issues | Max 3 levels |
| **ID selectors for styling** | Too specific | Use classes |
| **Styles in JS** | Splits styling concerns | CSS files with component |
| **Global element selectors** | Affects everything | Scope to component class |
| **max-width media queries** | Desktop-first thinking | Use min-width (mobile-first) |
| **Pixel units for font-size** | Ignores user preferences | Use rem |
| **Float for layout** | Outdated, fragile | Use Grid or Flexbox |
| **Margin for spacing between siblings** | Adds up, hard to manage | Use gap on parent |

---

## Property Order

Organize properties logically:

```css
.component {
  /* 1. Layout */
  display: flex;
  grid-template-columns: 1fr 1fr;

  /* 2. Positioning */
  position: relative;
  top: 0;
  z-index: var(--z-dropdown);

  /* 3. Box Model */
  width: 100%;
  padding: var(--space-4);
  margin: 0;

  /* 4. Typography */
  font-family: var(--font-sans);
  font-size: var(--font-size-base);
  color: var(--color-text);

  /* 5. Visual */
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);

  /* 6. Animation */
  transition: box-shadow var(--duration-fast);
}
```

---

## Checklist

### Design Tokens
- [ ] All colors use CSS variables
- [ ] All spacing uses CSS variables
- [ ] All font sizes use CSS variables
- [ ] All shadows use CSS variables
- [ ] No hardcoded hex colors in component CSS
- [ ] No hardcoded pixel values (except borders)

### Organization
- [ ] Tokens defined in central file
- [ ] CSS colocated with components
- [ ] BEM-style naming used
- [ ] No ID selectors for styling

### Responsive
- [ ] Mobile-first (min-width queries only)
- [ ] Standard breakpoints used
- [ ] Tested at all breakpoints

### Accessibility
- [ ] Focus indicators visible
- [ ] Reduced motion respected
- [ ] Color contrast meets WCAG AA
- [ ] No reliance on color alone

---

## When to Consider Alternatives

| Situation | Consider |
|-----------|----------|
| Large team, many contributors | CSS Modules for guaranteed scoping |
| Rapid prototyping | Tailwind CSS |
| Complex theming needs | CSS-in-JS (styled-components, Emotion) |
| Legacy browser support | PostCSS with autoprefixer |
