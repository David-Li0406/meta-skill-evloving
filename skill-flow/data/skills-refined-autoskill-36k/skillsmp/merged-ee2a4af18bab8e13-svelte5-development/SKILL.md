---
name: svelte5-development
description: Use this skill when building web applications with Svelte 5 and SvelteKit, covering components, routing, reactive patterns, and data loading.
---

# Svelte 5 Development Skill

## When to Activate

Activate this skill when:
- Creating Svelte 5 components
- Working with SvelteKit routing
- Implementing runes ($state, $derived, $effect)
- Building forms with actions
- Setting up SvelteKit projects

## Quick Commands

```bash
npx sv create <project-name>  # Create SvelteKit project
cd <project-name> && pnpm install
pnpm dev                       # Start dev server (localhost:5173)
pnpm build                     # Build for production
```

## Runes Quick Reference

| Rune      | Purpose            | Example                             |
|-----------|--------------------|-------------------------------------|
| `$state`  | Reactive state      | `let count = $state(0)`            |
| `$derived`| Computed values     | `let doubled = $derived(count * 2)`|
| `$effect` | Side effects        | `$effect(() => console.log(count))`|
| `$props`  | Component props     | `let { name } = $props()`          |
| `$bindable`| Two-way binding    | `let { value = $bindable() } = $props()` |

## Reactive State ($state)

```svelte
<script>
  let count = $state(0);
  let user = $state({ name: 'Alice', age: 30 });
</script>

<button onclick={() => count++}>
  Clicked {count} times
</button>

<button onclick={() => user.age++}>
  {user.name} is {user.age}
</button>
```

**Deep reactivity**: Objects and arrays update automatically on mutation.

## Computed Values ($derived)

```svelte
<script>
  let count = $state(0);
  let doubled = $derived(count * 2);
</script>

<p>{count} × 2 = {doubled}</p>
```

## Side Effects ($effect)

```svelte
<script>
  let count = $state(0);

  $effect(() => {
    console.log(`Count is ${count}`);
    document.title = `Count: ${count}`;
  });
</script>
```

## Component Props ($props)

```svelte
<!-- Button.svelte -->
<script>
  let { label, disabled = false, onclick } = $props();
</script>

<button {disabled} {onclick}>{label}</button>
```

## SvelteKit File Conventions

| File                     | Purpose                          |
|--------------------------|----------------------------------|
| `+page.svelte`          | Page component                   |
| `+page.server.js`       | Server-only load/actions         |
| `+layout.svelte`        | Shared layout                    |
| `+server.js`            | API endpoints                    |
| `+error.svelte`         | Error boundary                   |

## Data Loading

```javascript
// src/routes/posts/+page.server.js
export async function load({ fetch }) {
  const response = await fetch('/api/posts');
  return { posts: await response.json() };
}
```

## Form Actions

```javascript
// src/routes/login/+page.server.js
import { fail, redirect } from '@sveltejs/kit';

export const actions = {
  default: async ({ request, cookies }) => {
    const data = await request.formData();
    const email = data.get('email');

    if (!email) {
      return fail(400, { missing: true });
    }

    cookies.set('session', token, { path: '/' });
    throw redirect(303, '/dashboard');
  }
};
```

## Common Pitfalls

### Destructuring Breaks Reactivity
```javascript
// ❌ Bad
let { count } = $state({ count: 0 });

// ✅ Good
let state = $state({ count: 0 });
state.count++;
```

### Missing Keys in Each
```svelte
<!-- ❌ Bad -->
{#each items as item}

<!-- ✅ Good -->
{#each items as item (item.id)}
```

## Project Structure

```
src/
├── lib/
│   ├── components/
│   └── server/
├── routes/
│   ├── +layout.svelte
│   ├── +page.svelte
│   └── api/
├── app.html
└── hooks.server.js
```

## Best Practices

1. **Use $derived, not $effect, for computed values**
2. **Don't mutate props** (use callbacks or $bindable)
3. **Always provide keys in {#each} blocks** for dynamic lists
4. **Prefer server load functions** for sensitive data

## When to Consult External Resources

This skill covers the most common Svelte 5 and SvelteKit patterns. For advanced topics, refer to:
- SvelteKit adapters and deployment
- Advanced routing
- Service workers and offline support
- Custom Svelte stores

Remember: Start with the fundamentals in this skill, then explore advanced topics as needed.