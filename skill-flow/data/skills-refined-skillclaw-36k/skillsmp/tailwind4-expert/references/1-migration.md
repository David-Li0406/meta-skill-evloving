# 1. Migration from v3 to v4

**Impact: CRITICAL**

The transition to Tailwind CSS v4.0 represents a complete engine rewrite (Oxide). The most significant change is the removal of the JavaScript configuration file in favor of a CSS-first approach.

## 1.1 The Automated Upgrade Tool

The fastest way to migrate is using the official upgrade tool. It handles package updates, config migration, and template changes.

```bash
npx @tailwindcss/upgrade@latest
```

**What it does:**
- Updates `tailwindcss` and related dependencies to v4.
- Transforms `tailwind.config.js` into CSS variables inside a `@theme` block in your main CSS file.
- Migrates `@tailwind` directives to the new `@import "tailwindcss";` syntax.
- Fixes renamed or removed utilities in your HTML/JSX.

## 1.2 Manual Migration Steps

If you prefer manual migration or the tool fails, follow these steps:

### 1.2.1 Update Directives
Tailwind 4 uses a single entry point.

**Before (v3):**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**After (v4):**
```css
@import "tailwindcss";
```

### 1.2.2 Migrate Configuration
Move your `tailwind.config.js` content into your CSS file.

**Before (v3 JS):**
```js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: '#3b82f6'
      }
    }
  }
}
```

**After (v4 CSS):**
```css
@theme {
  --color-brand: #3b82f6;
}
```

### 1.2.3 Handle Plugins
Many official plugins (Forms, Typography, Aspect Ratio) are now built-in or handled differently.
- **Container Queries**: Now native. Remove `@tailwindcss/container-queries`.
- **Forms/Typography**: Still separate but integrated via `@import`.

## 1.3 PostCSS and Lightning CSS

Tailwind v4 includes **Lightning CSS** out of the box. 
- If you use the Vite plugin or the standalone CLI, you likely don't need a separate `postcss.config.js` anymore unless you have custom PostCSS plugins.
- Most v3 projects can simplify their build pipeline significantly.
