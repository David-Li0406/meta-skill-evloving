# Tailwind CSS in Nuxt

**Last Updated:** 2025-11 (Tailwind v4.1.16)

**Check:** `@nuxtjs/tailwindcss` in package.json

Tailwind CSS is automatically integrated into Nuxt through the `@nuxtjs/tailwindcss` module, providing utility-first CSS framework support.

## When to Use Tailwind

**Detection:** Check `package.json` for `@nuxtjs/tailwindcss` dependency before suggesting Tailwind patterns.

**If Tailwind is installed:**

- Prefer Tailwind utility classes in component templates
- Use utilities for layout, spacing, colors, typography, responsive design
- Combine utilities for common patterns (flex, grid, etc.)

**If Tailwind is NOT installed:**

- Use `<style scoped>` for component-specific styles
- Write traditional CSS/SCSS for styling

**Tailwind v4 Capabilities (No `<style>` needed):**

- Custom animations via `@theme` directive with `@keyframes`
- CSS variables for theming via `@theme` with `--color-*`, `--font-*`, etc.
- Scrollbar styling via arbitrary variants: `[&::-webkit-scrollbar]:w-1.5`
- Pseudo-elements via arbitrary variants: `before:content-['★']`

**When to Still Use `<style>` (even with Tailwind v4):**

- Very complex multi-step keyframes that are verbose in `@theme`
- Cross-browser scrollbar styling (Firefox requires different syntax than WebKit)
- Complex pseudo-element content with difficult escaping
- Styles that become unreadable as utility classes (use your judgment)

## Installation & Setup

### Tailwind v4 Setup (Current)

```bash
pnpm add -D tailwindcss @nuxtjs/tailwindcss
```

**nuxt.config.ts:**

```typescript
export default defineNuxtConfig({
  modules: ["@nuxtjs/tailwindcss"],

  tailwindcss: {
    // Optional configuration
    exposeConfig: true,
    viewer: true, // Enable /_tailwind in dev mode
  },
})
```

**assets/css/main.css:**

```css
@import "tailwindcss";
```

**Alternative (explicit layers):**

```css
@import "tailwindcss/base";
@import "tailwindcss/components";
@import "tailwindcss/utilities";
```

### Tailwind v3 Setup (Previous Version)

```bash
pnpm add -D tailwindcss @nuxtjs/tailwindcss
```

**assets/css/main.css:**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Configuration

### tailwind.config.ts

Tailwind v4 uses CSS-based configuration by default, but you can still use TypeScript config:

```typescript
import type { Config } from "tailwindcss"

export default {
  content: [
    "./components/**/*.{vue,js,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./composables/**/*.{js,ts}",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#f0f9ff",
          100: "#e0f2fe",
          200: "#bae6fd",
          300: "#7dd3fc",
          400: "#38bdf8",
          500: "#0ea5e9",
          600: "#0284c7",
          700: "#0369a1",
          800: "#075985",
          900: "#0c4a6e",
          950: "#082f49",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      spacing: {
        "128": "32rem",
        "144": "36rem",
      },
    },
  },
  plugins: [],
} satisfies Config
```

### CSS-Based Configuration (v4)

Tailwind v4 supports CSS variables for theming:

```css
/* assets/css/main.css */
@import "tailwindcss";

@layer base {
  :root {
    --color-primary-50: 240 249 255;
    --color-primary-500: 14 165 233;
    --color-primary-900: 12 74 110;
  }
}
```

## Common Patterns

### Responsive Design

```vue
<template>
  <div class="container mx-auto px-4 sm:px-6 lg:px-8">
    <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold">
      Responsive Heading
    </h1>

    <!-- Hide on mobile, show on desktop -->
    <div class="hidden lg:block">Desktop only content</div>

    <!-- Show on mobile, hide on desktop -->
    <div class="block lg:hidden">Mobile only content</div>
  </div>
</template>
```

### Dark Mode

Nuxt integrates with `@nuxtjs/color-mode` for automatic dark mode support:

```vue
<template>
  <div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
    <h1 class="text-gray-900 dark:text-gray-100">Auto Dark Mode</h1>

    <button
      class="bg-blue-500 hover:bg-blue-600 dark:bg-blue-700 dark:hover:bg-blue-800"
      @click="toggleDarkMode"
    >
      Toggle Dark Mode
    </button>
  </div>
</template>

<script setup lang="ts">
const colorMode = useColorMode()

function toggleDarkMode() {
  colorMode.preference = colorMode.value === "dark" ? "light" : "dark"
}
</script>
```

### Custom Components with @apply

```vue
<template>
  <button class="btn-primary">Primary Button</button>
</template>

<style>
.btn-primary {
  @apply px-4 py-2 bg-blue-500 text-white font-medium rounded-lg hover:bg-blue-600 transition-colors;
}
</style>
```

### Layout Utilities

