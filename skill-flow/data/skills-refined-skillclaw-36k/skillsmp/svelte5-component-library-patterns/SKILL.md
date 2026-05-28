---
name: svelte5-component-library-patterns
description: Production-grade Svelte 5 component library architecture using runes, TypeScript, snippets, and SvelteKit @sveltejs/package standards. Covers reactivity patterns, type safety, composition strategies, testing, and performance optimization for scalable, reusable components.
license: MIT
compatibility: opencode
metadata:
  audience: frontend-developers, senior-engineers, framework-architects
  domain: frontend-architecture
  workflow: component-library-development
  updated: "2025-01"
  keywords: svelte5, runes, component-library, typescript, snippets, composition, reactivity
---

## What I do

I guide the architecture and implementation of production-grade Svelte 5 component libraries using modern rune-based patterns. I help you:

- **Leverage Svelte 5 runes effectively** - Build reactive components using `$state`, `$derived`, `$props`, `$bindable`, and `$effect` runes instead of legacy reactive declarations
- **Design type-safe components** - Implement full TypeScript integration with proper generics, component prop types, and callable component interfaces
- **Compose with snippets** - Replace Svelte 4 slots with Svelte 5 snippets for flexible, type-safe component composition and composition patterns
- **Structure scalable libraries** - Organize components, utilities, types, and styles following SvelteKit packaging standards with proper export strategies
- **Test comprehensively** - Apply unit, integration, and snapshot testing patterns using Vitest and @testing-library/svelte for library-grade quality
- **Optimize performance** - Use `$derived.by`, `$state.raw`, lazy loading, and key blocks to minimize bundle size and rendering overhead
- **Export strategically** - Implement granular exports, conditional export conditions, and tree-shaking configuration for optimal consumer experience

## When to use me

Load this skill when:
- You're designing or building a new Svelte 5 component library from scratch
- You're migrating a Svelte 4 component library to Svelte 5's rune-based architecture
- You need guidance on best practices for component composition, state management, or reactivity patterns
- You're implementing TypeScript integration or type-safe component interfaces in a Svelte project
- You're architecting a multi-component system and need reusable patterns for snippets, props, and composition
- You're optimizing a component library for bundle size, performance, or tree-shaking
- You're setting up testing infrastructure or export strategies for a component library
- You're training a team on modern Svelte 5 patterns and architecture standards

## Project structure and setup

### Recommended directory organization

```
my-component-lib/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── Button.svelte
│   │   │   ├── Card.svelte
│   │   │   ├── Dialog.svelte
│   │   │   └── index.ts              # Public component exports
│   │   ├── utilities/
│   │   │   ├── hooks.svelte.ts       # Reactive utilities via $state, $derived
│   │   │   ├── format.ts             # Pure utility functions
│   │   │   └── index.ts
│   │   ├── types/
│   │   │   ├── component.ts          # Shared component types
│   │   │   └── index.ts
│   │   ├── styles/
│   │   │   ├── tokens.css            # Design tokens
│   │   │   └── global.css
│   │   └── index.ts                  # Main library entry point
│   └── routes/
│       └── demo/                      # Documentation and interactive examples
├── package.json
├── tsconfig.json
├── svelte.config.js
├── vite.config.js
└── vitest.config.ts
```

### package.json configuration

```json
{
  "name": "@your-org/components",
  "version": "1.0.0",
  "license": "MIT",
  "type": "module",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "svelte": "./dist/index.js",
      "default": "./dist/index.js"
    },
    "./Button": {
      "types": "./dist/Button.svelte.d.ts",
      "svelte": "./dist/Button.svelte",
      "default": "./dist/Button.svelte"
    },
    "./utilities": {
      "types": "./dist/utilities/index.d.ts",
      "default": "./dist/utilities/index.js"
    }
  },
  "svelte": "./dist/index.js",
  "files": ["dist", "src/lib"],
  "sideEffects": ["**/*.css"],
  "scripts": {
    "build": "svelte-package",
    "dev": "vite",
    "preview": "vite preview",
    "test": "vitest",
    "test:ui": "vitest --ui"
  },
  "devDependencies": {
    "@sveltejs/package": "^2.0.0",
    "@sveltejs/vite-plugin-svelte": "^3.0.0",
    "@testing-library/svelte": "^4.0.0",
    "@testing-library/user-event": "^14.0.0",
    "svelte": "^5.0.0",
    "typescript": "^5.0.0",
    "vitest": "^1.0.0"
  }
}
```

