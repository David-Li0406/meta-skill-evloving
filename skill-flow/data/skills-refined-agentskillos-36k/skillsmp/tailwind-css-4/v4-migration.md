# Tailwind CSS v4 Migration Guide

## Overview

Tailwind CSS v4 introduces significant changes from v3. This guide covers breaking changes and migration patterns.

## Major Changes

### 1. CSS-First Configuration

**v3 (JavaScript):**
```javascript
// tailwind.config.ts
module.exports = {
  content: ['./app/**/*.tsx', './components/**/*.tsx'],
  theme: {
    extend: {
      colors: {
        brand: '#3b82f6',
      },
    },
  },
  plugins: [],
};
```

**v4 (CSS):**
```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  --color-brand: #3b82f6;
}
```

### 2. Import Statement

**v3:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**v4:**
```css
@import "tailwindcss";
```

### 3. Content Configuration

**v3:**
```javascript
module.exports = {
  content: [
    './app/**/*.tsx',
    './node_modules/@szum-tech/design-system/**/*.js',
  ],
};
```

**v4:**
```css
/* Automatic detection for app/, components/, etc. */
/* Explicit for external packages: */
@source "../node_modules/@szum-tech/design-system";
```

## Breaking Changes

### Ring Utility

| Property | v3 Default | v4 Default | Migration |
|----------|-----------|-----------|-----------|
| Width | 3px | 1px | Use `ring-3` for old behavior |
| Color | blue-500 | currentColor | Add `ring-blue-500` explicitly |

**v3:**
```tsx
<input className="ring" />
// 3px blue-500 ring
```

**v4:**
```tsx
<input className="ring" />
// 1px currentColor ring

// To match v3 behavior:
<input className="ring-3 ring-blue-500" />
```

### Outline Utility

| Property | v3 Default | v4 Default |
|----------|-----------|-----------|
| Width | 2px | 1px |
| Style | (required) | solid |

**v3:**
```tsx
<button className="outline outline-2" />
```

**v4:**
```tsx
<button className="outline" />
// 1px solid by default

<button className="outline-2" />
// 2px solid (style is now implicit)
```

### Border Color

**v3:**
```tsx
<div className="border" />
// border-color: gray-200 (default)
```

**v4:**
```tsx
<div className="border" />
// border-color: currentColor

// Explicit color needed:
<div className="border border-gray-200" />
```

### Space Utilities

No changes, but `gap` is now preferred over `space-*`:

```tsx
// Both work, but gap is more flexible
<div className="flex space-x-4">...</div>  // v3 pattern
<div className="flex gap-4">...</div>       // Preferred
```

## Removed Features

### @tailwind Directives

No longer supported. Use `@import` instead:

```css
/* ❌ v3 */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* ✅ v4 */
@import "tailwindcss";
```

### theme() Function (Partial)

The `theme()` function still works but is less necessary with CSS variables:

```css
/* ❌ Less idiomatic in v4 */
.custom {
  color: theme('colors.blue.500');
}

/* ✅ Preferred in v4 */
.custom {
  color: var(--color-blue-500);
}
```

### screen() Function

Use CSS media queries instead:

```css
/* ❌ v3 */
@media screen(md) {
  .custom { ... }
}

/* ✅ v4 */
@media (min-width: 768px) {
  .custom { ... }
}
```

## Migration Checklist

### 1. Update Dependencies

```bash
npm install tailwindcss@latest
npm uninstall autoprefixer postcss  # Often not needed in v4
```

### 2. Remove tailwind.config.ts

Delete `tailwind.config.ts` and migrate settings to CSS:

```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  /* Move theme.extend.colors here */
  --color-brand-500: #3b82f6;

  /* Move theme.extend.fontFamily here */
  --font-display: "Inter", sans-serif;

  /* Move theme.extend.spacing here */
  --spacing-18: 4.5rem;
}
```

### 3. Update CSS Imports

```css
/* Before */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* After */
@import "tailwindcss";
```

### 4. Add @source for External Packages

```css
@source "../node_modules/@szum-tech/design-system";
```

### 5. Update Ring Utilities

Search and replace in codebase:

| Find | Replace |
|------|---------|
| `ring` (standalone) | `ring-3 ring-blue-500` |
| `focus:ring` | `focus:ring-3 focus:ring-blue-500` |

### 6. Update Border Colors

Add explicit colors where needed:

```tsx
// Before
<div className="border rounded" />

// After (if you need gray border)
<div className="border border-gray-200 rounded" />
```

### 7. Verify Outline Utilities

```tsx
// Outline now has default style
<button className="outline-2" />  // Works (solid is implicit)
```

## Automated Migration

Use the official upgrade tool:

```bash
npx @tailwindcss/upgrade
```

This handles:
- Dependency updates
- Config file migration
- Template updates

**Note:** Requires Node.js 20+

## Verification Steps

After migration:

1. **Visual inspection** - Check all pages for styling issues
2. **Focus states** - Verify ring and outline appearances
3. **Borders** - Check default border colors
4. **Dark mode** - Test light/dark transitions
5. **Responsive** - Test all breakpoints

## Rollback Plan

If issues arise:

1. Keep backup of `tailwind.config.ts`
2. Pin to v3: `npm install tailwindcss@3`
3. Restore old CSS imports
4. Document issues for incremental migration

## Common Issues

### Classes Not Working

**Problem:** Some classes don't generate.

**Solution:** Add `@source` for files containing those classes:

```css
@source "./content/**/*.mdx";
```

### Colors Missing

**Problem:** Custom colors from config not working.

**Solution:** Migrate to `@theme`:

```css
@theme {
  --color-custom: #abc123;
}
```

### Plugins Not Working

**Problem:** v3 plugins not compatible.

**Solution:** Check for v4-compatible versions or migrate to native CSS:

```css
/* Instead of typography plugin, use @layer */
@layer base {
  .prose h1 { @apply text-4xl font-bold mb-4; }
  .prose p { @apply text-lg leading-relaxed mb-4; }
}
```

### IDE Autocomplete

**Problem:** VSCode doesn't suggest classes.

**Solution:** Install latest Tailwind CSS IntelliSense extension and restart IDE.
