# XState (@xstate/svelte)

Full-featured statecharts: actors, parallel states, visual editor (Stately).

## Basic Usage

```svelte
<script>
  import { useMachine } from '@xstate/svelte';
  import { createMachine, assign } from 'xstate';

  const toggleMachine = createMachine({
    id: 'toggle',
    initial: 'inactive',
    context: { count: 0 },
    states: {
      inactive: {
        on: { TOGGLE: 'active' }
      },
      active: {
        entry: assign({ count: ({ context }) => context.count + 1 }),
        on: { TOGGLE: 'inactive' }
      }
    }
  });

  const { state, send } = useMachine(toggleMachine);
</script>

<button onclick={() => send({ type: 'TOGGLE' })}>
  {$state.value} (count: {$state.context.count})
</button>
```

## Async Actions

```ts
import { createMachine, assign, fromPromise } from "xstate";

const fetchMachine = createMachine(
  {
    id: "fetch",
    initial: "idle",
    context: { data: null, error: null },
    states: {
      idle: {
        on: { FETCH: "loading" },
      },
      loading: {
        invoke: {
          src: "fetchData",
          onDone: {
            target: "success",
            actions: assign({ data: ({ event }) => event.output }),
          },
          onError: {
            target: "error",
            actions: assign({ error: ({ event }) => event.error }),
          },
        },
      },
      success: { on: { FETCH: "loading" } },
      error: { on: { FETCH: "loading" } },
    },
  },
  {
    actors: {
      fetchData: fromPromise(async () => {
        const res = await fetch("/api/data");
        return res.json();
      }),
    },
  },
);
```

## Parallel States

```ts
const editorMachine = createMachine({
  id: "editor",
  type: "parallel",
  states: {
    bold: {
      initial: "off",
      states: {
        off: { on: { TOGGLE_BOLD: "on" } },
        on: { on: { TOGGLE_BOLD: "off" } },
      },
    },
    italic: {
      initial: "off",
      states: {
        off: { on: { TOGGLE_ITALIC: "on" } },
        on: { on: { TOGGLE_ITALIC: "off" } },
      },
    },
  },
});
```

## When to Use

- Complex flows with nested/parallel states
- Need visual state editor (Stately)
- Actor model for spawning child machines
- Large teams benefiting from formal statecharts
