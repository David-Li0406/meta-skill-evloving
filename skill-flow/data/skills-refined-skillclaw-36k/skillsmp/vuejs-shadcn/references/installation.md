# Installation

Setup guides for Vite, Nuxt, Laravel, and Astro.

## Table of Contents
- [Vite](#vite)
- [Nuxt](#nuxt)
- [Laravel](#laravel)
- [Astro](#astro)
- [Manual Installation](#manual-installation)

---

## Vite

### 1. Create Project

```bash
# npm 7+
npm create vite@latest my-vue-app -- --template vue-ts

# pnpm
pnpm create vite@latest my-vue-app --template vue-ts
```

### 2. Add Tailwind CSS

```bash
pnpm add tailwindcss @tailwindcss/vite
```

Replace `src/style.css`:

```css
@import "tailwindcss";
```

### 3. Configure TypeScript Paths

**tsconfig.json:**
```json
{
  "files": [],
  "references": [
    { "path": "./tsconfig.app.json" },
    { "path": "./tsconfig.node.json" }
  ],
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

**tsconfig.app.json:**
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### 4. Configure Vite

```bash
pnpm add -D @types/node
```

**vite.config.ts:**
```typescript
import path from 'node:path'
import tailwindcss from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

### 5. Run CLI

```bash
pnpm dlx shadcn-vue@latest init
```

Answer prompts:
- Base color: Neutral/Gray/Zinc/Stone/Slate
- CSS variables: Yes (recommended)

### 6. Add Components

```bash
pnpm dlx shadcn-vue@latest add button
```

### 7. Update Main Entry

```typescript
// main.ts
import { createApp } from 'vue'
import App from './App.vue'
import './assets/index.css'  // Changed from './style.css'

createApp(App).mount('#app')
```

---

## Nuxt

### 1. Create Project

```bash
pnpm create nuxt@latest my-nuxt-app
```

If TypeScript error occurs:
```bash
pnpm add -D typescript
```

### 2. Add Tailwind CSS

```bash
pnpm add tailwindcss @tailwindcss/vite
```

Create `app/assets/css/tailwind.css` (Nuxt v4) or `assets/css/tailwind.css` (Nuxt v3):

```css
@import "tailwindcss";
```

### 3. Configure Nuxt

**nuxt.config.ts:**
```typescript
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  css: ['~/assets/css/tailwind.css'],
  vite: {
    plugins: [tailwindcss()],
  },
})
```

### 4. Add shadcn-nuxt Module

```bash
pnpm dlx nuxi@latest module add shadcn-nuxt
```

**nuxt.config.ts:**
```typescript
export default defineNuxtConfig({
  modules: ['shadcn-nuxt'],
  shadcn: {
    prefix: '',  // Component prefix (default: "Ui")
    componentDir: '@/components/ui'  // Component directory
  }
})
```

### 5. SSR Width Plugin (Optional)

For components using VueUse, add `app/plugins/ssr-width.ts`:

```typescript
import { provideSSRWidth } from '@vueuse/core'

export default defineNuxtPlugin((nuxtApp) => {
  provideSSRWidth(1024, nuxtApp.vueApp)
})
```

### 6. Run CLI

```bash
pnpm dlx shadcn-vue@latest init
```

### 7. Add Components

```bash
pnpm dlx shadcn-vue@latest add button
```

Nuxt auto-imports handle component registration automatically:

```vue
<template>
  <Button>Click me</Button>
</template>
```

---

## Laravel

### 1. Create Project

```bash
laravel new my-app
```

Select:
- Vue with Inertia
- Tailwind CSS

### 2. Run CLI

```bash
pnpm dlx shadcn-vue@latest init
```

Configure paths for Laravel:
- Global CSS: `resources/css/app.css`
- Components alias: `@/Components`

### 3. Update Tailwind Config

The CLI may overwrite `tailwind.config.js`. Update content paths:

```javascript
export default {
  content: [
    './vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php',
    './storage/framework/views/*.php',
    './resources/views/**/*.blade.php',
    './resources/js/**/*.vue',
  ],
  // ... rest of config
}
```

### 4. Add Components

```bash
pnpm dlx shadcn-vue@latest add button
```

---

## Astro

### 1. Create Project

```bash
pnpm create astro@latest my-astro-app
```

### 2. Add Vue Integration

```bash
pnpm astro add vue
```

### 3. Add Tailwind

```bash
pnpm astro add tailwind
```

### 4. Configure for shadcn-vue

Create `src/styles/globals.css`:

```css
@import "tailwindcss";
```

### 5. Run CLI

```bash
pnpm dlx shadcn-vue@latest init
```

### 6. Use Components

```astro
---
import { Button } from '@/components/ui/button'
---

<Button client:load>Click me</Button>
```

Note: Use `client:load` or `client:visible` for interactive components.

---

## Manual Installation

### 1. Install Dependencies

```bash
pnpm add class-variance-authority clsx tailwind-merge radix-vue
```

### 2. Create Utils

**lib/utils.ts:**
```typescript
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### 3. Configure Tailwind

Add CSS variables to your global CSS file and configure `tailwind.config.js` with the shadcn-vue theme.

### 4. Copy Components

Manually copy component files from the shadcn-vue repository or use the CLI.

---

## Project Structure

### Vite

```
├── src/
│   ├── components/
│   │   └── ui/
│   │       ├── button/
│   │       │   └── Button.vue
│   │       └── ...
│   ├── lib/
│   │   └── utils.ts
│   └── assets/
│       └── index.css
├── components.json
├── tsconfig.json
└── vite.config.ts
```

### Nuxt

```
├── app/
│   ├── assets/
│   │   └── css/
│   │       └── tailwind.css
│   └── plugins/
│       └── ssr-width.ts
├── components/
│   └── ui/
│       ├── button/
│       │   └── Button.vue
│       └── ...
├── lib/
│   └── utils.ts
├── components.json
└── nuxt.config.ts
```
