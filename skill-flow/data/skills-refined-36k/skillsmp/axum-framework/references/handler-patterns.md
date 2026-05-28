# Axum Handler Patterns

## Basic Handlers

```rust
use axum::{
    extract::{Path, Query, State, Json},
    http::StatusCode,
    response::IntoResponse,
    routing::{get, post},
    Router,
};

// GET with path parameter
async fn get_user(Path(id): Path<i64>) -> impl IntoResponse {
    Json(User { id, name: "John".into() })
}

// POST with JSON body
async fn create_user(
    State(db): State<Database>,
    Json(payload): Json<CreateUserRequest>,
) -> Result<impl IntoResponse, AppError> {
    let user = db.create_user(&payload).await?;
    Ok((StatusCode::CREATED, Json(user)))
}

// Query parameters
async fn list_users(
    Query(params): Query<ListParams>,
) -> impl IntoResponse {
    Json(vec![/* users */])
}

// Router setup
fn app(db: Database) -> Router {
    Router::new()
        .route("/users", get(list_users).post(create_user))
        .route("/users/:id", get(get_user))
        .with_state(db)
}
```

## Error Handling

```rust
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};

pub enum AppError {
    NotFound,
    BadRequest(String),
    Internal(anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            AppError::NotFound => (StatusCode::NOT_FOUND, "Not found".into()),
            AppError::BadRequest(msg) => (StatusCode::BAD_REQUEST, msg),
            AppError::Internal(e) => {
                tracing::error!("Internal error: {:?}", e);
                (StatusCode::INTERNAL_SERVER_ERROR, "Internal error".into())
            }
        };

        (status, Json(serde_json::json!({ "error": message }))).into_response()
    }
}

// Usage in handler
async fn get_user(Path(id): Path<i64>) -> Result<Json<User>, AppError> {
    let user = find_user(id).await.ok_or(AppError::NotFound)?;
    Ok(Json(user))
}
```

## Middleware with Tower

```rust
use tower_http::{
    cors::CorsLayer,
    trace::TraceLayer,
    compression::CompressionLayer,
};

fn app() -> Router {
    Router::new()
        .route("/", get(root))
        .layer(TraceLayer::new_for_http())
        .layer(CompressionLayer::new())
        .layer(CorsLayer::permissive())
}
```
