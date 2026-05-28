---
id: rust-error-handling
name: "Rust Error Handling"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Rust Error Handling

## Overview

Rust uses Result and Option types for explicit error handling, avoiding exceptions and null pointer issues. This methodology covers idiomatic error handling patterns, custom error types, and the error ecosystem.

## When to Use

- All Rust projects
- Functions that can fail
- API design with clear error contracts
- Library development
- Application error handling

## Key Principles

1. **Explicit errors** - Result<T, E> for fallible operations
2. **No null** - Option<T> for optional values
3. **Propagate with ?** - Ergonomic error propagation
4. **Custom error types** - Domain-specific errors
5. **Recoverable vs unrecoverable** - Result vs panic

## Best Practices

### Result and Option Basics

```rust
use std::fs::File;
use std::io::{self, Read};

// Result<T, E> for fallible operations
fn read_file(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

// Option<T> for optional values
fn find_user(id: u64) -> Option<User> {
    users.iter().find(|u| u.id == id).cloned()
}

// Combining Result and Option
fn get_user_email(id: u64) -> Result<Option<String>, DbError> {
    let user = db.find_user(id)?; // Propagate error
    Ok(user.map(|u| u.email)) // Map Option
}
```

### Error Propagation with ?

```rust
use std::fs;
use std::io;

// The ? operator propagates errors
fn read_username() -> Result<String, io::Error> {
    let mut username = String::new();
    fs::File::open("username.txt")?
        .read_to_string(&mut username)?;
    Ok(username)
}

// ? works with Option too (returns None early)
fn first_word(s: &str) -> Option<&str> {
    let bytes = s.as_bytes();
    let pos = bytes.iter().position(|&b| b == b' ')?;
    Some(&s[..pos])
}

// Converting between Result and Option
fn get_value() -> Result<i32, &'static str> {
    let opt: Option<i32> = Some(42);
    opt.ok_or("value not found") // Option -> Result
}

fn maybe_get_value() -> Option<i32> {
    let res: Result<i32, &'static str> = Ok(42);
    res.ok() // Result -> Option (discards error)
}
```

### Custom Error Types

```rust
use std::fmt;

// Simple error enum
#[derive(Debug)]
pub enum AppError {
    NotFound(String),
    Unauthorized,
    Validation(String),
    Database(String),
    Internal(String),
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AppError::NotFound(msg) => write!(f, "not found: {}", msg),
            AppError::Unauthorized => write!(f, "unauthorized"),
            AppError::Validation(msg) => write!(f, "validation error: {}", msg),
            AppError::Database(msg) => write!(f, "database error: {}", msg),
            AppError::Internal(msg) => write!(f, "internal error: {}", msg),
        }
    }
}

impl std::error::Error for AppError {}

// Convert from other errors
impl From<sqlx::Error> for AppError {
    fn from(err: sqlx::Error) -> Self {
        AppError::Database(err.to_string())
    }
}

impl From<std::io::Error> for AppError {
    fn from(err: std::io::Error) -> Self {
        AppError::Internal(err.to_string())
    }
}

// Usage
fn get_user(id: &str) -> Result<User, AppError> {
    let user = db.find_user(id)?; // sqlx::Error -> AppError
    user.ok_or_else(|| AppError::NotFound(format!("user {}", id)))
}
```

