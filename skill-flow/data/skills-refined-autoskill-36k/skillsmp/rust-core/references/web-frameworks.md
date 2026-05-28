# Rust Web Frameworks

Comprehensive guide to choosing and using Axum, Actix-web, and Rocket for web development.

## Framework Comparison

| Feature | Axum | Actix-web | Rocket |
|---------|------|-----------|--------|
| **Performance** | Excellent | Excellent | Good |
| **Async** | Tokio-based | Custom runtime | Tokio-based |
| **Ergonomics** | Excellent | Good | Excellent |
| **Type Safety** | Excellent | Good | Excellent |
| **Learning Curve** | Moderate | Moderate | Easy |
| **Maturity** | Newer (stable) | Mature | Very Mature |
| **Ecosystem** | Tower ecosystem | Actix ecosystem | Rocket-specific |
| **Best For** | Modern APIs, microservices | High-performance APIs | Rapid prototyping, traditional web |

## When to Use Which

### Choose Axum When:
- Building modern REST/GraphQL APIs
- Need tight Tower/Hyper integration
- Want composable middleware
- Prefer extractors and type-driven design
- Building microservices

### Choose Actix-web When:
- Need maximum performance
- Building high-throughput APIs
- Want actor-based architecture
- Need mature, battle-tested framework

### Choose Rocket When:
- Rapid prototyping
- Prefer request guards and fairings
- Want built-in features (templates, forms, cookies)
- Smaller team or learning Rust web development

## Axum

### Basic Setup

```toml
[dependencies]
axum = "0.7"
tokio = { version = "1", features = ["full"] }
tower = "0.4"
serde = { version = "1.0", features = ["derive"] }
```

### Hello World

```rust
use axum::{
    routing::{get, post},
    Router,
    Json,
    extract::{Path, State},
};
use serde::{Deserialize, Serialize};

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(root))
        .route("/users/:id", get(get_user))
        .route("/users", post(create_user));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000")
        .await
        .unwrap();

    axum::serve(listener, app).await.unwrap();
}

async fn root() -> &'static str {
    "Hello, World!"
}

async fn get_user(Path(id): Path(u64>) -> Json<User> {
    Json(User { id, name: "Alice".into() })
}

async fn create_user(Json(payload): Json<CreateUser>) -> Json<User> {
    Json(User { id: 1, name: payload.name })
}

#[derive(Serialize)]
struct User {
    id: u64,
    name: String,
}

#[derive(Deserialize)]
struct CreateUser {
    name: String,
}
```

### Extractors

```rust
use axum::extract::{Query, Path, State, Json};
use std::sync::Arc;

// Query parameters
async fn search(Query(params): Query<SearchParams>) -> String {
    format!("Searching for: {}", params.q)
}

#[derive(Deserialize)]
struct SearchParams {
    q: String,
    page: Option<u32>,
}

// Path parameters
async fn get_post(Path((user_id, post_id)): Path<(u64, u64)>) -> String {
    format!("User: {}, Post: {}", user_id, post_id)
}

// State
#[derive(Clone)]
struct AppState {
    db: Arc<Database>,
}

async fn handler(State(state): State<AppState>) -> String {
    let count = state.db.count().await;
    format!("Count: {}", count)
}

// JSON body
async fn create(Json(payload): Json<CreateRequest>) -> Json<Response> {
    Json(Response { success: true })
}

// Custom extractor
struct AuthUser {
    id: u64,
    name: String,
}

#[async_trait]
impl<S> FromRequestParts<S> for AuthUser
where
    S: Send + Sync,
{
    type Rejection = (StatusCode, String);

    async fn from_request_parts(
        parts: &mut Parts,
        _state: &S,
    ) -> Result<Self, Self::Rejection> {
        let auth_header = parts
            .headers
            .get("Authorization")
            .and_then(|v| v.to_str().ok())
            .ok_or((StatusCode::UNAUTHORIZED, "Missing auth".to_string()))?;

        // Validate token and return user
        Ok(AuthUser { id: 1, name: "Alice".into() })
    }
}

async fn protected(user: AuthUser) -> String {
    format!("Hello, {}!", user.name)
}
```

### Middleware

