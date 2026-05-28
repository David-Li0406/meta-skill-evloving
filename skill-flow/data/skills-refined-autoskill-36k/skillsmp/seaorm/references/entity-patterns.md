# Sea ORM Entity Patterns

## Entity Definition

```rust
use sea_orm::entity::prelude::*;

#[derive(Clone, Debug, PartialEq, Eq, DeriveEntityModel)]
#[sea_orm(table_name = "users")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i32,
    pub name: String,
    #[sea_orm(unique)]
    pub email: String,
    pub age: Option<i32>,
    pub active: bool,
    pub created_at: DateTimeUtc,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {
    #[sea_orm(has_many = "super::post::Entity")]
    Posts,
}

impl Related<super::post::Entity> for Entity {
    fn to() -> RelationDef {
        Relation::Posts.def()
    }
}

impl ActiveModelBehavior for ActiveModel {}
```

## Basic CRUD

```rust
use sea_orm::{Database, EntityTrait, ActiveModelTrait, Set};

async fn crud_examples(db: &DatabaseConnection) -> Result<(), DbErr> {
    // Create
    let user = user::ActiveModel {
        name: Set("John".to_owned()),
        email: Set("john@example.com".to_owned()),
        active: Set(true),
        ..Default::default()
    };
    let user = user.insert(db).await?;
    
    // Read one
    let user = User::find_by_id(1).one(db).await?;
    
    // Read with conditions
    let users = User::find()
        .filter(user::Column::Active.eq(true))
        .filter(user::Column::Age.gt(18))
        .order_by_asc(user::Column::Name)
        .limit(10)
        .all(db)
        .await?;
    
    // Update
    let mut user: user::ActiveModel = user.unwrap().into();
    user.name = Set("Jane".to_owned());
    let user = user.update(db).await?;
    
    // Delete
    User::delete_by_id(1).exec(db).await?;
    
    Ok(())
}
```

## Relations

```rust
// Post entity
#[derive(Clone, Debug, PartialEq, Eq, DeriveEntityModel)]
#[sea_orm(table_name = "posts")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i32,
    pub title: String,
    pub user_id: i32,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {
    #[sea_orm(
        belongs_to = "super::user::Entity",
        from = "Column::UserId",
        to = "super::user::Column::Id"
    )]
    User,
}

impl Related<super::user::Entity> for Entity {
    fn to() -> RelationDef {
        Relation::User.def()
    }
}

// Query with relations
async fn with_relations(db: &DatabaseConnection) -> Result<(), DbErr> {
    // Eager loading
    let users_with_posts = User::find()
        .find_with_related(Post)
        .all(db)
        .await?;
    
    for (user, posts) in users_with_posts {
        println!("User: {}", user.name);
        for post in posts {
            println!("  Post: {}", post.title);
        }
    }
    
    // Join
    let results = User::find()
        .inner_join(Post)
        .filter(post::Column::Title.contains("rust"))
        .all(db)
        .await?;
    
    Ok(())
}
```

## Transactions

```rust
use sea_orm::TransactionTrait;

async fn transfer(db: &DatabaseConnection, from: i32, to: i32, amount: i64) -> Result<(), DbErr> {
    db.transaction::<_, (), DbErr>(|txn| {
        Box::pin(async move {
            // Debit
            let from_account = Account::find_by_id(from).one(txn).await?.unwrap();
            let mut from_account: account::ActiveModel = from_account.into();
            from_account.balance = Set(from_account.balance.unwrap() - amount);
            from_account.update(txn).await?;
            
            // Credit
            let to_account = Account::find_by_id(to).one(txn).await?.unwrap();
            let mut to_account: account::ActiveModel = to_account.into();
            to_account.balance = Set(to_account.balance.unwrap() + amount);
            to_account.update(txn).await?;
            
            Ok(())
        })
    })
    .await
}
```

## Custom Queries

```rust
use sea_orm::{FromQueryResult, Statement};

#[derive(Debug, FromQueryResult)]
struct UserStats {
    name: String,
    post_count: i64,
}

async fn custom_query(db: &DatabaseConnection) -> Result<Vec<UserStats>, DbErr> {
    UserStats::find_by_statement(Statement::from_sql_and_values(
        db.get_database_backend(),
        r#"
        SELECT u.name, COUNT(p.id) as post_count
        FROM users u
        LEFT JOIN posts p ON u.id = p.user_id
        GROUP BY u.id, u.name
        "#,
        vec![],
    ))
    .all(db)
    .await
}
```

## Migrations

```rust
// migration/src/m20220101_000001_create_users.rs
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .create_table(
                Table::create()
                    .table(Users::Table)
                    .if_not_exists()
                    .col(ColumnDef::new(Users::Id).integer().not_null().auto_increment().primary_key())
                    .col(ColumnDef::new(Users::Name).string().not_null())
                    .col(ColumnDef::new(Users::Email).string().unique_key().not_null())
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.drop_table(Table::drop().table(Users::Table).to_owned()).await
    }
}

#[derive(Iden)]
enum Users {
    Table,
    Id,
    Name,
    Email,
}
```
