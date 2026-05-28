---
name: tailwind-v4-shadcn-ui-setup
description: Use this skill when initializing React projects with Tailwind v4 and shadcn/ui, setting up dark mode, or troubleshooting common configuration issues.
---

# Tailwind v4 + shadcn/ui Setup

## Overview

This skill provides a comprehensive guide to setting up Tailwind CSS v4 with shadcn/ui, utilizing CSS variable architecture and the `@theme inline` pattern. It covers component composition, accessibility, and form integration, ensuring a robust and flexible design system.

## Scope

- Applies to: Tailwind v4 with shadcn/ui setup, CSS variable architecture, dark mode, theme configuration, component composition patterns, accessibility, form integration
- Does NOT cover: Tailwind v3, PostCSS configuration

## Assumptions

- Tailwind CSS v4+
- shadcn/ui latest
- Vite (use `@tailwindcss/vite` plugin)
- React 18+ or Next.js 14+
- TypeScript 5+

## Quick Start

### Installation Steps

```bash
# 1. Install dependencies
pnpm add tailwindcss @tailwindcss/vite
pnpm add -D @types/node tw-animate-css
pnpm dlx shadcn@latest init

# 2. Delete v3 config if exists
rm tailwind.config.ts  # v4 doesn't use this file
```

### Vite Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: { alias: { '@': path.resolve(__dirname, './src') } }
})
```

### Components Configuration

```json
{
  "tailwind": {
    "config": "",              // ← Empty for v4
    "css": "src/index.css",
    "baseColor": "slate",
    "cssVariables": true
  }
}
```

## The Four-Step Architecture (MANDATORY)

### Step 1: Define CSS Variables at Root

```css
/* src/index.css */
@import "tailwindcss";
@import "tw-animate-css";  /* Required for shadcn/ui animations */

:root {
  --background: hsl(0 0% 100%);      /* ← hsl() wrapper required */
  --foreground: hsl(222.2 84% 4.9%);
  --primary: hsl(221.2 83.2% 53.3%);
}

.dark {
  --background: hsl(222.2 84% 4.9%);
  --foreground: hsl(210 40% 98%);
  --primary: hsl(217.2 91.2% 59.8%);
}
```

### Step 2: Map Variables to Tailwind Utilities

```css
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  /* ... map ALL CSS variables */
}
```

### Step 3: Apply Base Styles

```css
@layer base {
  body {
    background-color: var(--background);  /* NO hsl() wrapper here */
    color: var(--foreground);
  }
}
```

### Step 4: Result - Automatic Dark Mode

```tsx
<div className="bg-background text-foreground">
  {/* No dark: variants needed - theme switches automatically */}
</div>
```

## Critical Rules

### ✅ Always Do:

1. Wrap colors with `hsl()` in `:root`/`.dark`
2. Use `@theme inline` to map all CSS variables
3. Set `"tailwind.config": ""` in components.json
4. Delete `tailwind.config.ts` if exists
5. Use `@tailwindcss/vite` plugin (NOT PostCSS)

### ❌ Never Do:

1. Put `:root`/`.dark` inside `@layer base`
2. Use `.dark { @theme { } }` pattern (v4 doesn't support nested @theme)
3. Double-wrap colors: `hsl(var(--background))`
4. Use `tailwind.config.ts` for theme (v4 ignores it)
5. Use `@apply` directive (deprecated in v4)

## Common Errors & Solutions

### 1. tw-animate-css Import Error

**Error**: "Cannot find module 'tailwindcss-animate'"

**Solution**:
```bash
pnpm add -D tw-animate-css
```

### 2. Colors Not Working

**Error**: `bg-primary` doesn't apply styles

**Solution**:
Ensure you have the correct `@theme inline` mapping.

### 3. Dark Mode Not Switching

**Error**: Theme stays light/dark

**Solution**: Implement a ThemeProvider and wrap your app.

## References

- [shadcn/ui Tailwind v4 Guide](https://ui.shadcn.com/docs/tailwind-v4)
- [Tailwind v4 Docs](https://tailwindcss.com/docs)

## Setup Checklist

- [ ] `@tailwindcss/vite` installed (NOT postcss)
- [ ] `vite.config.ts` uses `tailwindcss()` plugin
- [ ] `components.json` has `"config": ""`
- [ ] NO `tailwind.config.ts` exists
- [ ] `src/index.css` follows 4-step pattern
- [ ] ThemeProvider wraps app
- [ ] Theme toggle works