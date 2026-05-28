# Nuxt

**Category**: web-frameworks/frontend
**Description**: The Intuitive Vue Framework - Build production-ready Vue.js applications with server-side rendering

## Package Detection

### NPM
- `nuxt`
- `nuxt3`

### Related Packages
- `@nuxt/content`
- `@nuxt/image`
- `@nuxtjs/tailwindcss`
- `@pinia/nuxt`
- `@nuxtjs/color-mode`
- `nuxi`

## Import Detection

### Javascript
File extensions: .js, .ts, .vue

**Pattern**: `import.*from ['"]#app`
- Nuxt 3 auto-imports from #app
- Example: `import { useNuxtApp } from '#app';`

**Pattern**: `defineNuxtConfig`
- Nuxt configuration
- Example: `export default defineNuxtConfig({...})`

**Pattern**: `useNuxt|useFetch|useAsyncData`
- Nuxt composables
- Example: `const { data } = await useFetch('/api/data')`

### Common Imports
- `#app`
- `nuxt/app`
- `@nuxt/schema`

## Environment Variables

*Nuxt 3 public runtime config (exposed to client)*

- Prefix: `NUXT_PUBLIC_*`
*Nuxt 3 private runtime config (server-only)*

- Prefix: `NUXT_*`

## Configuration Files

- `nuxt.config.js`
- `nuxt.config.ts`
- `app.vue`
- `.nuxt/`

## Detection Notes

- Nuxt is built on Vue.js
- Nuxt 3 is the current major version
- Server-side rendering and static site generation

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 70% (MEDIUM)
- **API Endpoint Detection**: 75% (MEDIUM)