```vue
<template>
  <!-- Flexbox -->
  <div class="flex items-center justify-between gap-4">
    <div>Left</div>
    <div>Right</div>
  </div>

  <!-- Grid -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div>Card 1</div>
    <div>Card 2</div>
    <div>Card 3</div>
  </div>

  <!-- Container -->
  <div class="container mx-auto max-w-7xl px-4">Content with max width</div>
</template>
```

### Transitions & Animations

```vue
<template>
  <div class="transition-all duration-300 hover:scale-105 hover:shadow-lg">
    Hover to animate
  </div>

  <button class="animate-pulse bg-blue-500 text-white px-4 py-2 rounded">
    Pulsing Button
  </button>
</template>
```

## Custom Layers

### Adding Custom Utilities

```css
/* assets/css/main.css */
@import "tailwindcss";

@layer utilities {
  .text-gradient {
    @apply bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent;
  }

  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }

  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
}
```

Usage:

```vue
<template>
  <h1 class="text-gradient text-4xl font-bold">Gradient Text</h1>

  <div class="scrollbar-hide overflow-auto">Scrollable without scrollbar</div>
</template>
```

### Custom Components Layer

```css
/* assets/css/main.css */
@import "tailwindcss";

@layer components {
  .card {
    @apply bg-white dark:bg-gray-800 rounded-lg shadow-md p-6;
  }

  .card-title {
    @apply text-xl font-semibold mb-2 text-gray-900 dark:text-white;
  }

  .card-body {
    @apply text-gray-600 dark:text-gray-300;
  }
}
```

Usage:

```vue
<template>
  <div class="card">
    <h2 class="card-title">Card Title</h2>
    <p class="card-body">Card content goes here.</p>
  </div>
</template>
```

## Tailwind Plugins

### Using Official Plugins

```bash
pnpm add -D @tailwindcss/forms @tailwindcss/typography @tailwindcss/container-queries
```

```typescript
// tailwind.config.ts
import type { Config } from "tailwindcss"

export default {
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/container-queries"),
  ],
} satisfies Config
```

### @tailwindcss/typography

For rich text content:

```vue
<template>
  <article class="prose dark:prose-invert lg:prose-xl mx-auto">
    <h1>Article Title</h1>
    <p>
      Automatically styled rich text content with proper spacing, typography,
      and dark mode support.
    </p>
    <ul>
      <li>List item 1</li>
      <li>List item 2</li>
    </ul>
  </article>
</template>
```

### @tailwindcss/forms

Automatically styles form elements:

```vue
<template>
  <form class="space-y-4">
    <!-- Forms plugin provides base styling -->
    <input
      type="text"
      class="form-input rounded-md"
      placeholder="Auto-styled input"
    />

    <select class="form-select rounded-md">
      <option>Option 1</option>
      <option>Option 2</option>
    </select>

    <textarea class="form-textarea rounded-md" rows="4" />
  </form>
</template>
```

## Nuxt-Specific Features

### Tailwind Viewer

Enable Tailwind config viewer in development:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  tailwindcss: {
    viewer: true,
  },
})
```

Access at: `http://localhost:3000/_tailwind`

### IntelliSense Configuration

For VSCode autocomplete, create `.vscode/settings.json`:

```json
{
  "tailwindCSS.experimental.classRegex": [
    ["class:\\s*['\"`]([^'\"`]*)['\"`]", "([^'\"`]*)"],
    ["class:\\s*{([^}]*)", "['\"`]([^'\"`]*)['\"`]"]
  ],
  "tailwindCSS.includeLanguages": {
    "vue": "html",
    "typescript": "javascript"
  }
}
```

### Scoped Styles with Tailwind

```vue
<template>
  <div class="custom-component">Content</div>
</template>

<style scoped>
.custom-component {
  @apply bg-blue-500 text-white p-4 rounded-lg;
}

