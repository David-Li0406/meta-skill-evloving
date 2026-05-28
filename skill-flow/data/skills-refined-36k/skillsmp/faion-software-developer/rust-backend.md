# Rust Backend Development

**Rust backend patterns for production-grade applications with Axum and Actix frameworks.**

---

## Rust Project Structure (Actix/Axum)

### Problem
Organize Rust web applications for maintainability.

### Framework: Directory Layout

```
project/
├── Cargo.toml
├── src/
│   ├── main.rs              # Entry point
│   ├── lib.rs               # Library root
│   ├── config.rs            # Configuration
│   ├── error.rs             # Error types
│   ├── routes/
│   │   ├── mod.rs
│   │   └── users.rs         # User routes
│   ├── handlers/
│   │   ├── mod.rs
│   │   └── users.rs         # User handlers
│   ├── services/
│   │   ├── mod.rs
│   │   └── users.rs         # Business logic
│   ├── models/
│   │   ├── mod.rs
│   │   └── user.rs          # Domain models
│   ├── db/
│   │   ├── mod.rs
│   │   └── users.rs         # Database queries
│   └── middleware/
│       ├── mod.rs
│       └── auth.rs          # Auth middleware
├── migrations/
└── tests/
```

### Axum Router Setup

```rust
// src/main.rs

use axum::{
    routing::{get, post, put, delete},
    Router,
};
use std::sync::Arc;
use tower_http::trace::TraceLayer;

mod config;
mod db;
mod error;
mod handlers;
mod middleware;
mod models;
mod routes;
mod services;

use crate::config::Config;
use crate::db::Database;

#[derive(Clone)]
pub struct AppState {
    pub db: Database,
    pub config: Arc<Config>,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::init();

    let config = Config::from_env()?;
    let db = Database::connect(&config.database_url).await?;

    let state = AppState {
        db,
        config: Arc::new(config),
    };

    let app = Router::new()
        .nest("/api/v1", routes::api_routes())
        .layer(TraceLayer::new_for_http())
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
    tracing::info!("Server running on http://0.0.0.0:3000");
    axum::serve(listener, app).await?;

    Ok(())
}

// src/routes/mod.rs

use axum::{routing::get, Router};
use crate::AppState;

mod users;

pub fn api_routes() -> Router<AppState> {
    Router::new()
        .nest("/users", users::routes())
        .route("/health", get(|| async { "OK" }))
}

// src/routes/users.rs

use axum::{
    routing::{get, post, put, delete},
    Router,
};
use crate::{handlers::users, AppState};

pub fn routes() -> Router<AppState> {
    Router::new()
        .route("/", get(users::list).post(users::create))
        .route("/:id", get(users::get).put(users::update).delete(users::delete))
}
```

---

## Rust HTTP Handlers

### Problem
Build type-safe HTTP handlers with proper error handling.

### Framework: Handler Implementation

```rust
// src/handlers/users.rs

use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    Json,
};
use serde::{Deserialize, Serialize};
use validator::Validate;

use crate::{
    error::AppError,
    models::User,
    services::UserService,
    AppState,
};

#[derive(Debug, Deserialize)]
pub struct ListParams {
    #[serde(default = "default_page")]
    page: u32,
    #[serde(default = "default_per_page")]
    per_page: u32,
}

fn default_page() -> u32 { 1 }
fn default_per_page() -> u32 { 20 }

#[derive(Debug, Serialize)]
pub struct ListResponse {
    data: Vec<UserResponse>,
    total: i64,
    page: u32,
    per_page: u32,
}

#[derive(Debug, Serialize)]
pub struct UserResponse {
    id: i32,
    name: String,
    email: String,
    created_at: chrono::DateTime<chrono::Utc>,
}

impl From<User> for UserResponse {
    fn from(user: User) -> Self {
        Self {
            id: user.id,
            name: user.name,
            email: user.email,
            created_at: user.created_at,
        }
    }
}

#[derive(Debug, Deserialize, Validate)]
pub struct CreateUserRequest {
    #[validate(length(min = 2, max = 100))]
    name: String,
    #[validate(email)]
    email: String,
    #[validate(length(min = 8))]
    password: String,
}

pub async fn list(
    State(state): State<AppState>,
    Query(params): Query<ListParams>,
) -> Result<Json<ListResponse>, AppError> {
    let service = UserService::new(&state.db);
    let (users, total) = service.list(params.page, params.per_page).await?;

    Ok(Json(ListResponse {
        data: users.into_iter().map(UserResponse::from).collect(),
        total,
        page: params.page,
        per_page: params.per_page,
    }))
}

pub async fn get(
    State(state): State<AppState>,
    Path(id): Path<i32>,
) -> Result<Json<UserResponse>, AppError> {
    let service = UserService::new(&state.db);
    let user = service.get_by_id(id).await?;
    Ok(Json(user.into()))
}

pub async fn create(
    State(state): State<AppState>,
    Json(payload): Json<CreateUserRequest>,
) -> Result<(StatusCode, Json<UserResponse>), AppError> {
    payload.validate()?;

    let service = UserService::new(&state.db);
    let user = service.create(&payload.name, &payload.email, &payload.password).await?;

    Ok((StatusCode::CREATED, Json(user.into())))
}

pub async fn update(
    State(state): State<AppState>,
    Path(id): Path<i32>,
    Json(payload): Json<UpdateUserRequest>,
) -> Result<Json<UserResponse>, AppError> {
    let service = UserService::new(&state.db);
    let user = service.update(id, payload.name.as_deref()).await?;
    Ok(Json(user.into()))
}

pub async fn delete(
    State(state): State<AppState>,
    Path(id): Path<i32>,
) -> Result<StatusCode, AppError> {
    let service = UserService::new(&state.db);
    service.delete(id).await?;
    Ok(StatusCode::NO_CONTENT)
}
```

