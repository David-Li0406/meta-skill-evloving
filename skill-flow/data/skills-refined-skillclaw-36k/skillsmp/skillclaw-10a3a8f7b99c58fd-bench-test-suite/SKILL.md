---
name: bench-test-suite
description: Use this skill when adding a new benchmark view/test suite or when running benchmark UI tests and displaying their results.
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
```