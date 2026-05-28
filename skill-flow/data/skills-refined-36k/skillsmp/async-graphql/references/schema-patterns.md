# Async-GraphQL Schema Patterns

## Basic Types

```rust
use async_graphql::*;

#[derive(SimpleObject)]
struct User {
    id: ID,
    name: String,
    email: String,
    #[graphql(skip)]
    password_hash: String, // Hidden from schema
}

// Complex object with resolvers
#[derive(Default)]
struct Post {
    id: i64,
    title: String,
    author_id: i64,
}

#[Object]
impl Post {
    async fn id(&self) -> ID {
        self.id.into()
    }

    async fn title(&self) -> &str {
        &self.title
    }

    // Resolver with context
    async fn author(&self, ctx: &Context<'_>) -> Result<User> {
        let db = ctx.data::<Database>()?;
        db.find_user(self.author_id)
            .await
            .ok_or_else(|| Error::new("Author not found"))
    }
}

// Input types
#[derive(InputObject)]
struct CreatePostInput {
    title: String,
    content: String,
}

// Enums
#[derive(Enum, Copy, Clone, Eq, PartialEq)]
enum PostStatus {
    Draft,
    Published,
    Archived,
}
```

## Query and Mutation

```rust
struct Query;

#[Object]
impl Query {
    async fn user(&self, ctx: &Context<'_>, id: ID) -> Result<Option<User>> {
        let db = ctx.data::<Database>()?;
        Ok(db.find_user(id.parse()?).await)
    }

    async fn users(
        &self,
        ctx: &Context<'_>,
        #[graphql(default = 10)] limit: i32,
        #[graphql(default = 0)] offset: i32,
    ) -> Result<Vec<User>> {
        let db = ctx.data::<Database>()?;
        Ok(db.list_users(limit, offset).await)
    }
}

struct Mutation;

#[Object]
impl Mutation {
    async fn create_post(
        &self,
        ctx: &Context<'_>,
        input: CreatePostInput,
    ) -> Result<Post> {
        let db = ctx.data::<Database>()?;
        let user = ctx.data::<CurrentUser>()?;
        
        db.create_post(user.id, &input.title, &input.content).await
    }

    async fn delete_post(&self, ctx: &Context<'_>, id: ID) -> Result<bool> {
        let db = ctx.data::<Database>()?;
        Ok(db.delete_post(id.parse()?).await?)
    }
}
```

## Subscriptions

```rust
use async_graphql::*;
use futures_util::Stream;

struct Subscription;

#[Subscription]
impl Subscription {
    async fn posts(&self, ctx: &Context<'_>) -> impl Stream<Item = Post> {
        let rx = ctx.data::<broadcast::Receiver<Post>>().unwrap().resubscribe();
        tokio_stream::wrappers::BroadcastStream::new(rx)
            .filter_map(|r| r.ok())
    }
}
```

## DataLoader

```rust
use async_graphql::dataloader::{DataLoader, Loader};
use std::collections::HashMap;

struct UserLoader {
    db: Database,
}

#[async_trait::async_trait]
impl Loader<i64> for UserLoader {
    type Value = User;
    type Error = async_graphql::Error;

    async fn load(&self, keys: &[i64]) -> Result<HashMap<i64, Self::Value>, Self::Error> {
        let users = self.db.find_users_by_ids(keys).await?;
        Ok(users.into_iter().map(|u| (u.id, u)).collect())
    }
}

#[Object]
impl Post {
    async fn author(&self, ctx: &Context<'_>) -> Result<User> {
        let loader = ctx.data::<DataLoader<UserLoader>>()?;
        loader.load_one(self.author_id)
            .await?
            .ok_or_else(|| Error::new("Author not found"))
    }
}
```

## Guards (Authorization)

```rust
use async_graphql::*;

struct RoleGuard {
    role: Role,
}

#[async_trait::async_trait]
impl Guard for RoleGuard {
    async fn check(&self, ctx: &Context<'_>) -> Result<()> {
        let user = ctx.data::<CurrentUser>()?;
        if user.role >= self.role {
            Ok(())
        } else {
            Err("Forbidden".into())
        }
    }
}

#[Object]
impl Mutation {
    #[graphql(guard = "RoleGuard { role: Role::Admin }")]
    async fn delete_user(&self, ctx: &Context<'_>, id: ID) -> Result<bool> {
        // Only admins can access
        Ok(true)
    }
}
```

## Integration with Axum

```rust
use async_graphql_axum::{GraphQLRequest, GraphQLResponse};
use axum::{extract::State, routing::post, Router};

async fn graphql_handler(
    State(schema): State<Schema<Query, Mutation, Subscription>>,
    req: GraphQLRequest,
) -> GraphQLResponse {
    schema.execute(req.into_inner()).await.into()
}

#[tokio::main]
async fn main() {
    let schema = Schema::build(Query, Mutation, Subscription)
        .data(Database::new())
        .data(DataLoader::new(UserLoader::new(), tokio::spawn))
        .finish();

    let app = Router::new()
        .route("/graphql", post(graphql_handler))
        .with_state(schema);

    axum::Server::bind(&"0.0.0.0:8080".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}
```
