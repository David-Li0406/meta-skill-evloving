# Rust on fly.io

## Axum

### Dockerfile for Axum

See `assets/dockerfiles/axum.Dockerfile` for the complete template.

**Key points:**
- Multi-stage build: builder stage + minimal runtime
- Use `rust:1.75-slim` for builder
- Use `debian:bookworm-slim` for runtime (smaller final image)
- Cache cargo dependencies separately
- Strip binary for smaller size

### Basic Axum App

```rust
// src/main.rs
use axum::{
    routing::get,
    Router,
    Json,
};
use serde_json::{json, Value};
use std::net::SocketAddr;

#[tokio::main]
async fn main() {
    // Get port from env or default to 8080
    let port = std::env::var("PORT")
        .unwrap_or_else(|_| "8080".to_string())
        .parse::<u16>()
        .expect("PORT must be a valid number");

    // Build router
    let app = Router::new()
        .route("/", get(root))
        .route("/health", get(health));

    // Run server
    let addr = SocketAddr::from(([0, 0, 0, 0], port));
    println!("Listening on {}", addr);

    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn root() -> Json<Value> {
    Json(json!({ "message": "Hello World" }))
}

async fn health() -> Json<Value> {
    Json(json!({ "status": "ok" }))
}
```

### Cargo.toml

```toml
[package]
name = "my-axum-app"
version = "0.1.0"
edition = "2021"

[dependencies]
axum = "0.7"
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
tower = "0.4"
tower-http = { version = "0.5", features = ["cors", "trace"] }

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
strip = true
```

### fly.toml for Axum

```toml
app = "my-axum-app"
primary_region = "ord"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8080"
  RUST_LOG = "info"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 0

  [[http_service.checks]]
    grace_period = "5s"
    interval = "30s"
    method = "GET"
    timeout = "5s"
    path = "/health"

[[vm]]
  memory = "256mb"
  cpus = 1
```

### Database Integration (SQLx + PostgreSQL)

**Cargo.toml additions:**
```toml
[dependencies]
sqlx = { version = "0.7", features = ["runtime-tokio-rustls", "postgres", "migrate"] }
dotenvy = "0.15"
```

**Database setup:**
```rust
use sqlx::postgres::PgPoolOptions;

#[tokio::main]
async fn main() {
    let database_url = std::env::var("DATABASE_URL")
        .expect("DATABASE_URL must be set");

    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await
        .expect("Failed to connect to database");

    // Run migrations
    sqlx::migrate!("./migrations")
        .run(&pool)
        .await
        .expect("Failed to run migrations");

    let app = Router::new()
        .route("/", get(root))
        .route("/health", get(health))
        .with_state(pool);

    // ... rest of server setup
}
```

**fly.toml with migrations:**
```toml
[deploy]
  release_command = "./target/release/migrate"  # Or embed in binary
```

### CORS Configuration

```rust
use tower_http::cors::{CorsLayer, Any};

let app = Router::new()
    .route("/", get(root))
    .layer(
        CorsLayer::new()
            .allow_origin(Any)
            .allow_methods(Any)
            .allow_headers(Any)
    );
```

### Logging

```rust
use tower_http::trace::TraceLayer;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() {
    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::new(
            std::env::var("RUST_LOG").unwrap_or_else(|_| "info".into())
        ))
        .with(tracing_subscriber::fmt::layer())
        .init();

    let app = Router::new()
        .route("/", get(root))
        .layer(TraceLayer::new_for_http());

    // ... server setup
}
```

Add to Cargo.toml:
```toml
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

---

## Rocket

### Dockerfile for Rocket

See `assets/dockerfiles/rocket.Dockerfile` for the complete template.

**Similar to Axum but with Rocket-specific configuration.**

### Basic Rocket App

```rust
// src/main.rs
#[macro_use] extern crate rocket;

use rocket::serde::json::Json;
use serde::{Serialize, Deserialize};

#[derive(Serialize)]
struct Message {
    message: String,
}

#[derive(Serialize)]
struct Health {
    status: String,
}

#[get("/")]
fn index() -> Json<Message> {
    Json(Message {
        message: "Hello World".to_string()
    })
}

#[get("/health")]
fn health() -> Json<Health> {
    Json(Health {
        status: "ok".to_string()
    })
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![index, health])
}
```

### Cargo.toml

```toml
[package]
name = "my-rocket-app"
version = "0.1.0"
edition = "2021"

