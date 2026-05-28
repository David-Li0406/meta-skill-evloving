# SQLx Query Patterns

## Connection Pool

```rust
use sqlx::postgres::PgPoolOptions;
use sqlx::PgPool;

async fn create_pool() -> Result<PgPool, sqlx::Error> {
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .acquire_timeout(Duration::from_secs(3))
        .connect(&std::env::var("DATABASE_URL")?)
        .await?;
    
    Ok(pool)
}
```

## Compile-Time Checked Queries

```rust
// Requires DATABASE_URL at compile time
// Run: cargo sqlx prepare

// Single row
let user = sqlx::query!(
    "SELECT id, name, email FROM users WHERE id = $1",
    user_id
)
.fetch_one(&pool)
.await?;

println!("User: {} - {}", user.name, user.email);

// Multiple rows
let users = sqlx::query!(
    "SELECT id, name FROM users WHERE active = $1 LIMIT $2",
    true,
    10i64
)
.fetch_all(&pool)
.await?;

// Optional row
let user = sqlx::query!(
    "SELECT id, name FROM users WHERE email = $1",
    email
)
.fetch_optional(&pool)
.await?;
```

## Query As (Map to Struct)

```rust
#[derive(sqlx::FromRow)]
struct User {
    id: i64,
    name: String,
    email: String,
    created_at: DateTime<Utc>,
}

let users: Vec<User> = sqlx::query_as!(
    User,
    "SELECT id, name, email, created_at FROM users WHERE active = $1",
    true
)
.fetch_all(&pool)
.await?;

// Or with runtime query
let users: Vec<User> = sqlx::query_as::<_, User>(
    "SELECT id, name, email, created_at FROM users"
)
.fetch_all(&pool)
.await?;
```

## Insert, Update, Delete

```rust
// Insert with returning
let user = sqlx::query!(
    r#"
    INSERT INTO users (name, email)
    VALUES ($1, $2)
    RETURNING id, name, email, created_at
    "#,
    name,
    email
)
.fetch_one(&pool)
.await?;

// Update
let result = sqlx::query!(
    "UPDATE users SET name = $1 WHERE id = $2",
    new_name,
    user_id
)
.execute(&pool)
.await?;

println!("Rows affected: {}", result.rows_affected());

// Delete
sqlx::query!("DELETE FROM users WHERE id = $1", user_id)
    .execute(&pool)
    .await?;
```

## Transactions

```rust
async fn transfer_funds(
    pool: &PgPool,
    from: i64,
    to: i64,
    amount: i64,
) -> Result<(), sqlx::Error> {
    let mut tx = pool.begin().await?;

    sqlx::query!(
        "UPDATE accounts SET balance = balance - $1 WHERE id = $2",
        amount,
        from
    )
    .execute(&mut *tx)
    .await?;

    sqlx::query!(
        "UPDATE accounts SET balance = balance + $1 WHERE id = $2",
        amount,
        to
    )
    .execute(&mut *tx)
    .await?;

    tx.commit().await?;
    Ok(())
}
```

## Streaming

```rust
use futures::TryStreamExt;

let mut rows = sqlx::query!("SELECT id, name FROM users")
    .fetch(&pool);

while let Some(row) = rows.try_next().await? {
    println!("User: {} - {}", row.id, row.name);
}
```

## Custom Types

```rust
#[derive(sqlx::Type)]
#[sqlx(type_name = "user_role", rename_all = "lowercase")]
enum UserRole {
    Admin,
    User,
    Guest,
}

#[derive(sqlx::FromRow)]
struct User {
    id: i64,
    name: String,
    role: UserRole,
}

// In query
let users = sqlx::query_as!(
    User,
    r#"SELECT id, name, role as "role: UserRole" FROM users"#
)
.fetch_all(&pool)
.await?;
```

## Migrations

```bash
# Install CLI
cargo install sqlx-cli

# Create migration
sqlx migrate add create_users

# Run migrations
sqlx migrate run

# Prepare for offline compilation
cargo sqlx prepare
```

```sql
-- migrations/20240101000000_create_users.sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```