```rust
use tower::ServiceBuilder;
use tower_http::{
    trace::TraceLayer,
    cors::CorsLayer,
    compression::CompressionLayer,
};

let app = Router::new()
    .route("/", get(root))
    .layer(
        ServiceBuilder::new()
            .layer(TraceLayer::new_for_http())
            .layer(CorsLayer::permissive())
            .layer(CompressionLayer::new())
    );

// Custom middleware
async fn auth_middleware<B>(
    req: Request<B>,
    next: Next<B>,
) -> Result<Response, StatusCode> {
    let auth_header = req
        .headers()
        .get("Authorization")
        .and_then(|v| v.to_str().ok());

    if auth_header.is_none() {
        return Err(StatusCode::UNAUTHORIZED);
    }

    Ok(next.run(req).await)
}

let app = Router::new()
    .route("/protected", get(handler))
    .layer(middleware::from_fn(auth_middleware));
```

### Error Handling

```rust
use axum::{
    response::{IntoResponse, Response},
    http::StatusCode,
};

enum AppError {
    NotFound,
    Unauthorized,
    Internal(anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            AppError::NotFound => (StatusCode::NOT_FOUND, "Not found"),
            AppError::Unauthorized => (StatusCode::UNAUTHORIZED, "Unauthorized"),
            AppError::Internal(_) => (StatusCode::INTERNAL_SERVER_ERROR, "Internal error"),
        };

        (status, message).into_response()
    }
}

async fn handler() -> Result<Json<Data>, AppError> {
    let data = fetch_data().await.map_err(AppError::Internal)?;
    Ok(Json(data))
}
```

## Actix-web

### Basic Setup

```toml
[dependencies]
actix-web = "4"
actix-rt = "2"
serde = { version = "1.0", features = ["derive"] }
```

### Hello World

```rust
use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};
use serde::{Deserialize, Serialize};

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/", web::get().to(root))
            .route("/users/{id}", web::get().to(get_user))
            .route("/users", web::post().to(create_user))
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}

async fn root() -> impl Responder {
    HttpResponse::Ok().body("Hello, World!")
}

async fn get_user(path: web::Path<u64>) -> impl Responder {
    let user = User { id: *path, name: "Alice".into() };
    web::Json(user)
}

async fn create_user(user: web::Json<CreateUser>) -> impl Responder {
    web::Json(User { id: 1, name: user.name.clone() })
}

#[derive(Serialize)]
struct User {
    id: u64,
    name: String,
}

#[derive(Deserialize)]
struct CreateUser {
    name: String,
}
```

### State and Dependency Injection

```rust
use actix_web::web;

struct AppState {
    db: Database,
}

async fn handler(data: web::Data<AppState>) -> impl Responder {
    let count = data.db.count().await;
    HttpResponse::Ok().json(count)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let state = web::Data::new(AppState {
        db: Database::new(),
    });

    HttpServer::new(move || {
        App::new()
            .app_data(state.clone())
            .route("/count", web::get().to(handler))
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
```

### Middleware

```rust
use actix_web::middleware::{Logger, Compress, NormalizePath};

let app = App::new()
    .wrap(Logger::default())
    .wrap(Compress::default())
    .wrap(NormalizePath::trim())
    .route("/", web::get().to(index));

// Custom middleware
use actix_web::{dev::Service, Error};
use futures_util::future::FutureExt;

pub struct Authentication;

impl<S, B> Transform<S, ServiceRequest> for Authentication
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error>,
    S::Future: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = Error;
    type Transform = AuthenticationMiddleware<S>;
    type InitError = ();
    type Future = Ready<Result<Self::Transform, Self::InitError>>;

    fn new_transform(&self, service: S) -> Self::Future {
        ready(Ok(AuthenticationMiddleware { service }))
    }
}
```

## Rocket

### Basic Setup

```toml
[dependencies]
rocket = { version = "0.5", features = ["json"] }
serde = { version = "1.0", features = ["derive"] }
```

### Hello World

```rust
#[macro_use] extern crate rocket;

use rocket::serde::{json::Json, Serialize, Deserialize};

#[get("/")]
fn index() -> &'static str {
    "Hello, world!"
}

#[get("/users/<id>")]
fn get_user(id: u64) -> Json<User> {
    Json(User { id, name: "Alice".into() })
}

#[post("/users", data = "<user>")]
fn create_user(user: Json<CreateUser>) -> Json<User> {
    Json(User { id: 1, name: user.name.clone() })
}

#[derive(Serialize)]
struct User {
    id: u64,
    name: String,
}

#[derive(Deserialize)]
struct CreateUser {
    name: String,
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![index, get_user, create_user])
}
```

### Request Guards

