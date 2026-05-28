---
name: cloudflare-worker-typegen
description: Use this when Cloudflare bindings/env vars change and worker type definitions need regeneration (cf-typegen / worker-configuration.d.ts).
---

# Cloudflare Worker bindings + type generation

Use this skill when the user modifies `wrangler.jsonc`, adds/removes bindings, changes environment variables, or sees type errors related to worker bindings.

## Binding access pattern

- Use `import { env } from "cloudflare:workers"` to access bindings globally.

## Generate worker types

- For the user application:
  - `pnpm run --filter user-application cf-typegen`

This updates `worker-configuration.d.ts` based on `apps/user-application/wrangler.jsonc`.

- For the data service:
  - `pnpm run --filter data-service cf-typegen`

This updates `worker-configuration.d.ts` based on `apps/data-service/wrangler.jsonc`.

## Notes

- Local secrets belong in `apps/user-application/.dev.vars`.
- If bindings change in other workers (e.g., `apps/data-service`), ensure their corresponding typegen workflow is run (if configured) and `worker-configuration.d.ts` stays in sync.
