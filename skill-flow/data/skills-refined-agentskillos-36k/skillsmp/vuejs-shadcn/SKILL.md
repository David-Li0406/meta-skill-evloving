---
name: vuejs-shadcn
description: |
  shadcn/vue UI components for Vue 3: Button, Dialog, Form, Table, and theming.
  WHEN: Using shadcn-vue components, installing components via CLI, theming/dark mode, forms with VeeValidate/Zod, implementing shadcn patterns.
  WHEN NOT: Other UI libraries (Vuetify, PrimeVue), general Vue development (use vuejs-dev), charts (use vuejs-apex-charts).
---

# shadcn/vue

Beautifully designed components built with Radix Vue and Tailwind CSS. Copy and paste into your apps.

## Installation (Vite)

### 1. Create Project

```bash
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

### 3. Configure Path Aliases

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  }
}
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
    alias: { '@': path.resolve(__dirname, './src') }
  }
})
```

### 4. Run CLI

```bash
pnpm dlx shadcn-vue@latest init
```

### 5. Add Components

```bash
pnpm dlx shadcn-vue@latest add button
```

**For Nuxt, Laravel, or Astro setup, see `references/installation.md`**

## CLI Commands

| Command | Description |
|---------|-------------|
| `shadcn-vue init` | Initialize project with dependencies and config |
| `shadcn-vue add [component]` | Add specific component(s) |
| `shadcn-vue add --all` | Add all components |
| `shadcn-vue update [component]` | Update component(s) |

**For full CLI options, see `references/cli.md`**

## Basic Component Usage

```vue
<script setup lang="ts">
import { Button } from '@/components/ui/button'
</script>

<template>
  <Button variant="outline">Click me</Button>
</template>
```

## Component Categories

### Layout & Containers
`Card`, `Dialog`, `Sheet`, `Drawer`, `Sidebar`, `Collapsible`, `Resizable`, `Scroll Area`, `Separator`, `Aspect Ratio`

### Form Controls
`Button`, `Input`, `Textarea`, `Select`, `Checkbox`, `Radio Group`, `Switch`, `Slider`, `Toggle`, `Toggle Group`, `Form`, `Field`, `Label`, `Number Field`, `Pin Input`, `Tags Input`, `Combobox`, `Date Picker`, `Calendar`

### Navigation
`Tabs`, `Navigation Menu`, `Menubar`, `Breadcrumb`, `Pagination`, `Stepper`

### Feedback & Overlay
`Dialog`, `Alert Dialog`, `Popover`, `Tooltip`, `Hover Card`, `Dropdown Menu`, `Context Menu`, `Toast`, `Sonner`, `Alert`, `Progress`, `Skeleton`, `Spinner`

### Data Display
`Table`, `Data Table`, `Avatar`, `Badge`, `Card`, `Carousel`, `Accordion`, `Empty`

**For detailed component APIs, see:**
- `references/components-form.md` - Form controls and inputs
- `references/components-layout.md` - Layout and containers
- `references/components-overlay.md` - Dialogs, popovers, menus
- `references/components-data.md` - Tables, lists, data display
- `references/components-feedback.md` - Alerts, toasts, progress

## Theming

### CSS Variables (Default)

```vue
<div class="bg-background text-foreground" />
<div class="bg-primary text-primary-foreground" />
<div class="bg-muted text-muted-foreground" />
<div class="bg-destructive text-destructive-foreground" />
```

### Core Variables

```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --muted: oklch(0.97 0 0);
  --accent: oklch(0.97 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
  --radius: 0.625rem;
}
```

**For complete theming guide, see `references/theming.md`**

## Dark Mode (Vite)

```vue
<script setup lang="ts">
import { useColorMode } from '@vueuse/core'
import { Button } from '@/components/ui/button'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'

const mode = useColorMode()
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button variant="outline">Toggle theme</Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent>
      <DropdownMenuItem @click="mode = 'light'">Light</DropdownMenuItem>
      <DropdownMenuItem @click="mode = 'dark'">Dark</DropdownMenuItem>
      <DropdownMenuItem @click="mode = 'auto'">System</DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
```

## Forms with VeeValidate + Zod

```vue
<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import * as z from 'zod'
import { Button } from '@/components/ui/button'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'

const formSchema = toTypedSchema(z.object({
  username: z.string().min(2).max(50),
}))

const form = useForm({ validationSchema: formSchema })

const onSubmit = form.handleSubmit((values) => {
  console.log('Form submitted!', values)
})
</script>

<template>
  <form @submit="onSubmit">
    <FormField v-slot="{ componentField }" name="username">
      <FormItem>
        <FormLabel>Username</FormLabel>
        <FormControl>
          <Input placeholder="shadcn" v-bind="componentField" />
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>
    <Button type="submit">Submit</Button>
  </form>
</template>
```

**For complete form guide, see `references/forms.md`**

## Project Structure

```
├── src/
│   ├── components/
│   │   └── ui/
│   │       ├── button/
│   │       │   └── Button.vue
│   │       ├── dialog/
│   │       │   ├── Dialog.vue
│   │       │   └── ...
│   │       └── ...
│   ├── lib/
│   │   └── utils.ts
│   └── assets/
│       └── index.css
├── components.json
└── tailwind.config.js
```

## References

| File | Content |
|------|---------|
| `references/installation.md` | Vite, Nuxt, Laravel, Astro setup |
| `references/cli.md` | CLI commands and options |
| `references/theming.md` | CSS variables, colors, dark mode |
| `references/forms.md` | VeeValidate, Zod, TanStack Form |
| `references/components-form.md` | Button, Input, Select, Checkbox, etc. |
| `references/components-layout.md` | Card, Dialog, Sheet, Sidebar, etc. |
| `references/components-overlay.md` | Popover, Tooltip, Dropdown Menu, etc. |
| `references/components-data.md` | Table, Data Table, Avatar, Badge, etc. |
| `references/components-feedback.md` | Alert, Toast, Progress, Skeleton, etc. |
