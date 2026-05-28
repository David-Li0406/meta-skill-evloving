# Vue

**Category**: web-frameworks/frontend
**Description**: The Progressive JavaScript Framework - Approachable, performant and versatile framework for building web user interfaces
**Homepage**: https://vuejs.org

## Package Detection

### NPM
*Core Vue 3.x package and official tooling*

- `vue`

### YARN
*Core Vue package via Yarn*

- `vue`

### PNPM
*Core Vue package via pnpm*

- `vue`

### Related Packages
- `vue-router`
- `vuex`
- `pinia`
- `vite`
- `@vitejs/plugin-vue`
- `nuxt`
- `vue-loader`
- `vuepress`
- `quasar`
- `vuetify`
- `element-plus`
- `naive-ui`

## Import Detection

### Javascript
File extensions: .js, .mjs, .ts

**Pattern**: `import\s+.*\s+from\s+['"]vue['"]`
- ES6 import from Vue
- Example: `import { createApp } from 'vue';`

**Pattern**: `import\s+\{[^}]*(createApp|ref|reactive|computed|watch)[^}]*\}\s+from\s+['"]vue['"]`
- Vue 3 Composition API imports
- Example: `import { ref, reactive, computed } from 'vue';`

**Pattern**: `require\(['"]vue['"]\)`
- CommonJS require
- Example: `const Vue = require('vue');`

**Pattern**: `import\s+.*\s+from\s+['"]vue-router['"]`
- Vue Router import
- Example: `import { createRouter } from 'vue-router';`

**Pattern**: `import\s+.*\s+from\s+['"]pinia['"]`
- Pinia state management
- Example: `import { createPinia } from 'pinia';`

### Vue
File extensions: .vue

**Pattern**: `<template>`
- Vue single-file component template
- Example: `<template><div>Hello</div></template>`

**Pattern**: `<script\s+(setup)?`
- Vue script block (including setup)
- Example: `<script setup>`

**Pattern**: `<style\s+(scoped)?`
- Vue scoped styles
- Example: `<style scoped>`

### Common Imports
- `createApp`
- `ref`
- `reactive`
- `computed`
- `watch`
- `onMounted`
- `defineComponent`
- `createRouter`
- `createPinia`

## Environment Variables

*Vue CLI environment variables*

- Prefix: `VUE_APP_*`
*Vite environment variables (Vue 3 + Vite)*

- Prefix: `VITE_*`
*Vue CLI build environment variables*

- `NODE_ENV`
- `VUE_CLI_MODERN_BUILD`
- `VUE_CLI_MODERN_MODE`

## Configuration Files

- `vue.config.js`
- `vue.config.ts`
- `vite.config.js`
- `vite.config.ts`
- `.vuerc`
- `.vuepressrc`
- `*.vue`

## Detection Notes

- Check for vue in dependencies or devDependencies
- Look for .vue single-file components
- Check for vue.config.js or vite.config.js with Vue plugin
- Look for @vue scoped packages (Vue 3 ecosystem)
- Pinia is the new official state management (replaces Vuex in Vue 3)

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 85% (HIGH)
- **Environment Variable Detection**: 60% (MEDIUM)
- **API Endpoint Detection**: 50% (MEDIUM)