**Export strategy rationale**:
- Use conditional exports (`types`, `svelte`, `default`) for full Svelte ecosystem support
- Provide granular exports (e.g., `./Button`, `./utilities`) for better tree-shaking
- Maintain `sideEffects: ["**/*.css"]` so CSS isn't stripped by bundlers

## Svelte 5 runes: Core patterns for components

### $state rune: Component internal state

Use `$state` for reactive values that change within components:

```svelte
<script lang="ts">
  // Simple state
  let count = $state(0);
  
  // State with type annotation
  let items = $state<string[]>([]);
  
  // Deep reactivity: Mutations on nested objects are tracked
  let todos = $state([
    { id: 1, done: false, text: 'Learn runes' }
  ]);

  function increment() {
    count++; // Direct mutation, fully reactive
  }

  function toggleTodo(id: number) {
    const todo = todos.find(t => t.id === id);
    if (todo) todo.done = !todo.done; // Deep reactivity works
  }
</script>

<button onclick={increment}>Count: {count}</button>

{#each todos as todo (todo.id)}
  <label>
    <input type="checkbox" checked={todo.done} onchange={() => toggleTodo(todo.id)} />
    {todo.text}
  </label>
{/each}
```

**Pattern: Encapsulate state in custom objects**

```typescript
// hooks.svelte.ts
export function createCounter(initial = 0) {
  let count = $state(initial);

  return {
    get value() { return count; },
    increment: () => count++,
    decrement: () => count--,
    reset: () => count = initial
  };
}
```

**Best practice**: Use `$state` for component-internal state. For shared state across components, consider context or stores.

### $derived rune: Computed reactive values

Replace manual reactive assignments with `$derived` for automatic dependency tracking:

```svelte
<script lang="ts">
  let count = $state(0);

  // Automatic recomputation when count changes
  let doubled = $derived(count * 2);

  // Complex derived with $derived.by
  let status = $derived.by(() => {
    if (count === 0) return 'No items';
    if (count === 1) return 'One item';
    return `${count} items`;
  });

  // Derived from derived (chains are fine)
  let message = $derived(`You have ${status}`);
</script>

<p>Count: {count}</p>
<p>Doubled: {doubled}</p>
<p>Message: {message}</p>
```

**Pattern: Expensive computations with $derived.by**

```svelte
<script lang="ts">
  let items = $state([{ id: 1, active: true }, { id: 2, active: false }]);

  // ✅ Good: $derived.by caches result, recomputes only when items changes
  let filtered = $derived.by(() => {
    return items
      .filter(i => i.active)
      .map(i => ({ ...i, processed: true }));
  });

  // ❌ Avoid: Inline complex logic (less readable)
  // let filtered = $derived(items.filter(i => i.active).map(...))
</script>
```

**Best practice**: Use `$derived` for computed values; chains are cheap (rarely a performance concern).

### $props rune: Type-safe component props

Modern prop declaration with full TypeScript support and destructuring:

```svelte
<script lang="ts">
  import type { Snippet } from 'svelte';

  interface ButtonProps {
    label: string;                           // Required
    variant?: 'primary' | 'secondary';       // Optional with literal type
    disabled?: boolean;                      // Optional boolean
    onclick?: (e: MouseEvent) => void;       // Callback prop
    children?: Snippet;                      // Snippet for composition
  }

  // Destructure with defaults, all in one expression
  let { variant = 'primary', disabled = false, onclick, children, label }: ButtonProps = $props();
</script>

<button {disabled} {onclick} class={variant}>
  {label}
  {#if children}{@render children()}{/if}
</button>
```

**Pattern: Forwarding HTML attributes**

```svelte
<script lang="ts">
  import type { HTMLButtonAttributes } from 'svelte/elements';

  interface Props extends HTMLButtonAttributes {
    variant?: 'solid' | 'outline' | 'ghost';
  }

  let { variant = 'solid', ...rest }: Props = $props();
</script>

<button class={variant} {...rest}>
  <slot />
</button>
```

