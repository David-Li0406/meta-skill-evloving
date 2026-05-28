# pnpm → Bun migration notes (this repo)

## What Bun does automatically

- If `pnpm-lock.yaml` exists and `bun.lock` does not, running `bun install` will automatically migrate pnpm’s lockfile to `bun.lock`.
- If `pnpm-workspace.yaml` exists, Bun can migrate workspace settings into root `package.json` under `workspaces`.

## Lockfile format

- Bun v1.2+ uses a text lockfile named `bun.lock` (recommended to commit).
- Older Bun versions used a binary `bun.lockb`.

## Lifecycle scripts / native deps

Bun does not execute lifecycle scripts for dependencies by default.

If a package relies on install scripts:

- Add it to `trustedDependencies` in the relevant `package.json`.
- Re-run `bun install`.
- You can inspect what scripts were blocked with: `bun pm untrusted`.

## Cloudflare tooling cautions

- Wrangler/workerd are Cloudflare-managed toolchains.
- Bun is safe as a package manager, but avoid forcing Bun’s runtime for Wrangler.
- Prefer `bun run ...` scripts that invoke Wrangler normally (Node shebang), or run Wrangler directly with Node.

## Verification checklist

After generating `bun.lock`:

- Run builds for shared packages (especially `packages/data-ops`).
- Run typechecks per app/package.
- Run the two dev entrypoints (user-app + data-service) and ensure Wrangler starts.
- Ensure no pnpm-only commands remain in scripts you expect to use with Bun.

## Repo hygiene

- Do not mix package managers in CI.
- If you keep pnpm during transition, keep `pnpm-lock.yaml` committed until you’ve fully switched; otherwise delete it and rely on `bun.lock`.
