# Svelte

**Category**: web-frameworks/frontend
**Description**: Cybernetically enhanced web apps - Compiler-based framework with no virtual DOM
**Homepage**: https://svelte.dev

## Package Detection

### NPM
*Svelte compiler and SvelteKit*

- `svelte`

### Related Packages
- `@sveltejs/kit`
- `vite`
- `svelte-check`
- `svelte-preprocess`

## Import Detection

### Javascript
File extensions: .svelte

**Pattern**: `<script>`
- Svelte component script
- Example: `<script>let count = 0;</script>`

### Common Imports
- `svelte/store`
- `svelte/transition`

## Environment Variables

*Vite environment variables (used by SvelteKit)*

- Prefix: `VITE_*`

## Configuration Files

- `svelte.config.js`
- `vite.config.js`
- `*.svelte`

## Detection Notes

- Look for .svelte files
- SvelteKit is the meta-framework (like Next.js for React)
- Uses Vite for build tooling

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 85% (HIGH)
- **Environment Variable Detection**: 60% (MEDIUM)