**Pattern: Generic component props**

```svelte
<script lang="ts" generics="T extends { id: string; label: string }">
  import type { Snippet } from 'svelte';

  interface Props<T> {
    items: T[];
    selected?: T | null;
    onselect: (item: T) => void;
    children?: Snippet<[item: T]>;
  }

  let { items, selected, onselect, children }: Props<T> = $props();
</script>

{#each items as item (item.id)}
  <button 
    class:selected={selected?.id === item.id}
    onclick={() => onselect(item)}
  >
    {#if children}{@render children(item)}{:else}{item.label}{/if}
  </button>
{/each}
```

**Best practice**: Always use `$props()` to destructure props; it enables Svelte's reactivity tracking.

### $bindable rune: Two-way binding for wrapper components

Enable controlled two-way binding for input wrapper components:

```svelte
<!-- FancyInput.svelte -->
<script lang="ts">
  let { value = $bindable(''), placeholder = '' } = $props();
</script>

<input bind:value {placeholder} />
```

**Usage example:**

```svelte
<script lang="ts">
  let formData = $state({ email: '', password: '' });
</script>

<FancyInput bind:value={formData.email} placeholder="Email" />
<FancyInput bind:value={formData.password} placeholder="Password" />
```

**Caution**: Use `$bindable` sparingly. Prefer one-way data flow with callbacks for most cases:

```svelte
<!-- Better: One-way flow + callbacks -->
<script lang="ts">
  let { value, onchange } = $props();
</script>

<input {value} onchange={(e) => onchange(e.currentTarget.value)} />
```

### $effect rune: Managing side effects

Use `$effect` to automatically run code when state changes:

```svelte
<script lang="ts">
  let count = $state(0);
  let message = $state('');

  // Auto-runs when count changes
  $effect(() => {
    console.log(`Count is now ${count}`);
    document.title = `Count: ${count}`;

    // Cleanup function
    return () => {
      console.log('Cleanup');
    };
  });

  // Run before DOM updates (for scroll positioning, focus, etc)
  $effect.pre(() => {
    if (count > 10) {
      console.log('Count exceeded 10, auto-scrolling...');
    }
  });
</script>
```

**Pattern: API calls and side effects**

```svelte
<script lang="ts">
  let userId = $state(1);
  let user = $state<{ name: string; email: string } | null>(null);
  let loading = $state(false);

  $effect(() => {
    loading = true;
    fetch(`/api/users/${userId}`)
      .then(r => r.json())
      .then(data => {
        user = data;
        loading = false;
      });
  });
</script>

<p>{loading ? 'Loading...' : user?.name}</p>
```

**Best practice**: Use `$effect` for side effects only; prefer `$derived` for computed values.

## Snippets: Type-safe composition

Svelte 5 snippets replace slots with better composition, type safety, and context:

### Basic snippet pattern

```svelte
<!-- Card.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';

  interface Props {
    title: string;
    header?: Snippet;
    footer?: Snippet;
    children?: Snippet;
  }

  let { title, header, footer, children }: Props = $props();
</script>

<div class="card">
  <div class="card-header">
    {#if header}
      {@render header()}
    {:else}
      <h2>{title}</h2>
    {/if}
  </div>

  <div class="card-body">
    {#if children}{@render children()}{/if}
  </div>

  {#if footer}
    <div class="card-footer">
      {@render footer()}
    </div>
  {/if}
</div>
```

**Usage:**

```svelte
<Card title="My Card">
  {#snippet header()}
    <h2>Custom Header</h2>
  {/snippet}

  <p>Card content here</p>

  {#snippet footer()}
    <button>Save</button>
  {/snippet}
</Card>
```

### Snippets with context/parameters

```svelte
<!-- Table.svelte -->
<script lang="ts" generics="T">
  import type { Snippet } from 'svelte';

  interface Props<T> {
    data: T[];
    header: Snippet;
    row: Snippet<[item: T, index: number]>;
    footer?: Snippet<[items: T[]]>;
  }

  let { data, header, row, footer }: Props<T> = $props();
</script>

<table>
  <thead>
    <tr>{@render header()}</tr>
  </thead>
  <tbody>
    {#each data as item, i}
      <tr>{@render row(item, i)}</tr>
    {/each}
  </tbody>
  {#if footer}
    <tfoot>
      <tr>{@render footer(data)}</tr>
    </tfoot>
  {/if}
</table>
```

