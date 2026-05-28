---
name: sveltekit-development
description: Use this skill for comprehensive guidance on developing modern web applications with SvelteKit, TypeScript, and Tailwind CSS.
---

# SvelteKit Development

This skill provides expert guidance for developing web applications using SvelteKit, focusing on static site generation, TypeScript integration, and Tailwind CSS styling.

## Key Principles

- Write concise, technical SvelteKit code with accurate TypeScript examples.
- Use functional and declarative programming patterns; avoid classes.
- Prefer iteration and modularization over code duplication.
- Use descriptive variable names with auxiliary verbs (isLoading, hasError).
- Structure files for components, routes, and utilities.

## Project Structure

```
src/
├── lib/
│   ├── components/     # Reusable Svelte components
│   ├── server/         # Server-only utilities
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

### Server-Side Rendering
```typescript
// +page.server.ts
export const ssr = true;
export const csr = true;

export const load: PageServerLoad = async ({ locals }) => {
  return {
    user: locals.user
  };
};
```

### Static Generation
```typescript
// +page.ts
export const prerender = true;

export async function load() {
  return {
    // Static data
  };
}
```

## Form Actions

```typescript
// +page.server.ts
import type { Actions } from './$types';

export const actions: Actions = {
  default: async ({ request, cookies }) => {
    const data = await request.formData();
    const email = data.get('email');

    if (!email) {
      return { success: false, error: 'Email required' };
    }

    return { success: true };
  }
};
```

```svelte
<!-- +page.svelte -->
<script lang="ts">
  import { enhance } from '$app/forms';
  import type { ActionData } from './$types';

  export let form: ActionData;
</script>

<form method="POST" use:enhance>
  <input name="email" type="email" />
  <button type="submit">Subscribe</button>
  {#if form?.error}
    <p class="error">{form.error}</p>
  {/if}
</form>
```

## State Management

### Svelte Stores
```typescript
// lib/stores/counter.ts
import { writable, derived } from 'svelte/store';

export const count = writable(0);
export const doubled = derived(count, ($count) => $count * 2);

export function increment() {
  count.update((n) => n + 1);
}
```

## API Routes

```typescript
// routes/api/posts/+server.ts
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
  const limit = url.searchParams.get('limit') ?? '10';
  const posts = await getPosts(Number(limit));

  return json(posts);
};

export const POST: RequestHandler = async ({ request }) => {
  const body = await request.json();
  const post = await createPost(body);

  return json(post, { status: 201 });
};
```

## Styling with Tailwind CSS

```css
/* src/app.css */
@import 'tailwindcss';

@theme {
  /* Custom color palette */
  --color-primary: var(--color-slate-800);
  --color-primary-hover: var(--color-slate-700);
  --color-muted: var(--color-slate-50);
  --color-success: var(--color-green-600);
  --color-danger: var(--color-red-600);
}
```

## Performance Optimization

- Use `{#key}` blocks for component recreation.
- Implement lazy loading with dynamic imports.
- Optimize images with `@sveltejs/enhanced-img`.
- Prefetch links with `data-sveltekit-preload-data`.

## Best Practices

- Use TypeScript for all components and utilities.
- Design for static generation from the start.
- Follow atomic design principles for maintainable components.
- Optimize component re-rendering with `$:` reactive statements.

## Testing

```typescript
// Component testing with Vitest
import { render, screen } from '@testing-library/svelte';
import { expect, test } from 'vitest';
import Button from './Button.svelte';

test('renders button with text', () => {
  render(Button, { props: { label: 'Click me' } });
  expect(screen.getByRole('button')).toHaveTextContent('Click me');
});
```

## Accessibility

- Use semantic HTML elements.
- Add ARIA labels where needed.
- Ensure keyboard navigation.
- Test with screen readers.

## Development Workflow

- Use `npm run check` for type checking.
- Run `npm run lint` for code quality.
- Test static builds with `npm run build && npm run preview`.
- Use debug routes for component development.

## Related Skills

- **vite**: Build tool and development server used by SvelteKit.
- **bun**: Alternative JavaScript runtime for faster development.
- **github-actions**: CI/CD pipelines for automated deployment.
- **frontend-design**: UI/UX design patterns and component libraries.