```rust
use rocket::request::{self, FromRequest, Request};
use rocket::outcome::Outcome;

struct ApiKey(String);

#[rocket::async_trait]
impl<'r> FromRequest<'r> for ApiKey {
    type Error = ();

    async fn from_request(req: &'r Request<'_>) -> request::Outcome<Self, Self::Error> {
        match req.headers().get_one("X-API-Key") {
            Some(key) => Outcome::Success(ApiKey(key.to_string())),
            None => Outcome::Error((Status::Unauthorized, ())),
        }
    }
}

#[get("/protected")]
fn protected(_key: ApiKey) -> &'static str {
    "Authorized!"
}
```

### State Management

```rust
use rocket::State;
use std::sync::Mutex;

struct AppState {
    counter: Mutex<u64>,
}

#[get("/count")]
fn get_count(state: &State<AppState>) -> String {
    let count = state.counter.lock().unwrap();
    format!("Count: {}", *count)
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .manage(AppState { counter: Mutex::new(0) })
        .mount("/", routes![get_count])
}
```

### Fairings (Middleware)

```rust
use rocket::fairing::{Fairing, Info, Kind};
use rocket::{Request, Response};

pub struct RequestTimer;

#[rocket::async_trait]
impl Fairing for RequestTimer {
    fn info(&self) -> Info {
        Info {
            name: "Request Timer",
            kind: Kind::Request | Kind::Response,
        }
    }

    async fn on_request(&self, req: &mut Request<'_>, _: &mut Data<'_>) {
        req.local_cache(|| std::time::Instant::now());
    }

    async fn on_response<'r>(&self, req: &'r Request<'_>, res: &mut Response<'r>) {
        let start = req.local_cache(|| std::time::Instant::now());
        let duration = start.elapsed();
        res.set_raw_header("X-Response-Time", format!("{}ms", duration.as_millis()));
    }
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .attach(RequestTimer)
        .mount("/", routes![index])
}
```

## Common Patterns

### Database Integration

```rust
// Axum with SQLx
use sqlx::PgPool;

#[derive(Clone)]
struct AppState {
    pool: PgPool,
}

async fn get_users(State(state): State<AppState>) -> Result<Json<Vec<User>>, AppError> {
    let users = sqlx::query_as::<_, User>("SELECT * FROM users")
        .fetch_all(&state.pool)
        .await?;
    Ok(Json(users))
}

// Actix-web with SQLx
async fn get_users(pool: web::Data<PgPool>) -> Result<impl Responder> {
    let users = sqlx::query_as::<_, User>("SELECT * FROM users")
        .fetch_all(pool.get_ref())
        .await?;
    Ok(web::Json(users))
}

// Rocket with SQLx
#[get("/users")]
async fn get_users(pool: &State<PgPool>) -> Result<Json<Vec<User>>, Status> {
    let users = sqlx::query_as::<_, User>("SELECT * FROM users")
        .fetch_all(*pool)
        .await
        .map_err(|_| Status::InternalServerError)?;
    Ok(Json(users))
}
```

### WebSocket Support

```rust
// Axum WebSocket
use axum::{
    extract::ws::{WebSocket, WebSocketUpgrade},
    response::Response,
};

async fn ws_handler(ws: WebSocketUpgrade) -> Response {
    ws.on_upgrade(handle_socket)
}

async fn handle_socket(mut socket: WebSocket) {
    while let Some(msg) = socket.recv().await {
        if let Ok(msg) = msg {
            if socket.send(msg).await.is_err() {
                break;
            }
        }
    }
}

// Actix-web WebSocket
use actix_web_actors::ws;

async fn ws_index(
    req: HttpRequest,
    stream: web::Payload,
) -> Result<HttpResponse, Error> {
    ws::start(MyWebSocket {}, &req, stream)
}

struct MyWebSocket;

impl Actor for MyWebSocket {
    type Context = ws::WebsocketContext<Self>;
}

impl StreamHandler<Result<ws::Message, ws::ProtocolError>> for MyWebSocket {
    fn handle(&mut self, msg: Result<ws::Message, ws::ProtocolError>, ctx: &mut Self::Context) {
        match msg {
            Ok(ws::Message::Text(text)) => ctx.text(text),
            _ => (),
        }
    }
}
```

## Best Practices

### Choose Based On Needs

- **High performance, mature**: Actix-web
- **Modern, composable**: Axum
- **Rapid development, batteries-included**: Rocket

### Common Across All

1. Use extractors/guards for dependency injection
2. Implement proper error handling
3. Add logging and tracing
4. Use connection pooling for databases
5. Implement rate limiting for public APIs
6. Add CORS middleware for web clients
7. Use compression middleware
8. Implement proper authentication/authorization
9. Write integration tests
10. Monitor performance and errors
