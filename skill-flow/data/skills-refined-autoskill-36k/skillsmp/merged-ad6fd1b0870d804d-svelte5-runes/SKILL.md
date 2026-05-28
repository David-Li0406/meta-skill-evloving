---
name: svelte5-runes
description: Use this skill for guidance on Svelte 5 runes, including reactive state, props, effects, and migration from Svelte 4.
---

# Svelte 5 Runes

## Quick Start

**Which rune?** Props: `$props()` | Bindable: `$bindable()` | Computed: `$derived()` | Side effect: `$effect()` | State: `$state()`

**Key rules:** Runes are top-level only. `$derived` can be overridden (use `const` for read-only). Avoid mixing Svelte 4/5 syntax. Objects and arrays are deeply reactive by default.

## Example

```svelte
<script>
	let count = $state(0); // Mutable state
	const doubled = $derived(count * 2); // Computed (const = read-only)

	$effect(() => {
		console.log(`Count is ${count}`); // Side effect
	});
</script>

<button onclick={() => count++}>
	{count} (doubled: {doubled})
</button>
```

## Svelte 4 → Svelte 5 Migration

| Svelte 4 ❌                    | Svelte 5 ✅                                            |
| ------------------------------ | ------------------------------------------------------ |
| `export let foo`               | `let { foo } = $props()`                               |
| `export let foo = 'default'`   | `let { foo = 'default' } = $props()`                   |
| `$: doubled = x * 2`           | `let doubled = $derived(x * 2)`                        |
| `$: { sideEffect() }`          | `$effect(() => { sideEffect() })`                      |
| `on:click={handler}`           | `onclick={handler}`                                    |
| `on:input={handler}`           | `oninput={handler}`                                    |
| `on:click|preventDefault={h}` | `onclick={e => { e.preventDefault(); h(e) }}`          |
| `<slot />`                     | `{@render children()}`                                 |
| `<slot name="x" />`            | `{@render x?.()}`                                      |
| `$$props`                      | Use `$props()` with rest: `let { ...rest } = $props()` |
| `$$restProps`                  | `let { known, ...rest } = $props()`                    |
| `createEventDispatcher()`      | Pass callback props: `let { onchange } = $props()`     |

## Notes

- Use `onclick` instead of `on:click` in Svelte 5.
- Use `{@render children()}` in layouts.
- Check Svelte version before suggesting syntax.
- **Svelte 5.25+ breaking change:** `$derived` can now be reassigned (use `const` for read-only).
- **Last verified:** 2025-01-11

## Reference Files

- [reactivity-patterns.md](references/reactivity-patterns.md) - When to use each rune
- [migration-gotchas.md](references/migration-gotchas.md) - Svelte 4 → 5 translation
- [component-api.md](references/component-api.md) - $props, $bindable patterns
- [snippets-vs-slots.md](references/snippets-vs-slots.md) - New snippet syntax
- [common-mistakes.md](references/common-mistakes.md) - Anti-patterns with fixes