---
name: bun-monorepo-workflows
description: Use this when installing dependencies, running scripts, filtering packages, or migrating this monorepo from pnpm to Bun (bun.lock, workspaces, bun ci) while keeping Cloudflare Workers + Wrangler workflows working.
---

# Bun monorepo workflows (Cloudflare Workers SaaS kit)

This repo is currently pnpm-based, but Bun can act as the package manager for the monorepo.
This skill covers (1) day-to-day Bun equivalents for pnpm workflows and (2) a safe pnpm → Bun migration checklist.

## Quick commands (Bun)

- Install all deps: `bun install`
- CI install (frozen lockfile): `bun ci` (equivalent to `bun install --frozen-lockfile`)
- Run a root script: `bun run <script>`
- Run a workspace script (common patterns):
  - By filter: `bun --filter <workspace-name-or-glob> run <script>`
  - By path filter: `bun --filter ./apps/user-application run build`
- Add deps:
  - Prod: `bun add <pkg>`
  - Dev: `bun add -d <pkg>`
- List deps: `bun pm ls` (or `bun list`)
- Lockfile / migration utilities: `bun pm migrate`

## Filtering and “package scoping”

Bun’s primary mechanism is `--filter`.

Examples:

- Install everything except one workspace: `bun install --filter '!data-service'`
- Install only one workspace (by path): `bun install --filter './apps/user-application'`
- Run TS typecheck in just UI: `bun --filter @workspace/ui run tsc`

Notes:

- Bun supports workspace globs and negative patterns.
- Prefer filtering by path when package names aren’t unique or you’re unsure of the workspace name.

## Cloudflare/Wrangler note (important)

This repo uses Cloudflare Workers tooling (Wrangler, workerd). Bun is fine as a *package manager*, but Wrangler is not universally supported when *executed via Bun’s runtime*.

Practical guidance:

- Prefer `bun run <script>` without forcing Bun’s runtime.
- Bun’s `bun run` respects `#!/usr/bin/env node` shebangs by default, so CLIs like `wrangler` usually run on your system Node.
- If you hit Wrangler weirdness under Bun, run Wrangler directly with Node (or via the existing pnpm workflow) rather than forcing `bun --bun`.

## pnpm → Bun migration checklist (safe)

Bun will automatically migrate `pnpm-lock.yaml` to `bun.lock` when you run `bun install` **and no `bun.lock` exists yet**.

Recommended sequence:

1. Clean install state
   - Remove `node_modules` (and workspace node_modules if present).
2. Generate Bun lockfile
   - Run `bun install` at repo root.
   - Verify it produced `bun.lock`.
3. Verify key workflows still work
   - Run the same “known good” scripts you currently use for CI/dev (build + typecheck for each app/package).
   - Pay special attention to:
     - `packages/data-ops` build
     - app typechecks
     - Wrangler/dev scripts
4. Commit lockfile + any required config changes
   - Bun docs recommend committing `bun.lock`.
5. Optional: remove pnpm artifacts after verification
   - After you’re confident, remove `pnpm-lock.yaml` and `pnpm-workspace.yaml`.
   - If you keep pnpm around temporarily, do not mix installs (avoid generating both lockfiles in CI).

Bun-specific notes that matter during migration:

- Bun v1.2+ defaults to the text lockfile `bun.lock` (older versions used `bun.lockb`).
- Bun does not run dependency lifecycle scripts by default; if a dependency *requires* scripts, add it to `trustedDependencies` in the relevant `package.json`, then reinstall.

## What to update in repo configs (typical)

When the actual migration happens (if/when you switch the repo’s canonical PM):

- Root `package.json`:
  - Consider setting `packageManager` to `bun@<version>` to signal the expected tool.
  - Ensure `workspaces` config exists (Bun supports `workspaces` and will migrate from `pnpm-workspace.yaml` automatically).
- CI:
  - Replace `pnpm install` with `bun ci`.
  - Use `oven-sh/setup-bun` GitHub Action.

## References

- Command mapping + “pnpm filter” equivalents: see `.github/skills/bun-monorepo-workflows/references/command-mapping.md`
- Migration gotchas + verification checklist: see `.github/skills/bun-monorepo-workflows/references/migration-notes.md`
