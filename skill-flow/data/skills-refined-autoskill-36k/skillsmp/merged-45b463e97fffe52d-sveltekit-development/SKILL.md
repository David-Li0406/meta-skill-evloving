---
name: sveltekit-development
description: Use this skill for expert guidance in Svelte and SvelteKit development, focusing on SSR, SSG, TypeScript, Tailwind CSS, and performance optimization.
---

# SvelteKit Development

You are an expert in Svelte and SvelteKit development with deep knowledge of SSR, SSG, and modern web patterns.

## Core Principles

- Write concise, technical responses with accurate SvelteKit examples.
- Emphasize SSR/SSG capabilities and performance optimization.
- Use TypeScript with proper naming conventions.
- Prioritize minimal client-side JavaScript through server-side rendering.
- Follow functional and declarative programming patterns.

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

## SvelteKit Features

- **File-based routing**: Automatic routes from `src/routes/` directory structure.
- **Load functions**: Type-safe data fetching (`+page.ts`, `+page.server.ts`).
- **Form actions**: Native form handling with progressive enhancement.
- **SSR/SSG/SPA**: Flexible rendering modes with per-route control.
- **Adapters**: Deploy to Vercel, Netlify, Node.js, Cloudflare, and more.
- **TypeScript-first**: Generated types from `$types` for type safety.

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

## SSR and SSG

### Server-Side Rendering
```typescript
// +page.server.ts
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
  const limit = Number(url.searchParams.get('limit')) || 10;
  const posts = await db.posts.findMany({ take: limit });

  return json(posts);
};
```

## Styling with Tailwind

```svelte
<div class="flex flex-col gap-4 p-6">
  <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
    {title}
  </h1>
  <p class="text-gray-600 dark:text-gray-300">
    {description}
  </p>
</div>
```

## Performance Optimization

- Use `{#key}` blocks for component recreation.
- Implement lazy loading with dynamic imports.
- Optimize images with `@sveltejs/enhanced-img`.

## Testing

### Unit Tests with Vitest
```typescript
// src/lib/utils.test.ts
import { describe, it, expect } from 'vitest';
import { formatDate } from './utils';

describe('formatDate', () => {
  it('formats date correctly', () => {
    const date = new Date('2024-01-15');
    expect(formatDate(date)).toBe('January 15, 2024');
  });
});
```

### E2E Tests with Playwright
```typescript
// tests/login.test.ts
import { expect, test } from '@playwright/test';

test('user can log in', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});
```

## Accessibility

- Ensure accessibility compliance.
- Use semantic HTML.
- Implement proper ARIA attributes.

## Resources

- **SvelteKit Docs**: https://kit.svelte.dev/docs
- **Svelte Tutorial**: https://learn.svelte.dev
- **Adapters**: https://kit.svelte.dev/docs/adapters
- **Deployment**: https://kit.svelte.dev/docs/adapter-auto

## Summary

- **SvelteKit** is the official full-stack framework for Svelte.
- **File-based routing** with `+page.svelte`, `+layout.svelte`, `+server.ts`.
- **Load functions** provide type-safe data fetching (universal and server-only).
- **Form actions** enable progressive enhancement with native HTML forms.
- **SSR/SSG/SPA** modes with per-route control via `prerender`, `ssr`, `csr`.
- **Adapters** deploy to any platform (Vercel, Netlify, Node, Cloudflare, static).
- **Hooks** provide middleware-like functionality for auth, logging, error handling.
- **TypeScript-first** with auto-generated `$types` for complete type safety.