[dependencies]
rocket = { version = "0.5", features = ["json"] }
serde = { version = "1", features = ["derive"] }

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
strip = true
```

### Rocket.toml

```toml
[default]
address = "0.0.0.0"
port = 8080

[release]
address = "0.0.0.0"
port = 8080
log_level = "normal"
```

### fly.toml for Rocket

```toml
app = "my-rocket-app"
primary_region = "ord"

[build]
  dockerfile = "Dockerfile"

[env]
  ROCKET_ADDRESS = "0.0.0.0"
  ROCKET_PORT = "8080"
  ROCKET_LOG_LEVEL = "normal"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 0

  [[http_service.checks]]
    grace_period = "5s"
    interval = "30s"
    method = "GET"
    timeout = "5s"
    path = "/health"

[[vm]]
  memory = "256mb"
  cpus = 1
```

### Database Integration (Diesel + PostgreSQL)

**Cargo.toml additions:**
```toml
[dependencies]
rocket_sync_db_pools = { version = "0.1", features = ["diesel_postgres_pool"] }
diesel = { version = "2.1", features = ["postgres"] }
```

**Setup:**
```rust
use rocket_sync_db_pools::{database, diesel};

#[database("postgres_db")]
pub struct DbConn(diesel::PgConnection);

#[launch]
fn rocket() -> _ {
    rocket::build()
        .attach(DbConn::fairing())
        .mount("/", routes![index, health])
}
```

**Rocket.toml database config:**
```toml
[default.databases.postgres_db]
url = "${DATABASE_URL}"
```

### Environment Variables in Rocket

Rocket automatically reads from environment variables:

```toml
[release]
secret_key = "${SECRET_KEY}"
```

Set via fly secrets:
```bash
fly secrets set SECRET_KEY=$(openssl rand -base64 32)
```

---

## Rust Best Practices on fly.io

### Optimizing Build Times

**Use cargo-chef for Docker layer caching:**

```dockerfile
FROM lukemathwalker/cargo-chef:latest-rust-1.75 AS chef
WORKDIR /app

FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

FROM chef AS builder
COPY --from=planner /app/recipe.json recipe.json
# Build dependencies (cached layer)
RUN cargo chef cook --release --recipe-path recipe.json
# Build application
COPY . .
RUN cargo build --release

FROM debian:bookworm-slim AS runtime
WORKDIR /app
COPY --from=builder /app/target/release/my-app /usr/local/bin
ENTRYPOINT ["/usr/local/bin/my-app"]
```

### Minimal Runtime Image

**Use distroless for even smaller images:**

```dockerfile
FROM gcr.io/distroless/cc-debian12
COPY --from=builder /app/target/release/my-app /app
ENTRYPOINT ["/app"]
```

**Use musl for static binaries:**

```dockerfile
FROM rust:1.75-alpine AS builder
RUN apk add --no-cache musl-dev
WORKDIR /app
COPY . .
RUN cargo build --release --target x86_64-unknown-linux-musl

FROM scratch
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/my-app /app
ENTRYPOINT ["/app"]
```

### .dockerignore

```
target/
Cargo.lock
.git/
.env
*.db
*.sqlite3
```

### Cargo Configuration

**.cargo/config.toml:**
```toml
[build]
jobs = 4

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
strip = true
panic = "abort"
```

### Memory Usage

Rust apps typically use less memory than Node.js or Python:

- 256MB usually sufficient for basic APIs
- 512MB for database-heavy workloads
- 1GB for complex applications

Monitor:
```bash
fly ssh console -C "free -m"
```

### Cross-compilation (Optional)

For faster local builds, cross-compile for x86_64-unknown-linux-musl:

```bash
rustup target add x86_64-unknown-linux-musl
cargo build --release --target x86_64-unknown-linux-musl
```

### Performance Tips

1. **Use release builds** - Always `--release` for production
2. **Enable LTO** - Link-time optimization in Cargo.toml
3. **Strip binaries** - Remove debug symbols
4. **Async runtime** - Tokio for concurrent workloads
5. **Connection pooling** - Use pool for database connections

### Common Issues

**Binary not found:**
- Verify binary name matches package name in Cargo.toml
- Check ENTRYPOINT path in Dockerfile

**Slow builds:**
- Use cargo-chef for dependency caching
- Consider using fly.io remote builder
- Enable sccache for caching

**Port binding:**
- Always bind to `0.0.0.0`, not `127.0.0.1`
- Read PORT from environment variable

**Large image size:**
- Use multi-stage builds
- Strip binaries
- Use minimal base images (distroless, scratch)
