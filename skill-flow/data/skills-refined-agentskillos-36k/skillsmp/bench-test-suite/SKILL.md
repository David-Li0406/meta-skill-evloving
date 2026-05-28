---
name: bench-test-suite
description:
  Adds a new benchmark view/test suite under bench/, updates the runner, blueprints, framework
  views, and snapshot UI. Use when adding a new benchmark view/test suite or when running benchmark
  UI tests and displaying their results.
---

# Bench Test Suite

## When to Use

- Adding a new benchmark view/test suite (like `datatable` or `pokeboxes`)
- Extending the Playwright runner with new view operations
- Making UI test results show up in the snapshot UI

## Workflow

1. **Define the view id and ready selector**
   - Pick a lowercase `view` id (used in `?view=`).
   - Decide the first stable selector that signals the view is ready.

2. **Add the blueprint markup**
   - Create `bench/frameworks/blueprint-<view>.html`.
   - The initial DOM must match every framework’s initial render (preflight compares against it).
   - Reuse the view toggle markup and IDs used by existing blueprints.

3. **Update the benchmark runner**
   - Add the view id to `OperationView`, `AVAILABLE_VIEWS`, and `BLUEPRINTS`.
   - Add a `resolveViewReadySelector` branch for the new view.
   - Add new `Operation` entries that set `view: '<view>'` and `readySelector`.

4. **Add shared operations/data helpers**
   - Add new helpers in `bench/frameworks/shared.js`.
   - Add matching types and exports in `bench/frameworks/shared.d.ts`.

5. **Update framework implementations**
   - Each framework must render the same initial markup as the blueprint for the new view.
   - Parse `?view=` and render the correct view.
   - Add view toggle buttons and ensure they link to the correct `view` query param.

6. **Expose the suite in results UI**
   - Add human-friendly labels for new operations in `bench/snapshot/index.ts`.
   - Add the new view to `suiteOrder` and `suiteTitles`.

7. **Run UI tests and generate results**
   - Run the runner with preflight to validate markup and measure timings.
   - Open the snapshot UI to verify the new suite is visible.

## Templates

### `bench/runner.ts` additions

```ts
// 1) View type + constants
type OperationView = 'datatable' | 'pokeboxes' | '<view>'

const BLUEPRINTS = {
  datatable: path.join(import.meta.dirname, 'frameworks/blueprint-datatable.html'),
  pokeboxes: path.join(import.meta.dirname, 'frameworks/blueprint-pokeboxes.html'),
  <view>: path.join(import.meta.dirname, 'frameworks/blueprint-<view>.html'),
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

### `bench/frameworks/blueprint-<view>.html`

```html
<!-- Match initial DOM for *all* frameworks -->
<div class="bench-view-toggle" id="view-toggle">
  <!-- include one button per view (datatable/pokeboxes/<view>) -->
</div>

<!-- New view DOM should be here with stable IDs -->
```

### `bench/frameworks/shared.js` + `bench/frameworks/shared.d.ts`

```js
// shared.js (helpers used by all frameworks)
export function build<Thing>(/* params */) {
  // deterministic data helpers for the new view
}

export function <operationHelper>(/* params */) {
  // pure data operation (no DOM)
}
```

```ts
// shared.d.ts (types + function declarations)
export type <Thing> = {
  // ...
}

export declare function build<Thing>(/* params */): <Thing>[]
export declare function <operationHelper>(/* params */): <Thing>[]
```

### Framework view routing (each `bench/frameworks/*/index.ts[x]|index.js`)

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

### `bench/snapshot/index.ts` updates

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
  datatable: 'Data Table',
  pokeboxes: 'Pokeboxes',
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
  - `pnpm run bench:dev` → open `http://localhost:4555/snapshot`

## Notes

- Preflight DOM checks compare each framework against the blueprint for every view.
- If you add new helpers or data shapes, update `bench/frameworks/shared.js` and
  `bench/frameworks/shared.d.ts`.
- Keep button IDs and aria attributes aligned across all frameworks and blueprints.
