---
name: tailwind-v4-shadcn-ui-setup
description: Use this skill when initializing React projects with Tailwind v4 and shadcn/ui, setting up dark mode, or troubleshooting common issues related to CSS variables and theme application.
---

# Tailwind v4 + shadcn/ui Setup

## Overview

This skill provides a comprehensive guide to setting up Tailwind CSS v4 with shadcn/ui, utilizing CSS variable architecture and automatic dark mode. It includes essential patterns for component composition, accessibility, and form integration.

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

Follow these steps in order:

1. **Install Dependencies**:
   ```bash
   pnpm add tailwindcss @tailwindcss/vite
   pnpm add -D @types/node tw-animate-css
   pnpm dlx shadcn@latest init
   ```

2. **Delete v3 Config**:
   ```bash
   rm tailwind.config.ts  # v4 doesn't use this file
   ```

3. **Vite Configuration**:
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

4. **Components Config** (Critical):
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

## The Four-Step Architecture

### Step 1: Define CSS Variables at Root
```css
/* src/index.css */
@import "tailwindcss";
@import "tw-animate-css";  /* Required for shadcn/ui animations */

:root {
  --background: hsl(0 0% 100%);
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
}
```

### Step 3: Apply Base Styles
```css
@layer base {
  body {
    background-color: var(--background);
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
- Wrap colors with `hsl()` in `:root`/`.dark`
- Use `@theme inline` to map all CSS variables
- Set `"tailwind.config": ""` in components.json
- Delete `tailwind.config.ts` if exists
- Use `@tailwindcss/vite` plugin

### ❌ Never Do:
- Put `:root`/`.dark` inside `@layer base`
- Use `.dark { @theme { } }` pattern
- Double-wrap colors: `hsl(var(--background))`
- Use `tailwind.config.ts` for theme
- Use `@apply` directive (deprecated in v4)

## Common Errors & Solutions

1. **tw-animate-css Import Error**: Ensure `tw-animate-css` is installed and imported correctly.
2. **Colors Not Working**: Check for missing `@theme inline` mapping.
3. **Dark Mode Not Switching**: Ensure the ThemeProvider is correctly implemented.
4. **Duplicate @layer base**: Avoid adding multiple `@layer base` declarations.
5. **Build Fails with tailwind.config.ts**: Remove the file as v4 does not use it.

## References

- [shadcn/ui Tailwind v4 Guide](https://ui.shadcn.com/docs/tailwind-v4)
- [Tailwind v4 Docs](https://tailwindcss.com/docs)

## Setup Checklist

- [ ] `@tailwindcss/vite` installed
- [ ] `vite.config.ts` uses `tailwindcss()` plugin
- [ ] `components.json` has `"config": ""`
- [ ] NO `tailwind.config.ts` exists
- [ ] `src/index.css` follows the 4-step pattern
- [ ] ThemeProvider wraps app
- [ ] Theme toggle works

---

**Last Updated**: 2025-11-28
**Skill Version**: 2.0.0
**Production**: WordPress Auditor (https://wordpress-auditor.webfonts.workers.dev)