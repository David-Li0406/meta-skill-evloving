# Nuxt Modules Reference

Check package.json for installed modules before suggesting module-specific features.

## Image Optimization (@nuxt/image)

**Check:** `@nuxt/image` in package.json

Provides optimized image components with automatic format conversion and responsive images. For comprehensive guidance, see `references/nuxt-image.md`.

## Content Management (@nuxt/content)

**Check:** `@nuxt/content` in package.json

File-based CMS for Nuxt with markdown, YAML, and JSON support. For comprehensive guidance including queries, components, and content navigation, see `references/nuxt-content.md`.

## Icon Management (@nuxt/icon)

**Check:** `@nuxt/icon` in package.json

### Icon Component

```vue
<Icon name="heroicons:home" size="24" />
<Icon name="mdi:github" class="text-2xl" />
```

## UI Components (@nuxt/ui)

**Check:** `@nuxt/ui` in package.json

Provides pre-built components with Tailwind CSS. For comprehensive Nuxt UI guidance including setup, v3/v4 differences, and migration, see `references/nuxt-ui.md`.

## SEO (@nuxtjs/seo)

**Check:** `@nuxtjs/seo` in package.json

Provides SEO utilities including sitemap, robots.txt, and OG images.

```typescript
// Auto-generates sitemap
// Configure in nuxt.config.ts
export default defineNuxtConfig({
  site: {
    url: "https://example.com",
    name: "My Site",
  },
})
```

## Internationalization (@nuxtjs/i18n)

**Check:** `@nuxtjs/i18n` in package.json

Provides internationalization with auto-imports, locale routing, and SEO support. For comprehensive guidance including setup, translations, and routing, see `references/nuxt-i18n.md`.

## Tailwind CSS (@nuxtjs/tailwindcss)

**Check:** `@nuxtjs/tailwindcss` in package.json

Auto-configured Tailwind CSS integration. For comprehensive guidance including setup, configuration, dark mode, and best practices, see `references/tailwind.md`.

## Color Mode (@nuxtjs/color-mode)

**Check:** `@nuxtjs/color-mode` in package.json

**Documentation:** https://color-mode.nuxtjs.org/

### Installation

```bash
npx nuxt module add color-mode
```

### Composable API

```typescript
const colorMode = useColorMode()

// Properties:
colorMode.preference // User's preference ('system', 'light', 'dark', etc.) - writeable
colorMode.value // Actual detected mode when preference is 'system' - read-only
colorMode.unknown // True during SSR before client detection
colorMode.forced // True if page forces a color mode
```

### Toggle Dark Mode

```vue
<script setup lang="ts">
const colorMode = useColorMode()

function toggleDark() {
  colorMode.preference = colorMode.value === "dark" ? "light" : "dark"
}
</script>

<template>
  <button @click="toggleDark">
    {{ colorMode.value === "dark" ? "🌞" : "🌙" }}
  </button>
</template>
```

### Color Mode Selector

```vue
<template>
  <select v-model="$colorMode.preference">
    <option value="system">System</option>
    <option value="light">Light</option>
    <option value="dark">Dark</option>
  </select>
</template>
```

### Force Mode Per Page

Lock specific pages to a color mode (useful for incremental dark mode adoption):

```vue
<script setup lang="ts">
definePageMeta({
  colorMode: "light", // or 'dark'
})
</script>

<template>
  <!-- Hide color picker on forced pages -->
  <ColorPicker v-if="!$colorMode.forced" />
</template>
```

### Configuration

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  colorMode: {
    preference: "system", // Default: 'system'
    fallback: "light", // Fallback if system unavailable
    storage: "localStorage", // 'localStorage' | 'sessionStorage' | 'cookie'
    storageKey: "nuxt-color-mode",
    classPrefix: "", // e.g., 'theme-' → 'theme-dark'
    classSuffix: "", // e.g., '-mode' → 'dark-mode'
    dataValue: undefined, // Set to add data-theme="dark" attribute
  },
})
```

### CSS Styling

Module adds class to `<html>` (e.g., `.dark`, `.light`):

```css
/* Plain CSS */
.dark body {
  background: #1a1a1a;
  color: #fff;
}

/* Tailwind - works out of the box */
/* Uses Tailwind's dark: variant automatically */
```

## ESLint (@nuxt/eslint)

**Check:** `@nuxt/eslint` in package.json

Provides auto-configured ESLint with Nuxt-specific rules. Configuration in `eslint.config.mjs`:

```javascript
import { createConfigForNuxt } from "@nuxt/eslint-config/flat"

export default createConfigForNuxt({
  features: {
    stylistic: true,
  },
})
```

## Security (nuxt-security)

**Check:** `nuxt-security` in package.json

### Security Headers

Automatically applies security headers. Configure in nuxt.config.ts:

```typescript
export default defineNuxtConfig({
  security: {
    headers: {
      contentSecurityPolicy: {
        "img-src": ["'self'", "https:", "data:"],
      },
    },
    rateLimiter: {
      tokensPerInterval: 150,
      interval: "hour",
    },
  },
})
```

## Fonts (@nuxt/fonts)

**Check:** `@nuxt/fonts` in package.json

Automatically optimizes and loads fonts:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  fonts: {
    families: [{ name: "Inter", provider: "google" }],
  },
})
```

```vue
<style>
.text {
  font-family: "Inter", sans-serif;
}
</style>
```

## Scripts (@nuxt/scripts)

**Check:** `@nuxt/scripts` in package.json

Load third-party scripts efficiently:

```vue
<script setup lang="ts">
useScript({
  src: "https://www.googletagmanager.com/gtag/js",
  async: true,
})
</script>
```
