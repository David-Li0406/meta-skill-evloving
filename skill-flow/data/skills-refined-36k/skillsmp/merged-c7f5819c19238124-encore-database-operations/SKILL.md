---
name: encore-database-operations
description: Use this skill for performing database queries, migrations, and ORM integration with Encore in both TypeScript and Go.
---

# Encore Database Operations

## Instructions

### Database Setup

#### TypeScript

```typescript
import { SQLDatabase } from "encore.dev/storage/sqldb";

const db = new SQLDatabase("<database_name>", {
  migrations: "./migrations",
});
```

#### Go

```go
package user

import "encore.dev/storage/sqldb"

var db = sqldb.NewDatabase("<database_name>", sqldb.DatabaseConfig{
    Migrations: "./migrations",
})
```

## Query Methods

Encore provides type-safe query methods using generics.

### `query` / `Query` - Multiple Rows

#### TypeScript

```typescript
interface User {
  id: string;
  email: string;
  name: string;
}

const rows = await db.query<User>`
  SELECT id, email, name FROM users WHERE active = true
`;

const users: User[] = [];
for await (const row of rows) {
  users.push(row);
}
```

#### Go

```go
type User struct {
    ID    string
    Email string
    Name  string
}

func listActiveUsers(ctx context.Context) ([]*User, error) {
    rows, err := sqldb.Query[User](ctx, db, `
        SELECT id, email, name FROM users WHERE active = true
    `)
    if err != nil {
        return nil, err
    }
    defer rows.Close()
    
    var users []*User
    for rows.Next() {
        users = append(users, rows.Value())
    }
    return users, rows.Err()
}
```

### `queryRow` / `QueryRow` - Single Row

#### TypeScript

```typescript
const user = await db.queryRow<User>`
  SELECT id, email, name FROM users WHERE id = ${userId}
`;

if (!user) {
  throw APIError.notFound("user not found");
}
```

#### Go

```go
func getUser(ctx context.Context, id string) (*User, error) {
    user, err := sqldb.QueryRow[User](ctx, db, `
        SELECT id, email, name FROM users WHERE id = $1
    `, id)
    if errors.Is(err, sqldb.ErrNoRows) {
        return nil, &errs.Error{
            Code:    errs.NotFound,
            Message: "user not found",
        }
    }
    if err != nil {
        return nil, err
    }
    return user, nil
}
```

### `exec` / `Exec` - No Return Value

For INSERT, UPDATE, DELETE operations:

#### TypeScript

```typescript
await db.exec`
  INSERT INTO users (id, email, name)
  VALUES (${id}, ${email}, ${name})
`;
```

#### Go

```go
func createUser(ctx context.Context, email, name string) error {
    _, err := sqldb.Exec(ctx, db, `
        INSERT INTO users (id, email, name)
        VALUES ($1, $2, $3)
    `, generateID(), email, name)
    return err
}
```

## Migrations

### File Structure

```
<service>/
└── migrations/
    ├── 001_create_users.up.sql
    ├── 002_add_posts.up.sql
    └── 003_add_indexes.up.sql
```

### Naming Convention

- Start with a number (001, 002, etc.)
- Followed by underscore and description
- End with `.up.sql`
- Numbers must be sequential

### Example Migration

```sql
-- migrations/001_create_users.up.sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

## Transactions (Go Only)

```go
func transferFunds(ctx context.Context, fromID, toID string, amount int) error {
    tx, err := db.Begin(ctx)
    if err != nil {
        return err
    }
    defer tx.Rollback()  // No-op if committed
    
    _, err = tx.Exec(ctx, `
        UPDATE accounts SET balance = balance - $1 WHERE id = $2
    `, amount, fromID)
    if err != nil {
        return err
    }
    
    _, err = tx.Exec(ctx, `
        UPDATE accounts SET balance = balance + $1 WHERE id = $2
    `, amount, toID)
    if err != nil {
        return err
    }
    
    return tx.Commit()
}
```

## SQL Injection Protection

Always use parameterized queries:

#### TypeScript

```typescript
// SAFE - values are parameterized
const email = "user@example.com";
await db.queryRow`SELECT * FROM users WHERE email = ${email}`;
```

#### Go

```go
// SAFE - values are parameterized
user, err := sqldb.QueryRow[User](ctx, db, `
    SELECT * FROM users WHERE email = $1
`, email)
```

## Guidelines

- Always use template literals (TypeScript) or parameterized queries (Go) for queries to prevent SQL injection.
- Specify types with generics: `query<User>`, `queryRow<User>` (TypeScript) and `sqldb.Query[T]`, `sqldb.QueryRow[T]` (Go).
- Migrations are applied automatically on startup.
- Database names should be lowercase and descriptive.
- Each service typically has its own database.
- Use transactions for operations that must be atomic (Go only).