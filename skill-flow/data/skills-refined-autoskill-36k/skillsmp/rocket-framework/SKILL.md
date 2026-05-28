---
name: Rocket Framework
description: Type-safe, async Rust web framework with intuitive API.
metadata:
  labels: [rust, rocket, web, framework]
  triggers:
    files: ['**/main.rs', 'Rocket.toml']
    keywords: [rocket, get, post, launch, routes]
---

# Rocket Framework Standards

## Application Setup

```rust
#[macro_use] extern crate rocket;

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![index, users])
        .mount("/api", routes![api_routes])
        .attach(DbConn::fairing())
        .manage(AppState::new())
}

#[get("/")]
fn index() -> &'static str {
    "Hello, world!"
}
```

## Route Handlers

```rust
// Path parameters
#[get("/users/<id>")]
fn get_user(id: i64) -> Json<User> {
    Json(find_user(id))
}

// Optional parameters
#[get("/users?<page>&<limit>")]
fn list_users(page: Option<u32>, limit: Option<u32>) -> Json<Vec<User>> {
    let page = page.unwrap_or(1);
    let limit = limit.unwrap_or(10);
    Json(fetch_users(page, limit))
}

// Multiple segments
#[get("/files/<path..>")]
fn get_file(path: PathBuf) -> Option<NamedFile> {
    NamedFile::open(Path::new("static/").join(path)).ok()
}
```

## Request Guards

```rust
use rocket::request::{FromRequest, Outcome};

struct AuthUser {
    id: i64,
    role: String,
}

#[rocket::async_trait]
impl<'r> FromRequest<'r> for AuthUser {
    type Error = AuthError;

    async fn from_request(req: &'r Request<'_>) -> Outcome<Self, Self::Error> {
        match req.headers().get_one("Authorization") {
            Some(token) => match validate_token(token).await {
                Ok(user) => Outcome::Success(user),
                Err(e) => Outcome::Error((Status::Unauthorized, e)),
            },
            None => Outcome::Forward(Status::Unauthorized),
        }
    }
}

#[get("/protected")]
fn protected(user: AuthUser) -> String {
    format!("Hello, {}", user.id)
}
```

## JSON Handling

```rust
use rocket::serde::json::Json;

#[derive(Serialize, Deserialize)]
struct CreateUser {
    name: String,
    email: String,
}

#[post("/users", data = "<user>")]
fn create_user(user: Json<CreateUser>) -> Result<Json<User>, Status> {
    let user = user.into_inner();
    match insert_user(&user) {
        Ok(created) => Ok(Json(created)),
        Err(_) => Err(Status::InternalServerError),
    }
}
```

## State Management

```rust
struct AppState {
    config: Config,
    cache: Cache,
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .manage(AppState::new())
        .mount("/", routes![handler])
}

#[get("/config")]
fn handler(state: &State<AppState>) -> String {
    state.config.name.clone()
}
```

## Fairings (Middleware)

```rust
use rocket::fairing::{Fairing, Info, Kind};

struct RequestLogger;

#[rocket::async_trait]
impl Fairing for RequestLogger {
    fn info(&self) -> Info {
        Info {
            name: "Request Logger",
            kind: Kind::Request | Kind::Response,
        }
    }

    async fn on_request(&self, req: &mut Request<'_>, _: &mut Data<'_>) {
        println!("Request: {} {}", req.method(), req.uri());
    }

    async fn on_response<'r>(&self, _: &'r Request<'_>, res: &mut Response<'r>) {
        println!("Response: {}", res.status());
    }
}
```

## Error Handling

```rust
#[catch(404)]
fn not_found() -> Json<ErrorResponse> {
    Json(ErrorResponse { error: "Not found".into() })
}

#[catch(500)]
fn internal_error() -> Json<ErrorResponse> {
    Json(ErrorResponse { error: "Internal server error".into() })
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .register("/", catchers![not_found, internal_error])
}
```

## Best Practices

1. **Guards**: Use request guards for auth, validation
2. **Managed state**: Prefer `&State<T>` over global state
3. **Fairings**: Use for cross-cutting concerns
4. **Configuration**: Use `Rocket.toml` for environment-specific config
5. **Testing**: Use `rocket::local::blocking::Client` for tests
