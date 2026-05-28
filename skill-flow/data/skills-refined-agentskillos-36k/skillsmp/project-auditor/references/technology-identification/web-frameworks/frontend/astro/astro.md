# Astro

**Category**: web-frameworks/frontend
**Description**: The web framework for content-driven websites - Build fast websites with less client-side JavaScript

## Package Detection

### NPM
- `astro`

### Related Packages
- `@astrojs/react`
- `@astrojs/vue`
- `@astrojs/svelte`
- `@astrojs/solid-js`
- `@astrojs/tailwind`
- `@astrojs/mdx`

## Import Detection

### Javascript
File extensions: .astro, .js, .ts, .jsx, .tsx

**Pattern**: `import.*from ['"]astro`
- Astro framework imports
- Example: `import { defineConfig } from 'astro/config';`

**Pattern**: `import.*from ['"]@astrojs/`
- Astro integration imports
- Example: `import react from '@astrojs/react';`

### Common Imports
- `astro/config`
- `@astrojs/react`
- `@astrojs/vue`
- `@astrojs/svelte`

## Environment Variables

*Astro public environment variables (exposed to client)*

- Prefix: `PUBLIC_*`

## Configuration Files

- `astro.config.mjs`
- `astro.config.js`
- `astro.config.ts`
- `*.astro`

## Detection Notes

- Astro is a static site generator with component islands architecture
- Can use React, Vue, Svelte, or Solid components
- Focuses on zero JS by default

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 60% (MEDIUM)
- **API Endpoint Detection**: 70% (MEDIUM)