**Usage with context:**

```svelte
<script lang="ts">
  const users = [
    { id: 1, name: 'Alice', email: 'alice@example.com' },
    { id: 2, name: 'Bob', email: 'bob@example.com' }
  ];
</script>

<Table data={users}>
  {#snippet header()}
    <th>Name</th>
    <th>Email</th>
  {/snippet}

  {#snippet row(user, index)}
    <td>{user.name}</td>
    <td>{user.email}</td>
  {/snippet}

  {#snippet footer(items)}
    <td colspan="2">Total users: {items.length}</td>
  {/snippet}
</Table>
```

### Compound component pattern with snippets

```svelte
<!-- Dialog.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';

  interface Props {
    open: boolean;
    onclose: () => void;
    children?: Snippet;
  }

  let { open, onclose, children }: Props = $props();
</script>

{#if open}
  <div class="dialog-overlay" onclick={onclose}>
    <div class="dialog-content" onclick|stopPropagation>
      {#if children}{@render children()}{/if}
    </div>
  </div>
{/if}

<!-- Dialog.Header.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';

  interface Props {
    children?: Snippet;
  }

  let { children }: Props = $props();
</script>

<div class="dialog-header">
  {#if children}{@render children()}{/if}
</div>
```

**Usage:**

```svelte
<script lang="ts">
  let open = $state(false);
</script>

<button onclick={() => open = true}>Open Dialog</button>

<Dialog {open} onclose={() => open = false}>
  <Dialog.Header>Confirm Action</Dialog.Header>
  <p>Are you sure?</p>
  <button onclick={() => open = false}>Cancel</button>
</Dialog>
```

**Best practice**: Snippets provide type safety and better composition than slots; always use snippets for new Svelte 5 components.

## TypeScript integration and type safety

### Component prop types and exports

```svelte
<!-- Button.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';

  export interface ButtonProps {
    label: string;
    variant?: 'primary' | 'secondary' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    disabled?: boolean;
    onclick?: (e: MouseEvent) => void;
    prefixIcon?: Snippet;
    suffixIcon?: Snippet;
    children?: Snippet;
  }

  let { 
    label,
    variant = 'primary',
    size = 'md',
    disabled = false,
    onclick,
    prefixIcon,
    suffixIcon,
    children,
    ...rest
  }: ButtonProps = $props();
</script>

<button {disabled} {onclick} class={`btn btn-${variant} btn-${size}`} {...rest}>
  {#if prefixIcon}{@render prefixIcon()}{/if}
  {label}
  {#if suffixIcon}{@render suffixIcon()}{/if}
  {#if children}{@render children()}{/if}
</button>
```

### Export component props at library level

```typescript
// src/lib/index.ts
import type { Component, ComponentProps } from 'svelte';
import Button from './components/Button.svelte';

export { Button };

/**
 * Type export for Button component props
 * Usage: import type { ButtonProps } from 'my-lib';
 */
export type ButtonProps = ComponentProps<Button>;
```

### Generic components with TypeScript

```svelte
<script lang="ts" generics="T extends { id: string; label: string }">
  import type { Snippet } from 'svelte';

  interface Props<T> {
    items: T[];
    selected?: T | null;
    onselect: (item: T) => void;
    render?: Snippet<[item: T]>;
  }

  let { items, selected, onselect, render }: Props<T> = $props();
</script>

{#each items as item (item.id)}
  <button 
    class:selected={selected?.id === item.id}
    onclick={() => onselect(item)}
  >
    {#if render}{@render render(item)}{:else}{item.label}{/if}
  </button>
{/each}
```

**Consumer can now use it with strong type inference:**

```svelte
<script lang="ts">
  interface User {
    id: string;
    label: string;
    email: string;
  }

  const users: User[] = [...];
  let selected = $state<User | null>(null);
</script>

<!-- TypeScript knows T = User -->
<Select {items} {selected} onselect={(user) => selected = user} />
```

### Wrapper component typing

