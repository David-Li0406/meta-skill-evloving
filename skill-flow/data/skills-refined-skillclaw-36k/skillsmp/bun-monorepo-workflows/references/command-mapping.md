# pnpm → Bun command mapping (monorepo)

This is a quick cheat sheet for translating common pnpm workflows to Bun.

## Install

- `pnpm install` → `bun install`
- `pnpm install --frozen-lockfile` → `bun ci` (or `bun install --frozen-lockfile`)

## Run scripts

- `pnpm run <script>` → `bun run <script>`
- `pnpm -C <dir> <script>` → prefer filter-by-path:
  - `bun --filter ./apps/user-application run <script>`

## Filtering / targeting packages

- `pnpm --filter <pkg> <script>` → `bun --filter <pkg> run <script>`
- `pnpm --filter <glob> <script>` → `bun --filter <glob> run <script>`
- `pnpm --filter '!<pkg>' <script>` → `bun --filter '!<pkg>' run <script>`

Install-only filtering:

- `bun install --filter './apps/user-application'`
- `bun install --filter '!data-service'`

## Add/remove deps

- `pnpm add <pkg>` → `bun add <pkg>`
- `pnpm add -D <pkg>` → `bun add -d <pkg>`
- `pnpm remove <pkg>` → `bun remove <pkg>`

## Introspection

- `pnpm why <pkg>` → `bun why <pkg>`
- `pnpm list` → `bun pm ls` (or `bun list`)

## Running CLIs

- `pnpm dlx <tool>` → `bunx <tool>`

Note: Some Node CLIs (e.g., Wrangler) may behave differently under `bunx`. If a CLI gets flaky, run it via a project script using `bun run ...` (which typically uses system Node for Node-shebang CLIs), or execute the CLI with Node directly.
