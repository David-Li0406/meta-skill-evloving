---
name: database-migrations
description: Create, apply, and rollback goose migrations for SQLite using the embedded migrate tool.
license: MIT
compatibility: Requires bash, git, Go, make, and DATABASE_URL set.
metadata:
  repo: mjrwtf
  runner: github-copilot-cli
  version: 1.2
allowed-tools: Bash(git:*) Bash(make:*) Bash(go:*) Bash(curl:*) Read
---

## Key facts for this repo

- Migrations live in `internal/migrations/sqlite/`.
- Migrations are **embedded** into the `bin/migrate` tool at build time.
- `DATABASE_URL` must point at the SQLite database file you intend to migrate.

## Common workflows

### Apply migrations

```bash
export DATABASE_URL=./database.db
make build-migrate
make migrate-up
```

### Check migration status

```bash
make migrate-status
```

### Roll back one migration

```bash
make migrate-down
```

### Create a new migration

```bash
make migrate-create NAME=add_feature_x
```

Then implement it in:

- `internal/migrations/sqlite/<timestamp>_add_feature_x.sql`

## Checklist

1. Write both Up and Down.
2. Rebuild migrate tool (`make build-migrate`).
3. Verify `up` and `down` against a local DB.