```svelte
<!-- StyledInput.svelte -->
<script lang="ts">
  import type { HTMLInputAttributes } from 'svelte/elements';

  interface Props extends HTMLInputAttributes {
    variant?: 'default' | 'error' | 'success';
    label?: string;
  }

  let { variant = 'default', label, ...rest }: Props = $props();
</script>

{#if label}<label>{label}</label>{/if}
<input class={variant} {...rest} />
```

**Best practice**: Always export props interfaces for components; consumers need `ComponentProps<T>` type inference.

## Reusable utilities and hooks

### Hooks via .svelte.ts files

Create reusable reactive utilities in `.svelte.ts` files:

```typescript
// src/lib/utilities/hooks.svelte.ts

/**
 * Create a reactive counter with increment/decrement
 */
export function createCounter(initial = 0) {
  let count = $state(initial);

  return {
    get value() { return count; },
    increment: () => count++,
    decrement: () => count--,
    reset: () => count = initial
  };
}

/**
 * Create reactive form state with validation
 */
export function useForm<T extends Record<string, any>>(
  initialValues: T,
  onsubmit: (values: T) => void | Promise<void>
) {
  let values = $state(initialValues);
  let errors = $state<Record<string, string>>({});
  let isSubmitting = $state(false);

  return {
    get values() { return values; },
    get errors() { return errors; },
    get isSubmitting() { return isSubmitting; },
    
    setValue: (key: keyof T, value: any) => {
      values[key] = value;
      // Clear error for this field
      delete errors[key as string];
    },

    setError: (key: keyof T, error: string) => {
      errors[key as string] = error;
    },

    submit: async () => {
      isSubmitting = true;
      try {
        await onsubmit(values);
      } catch (e) {
        errors['_submit'] = e instanceof Error ? e.message : 'Unknown error';
      } finally {
        isSubmitting = false;
      }
    },

    reset: () => {
      values = { ...initialValues };
      errors = {};
    }
  };
}

/**
 * Create reactive todo list
 */
export function useTodoList(initial: string[] = []) {
  let todos = $state(initial);

  return {
    get items() { return todos; },
    get count() { return todos.length; },
    
    add: (text: string) => {
      if (text.trim()) todos.push(text);
    },

    remove: (index: number) => {
      todos.splice(index, 1);
    },

    clear: () => {
      todos = [];
    }
  };
}
```

**Component usage:**

```svelte
<script lang="ts">
  import { useTodoList, useForm } from '$lib/utilities/hooks.svelte.js';

  const todos = useTodoList(['Learn Svelte 5']);
  const form = useForm({ name: '' }, async (values) => {
    todos.add(values.name);
    form.reset();
  });
</script>

<form onsubmit={form.submit}>
  <input bind:value={form.values.name} placeholder="New todo" />
  <button disabled={form.isSubmitting}>Add</button>
</form>

<ul>
  {#each todos.items as item}
    <li>{item}</li>
  {/each}
</ul>
```

### Pure utility functions

```typescript
// src/lib/utilities/format.ts

/**
 * Format a date in user-friendly way
 */
export function formatDate(date: Date, locale = 'en-US'): string {
  return date.toLocaleDateString(locale);
}

/**
 * Create a debounced function
 */
export function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;

  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
}

/**
 * Combine CSS class names, filtering falsy values
 */
export function cn(...classes: (string | undefined | boolean | null)[]): string {
  return classes.filter(Boolean).join(' ');
}

/**
 * Type-safe localStorage with JSON serialization
 */
export function createStorage<T>(key: string, initial: T) {
  return {
    get: (): T => {
      try {
        const stored = localStorage.getItem(key);
        return stored ? JSON.parse(stored) : initial;
      } catch {
        return initial;
      }
    },

    set: (value: T) => {
      localStorage.setItem(key, JSON.stringify(value));
    },

    clear: () => {
      localStorage.removeItem(key);
    }
  };
}
```

## Testing patterns

### Unit tests with Vitest

