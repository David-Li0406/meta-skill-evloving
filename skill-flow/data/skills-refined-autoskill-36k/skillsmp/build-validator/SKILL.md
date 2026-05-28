---
name: build-validator
description: Validate builds, type checks, and linting after code changes. Use proactively before finishing tasks or opening PRs.
---

# Build Validation

## Workflow

1. Identify project type (e.g., `package.json`, `Makefile`, `Cargo.toml`, `go.mod`).
2. Check dependencies and required env vars.
3. Run build commands.
4. Run type checks and lint where applicable.
5. Analyze failures and propose fixes.

## Common commands

- Node.js/TypeScript: `npm run build`, `npm run typecheck`, `npm run lint`
- Go: `go build ./...`, `go vet ./...`
- Rust: `cargo build`, `cargo clippy`
- Python: `python -m py_compile`, `mypy`, `ruff check`

## Report format

```
## Build Validation Report

### Status: ✅ Success / ❌ Failure

### Commands
- `cmd`: result

### Issues (if any)
1. [Severity] file:line - description

### Recommended actions
- next steps
```
