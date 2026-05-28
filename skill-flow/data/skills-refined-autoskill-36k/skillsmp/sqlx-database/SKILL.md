---
name: SQLx Database
description: Async Rust SQL toolkit with compile-time checked queries.
metadata:
  labels: [rust, sqlx, database, async, postgresql]
  triggers:
    files: ['**/*.rs', 'sqlx-data.json']
    keywords: [sqlx, query, query_as, PgPool]
---

# SQLx Standards

## Connection Pool

```rust
use sqlx::postgres::PgPoolOptions;

let pool = PgPoolOptions::new()
    .max_connections(5)
    .connect("postgres://user:pass@localhost/db")
    .await?;

// Or from environment
let pool = PgPool::connect(&std::env::var("DATABASE_URL")?).await?;
```

## Compile-Time Checked Queries

```rust
// Requires DATABASE_URL at compile time
let user = sqlx::query_as!(
    User,
    "SELECT id, name, email FROM users WHERE id = $1",
    user_id
)
.fetch_one(&pool)
.await?;

// Query with type override
let count = sqlx::query_scalar!(
    r#"SELECT COUNT(*) as "count!" FROM users"#
)
.fetch_one(&pool)
.await?;
```

## Runtime Queries

```rust
use sqlx::{query, query_as, FromRow};

#[derive(FromRow)]
struct User {
    id: i64,
    name: String,
    email: String,
}

// Named struct mapping
let users: Vec<User> = query_as("SELECT * FROM users WHERE active = $1")
    .bind(true)
    .fetch_all(&pool)
    .await?;

// Dynamic query
let user = query("SELECT * FROM users WHERE id = $1")
    .bind(user_id)
    .fetch_optional(&pool)
    .await?;
```

## Fetch Methods

| Method | Returns | Use Case |
|--------|---------|----------|
| `fetch_one` | `T` | Exactly one row expected |
| `fetch_optional` | `Option<T>` | Zero or one row |
| `fetch_all` | `Vec<T>` | All rows in memory |
| `fetch` | `Stream<T>` | Large result sets |

## Transactions

```rust
let mut tx = pool.begin().await?;

sqlx::query("INSERT INTO users (name) VALUES ($1)")
    .bind(&user.name)
    .execute(&mut *tx)
    .await?;

sqlx::query("INSERT INTO audit_log (action) VALUES ($1)")
    .bind("user_created")
    .execute(&mut *tx)
    .await?;

tx.commit().await?;

// Or automatic rollback on drop
```

## Migrations

```bash
# Create migration
sqlx migrate add create_users_table

# Run migrations
sqlx migrate run

# Revert last migration
sqlx migrate revert
```

```rust
// Run embedded migrations at startup
sqlx::migrate!("./migrations")
    .run(&pool)
    .await?;
```

## Type Mappings

| PostgreSQL | Rust | Notes |
|------------|------|-------|
| `BIGINT` | `i64` | |
| `INTEGER` | `i32` | |
| `TEXT/VARCHAR` | `String` | |
| `BOOLEAN` | `bool` | |
| `TIMESTAMP` | `chrono::NaiveDateTime` | Requires `chrono` feature |
| `TIMESTAMPTZ` | `chrono::DateTime<Utc>` | |
| `UUID` | `uuid::Uuid` | Requires `uuid` feature |
| `JSONB` | `serde_json::Value` | Requires `json` feature |

## Best Practices

1. **Compile-time checks**: Use `query!` macros when possible
2. **Connection limits**: Match pool size to Postgres `max_connections`
3. **Prepared statements**: sqlx caches automatically per connection
4. **Offline mode**: Generate `sqlx-data.json` for CI without database
5. **Nullable columns**: Use `Option<T>` for nullable, or override with `"column!"`