```typescript
// src/lib/utilities/__tests__/format.test.ts
import { describe, it, expect } from 'vitest';
import { formatDate, debounce, cn } from '../format.js';

describe('formatDate', () => {
  it('formats date correctly in US locale', () => {
    const date = new Date('2025-01-14');
    expect(formatDate(date, 'en-US')).toBe('1/14/2025');
  });

  it('handles different locales', () => {
    const date = new Date('2025-01-14');
    expect(formatDate(date, 'de-DE')).toBe('14.1.2025');
  });
});

describe('debounce', () => {
  it('delays function execution', async () => {
    const fn = vi.fn();
    const debounced = debounce(fn, 100);

    debounced();
    debounced();
    debounced();

    expect(fn).not.toHaveBeenCalled();

    await new Promise(resolve => setTimeout(resolve, 150));
    expect(fn).toHaveBeenCalledOnce();
  });
});

describe('cn', () => {
  it('combines class names', () => {
    expect(cn('btn', 'btn-primary')).toBe('btn btn-primary');
  });

  it('filters falsy values', () => {
    expect(cn('btn', undefined, false, null, 'active')).toBe('btn active');
  });
});
```

### Component tests with @testing-library/svelte

```typescript
// src/lib/components/__tests__/Button.test.ts
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/svelte';
import userEvent from '@testing-library/user-event';
import Button from '../Button.svelte';

describe('Button', () => {
  it('renders with label', () => {
    render(Button, { props: { label: 'Click me' } });
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });

  it('calls onclick handler when clicked', async () => {
    const user = await userEvent.setup();
    const onclick = vi.fn();

    render(Button, { props: { label: 'Click', onclick } });
    await user.click(screen.getByRole('button'));

    expect(onclick).toHaveBeenCalledOnce();
  });

  it('respects disabled state', () => {
    render(Button, { props: { label: 'Click', disabled: true } });
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('applies variant class', () => {
    const { container } = render(Button, {
      props: { label: 'Click', variant: 'secondary' }
    });
    expect(container.querySelector('.btn-secondary')).toBeInTheDocument();
  });
});
```

### Testing reactive state

```typescript
// src/lib/utilities/__tests__/hooks.test.ts
import { describe, it, expect } from 'vitest';
import { useTodoList, useForm } from '../hooks.svelte.js';

describe('useTodoList', () => {
  it('initializes with items', () => {
    const todos = useTodoList(['Learn Svelte 5', 'Build components']);
    expect(todos.count).toBe(2);
    expect(todos.items).toEqual(['Learn Svelte 5', 'Build components']);
  });

  it('adds items', () => {
    const todos = useTodoList();
    todos.add('New task');
    expect(todos.count).toBe(1);
    expect(todos.items[0]).toBe('New task');
  });

  it('removes items by index', () => {
    const todos = useTodoList(['Task 1', 'Task 2']);
    todos.remove(0);
    expect(todos.count).toBe(1);
    expect(todos.items[0]).toBe('Task 2');
  });

  it('clears all items', () => {
    const todos = useTodoList(['Task 1', 'Task 2']);
    todos.clear();
    expect(todos.count).toBe(0);
  });
});

describe('useForm', () => {
  it('tracks form state', () => {
    const form = useForm({ name: '', email: '' }, async () => {});
    form.setValue('name', 'Alice');
    expect(form.values.name).toBe('Alice');
  });

  it('handles submission', async () => {
    const onsubmit = vi.fn();
    const form = useForm({ name: 'Alice' }, onsubmit);

    await form.submit();
    expect(onsubmit).toHaveBeenCalledWith({ name: 'Alice' });
  });

  it('sets and clears errors', () => {
    const form = useForm({ name: '' }, async () => {});
    form.setError('name', 'Name is required');
    expect(form.errors.name).toBe('Name is required');

    form.setValue('name', 'Alice');
    expect(form.errors.name).toBeUndefined();
  });
});
```

## Export and distribution

### Strategic export configuration

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "svelte": "./dist/index.js",
      "default": "./dist/index.js"
    },
    "./components": {
      "types": "./dist/components/index.d.ts",
      "svelte": "./dist/components/index.js"
    },
    "./Button": {
      "types": "./dist/Button.svelte.d.ts",
      "svelte": "./dist/Button.svelte"
    },
    "./utilities": {
      "types": "./dist/utilities/index.d.ts",
      "default": "./dist/utilities/index.js"
    }
  }
}
```

### Main entry point exports

```typescript
// src/lib/index.ts
// Re-export all public components and utilities

