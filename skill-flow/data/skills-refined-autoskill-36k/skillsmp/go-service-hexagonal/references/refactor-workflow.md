# Refactor Workflow (Existing Go Project → Hexagonal)

Use this workflow to refactor any Go project into the hexagonal layout in small, user-approved steps.

## 1) Inventory the current repo

- Identify entrypoints: list `cmd/*`, `main.go` files, and any runnable binaries.
- List inbound transports: HTTP, gRPC, CLI, workers, cron, queues.
- List outbound dependencies: DBs, caches, queues, external APIs, filesystems.
- Find configuration handling: env, config files, flags, global vars.
- Run a quick tree sketch of top-level packages (no deep analysis yet).

## 2) Choose target shape

- Pick repo shape (single service, multi-binary, monorepo).
- Pick service kind(s) (HTTP, gRPC, worker, CLI).
- Decide settings mode: none, env, or config (Koanf).
- Map current packages to target hex boundaries:
  - `domain`: entities/invariants/pure business logic
  - `app`: use-cases (application services)
  - `interface`: inbound ports/adapters (http/grpc/cli/worker)
  - `adapter`: outbound ports/adapters (db/queue/cache/httpclient)
  - `bootstrap`: composition root

## 3) Create a refactor plan

- Use `references/refactor-plan-template.md`.
- Identify minimal characterization tests to lock behavior before moving code. See `references/refactor-testing.md`.
- Create a checkboxed `REFACTORING.md` at repo root; this file is the live plan and status tracker.
- Keep steps small and reversible.
- Require explicit user approval before any code changes.

## 4) Execute in small steps

- Follow the plan step-by-step.
- After each step: update imports, build or run targeted tests, mark the related checkbox complete in `REFACTORING.md`, and ask for confirmation.
- If a step expands in scope, split it and re-confirm.

## 5) Final verification

- Run the project’s standard tests (`go test ./...` if appropriate).
- Confirm entrypoints still build and run.
- Summarize moved packages and new layout.
