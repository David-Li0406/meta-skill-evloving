---
name: tailwind-v4-shadcn-ui-setup
description: Use this skill when setting up Tailwind v4 with shadcn/ui for React projects, ensuring proper dark mode support and CSS variable architecture.
---

# Skill body

## Scope

- Applies to: Tailwind v4 with shadcn/ui setup, CSS variable architecture, dark mode, theme configuration, component composition patterns, accessibility, form integration
- Does NOT cover: Tailwind v3, PostCSS configuration

## Assumptions

- Tailwind CSS v4+
- shadcn/ui latest
- Vite (use `@tailwindcss/vite` plugin)
- React 18+ or Next.js 14+
- TypeScript 5+

## Principles

- Use `@theme inline` to map CSS variables to Tailwind tokens.
- Use `hsl()` wrapper for color values in `:root` and `.dark`.
- Set `"tailwind.config": ""` in `components.json` (empty for v4).
- Delete `tailwind.config.ts` if it exists (v4 uses CSS-based config).
- Use `@tailwindcss/vite` plugin (not PostCSS).
- Use `cn()` utility for conditional classes.
- Semantic colors automatically adapt to dark mode (no `dark:` variants needed).
- Use `@plugin` directive for plugins (not `@import` or `require()`).
- Compose complex components from smaller shadcn primitives.
- Extend components via wrapper pattern (don't modify originals).
- Use CVA (class-variance-authority) for variant systems.
- Always use `forwardRef` for form-compatible components.
- Leverage Radix UI primitives for built-in accessibility.

## Quick Start

1. **Install dependencies**:
   ```bash
   pnpm add tailwindcss @tailwindcss/vite
   pnpm add -D @types/node tw-animate-css
   pnpm dlx shadcn@latest init
   ```

2. **Delete v3 config if exists**:
   ```bash
   rm tailwind.config.ts  # v4 doesn't use this file
   ```

3. **Configure Vite**:
   Create or update `vite.config.ts`:
   ```typescript
   import { defineConfig } from 'vite'
   import react from '@vitejs/plugin-react'
   import tailwindcss from '@tailwindcss/vite'
   import path from 'path'

   export default defineConfig({
     plugins: [react(), tailwindcss()],
     resolve: { alias: { '@': path.resolve(__dirname, './src') } }
   })
   ```

4. **Set up components.json**:
   Create or update `components.json`:
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
  /* ... all light mode colors */
}

.dark {
  --background: hsl(222.2 84% 4.9%);
  --foreground: hsl(210 40% 98%);
  --primary: hsl(217.2 91.2% 59.8%);
  /* ... all dark mode colors */
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
- Ensure that your base styles are applied correctly to utilize the defined CSS variables.

### Step 4: Enable Automatic Dark Mode
- Ensure that your setup supports automatic dark mode by leveraging the defined CSS variables in your components.

## Additional Notes
- Test accessibility with keyboard navigation and screen readers.
- Use Radix UI primitives for complex interactions.