# Actix Web Handler Patterns

## Basic Handlers

```rust
use actix_web::{web, App, HttpServer, HttpResponse, Responder};

async fn hello() -> impl Responder {
    HttpResponse::Ok().body("Hello world!")
}

async fn echo(req_body: String) -> impl Responder {
    HttpResponse::Ok().body(req_body)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/", web::get().to(hello))
            .route("/echo", web::post().to(echo))
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
```

## Extractors

```rust
use actix_web::{web, HttpResponse};
use serde::Deserialize;

// Path parameters
async fn get_user(path: web::Path<(u64,)>) -> HttpResponse {
    let user_id = path.into_inner().0;
    HttpResponse::Ok().json(format!("User {}", user_id))
}

// Named path parameters
#[derive(Deserialize)]
struct UserPath {
    id: u64,
}

async fn get_user_named(path: web::Path<UserPath>) -> HttpResponse {
    HttpResponse::Ok().json(format!("User {}", path.id))
}

// Query parameters
#[derive(Deserialize)]
struct ListQuery {
    page: Option<u32>,
    limit: Option<u32>,
}

async fn list_users(query: web::Query<ListQuery>) -> HttpResponse {
    let page = query.page.unwrap_or(1);
    let limit = query.limit.unwrap_or(10);
    HttpResponse::Ok().json(format!("Page {} limit {}", page, limit))
}

// JSON body
#[derive(Deserialize)]
struct CreateUser {
    name: String,
    email: String,
}

async fn create_user(body: web::Json<CreateUser>) -> HttpResponse {
    HttpResponse::Created().json(format!("Created {}", body.name))
}
```

## Application State

```rust
use std::sync::Mutex;

struct AppState {
    counter: Mutex<i32>,
    db: PgPool,
}

async fn increment(data: web::Data<AppState>) -> HttpResponse {
    let mut counter = data.counter.lock().unwrap();
    *counter += 1;
    HttpResponse::Ok().json(*counter)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let pool = create_pool().await;
    let state = web::Data::new(AppState {
        counter: Mutex::new(0),
        db: pool,
    });

    HttpServer::new(move || {
        App::new()
            .app_data(state.clone())
            .route("/count", web::get().to(increment))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
```

## Error Handling

```rust
use actix_web::{error, HttpResponse};
use derive_more::{Display, Error};

#[derive(Debug, Display, Error)]
enum AppError {
    #[display(fmt = "Not found")]
    NotFound,
    #[display(fmt = "Bad request: {}", _0)]
    BadRequest(String),
    #[display(fmt = "Internal error")]
    Internal,
}

impl error::ResponseError for AppError {
    fn error_response(&self) -> HttpResponse {
        match self {
            AppError::NotFound => HttpResponse::NotFound().json("Not found"),
            AppError::BadRequest(msg) => HttpResponse::BadRequest().json(msg),
            AppError::Internal => HttpResponse::InternalServerError().json("Error"),
        }
    }
}

async fn get_user(path: web::Path<u64>) -> Result<HttpResponse, AppError> {
    let user = find_user(path.into_inner())
        .await
        .ok_or(AppError::NotFound)?;
    Ok(HttpResponse::Ok().json(user))
}
```

## Middleware

```rust
use actix_web::middleware::{Logger, Compress};
use actix_cors::Cors;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        let cors = Cors::default()
            .allowed_origin("https://example.com")
            .allowed_methods(vec!["GET", "POST"])
            .max_age(3600);

        App::new()
            .wrap(Logger::default())
            .wrap(Compress::default())
            .wrap(cors)
            .service(web::resource("/").to(index))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
```

## Route Configuration

```rust
fn config(cfg: &mut web::ServiceConfig) {
    cfg.service(
        web::resource("/users")
            .route(web::get().to(list_users))
            .route(web::post().to(create_user))
    )
    .service(
        web::resource("/users/{id}")
            .route(web::get().to(get_user))
            .route(web::put().to(update_user))
            .route(web::delete().to(delete_user))
    );
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .configure(config)
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
```
