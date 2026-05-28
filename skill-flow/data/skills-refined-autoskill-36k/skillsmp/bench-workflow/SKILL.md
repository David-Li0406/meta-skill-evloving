---
name: bench-workflow
description: Configure, author, and run benchmark implementations in this repo.
---

# Bench Workflow

## When to Use

- Adding a new framework implementation under `frameworks/`
- Wiring a framework into the shared Vite setup
- Adding or updating manual UI tests in `src/pages`
- Running or validating benchmark results

## Steps

1. **Add or update a framework implementation**
   - Create `frameworks/<id>/index.html` that imports `../../src/styles.css` and uses the
     `.bench-shell` body class.
   - Add `index.ts` and `app.<suffix>` with the framework-specific entry.
   - Keep initial DOM aligned to the blueprint markup.

2. **Wire up configuration**
   - Register the framework in `package.json` under `benchmarks.frameworks`.
   - Add the framework to `plugins/vite-plugin-multi-framework.ts` and the `frameworks` list in
     `vite.config.ts`.
   - Add a `tsconfigs/tsconfig.<id>.json` and include it in `tsconfig.json` references.

3. **Apply design system rules**
   - Prefer `src/design-system.css` classes for UI.
   - Use at most 3 classes per element; add a new component class if you need more.

4. **Add or update manual UI tests**
   - Create a new directory under `src/pages/manual-tests/<test>/`.
   - Add the test to the homepage list in `src/pages/index.ts`.

5. **Run and verify**
   - `pnpm run dev` for local UI checks.
   - `pnpm run bench` to run the benchmark runner.

## Output

Provide:

- The files created or updated
- Any new framework IDs or view names
- Commands to run for verification

## Present Results to User

Give a concise bullet list of changes, then a short test plan.