/* Scoped styles work with Tailwind utilities */
.custom-component:hover {
  @apply bg-blue-600;
}
</style>
```

## JIT Mode (On by Default in v3+)

Just-In-Time compilation is default in Tailwind v3+. Benefits:

- **Arbitrary values:** `w-[137px]`, `top-[117px]`
- **Arbitrary variants:** `[&>*]:text-red-500`
- **Dynamic values:** `bg-[#1da1f2]`

```vue
<template>
  <div>
    <!-- Arbitrary values -->
    <div class="w-[137px] h-[91px] bg-[#1da1f2]">Custom size and color</div>

    <!-- Arbitrary variants -->
    <ul class="[&>li]:text-blue-500 [&>li]:font-bold">
      <li>Item 1</li>
      <li>Item 2</li>
    </ul>

    <!-- Dynamic spacing -->
    <div class="m-[calc(100%-3rem)]">Calculated margin</div>
  </div>
</template>
```

## Performance Optimization

### Purging Unused Styles

Automatically handled by Tailwind. Ensure `content` paths in config are correct:

```typescript
// tailwind.config.ts
export default {
  content: [
    "./components/**/*.{vue,js,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
  ],
} satisfies Config
```

### Safelist Dynamic Classes

For dynamically generated classes:

```typescript
// tailwind.config.ts
export default {
  safelist: [
    "bg-red-500",
    "bg-blue-500",
    "bg-green-500",
    {
      pattern: /bg-(red|blue|green)-(400|500|600)/,
    },
  ],
} satisfies Config
```

Or use string interpolation with full class names:

```vue
<script setup lang="ts">
// Bad: Classes may be purged
const color = ref("blue")
const bgClass = computed(() => `bg-${color.value}-500`)

// Good: Full class names are detected
const bgClass = computed(() => {
  if (color.value === "blue") return "bg-blue-500"
  if (color.value === "red") return "bg-red-500"
  return "bg-green-500"
})
</script>
```

## Common Utilities Reference

### Spacing

- `p-{size}` - padding
- `m-{size}` - margin
- `space-x-{size}` - horizontal gap between children
- `space-y-{size}` - vertical gap between children
- `gap-{size}` - gap in flex/grid

### Sizing

- `w-{size}` - width
- `h-{size}` - height
- `max-w-{size}` - max width
- `min-h-{size}` - min height

### Typography

- `text-{size}` - font size
- `font-{weight}` - font weight
- `leading-{size}` - line height
- `tracking-{size}` - letter spacing
- `text-{align}` - text alignment

### Colors

- `text-{color}-{shade}` - text color
- `bg-{color}-{shade}` - background color
- `border-{color}-{shade}` - border color

### Layout

- `flex`, `inline-flex` - flexbox
- `grid`, `inline-grid` - grid
- `block`, `inline-block`, `hidden` - display
- `relative`, `absolute`, `fixed`, `sticky` - positioning

### Borders

- `border`, `border-{width}` - border width
- `rounded-{size}` - border radius
- `border-{side}` - specific side border

### Effects

- `shadow-{size}` - box shadow
- `opacity-{amount}` - opacity
- `blur-{amount}` - blur effect

## Best Practices

1. **Use Tailwind viewer in dev** - Enable `viewer: true` to explore your config
2. **Avoid @apply overuse** - Prefer composition over extraction for most cases
3. **Use arbitrary values sparingly** - Stick to design system values when possible
4. **Leverage dark mode utilities** - Test with `dark:` variants
5. **Keep config minimal** - Only extend when design system requires it
6. **Use safelist for dynamic classes** - Or ensure full class names in templates
7. **Enable IntelliSense** - Configure VSCode for autocomplete
8. **Responsive-first** - Use mobile-first breakpoints (`sm:`, `md:`, `lg:`)
9. **Use Tailwind plugins** - Leverage official plugins for common needs
10. **Avoid inline styles** - Prefer Tailwind utilities over style attributes

## Troubleshooting

### Styles Not Applied

Check:

1. `@import "tailwindcss"` in `main.css` (v4) or `@tailwind` directives (v3)
2. `main.css` imported in `nuxt.config.ts` or `app.vue`
3. `content` paths in `tailwind.config.ts` include all component files
4. Class names are complete strings (not dynamically concatenated)

### Dark Mode Not Working

Ensure `@nuxtjs/color-mode` is installed:

```bash
pnpm add @nuxtjs/color-mode
```

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ["@nuxtjs/tailwindcss", "@nuxtjs/color-mode"],
})
```

### IntelliSense Not Working

1. Install "Tailwind CSS IntelliSense" VSCode extension
2. Create `.vscode/settings.json` with Tailwind config
3. Restart VSCode

### Build Size Too Large

1. Verify `content` paths only include necessary files
2. Remove unused plugins
3. Avoid safelisting large pattern sets
4. Use CDN for development, bundled for production

## Migration from v3 to v4

Key changes when upgrading to Tailwind v4:

1. **Import syntax:**

   ```css
   /* v3 */
   @tailwind base;
   @tailwind components;
   @tailwind utilities;

   /* v4 */
   @import "tailwindcss";
   ```

2. **CSS-based configuration** - Use CSS variables alongside TypeScript config

3. **Removed PostCSS plugins** - Many features now built-in

4. **New color system** - Improved color utilities with better composability

Consult official Tailwind v4 migration guide for comprehensive changes.

## Official Resources

- **Tailwind CSS Docs:** https://tailwindcss.com
- **Nuxt Tailwind Module:** https://tailwindcss.nuxtjs.org
- **Cheat Sheet:** https://nerdcave.com/tailwind-cheat-sheet
- **Component Examples:** https://tailwindui.com (official, paid)
- **Community Components:** https://tailwindcomponents.com

---

**Note:** Verify version-specific features with official documentation. This guide covers both Tailwind v3 and v4, focusing on Nuxt integration.
