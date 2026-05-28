# Robot3

Lightweight (1kb) functional FSM. Simpler API than XState.

## Basic Usage

```ts
import { createMachine, state, transition } from "robot3";

const toggleMachine = createMachine({
  inactive: state(transition("toggle", "active")),
  active: state(transition("toggle", "inactive")),
});
```

## Async Actions

```ts
import { createMachine, state, transition, invoke, reduce } from "robot3";

const fetchMachine = createMachine({
  idle: state(transition("fetch", "loading")),
  loading: invoke(
    () => fetch("/api/data").then((r) => r.json()),
    transition(
      "done",
      "success",
      reduce((ctx, ev) => ({ ...ctx, data: ev.data })),
    ),
    transition("error", "error"),
  ),
  success: state(),
  error: state(transition("retry", "loading")),
});
```

## Svelte 5 Integration

```ts
// $lib/useMachine.svelte.ts
import { interpret } from "robot3";

export function useMachine<T>(machine: T, initialContext = {}) {
  let current = $state(machine.current);
  let context = $state(initialContext);

  const service = interpret(
    machine,
    (service) => {
      current = service.machine.current;
      context = service.context;
    },
    initialContext,
  );

  return {
    get current() {
      return current;
    },
    get context() {
      return context;
    },
    send: service.send,
  };
}
```

```svelte
<script>
  import { useMachine } from '$lib/useMachine.svelte';
  import { fetchMachine } from './machines';

  const { current, context, send } = useMachine(fetchMachine);
</script>

<p>State: {current}</p>
{#if current === 'idle'}
  <button onclick={() => send('fetch')}>Fetch</button>
{:else if current === 'loading'}
  <p>Loading...</p>
{:else if current === 'success'}
  <pre>{JSON.stringify(context.data)}</pre>
{:else if current === 'error'}
  <button onclick={() => send('retry')}>Retry</button>
{/if}
```

## When to Use

- Simple state machines
- Bundle size matters (1kb vs 13kb)
- Prefer functional composition
- Quick prototyping
