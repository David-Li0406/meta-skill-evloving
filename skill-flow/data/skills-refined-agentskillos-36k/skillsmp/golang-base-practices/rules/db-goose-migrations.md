---
title: Database Migrations with Goose
impact: CRITICAL
impactDescription: Version-controlled database changes
tags: database, goose, migration
---

## Database Migrations with Goose

Use Goose to manage database schema changes with version control.

**Installation:**

```bash
go install github.com/pressly/goose/v3/cmd/goose@latest
```

**Create Migration File:**

```bash
goose -dir migrations create add_users_table sql
```

**Migration File Example (SQL):**

```sql
-- migrations/20240115120000_add_users_table.sql

-- +goose Up
CREATE TABLE users (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);

-- +goose Down
DROP TABLE users;
```

**Go Code Migration:**

```go
// migrations/20240115130000_seed_admin.go
package migrations

import (
    "context"
    "database/sql"
    "github.com/pressly/goose/v3"
)

func init() {
    goose.AddMigrationContext(upSeedAdmin, downSeedAdmin)
}

func upSeedAdmin(ctx context.Context, tx *sql.Tx) error {
    _, err := tx.ExecContext(ctx,
        "INSERT INTO users (name, email) VALUES (?, ?)",
        "admin", "admin@example.com",
    )
    return err
}

func downSeedAdmin(ctx context.Context, tx *sql.Tx) error {
    _, err := tx.ExecContext(ctx, "DELETE FROM users WHERE email = ?", "admin@example.com")
    return err
}
```

**Common Commands:**

```bash
goose -dir migrations mysql "user:pass@/dbname" up      # Run all pending migrations
goose -dir migrations mysql "user:pass@/dbname" down    # Rollback one migration
goose -dir migrations mysql "user:pass@/dbname" status  # View migration status
goose -dir migrations mysql "user:pass@/dbname" reset   # Rollback all migrations
```
