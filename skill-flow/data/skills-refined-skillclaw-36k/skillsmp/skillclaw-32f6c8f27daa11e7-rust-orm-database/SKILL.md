---
name: rust-orm-database
description: Use this skill when you need to interact with a PostgreSQL database in Rust using an ORM, supporting both synchronous and asynchronous operations.
---

# Skill body

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

### SQLx

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
use crate::schema::users;

#[derive(Queryable, Insertable, AsChangeset)]
#[diesel(table_name = users)]
pub struct User {
    pub id: i32,
    pub name: String,
    pub email: String,
    pub created_at: NaiveDateTime,
}

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

### SQLx

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

// Update
async fn update_user(db: &DbConn, id: i32, name: String) -> Result<user::Model, DbErr> {
    let user: user::ActiveModel = User::find_by_id(id)
        .one(db)
        .await?
        .ok_or(DbErr::RecordNotFound("User not found".into()))?
        .into();

    user::ActiveModel {
        name: Set(name),
        ..user
    }.update(db).await
}

// Delete
async fn delete_user(db: &DbConn, id: i32) -> Result<DeleteResult, DbErr> {
    User::delete_by_id(id).exec(db).await
}
```

## Query Building

### Diesel ORM

```rust
let active_users = users
    .filter(active.eq(true))
    .filter(created_at.gt(cutoff_date))
    .load::<User>(conn)?;
```

### SQLx

```rust
let users: Vec<User> = query_as("SELECT * FROM users WHERE active = $1")
    .bind(true)
    .fetch_all(&pool)
    .await?;
```

### SeaORM

```rust
let users = User::find()
    .filter(user::Column::Email.contains("@example.com"))
    .all(db)
    .await?;
```