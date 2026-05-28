---
id: rust-project-structure
name: "Project Structure (Actix/Axum)"
domain: RUST
skill: faion-software-developer
category: "backend"
---

## Project Structure (Actix/Axum)

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

### Agent

faion-backend-agent