### Using thiserror Crate

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum UserError {
    #[error("user not found: {0}")]
    NotFound(String),

    #[error("invalid email format: {email}")]
    InvalidEmail { email: String },

    #[error("database error")]
    Database(#[from] sqlx::Error),

    #[error("validation failed")]
    Validation(#[from] ValidationError),

    #[error(transparent)]
    Other(#[from] anyhow::Error),
}

#[derive(Error, Debug)]
pub enum ValidationError {
    #[error("field {field} is required")]
    Required { field: String },

    #[error("field {field} must be at least {min} characters")]
    TooShort { field: String, min: usize },

    #[error("field {field} must be at most {max} characters")]
    TooLong { field: String, max: usize },
}
```

### Using anyhow for Applications

```rust
use anyhow::{anyhow, bail, Context, Result};

// anyhow::Result for application code
fn run_app() -> Result<()> {
    let config = load_config()
        .context("failed to load configuration")?;

    let db = connect_db(&config.database_url)
        .context("failed to connect to database")?;

    if config.port == 0 {
        bail!("invalid port configuration");
    }

    start_server(config.port)?;
    Ok(())
}

// Adding context to errors
fn process_file(path: &str) -> Result<String> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("failed to read file: {}", path))?;

    parse_content(&content)
        .with_context(|| format!("failed to parse file: {}", path))
}

// Creating errors
fn validate(input: &str) -> Result<()> {
    if input.is_empty() {
        return Err(anyhow!("input cannot be empty"));
    }
    Ok(())
}

// Downcasting errors
fn handle_error(err: anyhow::Error) {
    if let Some(db_err) = err.downcast_ref::<sqlx::Error>() {
        println!("Database error: {}", db_err);
    } else if let Some(io_err) = err.downcast_ref::<std::io::Error>() {
        println!("IO error: {}", io_err);
    } else {
        println!("Other error: {}", err);
    }
}
```

### Result Combinators

```rust
fn main() {
    // map: transform success value
    let result: Result<i32, &str> = Ok(2);
    let doubled = result.map(|v| v * 2); // Ok(4)

    // map_err: transform error value
    let result: Result<i32, i32> = Err(1);
    let string_err = result.map_err(|e| format!("error code: {}", e));

    // and_then: chain fallible operations
    let result: Result<i32, &str> = Ok(2);
    let chained = result.and_then(|v| {
        if v > 0 { Ok(v * 2) } else { Err("must be positive") }
    });

    // or_else: provide fallback
    let result: Result<i32, &str> = Err("error");
    let fallback = result.or_else(|_| Ok(0));

    // unwrap_or: default value on error
    let result: Result<i32, &str> = Err("error");
    let value = result.unwrap_or(0);

    // unwrap_or_else: lazy default
    let result: Result<i32, &str> = Err("error");
    let value = result.unwrap_or_else(|_| expensive_default());
}
```

### Option Combinators

```rust
fn main() {
    // map: transform Some value
    let opt: Option<i32> = Some(2);
    let doubled = opt.map(|v| v * 2); // Some(4)

    // and_then (flatMap): chain Options
    let opt: Option<String> = Some("42".to_string());
    let parsed = opt.and_then(|s| s.parse::<i32>().ok());

    // or: provide alternative
    let opt: Option<i32> = None;
    let alternative = opt.or(Some(0));

    // or_else: lazy alternative
    let opt: Option<i32> = None;
    let alternative = opt.or_else(|| compute_default());

    // filter: conditional Some
    let opt: Option<i32> = Some(3);
    let filtered = opt.filter(|&v| v > 5); // None

    // take: move value out, leaving None
    let mut opt = Some(5);
    let taken = opt.take(); // taken = Some(5), opt = None

    // replace: swap value
    let mut opt = Some(5);
    let old = opt.replace(10); // old = Some(5), opt = Some(10)
}
```

### Error Handling in Async Code

```rust
use tokio;
use anyhow::Result;

async fn fetch_user(id: &str) -> Result<User> {
    let response = reqwest::get(format!("https://api.example.com/users/{}", id))
        .await
        .context("failed to fetch user")?;

    if !response.status().is_success() {
        bail!("API returned status: {}", response.status());
    }

    let user = response
        .json::<User>()
        .await
        .context("failed to parse user response")?;

    Ok(user)
}

// Collecting results from multiple async operations
async fn fetch_all_users(ids: Vec<String>) -> Result<Vec<User>> {
    let futures: Vec<_> = ids
        .iter()
        .map(|id| fetch_user(id))
        .collect();

    let results = futures::future::join_all(futures).await;

    results.into_iter().collect() // Fails on first error
}

// Continue on error, collect successes
async fn fetch_users_best_effort(ids: Vec<String>) -> Vec<User> {
    let futures: Vec<_> = ids
        .iter()
        .map(|id| fetch_user(id))
        .collect();

    let results = futures::future::join_all(futures).await;

    results.into_iter()
        .filter_map(|r| r.ok())
        .collect()
}
```

### Panic vs Result

```rust
// Use panic for programming errors (bugs)
fn get_element(slice: &[i32], index: usize) -> i32 {
    // Panics if index out of bounds - this is a bug
    slice[index]
}

// Use Result for expected failures
fn parse_port(s: &str) -> Result<u16, ParseIntError> {
    s.parse()
}

// Use expect for unreachable errors
fn main() {
    let config = std::env::var("CONFIG_PATH")
        .expect("CONFIG_PATH environment variable must be set");

    // Or with Result
    let port: u16 = std::env::var("PORT")
        .expect("PORT must be set")
        .parse()
        .expect("PORT must be a valid number");
}

// Unwrap only in tests or when logically guaranteed
#[cfg(test)]
mod tests {
    #[test]
    fn test_something() {
        let result = do_something();
        assert!(result.is_ok());
        let value = result.unwrap();
        assert_eq!(value, expected);
    }
}
```

## Anti-patterns

### Avoid: Unwrap in Production Code

```rust
// BAD - panics on None/Err
let user = get_user(id).unwrap();
let name = user.name.unwrap();

// GOOD - handle errors explicitly
let user = get_user(id)?;
let name = user.name.ok_or(AppError::MissingField("name"))?;

// Or with defaults
let name = user.name.unwrap_or_default();
```

### Avoid: Ignoring Errors

```rust
// BAD - silently ignores error
let _ = save_to_db(data);

// GOOD - at least log
if let Err(e) = save_to_db(data) {
    log::error!("Failed to save: {}", e);
}

// Or propagate
save_to_db(data)?;
```

### Avoid: Stringly Typed Errors

```rust
// BAD - error information lost
fn process() -> Result<(), String> {
    Err("something went wrong".to_string())
}

// GOOD - typed errors
fn process() -> Result<(), ProcessError> {
    Err(ProcessError::InvalidInput { field: "name".to_string() })
}
```

## References

- [The Rust Book - Error Handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html)
- [thiserror crate](https://docs.rs/thiserror)
- [anyhow crate](https://docs.rs/anyhow)
- [Error Handling in Rust](https://blog.burntsushi.net/rust-error-handling/)
