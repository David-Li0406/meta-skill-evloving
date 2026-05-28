---
name: sveltekit-development
description: Use this skill when you need comprehensive guidance for developing modern web applications with SvelteKit, TypeScript, and Tailwind CSS.
---

# SvelteKit Development

This skill provides expert guidance for developing web applications using SvelteKit, focusing on key principles, project structure, component development, routing, and performance optimization.

## Key Principles

- Write concise, technical SvelteKit code with accurate TypeScript examples.
- Use functional and declarative programming patterns; avoid classes.
- Prefer iteration and modularization over code duplication.
- Use descriptive variable names with auxiliary verbs (e.g., isLoading, hasError).

## Project Structure

```
src/
├── lib/
│   ├── components/     # Reusable Svelte components
│   ├── features/       # Feature-based organization
│   ├── stores/         # Svelte stores
│   └── utils/          # Shared utilities
├── routes/
│   ├── +layout.svelte  # Root layout
│   ├── +page.svelte    # Home page
│   └── api/            # API routes
├── app.html            # HTML template
└── app.css             # Global styles
```

## Component Development

### Script Setup with TypeScript
```svelte
<script lang="ts">
  import { onMount } from 'svelte';
  import type { PageData } from './$types';

  export let data: PageData;

  let count = 0;
  $: doubled = count * 2;

  function increment() {
    count += 1;
  }
</script>
```

### Props and Events
```svelte
<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  export let title: string;
  export let disabled = false;

  const dispatch = createEventDispatcher<{
    submit: { value: string };
  }>();

  function handleSubmit() {
    dispatch('submit', { value: title });
  }
</script>
```

## Routing

### File-Based Routes
```
routes/
├── +page.svelte          # /
├── about/+page.svelte    # /about
├── blog/
│   ├── +page.svelte      # /blog
│   └── [slug]/
│       └── +page.svelte  # /blog/:slug
```

### Dynamic Routes
```svelte
<!-- routes/blog/[slug]/+page.svelte -->
<script lang="ts">
  import type { PageData } from './$types';
  export let data: PageData;
</script>

<h1>{data.post.title}</h1>
```

### Load Functions
```typescript
// +page.server.ts
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, fetch }) => {
  const response = await fetch(`/api/posts/${params.slug}`);
  const post = await response.json();

  return { post };
};
```

## SSR and SSG

### Static Site Generation Configuration
```javascript
// svelte.config.js
import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({
      pages: 'build',
      assets: 'build',
      fallback: undefined,
      precompress: false,
      strict: true
    }),
    paths: {
      base: process.argv.includes('dev') ? '' : process.env.BASE_PATH
    }
  }
};
```

## TailwindCSS v4 Theme
```css
/* TailwindCSS configuration for custom theme */
```