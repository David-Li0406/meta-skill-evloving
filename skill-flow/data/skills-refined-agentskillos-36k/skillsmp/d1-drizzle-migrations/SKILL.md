---
name: d1-drizzle-migrations
description: Use this when changing the database schema, generating/applying Drizzle migrations for Cloudflare D1 (SQLite), or working with Better Auth schema generation.
---

# Cloudflare D1 + Drizzle migrations (via packages/data-ops)

Use this skill when the user asks to add or modify tables, regenerate auth schema, generate migration SQL, or apply migrations locally/remote.

## Hard rules (architecture)

- Do not define DB schemas in apps.
- Always define schemas in `packages/data-ops/src/drizzle/` and import from there.

## Better Auth schema

- Generate auth schema:
  - `pnpm run --filter data-ops better-auth:generate`

## Drizzle migrations

- Generate SQL migrations:
  - `pnpm run --filter data-ops drizzle:generate`

- Run migrations (uses the `packages/data-ops` script `drizzle:migrate`):
  - `pnpm run --filter data-ops drizzle:migrate`

## Apply migrations

- Apply locally (recommended):
  - Run the user app at least once so a local D1 SQLite file exists under `apps/user-application/.wrangler/state/...`.
  - Then run: `pnpm run --filter data-ops drizzle:migrate`

- Apply locally (manual / fallback, run from `apps/user-application`):
  - `npx wrangler d1 execute DB --local --file=../../packages/data-ops/src/drizzle/<migration_file>.sql`

- Apply remotely (D1 HTTP driver):
  - `NODE_ENV=production pnpm run --filter data-ops drizzle:migrate`

Remote migrate requires `CLOUDFLARE_ACCOUNT_ID` (or `CLOUDFLARE_D1_ACCOUNT_ID`), `CLOUDFLARE_DATABASE_ID`, and `CLOUDFLARE_D1_TOKEN` (or `CLOUDFLARE_D1_API_TOKEN`).

## Verification

- After schema changes, rebuild the shared library:
  - `pnpm run build:data-ops`
- If runtime bindings/types changed, regenerate worker types (see worker typegen skill).
