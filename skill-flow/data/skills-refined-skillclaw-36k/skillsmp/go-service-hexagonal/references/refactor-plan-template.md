# Refactor Plan Template

Copy this template into `REFACTORING.md` at the repo root, fill it in with checkboxes, and get user approval before making any changes.

## Context

- Repo: `<path or name>`
- Target shape: `<single-service | multi-binary | monorepo>`
- Service kind(s): `<http | grpc | worker | cli>`
- Settings mode: `<none | env | config>`

## Current inventory (summary)

- Entrypoints: `<list cmd/* or main.go>`
- Inbound transports: `<http/grpc/cli/worker/...>`
- Outbound dependencies: `<db/cache/queue/httpclient/...>`
- Config style: `<env/files/flags/...>`

## Package mapping (current → target)

| Current package | Target package | Reason | Touch points |
| --- | --- | --- | --- |
| `<path>` | `internal/domain/...` | `<why>` | `<imports/tests>` |

## Minimal tests to add

- `<entrypoint or use case>`: `<test description>`
- `<entrypoint or use case>`: `<test description>`

## Refactor steps

For each step, keep scope small and confirm before moving on.

### Step 1: `<short goal>`

- Change: `<move/rename/create/delete>`
- Files: `<paths>`
- Import updates: `<packages affected>`
- Tests to add: `<new or updated tests>`
- Build/test: `<command(s)>`
- Confirmation: `Ask user to approve before next step`

### Step 2: `<short goal>`

- Change: `<move/rename/create/delete>`
- Files: `<paths>`
- Import updates: `<packages affected>`
- Tests to add: `<new or updated tests>`
- Build/test: `<command(s)>`
- Confirmation: `Ask user to approve before next step`
