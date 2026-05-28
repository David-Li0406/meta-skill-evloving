---
name: shadcn-ui-builder
description: Use this when adding/updating shadcn/ui components or blocks in this monorepo (Tailwind v4, shared UI package, CSS variable theming).
---

# shadcn/ui builder (monorepo + Tailwind v4)

Use this skill when you need to add or update UI components/blocks via the shadcn CLI, or when refactoring UI to follow the repo’s conventions.

## Hard rules (this repo)

- Don’t hardcode Tailwind palette colors. Use semantic tokens like `bg-background`, `text-foreground`, `border-border`, etc.
- Prefer shared components from `@workspace/ui/*`.
- Keep filenames kebab-case.

## Where components live

- Shared UI components: `packages/ui/src/components/*` (import as `@workspace/ui/components/<name>`)
- Shared UI styles: `packages/ui/src/styles/globals.css`
- App-specific composition/components: `apps/user-application/src/components/*`

## shadcn CLI (latest)

The shadcn CLI supports monorepos. In this repo, each workspace has a `components.json` that tells the CLI where to write files.

### Inspect registry items before adding

- View an item: `pnpm dlx shadcn@latest view button`
- Search/list items: `pnpm dlx shadcn@latest search @shadcn -q "dialog"`

### Add components (recommended)

Run from the app workspace so the CLI can resolve monorepo paths correctly:

- From repo root: `pnpm dlx shadcn@latest add button --cwd apps/user-application`
- Or cd first: `cd apps/user-application && pnpm dlx shadcn@latest add button`

Notes:
- Adding a “block” (e.g. `login-01`) may install primitives into `packages/ui` and the composed block into the app.
- If you need to control where files land, use `--path` (and prefer app-level composition in `apps/user-application/src/components`).

### Updating existing components

Shadcn recommends re-adding components to pick up upstream improvements. This overwrites local modifications.

- Commit first.
- Then (example): `pnpm dlx shadcn@latest add --all --overwrite --cwd apps/user-application`

## Tailwind v4 + React 19 notes (upstream)

- Tailwind v4 shadcn components use CSS variables and `@theme inline` patterns.
- Many components removed `forwardRef` and added `data-slot` attributes for styling.
- `toast` is deprecated upstream in favor of `sonner`.

## Quick repo sanity checks after UI changes

- Lint UI package: `pnpm --filter @workspace/ui lint`
- Typecheck user app: `pnpm -C apps/user-application tsc --noEmit`
- Typecheck UI package: `pnpm -C packages/ui tsc --noEmit`
