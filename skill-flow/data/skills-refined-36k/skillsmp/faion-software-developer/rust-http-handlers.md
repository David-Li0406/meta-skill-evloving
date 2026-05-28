---
id: rust-http-handlers
name: "HTTP Handlers"
domain: RUST
skill: faion-software-developer
category: "backend"
---

## HTTP Handlers

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

### Agent

faion-backend-agent
