---
name: pnpm-monorepo-workflows
description: Use this when installing dependencies, running dev servers, building packages, or running scripts in this pnpm monorepo.
---

# pnpm monorepo workflows (Cloudflare Workers SaaS kit)

Use this skill whenever the user asks to set up the repo, run dev servers, rebuild shared packages, or troubleshoot script execution.

## Key packages

- `apps/user-application`: TanStack Start (SSR) app running on Cloudflare Workers
- `apps/data-service`: Backend API Worker (Hono)
- `packages/data-ops`: Shared library for Drizzle ORM + Better Auth

## Setup

- Initial setup (install + build shared lib): `pnpm run setup`

## Dev servers

- User app dev: `pnpm run dev:user-application` (typically on port 3000)
- Data service dev: `pnpm run dev:data-service`

## Shared package builds

- Rebuild shared library after changes: `pnpm run build:data-ops`

## Script hygiene

- Use `pnpm -w ...` only if a script is defined at workspace root.
- Prefer package-scoped scripts:
  - `pnpm --filter data-ops <script>`
  - `pnpm --filter user-application <script>`
  - `pnpm --filter data-service <script>`

## Linting & typechecking

- Lint UI package: `pnpm --filter @workspace/ui lint`
- Typecheck a single package/app (recommended when debugging TS issues):
  - `pnpm -C apps/user-application tsc --noEmit`
  - `pnpm -C apps/data-service tsc --noEmit`
  - `pnpm -C packages/data-ops tsc --noEmit`
  - `pnpm -C packages/ui tsc --noEmit`

## Troubleshooting quick checks

- Ensure `pnpm-lock.yaml` is consistent (avoid mixing npm/yarn).
- If types/bindings changed, regenerate worker types (see the worker typegen skill).
- If `packages/data-ops` changed and consumers are broken, run `pnpm run build:data-ops` and restart dev servers.
