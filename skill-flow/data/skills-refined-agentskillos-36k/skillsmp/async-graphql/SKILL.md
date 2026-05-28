---
name: async-graphql
description: High-performance GraphQL server library for Rust.
metadata:
  labels: [rust, graphql, async-graphql, api]
  triggers:
    files: ['**/schema.rs', '**/graphql.rs']
    keywords: [async_graphql, Object, Query, Mutation, Subscription, Schema]
---

# async-graphql Standards

## Schema Setup

```rust
use async_graphql::{Schema, EmptySubscription};

type AppSchema = Schema<QueryRoot, MutationRoot, EmptySubscription>;

fn create_schema(db: Database) -> AppSchema {
    Schema::build(QueryRoot, MutationRoot, EmptySubscription)
        .data(db)
        .finish()
}
```

## Query

```rust
use async_graphql::{Object, Context, Result};

struct QueryRoot;

#[Object]
impl QueryRoot {
    async fn user(&self, ctx: &Context<'_>, id: i32) -> Result<Option<User>> {
        let db = ctx.data::<Database>()?;
        Ok(db.find_user(id).await?)
    }

    async fn users(
        &self,
        ctx: &Context<'_>,
        #[graphql(default = 10)] limit: i32,
        #[graphql(default = 0)] offset: i32,
    ) -> Result<Vec<User>> {
        let db = ctx.data::<Database>()?;
        Ok(db.list_users(limit, offset).await?)
    }
}
```

## Types

```rust
use async_graphql::{Object, SimpleObject, InputObject, Enum};

// Simple object (auto-implement resolvers)
#[derive(SimpleObject)]
struct User {
    id: i32,
    name: String,
    email: String,
    #[graphql(skip)]  // Don't expose
    password_hash: String,
}

// Complex object (custom resolvers)
#[Object]
impl User {
    async fn posts(&self, ctx: &Context<'_>) -> Result<Vec<Post>> {
        let db = ctx.data::<Database>()?;
        Ok(db.posts_by_user(self.id).await?)
    }
}

// Input type
#[derive(InputObject)]
struct CreateUserInput {
    name: String,
    email: String,
    password: String,
}

// Enum
#[derive(Enum, Copy, Clone, Eq, PartialEq)]
enum Role {
    Admin,
    User,
    Guest,
}
```

## Mutation

```rust
struct MutationRoot;

#[Object]
impl MutationRoot {
    async fn create_user(
        &self,
        ctx: &Context<'_>,
        input: CreateUserInput,
    ) -> Result<User> {
        let db = ctx.data::<Database>()?;
        Ok(db.create_user(input).await?)
    }

    async fn delete_user(&self, ctx: &Context<'_>, id: i32) -> Result<bool> {
        let db = ctx.data::<Database>()?;
        db.delete_user(id).await?;
        Ok(true)
    }
}
```

## Subscription

```rust
use async_graphql::{Subscription, Object};
use futures_util::Stream;

struct SubscriptionRoot;

#[Subscription]
impl SubscriptionRoot {
    async fn messages(&self, room_id: i32) -> impl Stream<Item = Message> {
        // Return stream of messages
        tokio_stream::wrappers::BroadcastStream::new(rx)
            .filter_map(|r| r.ok())
    }
}
```

## DataLoader

```rust
use async_graphql::dataloader::{DataLoader, Loader};
use std::collections::HashMap;

struct UserLoader(Database);

impl Loader<i32> for UserLoader {
    type Value = User;
    type Error = Error;

    async fn load(&self, keys: &[i32]) -> Result<HashMap<i32, User>, Error> {
        let users = self.0.users_by_ids(keys).await?;
        Ok(users.into_iter().map(|u| (u.id, u)).collect())
    }
}

// Use in resolver
#[Object]
impl Post {
    async fn author(&self, ctx: &Context<'_>) -> Result<User> {
        let loader = ctx.data::<DataLoader<UserLoader>>()?;
        loader.load_one(self.author_id).await?.ok_or("not found".into())
    }
}

// Setup
Schema::build(query, mutation, subscription)
    .data(DataLoader::new(UserLoader(db), tokio::spawn))
```

## Error Handling

```rust
use async_graphql::{Error, ErrorExtensions};

#[Object]
impl QueryRoot {
    async fn user(&self, id: i32) -> Result<User> {
        find_user(id)
            .await
            .ok_or_else(|| Error::new("User not found")
                .extend_with(|_, e| e.set("code", "NOT_FOUND")))
    }
}

// Custom error type
#[derive(thiserror::Error, Debug)]
enum AppError {
    #[error("Not found")]
    NotFound,
    #[error("Unauthorized")]
    Unauthorized,
}

impl ErrorExtensions for AppError {
    fn extend(&self) -> Error {
        Error::new(self.to_string()).extend_with(|_, e| {
            e.set("code", match self {
                AppError::NotFound => "NOT_FOUND",
                AppError::Unauthorized => "UNAUTHORIZED",
            });
        })
    }
}
```

## Axum Integration

```rust
use async_graphql_axum::{GraphQLRequest, GraphQLResponse};
use axum::{Extension, Router, routing::post};

async fn graphql_handler(
    Extension(schema): Extension<AppSchema>,
    req: GraphQLRequest,
) -> GraphQLResponse {
    schema.execute(req.into_inner()).await.into()
}

let app = Router::new()
    .route("/graphql", post(graphql_handler))
    .layer(Extension(schema));
```

## Best Practices

1. **DataLoader**: Use for N+1 query prevention
2. **Context**: Store shared state (DB, auth) in context
3. **Input validation**: Validate in resolvers, return typed errors
4. **Pagination**: Use cursor-based pagination for lists
5. **Subscriptions**: Use for real-time features only
