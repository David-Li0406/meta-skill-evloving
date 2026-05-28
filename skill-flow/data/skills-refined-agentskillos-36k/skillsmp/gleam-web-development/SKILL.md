---
name: gleam-web-development
description: Guides Claude through Gleam backend web development with Wisp and Mist. Use for REST APIs, web services, and server-side rendering. For frontend/SPA development with Lustre, use the gleam-lustre-development skill instead.
---

# Gleam Web Development Skill

This skill guides Claude through **backend web development** with Wisp and Mist, following official examples from the Wisp repository.

## Primary Sources

1. **[Wisp Documentation](https://hexdocs.pm/wisp/)** - Practical web framework
2. **[Wisp Examples](https://github.com/lpil/wisp/tree/main/examples)** - Official examples (this skill is based on these)
3. **[Mist Documentation](https://hexdocs.pm/mist/)** - HTTP server
4. **[Gleam HTTP](https://hexdocs.pm/gleam_http/)** - HTTP types

## Project Structure

Every Wisp project follows this structure:

```
src/
├── app.gleam                    # Entry point
└── app/
    ├── router.gleam             # Routing (pattern matching)
    ├── web.gleam                # Middleware stack + Context type
    └── web/
        ├── people.gleam         # Feature module
        └── products.gleam       # Feature module
```

## Entry Point (app.gleam)

```gleam
import gleam/erlang/process
import mist
import wisp
import wisp_mist
import app/router
import app/web.{Context}

pub fn main() {
  // Configure logger for web application defaults
  wisp.configure_logger()
  
  // In production, load from environment/config
  let secret_key_base = wisp.random_string(64)
  
  // Create context with dependencies
  let ctx = Context(
    db: db_connection,
    static_directory: static_directory(),
  )
  
  // Partially apply context to handler
  let handler = router.handle_request(_, ctx)
  
  let assert Ok(_) =
    wisp_mist.handler(handler, secret_key_base)
    |> mist.new
    |> mist.port(8000)
    |> mist.start

  process.sleep_forever()
}

pub fn static_directory() -> String {
  let assert Ok(priv_directory) = wisp.priv_directory("app")
  priv_directory <> "/static"
}
```

## Context Type (app/web.gleam)

The Context holds dependencies that handlers need:

```gleam
import wisp

/// Context holds dependencies for request handlers.
/// Add database connections, API keys, config, etc.
pub type Context {
  Context(
    db: Database,
    static_directory: String,
  )
}

/// The middleware stack. This is the RECOMMENDED stack for most apps.
pub fn middleware(
  req: wisp.Request,
  handle_request: fn(wisp.Request) -> wisp.Response,
) -> wisp.Response {
  // Allow browsers to simulate PUT/DELETE via _method parameter
  let req = wisp.method_override(req)
  
  // Log request info
  use <- wisp.log_request(req)
  
  // Return 500 if handler crashes
  use <- wisp.rescue_crashes
  
  // Rewrite HEAD to GET with empty body
  use req <- wisp.handle_head(req)
  
  // CSRF protection for non-GET/HEAD requests
  use req <- wisp.csrf_known_header_protection(req)
  
  handle_request(req)
}

/// Middleware with static file serving
pub fn middleware_with_static(
  req: wisp.Request,
  ctx: Context,
  handle_request: fn(wisp.Request) -> wisp.Response,
) -> wisp.Response {
  let req = wisp.method_override(req)
  use <- wisp.log_request(req)
  use <- wisp.rescue_crashes
  use req <- wisp.handle_head(req)
  use req <- wisp.csrf_known_header_protection(req)
  
  // Serve static files from /static/* 
  use <- wisp.serve_static(req, under: "/static", from: ctx.static_directory)
  
  handle_request(req)
}
```

## Router (app/router.gleam)

Use pattern matching on `wisp.path_segments(req)`:

```gleam
import gleam/http.{Get, Post, Delete}
import wisp.{type Request, type Response}
import app/web.{type Context}
import app/web/people
import app/web/products

pub fn handle_request(req: Request, ctx: Context) -> Response {
  use req <- web.middleware(req)
  
  // Pattern match on path segments
  case wisp.path_segments(req) {
    // GET /
    [] -> home_page(req)
    
    // /people and /people/:id
    ["people"] -> people.all(req, ctx)
    ["people", id] -> people.one(req, ctx, id)
    
    // /products and /products/:id
    ["products"] -> products.all(req, ctx)
    ["products", id] -> products.one(req, ctx, id)
    
    // 404 for everything else
    _ -> wisp.not_found()
  }
}

fn home_page(req: Request) -> Response {
  use <- wisp.require_method(req, Get)
  wisp.html_response("<h1>Welcome</h1>", 200)
}
```

## Feature Modules (app/web/people.gleam)

Group related handlers in feature modules:

```gleam
import gleam/dynamic/decode
import gleam/http.{Get, Post, Delete}
import gleam/json
import gleam/result.{try}
import wisp.{type Request, type Response}
import app/web.{type Context}

// TYPES -----------------------------------------------------------------------

pub type Person {
  Person(name: String, email: String)
}

// HANDLERS --------------------------------------------------------------------

/// Handle /people - list and create
pub fn all(req: Request, ctx: Context) -> Response {
  case req.method {
    Get -> list_people(ctx)
    Post -> create_person(req, ctx)
    _ -> wisp.method_not_allowed([Get, Post])
  }
}

/// Handle /people/:id - read, update, delete
pub fn one(req: Request, ctx: Context, id: String) -> Response {
  case req.method {
    Get -> read_person(ctx, id)
    Delete -> delete_person(ctx, id)
    _ -> wisp.method_not_allowed([Get, Delete])
  }
}

// LIST ------------------------------------------------------------------------

fn list_people(ctx: Context) -> Response {
  case db.list_people(ctx.db) {
    Ok(people) -> {
      let json = json.to_string(json.object([
        #("people", json.array(people, person_to_json)),
      ]))
      wisp.json_response(json, 200)
    }
    Error(_) -> wisp.internal_server_error()
  }
}

// CREATE ----------------------------------------------------------------------

fn create_person(req: Request, ctx: Context) -> Response {
  // Use require_json middleware to parse JSON body
  use json <- wisp.require_json(req)
  
  let result = {
    // Decode JSON into Person
    use person <- try(
      decode.run(json, person_decoder())
      |> result.replace_error(Nil)
    )
    
    // Save to database
    use id <- try(db.create_person(ctx.db, person))
    
    // Return created response
    Ok(json.to_string(json.object([#("id", json.string(id))])))
  }
  
  case result {
    Ok(json) -> wisp.json_response(json, 201)
    Error(_) -> wisp.unprocessable_content()
  }
}

// READ ------------------------------------------------------------------------

fn read_person(ctx: Context, id: String) -> Response {
  case db.find_person(ctx.db, id) {
    Ok(person) -> {
      let json = json.to_string(json.object([
        #("id", json.string(id)),
        #("name", json.string(person.name)),
        #("email", json.string(person.email)),
      ]))
      wisp.json_response(json, 200)
    }
    Error(_) -> wisp.not_found()
  }
}

// DELETE ----------------------------------------------------------------------

fn delete_person(ctx: Context, id: String) -> Response {
  case db.delete_person(ctx.db, id) {
    Ok(_) -> wisp.no_content()
    Error(_) -> wisp.not_found()
  }
}

// DECODERS --------------------------------------------------------------------

fn person_decoder() -> decode.Decoder(Person) {
  use name <- decode.field("name", decode.string)
  use email <- decode.field("email", decode.string)
  decode.success(Person(name:, email:))
}

fn person_to_json(person: Person) -> json.Json {
  json.object([
    #("name", json.string(person.name)),
    #("email", json.string(person.email)),
  ])
}
```

## Request Body Middlewares

### JSON Body

```gleam
pub fn create_item(req: Request) -> Response {
  // Parses JSON, returns 415 if wrong content-type, 400 if invalid JSON
  use json <- wisp.require_json(req)
  
  case decode.run(json, item_decoder()) {
    Ok(item) -> // process item
    Error(_) -> wisp.unprocessable_content()
  }
}
```

### Form Data

```gleam
pub fn handle_form(req: Request) -> Response {
  // Parses form data (application/x-www-form-urlencoded or multipart/form-data)
  use formdata <- wisp.require_form(req)
  
  // formdata.values is List(#(String, String))
  // formdata.files is List(#(String, UploadedFile))
  case list.key_find(formdata.values, "name") {
    Ok(name) -> // process name
    Error(_) -> wisp.bad_request("Missing name field")
  }
}
```

### File Uploads

```gleam
pub fn handle_upload(req: Request) -> Response {
  use formdata <- wisp.require_form(req)
  
  case list.key_find(formdata.files, "document") {
    Ok(file) -> {
      // file.path - temporary file path (deleted after request)
      // file.file_name - reported name (NEVER trust this!)
      wisp.log_info("File at: " <> file.path)
      
      // Move file to permanent location if you want to keep it
      // simplifile.rename(file.path, permanent_path)
      
      wisp.ok()
    }
    Error(_) -> wisp.bad_request("Missing file")
  }
}
```

### Raw String Body

```gleam
pub fn handle_csv(req: Request) -> Response {
  use <- wisp.require_content_type(req, "text/csv")
  use body <- wisp.require_string_body(req)
  
  // body is now a String
  case csv.parse(body) {
    Ok(rows) -> // process rows
    Error(_) -> wisp.unprocessable_content()
  }
}
```

## Responses

### Common Responses

```gleam
// Status codes
wisp.ok()                    // 200
wisp.created()               // 201
wisp.no_content()            // 204 (empty body)
wisp.bad_request(message)    // 400
wisp.not_found()             // 404
wisp.method_not_allowed([Get, Post])  // 405
wisp.unprocessable_content() // 422
wisp.internal_server_error() // 500

// With body
wisp.html_response(body, status)   // HTML with content-type
wisp.json_response(json, status)   // JSON with content-type

// Building responses
wisp.ok()
|> wisp.set_header("content-type", "text/csv")
|> wisp.string_body(csv_content)

wisp.ok()
|> wisp.html_body("<h1>Hello</h1>")
```

### File Downloads

```gleam
// From disk (efficient for large files)
fn download_report(req: Request) -> Response {
  wisp.ok()
  |> wisp.set_header("content-type", "application/pdf")
  |> wisp.file_download(named: "report.pdf", from: "/path/to/report.pdf")
}

// From memory (for generated content)
fn download_csv(req: Request) -> Response {
  let content = bytes_tree.from_string("name,email\nJoe,joe@example.com")
  
  wisp.ok()
  |> wisp.set_header("content-type", "text/csv")
  |> wisp.file_download_from_memory(named: "export.csv", containing: content)
}
```

### Redirects

```gleam
wisp.redirect("/login")
wisp.redirect("/users/" <> id)
```

## Cookies

```gleam
const session_cookie = "session_id"

pub fn login(req: Request) -> Response {
  use formdata <- wisp.require_form(req)
  
  case authenticate(formdata) {
    Ok(user) -> {
      let session_id = create_session(user)
      
      wisp.redirect("/dashboard")
      |> wisp.set_cookie(
        req,
        session_cookie,
        session_id,
        wisp.Signed,      // Sign cookie to prevent tampering
        60 * 60 * 24 * 7, // Max age in seconds (7 days)
      )
    }
    Error(_) -> wisp.redirect("/login?error=invalid")
  }
}

pub fn dashboard(req: Request) -> Response {
  case wisp.get_cookie(req, session_cookie, wisp.Signed) {
    Ok(session_id) -> {
      case get_user_from_session(session_id) {
        Ok(user) -> render_dashboard(user)
        Error(_) -> wisp.redirect("/login")
      }
    }
    Error(_) -> wisp.redirect("/login")
  }
}

pub fn logout(req: Request) -> Response {
  // Set max_age to 0 to delete cookie
  case wisp.get_cookie(req, session_cookie, wisp.Signed) {
    Ok(value) -> {
      wisp.redirect("/login")
      |> wisp.set_cookie(req, session_cookie, value, wisp.Signed, 0)
    }
    Error(_) -> wisp.redirect("/login")
  }
}
```

## Logging

```gleam
// Levels from most to least important:
// emergency, alert, critical, error, warning, notice, info, debug

pub fn handle_request(req: Request) -> Response {
  use req <- web.middleware(req)
  
  case wisp.path_segments(req) {
    [] -> {
      wisp.log_debug("Home page accessed")
      home_page(req)
    }
    
    ["admin"] -> {
      wisp.log_warning("Admin page accessed")
      admin_page(req)
    }
    
    ["secret"] -> {
      wisp.log_error("Secret page discovered!")
      wisp.not_found()
    }
    
    _ -> {
      wisp.log_info("404: " <> req.path)
      wisp.not_found()
    }
  }
}
```

## Query Parameters

```gleam
pub fn list_items(req: Request) -> Response {
  // wisp.get_query returns List(#(String, String))
  let query = wisp.get_query(req)
  
  let page = 
    list.key_find(query, "page")
    |> result.try(int.parse)
    |> result.unwrap(1)
  
  let limit = 
    list.key_find(query, "limit")
    |> result.try(int.parse)
    |> result.unwrap(20)
    |> int.clamp(1, 100)
  
  let search = list.key_find(query, "q") |> option.from_result
  
  // Use page, limit, search to query database
}
```

## Static Files

In middleware:

```gleam
pub fn middleware(req, ctx, handle_request) {
  // ... other middleware ...
  
  // Serve files from priv/static at /static/*
  use <- wisp.serve_static(req, under: "/static", from: ctx.static_directory)
  
  handle_request(req)
}
```

In HTML:

```html
<link rel="stylesheet" href="/static/styles.css">
<script src="/static/main.js"></script>
```

## Testing

```gleam
import gleeunit
import gleeunit/should
import wisp/simulate
import app/router

pub fn main() {
  gleeunit.main()
}

pub fn home_page_test() {
  let req = simulate.request(http.Get, "/")
  let response = router.handle_request(req, test_context())
  
  response.status
  |> should.equal(200)
}

pub fn create_person_test() {
  let json = "{\"name\": \"Joe\", \"email\": \"joe@example.com\"}"
  
  let req = 
    simulate.request(http.Post, "/people")
    |> simulate.string_body(json, "application/json")
  
  let response = router.handle_request(req, test_context())
  
  response.status
  |> should.equal(201)
}

fn test_context() -> Context {
  Context(db: test_db(), static_directory: "priv/static")
}
```

## Common Patterns

### Method Dispatch

```gleam
// Single method
fn home(req: Request) -> Response {
  use <- wisp.require_method(req, Get)
  // Only GET allowed
}

// Multiple methods
fn resource(req: Request) -> Response {
  case req.method {
    Get -> list()
    Post -> create(req)
    _ -> wisp.method_not_allowed([Get, Post])
  }
}
```

### Error Handling

```gleam
pub fn create(req: Request, ctx: Context) -> Response {
  use json <- wisp.require_json(req)
  
  let result = {
    use data <- result.try(decode.run(json, decoder()))
    use validated <- result.try(validate(data))
    use created <- result.try(db.create(ctx.db, validated))
    Ok(created)
  }
  
  case result {
    Ok(item) -> wisp.json_response(to_json(item), 201)
    Error(ValidationError(msg)) -> wisp.bad_request(msg)
    Error(DecodeError(_)) -> wisp.unprocessable_content()
    Error(DbError(_)) -> wisp.internal_server_error()
  }
}
```

### HTML Escaping

```gleam
// ALWAYS escape user input in HTML
let name = wisp.escape_html(user_input)
let html = "<p>Hello, " <> name <> "!</p>"
```

## References

- [Wisp Documentation](https://hexdocs.pm/wisp/)
- [Wisp Examples](https://github.com/lpil/wisp/tree/main/examples)
- [Mist Documentation](https://hexdocs.pm/mist/)
- [Gleam JSON](https://hexdocs.pm/gleam_json/)
