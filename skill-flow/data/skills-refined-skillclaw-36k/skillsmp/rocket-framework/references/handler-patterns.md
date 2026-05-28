# Rocket Handler Patterns

## Basic Routes

```rust
#[macro_use] extern crate rocket;

use rocket::serde::json::Json;
use serde::{Deserialize, Serialize};

#[get("/")]
fn index() -> &'static str {
    "Hello, world!"
}

#[get("/users/<id>")]
fn get_user(id: i64) -> Json<User> {
    Json(User { id, name: "John".into() })
}

#[post("/users", data = "<user>")]
fn create_user(user: Json<CreateUser>) -> Json<User> {
    Json(User {
        id: 1,
        name: user.name.clone(),
    })
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![index, get_user, create_user])
}

#[derive(Serialize)]
struct User {
    id: i64,
    name: String,
}

#[derive(Deserialize)]
struct CreateUser {
    name: String,
}
```

## Request Guards

```rust
use rocket::request::{self, FromRequest, Request};
use rocket::http::Status;

struct ApiKey<'r>(&'r str);

#[rocket::async_trait]
impl<'r> FromRequest<'r> for ApiKey<'r> {
    type Error = ();

    async fn from_request(req: &'r Request<'_>) -> request::Outcome<Self, Self::Error> {
        match req.headers().get_one("X-Api-Key") {
            Some(key) if is_valid(key) => request::Outcome::Success(ApiKey(key)),
            Some(_) => request::Outcome::Error((Status::Unauthorized, ())),
            None => request::Outcome::Forward(Status::Unauthorized),
        }
    }
}

#[get("/protected")]
fn protected(key: ApiKey<'_>) -> &'static str {
    "Secret data"
}

// Optional guard
#[get("/maybe-auth")]
fn maybe_auth(key: Option<ApiKey<'_>>) -> &'static str {
    match key {
        Some(_) => "Authenticated",
        None => "Anonymous",
    }
}
```

## Managed State

```rust
use std::sync::atomic::{AtomicUsize, Ordering};

struct HitCount(AtomicUsize);

#[get("/count")]
fn count(hit_count: &State<HitCount>) -> String {
    let count = hit_count.0.fetch_add(1, Ordering::Relaxed);
    format!("Hits: {}", count)
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .manage(HitCount(AtomicUsize::new(0)))
        .mount("/", routes![count])
}
```

## Error Handling

```rust
use rocket::response::status;
use rocket::http::Status;

#[derive(Responder)]
pub enum ApiResponse<T> {
    #[response(status = 200)]
    Ok(Json<T>),
    #[response(status = 404)]
    NotFound(Json<ErrorMessage>),
    #[response(status = 500)]
    InternalError(Json<ErrorMessage>),
}

#[derive(Serialize)]
pub struct ErrorMessage {
    message: String,
}

#[get("/users/<id>")]
async fn get_user(id: i64, db: &State<Database>) -> ApiResponse<User> {
    match db.find_user(id).await {
        Ok(Some(user)) => ApiResponse::Ok(Json(user)),
        Ok(None) => ApiResponse::NotFound(Json(ErrorMessage {
            message: "User not found".into(),
        })),
        Err(_) => ApiResponse::InternalError(Json(ErrorMessage {
            message: "Database error".into(),
        })),
    }
}

// Catchers for default error pages
#[catch(404)]
fn not_found() -> Json<ErrorMessage> {
    Json(ErrorMessage { message: "Not found".into() })
}

#[catch(500)]
fn internal_error() -> Json<ErrorMessage> {
    Json(ErrorMessage { message: "Internal error".into() })
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .register("/", catchers![not_found, internal_error])
}
```

## Fairings (Middleware)

```rust
use rocket::fairing::{Fairing, Info, Kind};
use rocket::{Request, Response, Data};

pub struct Timer;

#[rocket::async_trait]
impl Fairing for Timer {
    fn info(&self) -> Info {
        Info {
            name: "Request Timer",
            kind: Kind::Request | Kind::Response,
        }
    }

    async fn on_request(&self, request: &mut Request<'_>, _: &mut Data<'_>) {
        request.local_cache(|| std::time::Instant::now());
    }

    async fn on_response<'r>(&self, request: &'r Request<'_>, response: &mut Response<'r>) {
        let start = request.local_cache(|| std::time::Instant::now());
        let duration = start.elapsed();
        response.set_raw_header("X-Response-Time", format!("{}ms", duration.as_millis()));
    }
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .attach(Timer)
}
```

## Forms and Validation

```rust
use rocket::form::{Form, FromForm};

#[derive(FromForm)]
struct LoginForm<'r> {
    #[field(validate = len(3..=20))]
    username: &'r str,
    #[field(validate = len(8..))]
    password: &'r str,
}

#[post("/login", data = "<form>")]
fn login(form: Form<LoginForm<'_>>) -> &'static str {
    // Process login
    "Logged in"
}
```
