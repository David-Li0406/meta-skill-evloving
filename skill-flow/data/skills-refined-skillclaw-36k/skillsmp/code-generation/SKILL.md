---
name: code-generation
description: Run and troubleshoot project code generation (sqlc + templ).
license: MIT
compatibility: Requires bash, git, Go, make, sqlc v1.30.0+, and templ.
metadata:
  repo: mjrwtf
  runner: github-copilot-cli
  version: 1.2
allowed-tools: Bash(git:*) Bash(make:*) Bash(go:*) Bash(sqlc:*) Bash(templ:*) Bash(curl:*) Read
---

## What this skill covers

This repo relies on generated code for:

- **sqlc**: generates DB access code into `internal/adapters/repository/sqlc/sqlite/`
- **templ**: generates Go code from `.templ` templates

## Standard commands

```bash
make generate
```

Manual equivalents:

```bash
sqlc generate
templ generate
```

## When to run generation

Run `make generate` when you change:
- `internal/adapters/repository/sqlc/sqlite/queries.sql`
- `sqlc.yaml`
- migration files referenced by `sqlc.yaml` under `schema:`
- any `.templ` files

## Troubleshooting

If you see compile errors referencing missing generated code, re-run:

```bash
make generate
```
