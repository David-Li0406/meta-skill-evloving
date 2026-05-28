# Tailwind 4 Monorepo Configuration

## The CSS-First Shift
In Tailwind 4, the `@theme` block in CSS replaces the `tailwind.config.js`.

### 1. Centralized Theme Package
Create `@repo/design-tokens` with a `base.css` file.

```css
/* @repo/design-tokens/base.css */
@import "tailwindcss";

@theme {
  --color-brand: #7c3aed;
  --font-sans: "Geist", sans-serif;
}
```

### 2. Consuming the Theme
In your Next.js app:
```css
/* apps/web/src/globals.css */
@import "@repo/design-tokens/base.css";

/* App-specific extensions */
@theme {
  --color-surface: #ffffff;
}
```

---

## Remote Scanning
Ensure Tailwind scans your shared packages for classes.

```css
/* In apps/web/src/globals.css */
@source "../../../packages/ui/src/**/*.tsx";
```

---

## Interoperability with JS
Since tokens are native CSS variables, you can access them in React without a bridge:
```tsx
const brandColor = "var(--color-brand)";
```
This is the "Elite" way to handle colors in Canvas, Three.js, or inline styles in 2026.