---

## Tokio Async Patterns

### Problem
Handle concurrent operations efficiently.

### Framework: Async Service

```rust
// src/services/users.rs

use crate::{
    db::Database,
    error::AppError,
    models::User,
};
use argon2::{
    password_hash::{rand_core::OsRng, PasswordHasher, SaltString},
    Argon2,
};

pub struct UserService<'a> {
    db: &'a Database,
}

impl<'a> UserService<'a> {
    pub fn new(db: &'a Database) -> Self {
        Self { db }
    }

    pub async fn list(&self, page: u32, per_page: u32) -> Result<(Vec<User>, i64), AppError> {
        let offset = ((page - 1) * per_page) as i64;

        // Run count and fetch in parallel
        let (users, total) = tokio::try_join!(
            self.db.fetch_users(per_page as i64, offset),
            self.db.count_users()
        )?;

        Ok((users, total))
    }

    pub async fn get_by_id(&self, id: i32) -> Result<User, AppError> {
        self.db
            .fetch_user_by_id(id)
            .await?
            .ok_or(AppError::NotFound("User not found".into()))
    }

    pub async fn create(
        &self,
        name: &str,
        email: &str,
        password: &str,
    ) -> Result<User, AppError> {
        // Check if email already exists
        if self.db.fetch_user_by_email(email).await?.is_some() {
            return Err(AppError::Conflict("Email already exists".into()));
        }

        // Hash password (CPU-intensive, use spawn_blocking)
        let password_hash = tokio::task::spawn_blocking({
            let password = password.to_string();
            move || {
                let salt = SaltString::generate(&mut OsRng);
                Argon2::default()
                    .hash_password(password.as_bytes(), &salt)
                    .map(|h| h.to_string())
            }
        })
        .await??;

        self.db.insert_user(name, email, &password_hash).await
    }

    pub async fn update(&self, id: i32, name: Option<&str>) -> Result<User, AppError> {
        let user = self.get_by_id(id).await?;

        let new_name = name.unwrap_or(&user.name);
        self.db.update_user(id, new_name).await
    }

    pub async fn delete(&self, id: i32) -> Result<(), AppError> {
        let deleted = self.db.delete_user(id).await?;
        if !deleted {
            return Err(AppError::NotFound("User not found".into()));
        }
        Ok(())
    }
}
```

### Concurrent Processing

```rust
// src/services/batch.rs

use futures::stream::{self, StreamExt};
use std::sync::Arc;
use tokio::sync::Semaphore;

pub struct BatchProcessor {
    concurrency: usize,
}

impl BatchProcessor {
    pub fn new(concurrency: usize) -> Self {
        Self { concurrency }
    }

    pub async fn process_items<T, F, Fut, R, E>(
        &self,
        items: Vec<T>,
        processor: F,
    ) -> Vec<Result<R, E>>
    where
        T: Send + 'static,
        F: Fn(T) -> Fut + Send + Sync + 'static,
        Fut: std::future::Future<Output = Result<R, E>> + Send,
        R: Send + 'static,
        E: Send + 'static,
    {
        let semaphore = Arc::new(Semaphore::new(self.concurrency));
        let processor = Arc::new(processor);

        stream::iter(items)
            .map(|item| {
                let semaphore = semaphore.clone();
                let processor = processor.clone();

                async move {
                    let _permit = semaphore.acquire().await.unwrap();
                    processor(item).await
                }
            })
            .buffer_unordered(self.concurrency)
            .collect()
            .await
    }
}

// Usage
let processor = BatchProcessor::new(10);
let results = processor.process_items(
    user_ids,
    |id| async move { fetch_user(id).await }
).await;
```

