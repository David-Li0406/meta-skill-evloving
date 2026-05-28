# Theming

CSS variables, colors, and dark mode configuration.

## Table of Contents
- [CSS Variables vs Utility Classes](#css-variables-vs-utility-classes)
- [Color Convention](#color-convention)
- [CSS Variables Reference](#css-variables-reference)
- [Adding Custom Colors](#adding-custom-colors)
- [Base Color Palettes](#base-color-palettes)
- [Dark Mode](#dark-mode)

---

## CSS Variables vs Utility Classes

### CSS Variables (Recommended)

Set `tailwind.cssVariables: true` in `components.json`:

```vue
<template>
  <div class="bg-background text-foreground" />
  <div class="bg-primary text-primary-foreground" />
  <div class="bg-card text-card-foreground" />
</template>
```

### Utility Classes

Set `tailwind.cssVariables: false` in `components.json`:

```vue
<template>
  <div class="bg-white dark:bg-zinc-950 text-zinc-950 dark:text-white" />
</template>
```

---

## Color Convention

shadcn-vue uses a `background` and `foreground` convention:

- `--{color}` - Background color
- `--{color}-foreground` - Text color for that background

```css
/* Definition */
--primary: oklch(0.205 0 0);
--primary-foreground: oklch(0.985 0 0);
```

```vue
<!-- Usage -->
<div class="bg-primary text-primary-foreground">
  Primary button
</div>
```

---

## CSS Variables Reference

### Layout Colors

| Variable | Usage |
|----------|-------|
| `--background` | Page background |
| `--foreground` | Default text color |
| `--card` | Card backgrounds |
| `--card-foreground` | Card text |
| `--popover` | Popover/dropdown backgrounds |
| `--popover-foreground` | Popover text |

### Semantic Colors

| Variable | Usage |
|----------|-------|
| `--primary` | Primary actions, links |
| `--primary-foreground` | Text on primary |
| `--secondary` | Secondary actions |
| `--secondary-foreground` | Text on secondary |
| `--muted` | Muted backgrounds |
| `--muted-foreground` | Muted text, placeholders |
| `--accent` | Accent highlights |
| `--accent-foreground` | Text on accent |
| `--destructive` | Destructive actions |
| `--destructive-foreground` | Text on destructive |

### UI Colors

| Variable | Usage |
|----------|-------|
| `--border` | Borders |
| `--input` | Input borders |
| `--ring` | Focus rings |
| `--radius` | Border radius |

### Chart Colors

| Variable | Usage |
|----------|-------|
| `--chart-1` | Chart series 1 |
| `--chart-2` | Chart series 2 |
| `--chart-3` | Chart series 3 |
| `--chart-4` | Chart series 4 |
| `--chart-5` | Chart series 5 |

### Sidebar Colors

| Variable | Usage |
|----------|-------|
| `--sidebar` | Sidebar background |
| `--sidebar-foreground` | Sidebar text |
| `--sidebar-primary` | Sidebar primary |
| `--sidebar-accent` | Sidebar accent |
| `--sidebar-border` | Sidebar borders |
| `--sidebar-ring` | Sidebar focus rings |

---

## Complete Light/Dark Theme

```css
:root {
  --radius: 0.625rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  --chart-3: oklch(0.398 0.07 227.392);
  --chart-4: oklch(0.828 0.189 84.429);
  --chart-5: oklch(0.769 0.188 70.08);
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --card: oklch(0.205 0 0);
  --card-foreground: oklch(0.985 0 0);
  --popover: oklch(0.269 0 0);
  --popover-foreground: oklch(0.985 0 0);
  --primary: oklch(0.922 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --secondary: oklch(0.269 0 0);
  --secondary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --accent: oklch(0.371 0 0);
  --accent-foreground: oklch(0.985 0 0);
  --destructive: oklch(0.704 0.191 22.216);
  --border: oklch(1 0 0 / 10%);
  --input: oklch(1 0 0 / 15%);
  --ring: oklch(0.556 0 0);
  --chart-1: oklch(0.488 0.243 264.376);
  --chart-2: oklch(0.696 0.17 162.48);
  --chart-3: oklch(0.769 0.188 70.08);
  --chart-4: oklch(0.627 0.265 303.9);
  --chart-5: oklch(0.645 0.246 16.439);
}
```

---

## Adding Custom Colors

### 1. Define CSS Variables

```css
:root {
  --warning: oklch(0.84 0.16 84);
  --warning-foreground: oklch(0.28 0.07 46);
}

.dark {
  --warning: oklch(0.41 0.11 46);
  --warning-foreground: oklch(0.99 0.02 95);
}
```

### 2. Register with Tailwind

```css
@theme inline {
  --color-warning: var(--warning);
  --color-warning-foreground: var(--warning-foreground);
}
```

### 3. Use in Components

```vue
<template>
  <div class="bg-warning text-warning-foreground">
    Warning message
  </div>
</template>
```

---

## Base Color Palettes

Available palettes: `neutral`, `stone`, `zinc`, `gray`, `slate`

Select during `init` or set in `components.json`:

```json
{
  "tailwind": {
    "baseColor": "zinc"
  }
}
```

---

## Dark Mode

### Vite (VueUse)

```bash
pnpm add @vueuse/core
```

```vue
<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { useColorMode } from '@vueuse/core'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger
} from '@/components/ui/dropdown-menu'

const mode = useColorMode()
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button variant="outline">
        <Icon 
          icon="radix-icons:moon" 
          class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" 
        />
        <Icon 
          icon="radix-icons:sun" 
          class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" 
        />
        <span class="sr-only">Toggle theme</span>
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="end">
      <DropdownMenuItem @click="mode = 'light'">Light</DropdownMenuItem>
      <DropdownMenuItem @click="mode = 'dark'">Dark</DropdownMenuItem>
      <DropdownMenuItem @click="mode = 'auto'">System</DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
```

### Nuxt (Color Mode)

```bash
pnpm add @nuxtjs/color-mode
```

**nuxt.config.ts:**
```typescript
export default defineNuxtConfig({
  modules: ['@nuxtjs/color-mode'],
  colorMode: {
    classSuffix: ''
  }
})
```

```vue
<script setup lang="ts">
const colorMode = useColorMode()
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button variant="outline">Toggle theme</Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent>
      <DropdownMenuItem @click="colorMode.preference = 'light'">
        Light
      </DropdownMenuItem>
      <DropdownMenuItem @click="colorMode.preference = 'dark'">
        Dark
      </DropdownMenuItem>
      <DropdownMenuItem @click="colorMode.preference = 'system'">
        System
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
```

### Simple Toggle

```vue
<script setup lang="ts">
import { ref, watchEffect } from 'vue'

const isDark = ref(false)

watchEffect(() => {
  document.documentElement.classList.toggle('dark', isDark.value)
})
</script>

<template>
  <Button @click="isDark = !isDark">
    {{ isDark ? 'Light' : 'Dark' }} Mode
  </Button>
</template>
```
