# Tailwind 4 Migration: CSS-First Architecture (2026)

The transition to Tailwind 4 marks a shift from JavaScript-heavy configuration to a native CSS experience.

## 1. The `@theme` Directive
Replace `tailwind.config.js` with declarative CSS.

```css
@theme {
  --font-sans: "Inter", system-ui, sans-serif;
  --color-brand: oklch(0.65 0.24 169.22);
  --breakpoint-3xl: 1920px;
}
```

## 2. Global Imports
No more `@tailwind base;` etc. Use the single entry point.

```css
@import "tailwindcss";
```

## 3. Dynamic Spacing & Radius
Standardize on CSS variables for consistent layout scaling.

```css
:root {
  --radius: 0.75rem;
  --spacing-fluid: clamp(1rem, 5vw, 3rem);
}
```

---
*Updated: January 23, 2026*