---

## Rust Testing Patterns

### Problem
Write comprehensive tests for Rust applications.

### Framework: Unit Tests

```rust
// src/services/users.rs

#[cfg(test)]
mod tests {
    use super::*;
    use mockall::predicate::*;
    use mockall::mock;

    mock! {
        Database {}

        impl Database {
            async fn fetch_user_by_id(&self, id: i32) -> Result<Option<User>, sqlx::Error>;
            async fn fetch_user_by_email(&self, email: &str) -> Result<Option<User>, sqlx::Error>;
            async fn insert_user(&self, name: &str, email: &str, password_hash: &str) -> Result<User, sqlx::Error>;
        }
    }

    fn create_test_user() -> User {
        User {
            id: 1,
            name: "John Doe".into(),
            email: "john@example.com".into(),
            password_hash: "hash".into(),
            created_at: chrono::Utc::now(),
            updated_at: chrono::Utc::now(),
        }
    }

    #[tokio::test]
    async fn test_get_by_id_returns_user() {
        let mut mock_db = MockDatabase::new();
        mock_db
            .expect_fetch_user_by_id()
            .with(eq(1))
            .times(1)
            .returning(|_| Ok(Some(create_test_user())));

        let service = UserService::new(&mock_db);
        let result = service.get_by_id(1).await;

        assert!(result.is_ok());
        assert_eq!(result.unwrap().name, "John Doe");
    }

    #[tokio::test]
    async fn test_get_by_id_not_found() {
        let mut mock_db = MockDatabase::new();
        mock_db
            .expect_fetch_user_by_id()
            .with(eq(999))
            .times(1)
            .returning(|_| Ok(None));

        let service = UserService::new(&mock_db);
        let result = service.get_by_id(999).await;

        assert!(matches!(result, Err(AppError::NotFound(_))));
    }

    #[tokio::test]
    async fn test_create_rejects_duplicate_email() {
        let mut mock_db = MockDatabase::new();
        mock_db
            .expect_fetch_user_by_email()
            .with(eq("john@example.com"))
            .times(1)
            .returning(|_| Ok(Some(create_test_user())));

        let service = UserService::new(&mock_db);
        let result = service.create("John", "john@example.com", "password").await;

        assert!(matches!(result, Err(AppError::Conflict(_))));
    }
}
```

### Integration Tests

```rust
// tests/api_tests.rs

use axum::{
    body::Body,
    http::{Request, StatusCode},
};
use tower::ServiceExt;
use serde_json::json;

async fn setup_app() -> Router {
    // Create test database, run migrations, return app
    todo!()
}

#[tokio::test]
async fn test_create_user() {
    let app = setup_app().await;

    let response = app
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/api/v1/users")
                .header("Content-Type", "application/json")
                .body(Body::from(
                    json!({
                        "name": "John Doe",
                        "email": "john@example.com",
                        "password": "password123"
                    })
                    .to_string(),
                ))
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::CREATED);

    let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
    let user: serde_json::Value = serde_json::from_slice(&body).unwrap();

    assert_eq!(user["name"], "John Doe");
    assert_eq!(user["email"], "john@example.com");
}

#[tokio::test]
async fn test_list_users_pagination() {
    let app = setup_app().await;

    let response = app
        .oneshot(
            Request::builder()
                .method("GET")
                .uri("/api/v1/users?page=1&per_page=10")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);

    let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
    let result: serde_json::Value = serde_json::from_slice(&body).unwrap();

    assert!(result["data"].is_array());
    assert_eq!(result["page"], 1);
    assert_eq!(result["per_page"], 10);
}
```

---

## Sources

- [Rust Axum](https://docs.rs/axum/latest/axum/)
- [Rust Actix](https://actix.rs/docs/)
- [Tokio](https://tokio.rs/tokio/tutorial)
