---
name: go
description: Go Constraints. Errors, Context, testify/require, SQLBoiler, Nx Support.
---

# Lang: Go

## Rules

1. **Errors:** Wrap with `fmt.Errorf("...: %w", err)`. Never ignore.
2. **Context:** `ctx context.Context` MUST be 1st arg.
3. **DB:** Use **SQLBoiler** models/executors. NO GORM/Raw SQL.
4. **Tests:** Table-Driven (`struct` slice) + `testify/require`.
5. **Layout:** Use `skill nx-monorepo` if `nx.json` exists. Otherwise use standard `cmd/`, `internal/`, `pkg/`.
6. **Libs:** Log=`log/slog`, Conc=`errgroup`.

## Workflow

- Use `skill workflow-env` before build/run commands.
- Build: `go build ./cmd/<app>`
- Test: `go test -v ./...`
- Format: `gofmt -w .`

## Documentation Access

When you need to verify standard library APIs, language spec details, or idiomatic patterns:

1. **Primary (Context7)**: `/golang/go`
2. **Fallback**: <https://go.dev/doc>

**Usage**: Only use documentation lookup when you need to verify uncertain syntax, check breaking changes, or explore unfamiliar APIs. Apply this skill's established rules directly for routine tasks.
