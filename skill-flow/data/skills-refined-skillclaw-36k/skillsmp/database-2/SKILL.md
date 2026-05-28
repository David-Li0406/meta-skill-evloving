---
name: database
description: Database operation rules (SeaORM, migrations, transaction rules, PostgreSQL). Use when working with database, creating migrations, using SeaORM, asking about DB operations, schema changes, queries, or entity definitions.
---

# Database Operations Guide

## Tech Stack

- **ORM**: SeaORM 1.1
- **Database**: PostgreSQL
- **Migration**: sea-orm-cli

## Transaction Rules

### Required Rules

1. **Prohibited**: DB operations outside transactions
2. **Prohibited**: Transaction creation/commit/rollback in Service/Repository layers
3. **Prohibited**: Long-held transactions

### Transaction Management Pattern

#### Facade Layer (Manages Transactions)

```rust
use sea_orm::DatabaseTransaction;

pub async fn create_user_facade(
    app_state: &AppState,
    user_data: UserData,
) -> Result<User, FacadeError> {
    let txn = app_state.db().begin().await?;

    let result = async {
        let user = user_service.create(&txn, user_data).await?;
        Ok(user)
    }.await;

    match result {
        Ok(user) => {
            txn.commit().await?;
            Ok(user)
        }
        Err(e) => {
            txn.rollback().await?;
            Err(e)
        }
    }
}
```

#### Service Layer (Receives Transaction)

```rust
pub async fn create(
    &self,
    txn: &DatabaseTransaction,
    user_data: UserData,
) -> Result<User, ServiceError> {
    self.validate(&user_data)?;
    let user = self.repository.create_with_txn(txn, user_data).await?;
    Ok(user)
    // No commit/rollback
}
```

#### Repository Layer (Uses Transaction)

```rust
pub async fn create_with_txn(
    &self,
    txn: &DatabaseTransaction,
    user_data: UserData,
) -> Result<User, RepositoryError> {
    let active_model = user::ActiveModel {
        name: Set(user_data.name),
        email: Set(user_data.email),
        ..Default::default()
    };

    let user = active_model.insert(txn).await?;
    Ok(user)
    // No commit/rollback
}
```

## SeaORM Operations

### Entity Definition

```rust
use sea_orm::entity::prelude::*;

#[derive(Clone, Debug, PartialEq, DeriveEntityModel)]
#[sea_orm(table_name = "users")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i32,
    pub name: String,
    pub email: String,
    pub created_at: DateTime,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {}

impl ActiveModelBehavior for ActiveModel {}
```

### CRUD Operations

#### Create

```rust
let active_model = user::ActiveModel {
    name: Set("太郎".to_string()),
    email: Set("taro@example.com".to_string()),
    ..Default::default()
};

let user = active_model.insert(txn).await?;
```

#### Read

```rust
// Find by ID
let user = User::find_by_id(1)
    .one(txn)
    .await?
    .ok_or(RepositoryError::NotFound)?;

// Find with condition
let users = User::find()
    .filter(user::Column::Email.contains("example.com"))
    .all(txn)
    .await?;
```

#### Update

```rust
let mut user: user::ActiveModel = user.into();
user.name = Set("次郎".to_string());
let updated_user = user.update(txn).await?;
```

#### Delete

```rust
user.delete(txn).await?;
```

### Relations

```rust
#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {
    #[sea_orm(has_many = "super::post::Entity")]
    Posts,
}

// Fetch related data
let user_with_posts = User::find_by_id(1)
    .find_with_related(Post)
    .all(txn)
    .await?;
```

## Migrations

### Commands

```bash
# Run migrations
cargo run -- migrate

# Create new migration
cd migration
sea-orm-cli migrate generate migration_name
```

### Migration File

```rust
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .create_table(
                Table::create()
                    .table(User::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(User::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(ColumnDef::new(User::Name).string().not_null())
                    .col(ColumnDef::new(User::Email).string().not_null())
                    .col(
                        ColumnDef::new(User::CreatedAt)
                            .timestamp()
                            .not_null()
                            .default(Expr::current_timestamp()),
                    )
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .drop_table(Table::drop().table(User::Table).to_owned())
            .await
    }
}
```

## Best Practices

### Query Optimization

```rust
// ❌ N+1 problem
for user in users {
    let posts = Post::find()
        .filter(post::Column::UserId.eq(user.id))
        .all(txn)
        .await?;
}

// ✅ Batch fetch
let users_with_posts = User::find()
    .find_with_related(Post)
    .all(txn)
    .await?;
```

### Index

```rust
// Add index in migration
manager
    .create_index(
        Index::create()
            .table(User::Table)
            .name("idx_user_email")
            .col(User::Email)
            .to_owned(),
    )
    .await?;
```

## Prohibited

- ❌ DB operations outside transactions
- ❌ Transaction creation in Service/Repository layers
- ❌ Long-held transactions (deadlock risk)
- ❌ Business logic in Repository layer
- ❌ Excessive raw SQL (use SeaORM)