// Components
export { default as Button } from './components/Button.svelte';
export { default as Card } from './components/Card.svelte';
export { default as Dialog } from './components/Dialog.svelte';

// Types
export type { ButtonProps } from './components/Button.svelte';
export type { CardProps } from './components/Card.svelte';

// Utilities
export { formatDate, debounce, cn, createStorage } from './utilities/format.js';
export { useTodoList, useForm, createCounter } from './utilities/hooks.svelte.js';

// Re-export types for convenience
export type { Snippet } from 'svelte';
```

### Granular exports for tree-shaking

```typescript
// src/lib/utilities/index.ts
// Export individual utilities to enable tree-shaking
export { formatDate } from './format.js';
export { debounce } from './format.js';
export { cn } from './format.js';

// Only import what you need
// import { cn } from '@my-lib/utilities';
```

**Tree-shaking considerations:**
- Use granular exports (one function per file if heavily used)
- Avoid circular dependencies
- Mark CSS as `sideEffects: ["**/*.css"]` so it's preserved

## Performance optimization

### Use $derived.by for expensive computations

```svelte
<script lang="ts">
  let items = $state<{ id: number; active: boolean }[]>([]);

  // ✅ Good: Caches result, recomputes only when items changes
  let activeItems = $derived.by(() => {
    return items
      .filter(i => i.active)
      .map(i => ({ ...i, processed: true, timestamp: Date.now() }));
  });

  // ❌ Avoid: Expensive operations inline
  // let activeItems = $derived(items.filter(...).map(...))
</script>
```

### Use $state.raw for non-mutated state

```svelte
<script lang="ts">
  // ❌ Creates proxy overhead for large objects
  let config = $state({
    theme: 'dark',
    locale: 'en',
    // ... many more properties
  });

  // ✅ No proxy overhead; must reassign instead of mutate
  let config = $state.raw({
    theme: 'dark',
    locale: 'en'
  });

  function updateTheme(newTheme: string) {
    config = { ...config, theme: newTheme };
  }
</script>
```

### Lazy loading heavy components

```svelte
<script lang="ts">
  import { mount } from 'svelte';
  
  let showHeavy = $state(false);
  let HeavyComponent: any;

  function toggleHeavy() {
    showHeavy = !showHeavy;
  }

  $effect(() => {
    if (showHeavy) {
      import('./HeavyComponent.svelte').then(mod => {
        HeavyComponent = mod.default;
      });
    }
  });
</script>

<button onclick={toggleHeavy}>Toggle heavy component</button>

