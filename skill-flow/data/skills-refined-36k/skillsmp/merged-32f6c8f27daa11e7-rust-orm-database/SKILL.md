---
name: rust-orm-database
description: Use this skill when you need to interact with databases in Rust using various ORM libraries with compile-time checked queries and async support.
---

# Database ORM Standards

## Connection Pool

### Diesel ORM

```rust
use diesel::pg::PgConnection;
use diesel::r2d2::{Pool, ConnectionManager};

type DbPool = Pool<ConnectionManager<PgConnection>>;

fn establish_pool(database_url: &str) -> DbPool {
    let manager = ConnectionManager::<PgConnection>::new(database_url);
    Pool::builder()
        .max_size(15)
        .build(manager)
        .expect("Failed to create pool")
}
```

### SQLx Database

```rust
use sqlx::postgres::PgPoolOptions;

let pool = PgPoolOptions::new()
    .max_connections(5)
    .connect("postgres://user:pass@localhost/db")
    .await?;
```

### SeaORM

```rust
use sea_orm::{Database, DbConn, ConnectOptions};

async fn connect() -> Result<DbConn, DbErr> {
    let mut opt = ConnectOptions::new("postgres://user:pass@localhost/db");
    opt.max_connections(100)
       .min_connections(5)
       .sqlx_logging(true);

    Database::connect(opt).await
}
```

## CRUD Operations

### Diesel ORM

```rust
use diesel::prelude::*;
use crate::schema::users::dsl::*;

// Create
fn create_user(conn: &mut PgConnection, new_user: &NewUser) -> QueryResult<User> {
    diesel::insert_into(users)
        .values(new_user)
        .get_result(conn)
}

// Read
fn find_user(conn: &mut PgConnection, user_id: i32) -> QueryResult<User> {
    users.find(user_id).first(conn)
}

// Update
fn update_user(conn: &mut PgConnection, user_id: i32, changes: &UpdateUser) -> QueryResult<User> {
    diesel::update(users.find(user_id))
        .set(changes)
        .get_result(conn)
}

// Delete
fn delete_user(conn: &mut PgConnection, user_id: i32) -> QueryResult<usize> {
    diesel::delete(users.find(user_id)).execute(conn)
}
```

### SQLx Database

```rust
use sqlx::{query, query_as, FromRow};

#[derive(FromRow)]
struct User {
    id: i64,
    name: String,
    email: String,
}

// Create
let user = sqlx::query("INSERT INTO users (name, email) VALUES ($1, $2)")
    .bind(&new_user.name)
    .bind(&new_user.email)
    .execute(&pool)
    .await?;

// Read
let user = sqlx::query_as!(User, "SELECT id, name, email FROM users WHERE id = $1", user_id)
    .fetch_one(&pool)
    .await?;
```

### SeaORM

```rust
use sea_orm::{ActiveModelTrait, EntityTrait, Set};

// Create
async fn create_user(db: &DbConn, name: String, email: String) -> Result<user::Model, DbErr> {
    let user = user::ActiveModel {
        name: Set(name),
        email: Set(email),
        created_at: Set(Utc::now()),
        ..Default::default()
    };
    user.insert(db).await
}

// Read
async fn find_user(db: &DbConn, id: i32) -> Result<Option<user::Model>, DbErr> {
    User::find_by_id(id).one(db).await
}
```

## Transactions

### Diesel ORM

```rust
conn.transaction(|conn| {
    diesel::insert_into(users)
        .values(&new_user)
        .execute(conn)?;

    diesel::insert_into(audit_log)
        .values(&log_entry)
        .execute(conn)?;

    Ok(())
})
```

### SQLx Database

```rust
let mut tx = pool.begin().await?;

sqlx::query("INSERT INTO users (name) VALUES ($1)")
    .bind(&user.name)
    .execute(&mut *tx)
    .await?;

tx.commit().await?;
```

### SeaORM

```rust
use sea_orm::TransactionTrait;

async fn transfer(db: &DbConn, from: i32, to: i32, amount: i32) -> Result<(), DbErr> {
    db.transaction::<_, (), DbErr>(|txn| {
        Box::pin(async move {
            // Debit from source
            let from_account = Account::find_by_id(from).one(txn).await?.unwrap();
            account::ActiveModel {
                balance: Set(from_account.balance - amount),
                ..from_account.into()
            }.update(txn).await?;

            // Credit to destination
            let to_account = Account::find_by_id(to).one(txn).await?.unwrap();
            account::ActiveModel {
                balance: Set(to_account.balance + amount),
                ..to_account.into()
            }.update(txn).await?;

            Ok(())
        })
    }).await
}
```

## Migrations

### Diesel ORM

```bash
# Create migration
diesel migration generate create_users

# Run pending migrations
diesel migration run
```

### SQLx Database

```bash
# Create migration
sqlx migrate add create_users_table

# Run migrations
sqlx migrate run
```

### SeaORM

```rust
// migration/src/m20220101_000001_create_users.rs
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.create_table(
            Table::create()
                .table(Users::Table)
                .col(ColumnDef::new(Users::Id).integer().auto_increment().primary_key())
                .col(ColumnDef::new(Users::Name).string().not_null())
                .col(ColumnDef::new(Users::Email).string().unique_key().not_null())
                .to_owned()
        ).await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.drop_table(Table::drop().table(Users::Table).to_owned()).await
    }
}
```

## Best Practices

1. **Schema sync**: Run migrations before compile.
2. **Connection limits**: Match pool size to expected concurrent connections.
3. **Use `Option<T>`**: For nullable columns.
4. **ActiveModel**: Use `Set()` for values to update in SeaORM.
5. **Logging**: Enable logging for debugging in SQLx and SeaORM.