---
name: nuxt-code-editor
description: Use this skill when you need to generate and modify Vue 3, TypeScript, and SCSS code following project standards.
---

# Skill body

## Capabilities

- **Vue 3 Composition API**: Generate `<script setup lang="ts">` components.
- **PrimeVue 4 Integration**: Correctly use PrimeVue 4 components based on `utils/` or existing `components/` usage.
- **Icon Library**: Use `@mdi/font` (Material Design Icons) as the icon library.
- **Type Safety**: Ensure all backend code uses TypeORM entities and DTOs defined in `server/entities` or `types/`.
- **Incremental Editing**: Prefer patching rather than rewriting entire files to retain context.

## Instructions

1. **Code Style Guide**: Follow ESLint and Stylelint configurations. Use SCSS for styling and apply BEM naming conventions.
2. **Component Standards**: Use `defineProps`, `defineEmits`, and TypeScript interfaces/types.
3. **Backend Standards**: Ensure `server/api` handlers use `defineEventHandler` and return standardized responses (refer to `docs/standards/api.md`).
4. **Internationalization (I18n)**: Follow the guidelines in `docs/standards/i18n.md` to gradually replace hardcoded text with translation keys.
5. **File Creation**: When creating files, ensure they are placed in the correct Nuxt directories (`components`, `composables`, `server/api`, etc.).

## Usage Example

Input: "Create a button component."
Action: Generate `components/base/AppButton.vue` using PrimeVue 4 Button, define props in the TS interface, and use `mdi-*` class names for icons.

Input: "Create an API to fetch a list of articles."
Action: In `server/api/posts.get.ts`, use `defineEventHandler` and TypeORM's Repository to fetch data.