{#if HeavyComponent && showHeavy}
  <svelte:component this={HeavyComponent} />
{/if}
```

### Optimize rendering with #key blocks

```svelte
<script lang="ts">
  let selectedId = $state(1);
</script>

<!-- Force component recreation when selectedId changes -->
{#key selectedId}
  <UserDetail userId={selectedId} />
{/key}
```

### Bundle size optimization with sideEffects

```json
{
  "sideEffects": [
    "**/*.css",
    "**/*.svelte"
  ],
  "exports": {
    ".": {
      "svelte": "./dist/index.js"
    }
  }
}
```

**Best practice**: Use selective imports; consumers should only bundle what they use.

## Documentation and developer experience

### Component JSDoc comments

```svelte
<!--
  @component
  A reusable Button component with multiple variants and sizes.

  Features:
  - Type-safe props with full TypeScript support
  - Flexible rendering with snippet props
  - Accessibility built-in (aria attributes)

  @example
  ```svelte
  <Button label="Submit" variant="primary" onclick={handleSubmit} />
  ```

  @example
  ```svelte
  <Button variant="outline" size="lg" disabled={isLoading}>
    {#snippet prefixIcon()}
      <Icon name="save" />
    {/snippet}
    Save Changes
  </Button>
  ```
-->
<script lang="ts">
  // ...
</script>
```

### Library README template

```markdown
# Component Library

Production-grade Svelte 5 component library with runes, TypeScript, and snippets.

## Installation

\`\`\`bash
npm install @your-org/components
\`\`\`

## Quick start

\`\`\`svelte
<script>
  import { Button, Card } from '@your-org/components';
</script>

<Button label="Click me" onclick={() => alert('Clicked!')} />

<Card title="Welcome">
  <p>This is a card component.</p>
</Card>
\`\`\`

## Features

- ✅ Full TypeScript support with component prop types
- ✅ Svelte 5 runes: \`$state\`, \`$derived\`, \`$props\`, \`$bindable\`, \`$effect\`
- ✅ Type-safe composition with snippets
- ✅ Comprehensive testing with Vitest
- ✅ Tree-shakeable exports
- ✅ Production-ready performance

## Components

- [Button](#button) - CTA with variants and sizes
- [Card](#card) - Container with header/footer
- [Dialog](#dialog) - Modal component

### Button

\`\`\`svelte
<Button 
  label="Save"
  variant="primary"
  size="lg"
  onclick={handleSave}
/>
\`\`\`

Props: See [ButtonProps](./src/lib/components/Button.svelte)

## TypeScript support

Full types are included:

\`\`\`typescript
import type { ButtonProps } from '@your-org/components';

const buttonProps: ButtonProps = {
  label: 'Click me',
  variant: 'primary'
};
\`\`\`
```

## Common patterns reference

| Pattern | Use Case | Example |
|---------|----------|---------|
| Snippet composition | Flexible rendering | Card, Dialog, Table |
| $state hooks | Shared component logic | useForm, useTodoList |
| $derived | Computed values | Filtered lists, status text |
| $bindable | Controlled form inputs | Input, Textarea wrappers |
| Context | Theme, locale settings | ThemeProvider, I18n |
| .svelte.ts utilities | Reactive utilities | formatters, validators |

## Guidelines for new contributors

- Use `$props()` for all component props (mandatory for reactivity)
- Prefer `$derived` for computed values over `$effect`
- Use snippets, not slots, for composition
- Export prop interfaces from components
- Write tests for utilities and reactive hooks
- Keep components focused (single responsibility)
- Document props with JSDoc comments

## References

- [Svelte 5 Docs](https://svelte.dev/docs/svelte)
- [Runes Guide](https://svelte.dev/docs/svelte/what-are-runes)
- [Snippets](https://svelte.dev/docs/svelte/snippet)
- [SvelteKit Packaging](https://svelte.dev/docs/kit/packaging)
```

## Key mistakes to avoid

| Mistake | Impact | Solution |
|---------|--------|----------|
| Using legacy reactive declarations | Components don't track state properly | Migrate to `$state`, `$derived`, `$props` runes |
| Not destructuring with `$props()` | Reactive tracking fails; component bloats | Always use `let { ...} = $props()` |
| Using slots instead of snippets | Type safety lost, composition inflexible | Replace slots with `Snippet<[context]>` props |
| Weak TypeScript integration | IDE autocompletion fails, type errors at runtime | Export `ComponentProps<T>` for all components |
| Deep nesting without `$derived.by` | Expensive recomputes on every render | Use `$derived.by()` for complex derived state |
| Circular dependencies between modules | Tree-shaking breaks, bundle bloats | Organize exports to prevent circular imports |
| Not testing reactive utilities | Logic bugs slip to production | Test hooks and `$state` patterns with Vitest |
| Exposing internal state in exports | API surface changes break consumers | Only export public interfaces and utilities |

## References and resources

**Official Svelte 5 Documentation**
- [Runes Overview](https://svelte.dev/docs/svelte/what-are-runes) - Foundation for modern Svelte
- [$state Rune](https://svelte.dev/docs/svelte/$state) - Reactive state management
- [$props Rune](https://svelte.dev/docs/svelte/$props) - Type-safe component props
- [$derived Rune](https://svelte.dev/docs/svelte/$derived) - Computed reactive values
- [Snippets](https://svelte.dev/docs/svelte/snippet) - Modern composition
- [TypeScript Guide](https://svelte.dev/docs/svelte/typescript) - Full type safety
- [Testing Guide](https://svelte.dev/docs/svelte/testing) - Test infrastructure
- [SvelteKit Packaging](https://svelte.dev/docs/kit/packaging) - Library distribution

**Related skills**
- **svelte5-development**: General Svelte 5 component development and runes
- **software-architecture**: Principles for library design and component organization
- **context-engineering**: Prompt optimization for documentation and examples
