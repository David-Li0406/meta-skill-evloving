---
name: benchmark-test-suite
description: Use this skill when adding a new benchmark view/test suite or when running benchmark UI tests and displaying their results.
---

# Benchmark Test Suite

## When to Use

- Adding a new benchmark view/test suite (like `datatable` or `pokeboxes`)
- Extending the Playwright runner with new view operations
- Making UI test results show up in the snapshot UI

## Workflow

1. **Define the view id and ready selector**
   - Pick a lowercase `view` id (used in `?view=`).
   - Decide the first stable selector that signals the view is ready.

2. **Add the blueprint markup**
   - Create `src/core/blueprint-<view>.html`.
   - The initial DOM must match every framework’s initial render (preflight compares against it).
   - Reuse the view toggle markup and IDs used by existing blueprints.

3. **Update the benchmark runner**
   - Add the view id to `OperationView`, `AVAILABLE_VIEWS`, and `BLUEPRINTS`.
   - Add a `resolveViewReadySelector` branch for the new view.
   - Add new `Operation` entries that set `view: '<view>'` and `readySelector`.

4. **Add shared operations/data helpers**
   - Add new helpers in `src/core/helpers-<view>.ts`.
   - Add matching types in `src/core/types.ts`.
   - Export the new helpers from `src/core/index.ts`.

5. **Update framework implementations**
   - Each framework must render the same initial markup as the blueprint for the new view.
   - Parse `?view=` and render the correct view.
   - Add view toggle buttons and ensure they link to the correct `view` query param.
   - Use design system classes from `src/design-system.css` (max 3 classes per element).

6. **Expose the suite in results UI**
   - Add human-friendly labels for new operations in `src/pages/results/index.vani.tsx`.
   - Add the new view to `suiteOrder` and `suiteTitles`.

7. **Run UI tests and generate results**
   - Run the runner with preflight to validate markup and measure timings.
   - Open the snapshot UI to verify the new suite is visible.

## Templates

### `src/runner.ts` additions

```ts
// 1) View type + constants
type OperationView = 'datatable' | 'pokeboxes' | '<view>'

const BLUEPRINTS = {
  datatable: path.join(import.meta.dirname, 'src/core/blueprint-datatable.html'),
  pokeboxes: path.join(import.meta.dirname, 'src/core/blueprint-pokeboxes.html'),
  <view>: path.join(import.meta.dirname, 'src/core/blueprint-<view>.html'),
}

const AVAILABLE_VIEWS: OperationView[] = ['datatable', 'pokeboxes', '<view>']

function resolveViewReadySelector(view: OperationView): string {
  if (view === 'pokeboxes') return '#append40'
  if (view === '<view>') return '#<ready-id>'
  return '#run'
}

// 2) New operations
const operations: Operation[] = [
  // ...
  {
    name: '<operationName>',
    view: '<view>',
    readySelector: '#<ready-id>',
    setup: (page) => /* optional */,
    action: (page) => clickAndMeasure(page, '#<action-id>', '<operationName>'),
    teardown: (page) => /* optional */,
  },
]
```

### `src/core/blueprint-<view>.html`

```html
<!-- Match initial DOM for *all* frameworks -->
<div class="bench-view-toggle" id="view-toggle">
  <!-- include one button per view (datatable/pokeboxes/<view>) -->
</div>

<!-- New view DOM should be here with stable IDs -->
```

### `src/core/helpers-<view>.ts` + `src/core/types.ts`

```ts
// helpers-<view>.ts (helpers used by all frameworks)
export function build<Thing>(/* params */) {
  // deterministic data helpers for the new view
}

export function <operationHelper>(/* params */) {
  // pure data operation (no DOM)
}
```

```ts
// types.ts (types + function declarations)
export type <Thing> = {
  // ...
}
```

### Framework view routing (each `frameworks/*/index.ts[x]|index.js`)

```ts
const resolveView = () => {
  const params = new URLSearchParams(window.location.search)
  return params.get('view') === '<view>' ? '<view>' : 'datatable'
}

const navigateToView = (view: string) => {
  const url = new URL(window.location.href)
  url.searchParams.set('view', view)
  window.location.href = url.toString()
}

// Render toggle buttons + new view
```

### `src/pages/results/index.vani.tsx` updates

```ts
const OPERATION_LABELS = {
  // ...
  <operationName>: {
    title: '<human title>',
    description: '<what it measures>',
  },
}

let suiteOrder = ['datatable', 'pokeboxes', '<view>']
let suiteTitles: Record<string, string> = {
  datatable: 'Data Table Benchmarks',
  pokeboxes: 'Pokeboxes Benchmarks',
  <view>: '<View Title>',
}
```

## Commands

- Run the full benchmark suite:
  - `pnpm run bench`
- Run only the new view:
  - `pnpm run bench -- --view <view>`
- Validate markup only (preflight):
  - `pnpm run bench -- --preflight-only --view <view>`
- View results UI:
  - `pnpm run dev` → open `http://localhost:4555/results`

## Notes

- Preflight DOM checks compare each framework against the blueprint for every view.
- If you add new helpers or data shapes, update `src/core/helpers-<view>.ts`, `src/core/types.ts`,
  and export them from `src/core/index.ts`.
- Keep button IDs and aria attributes aligned across all frameworks and blueprints.