# Rust Error Handling Patterns

## Table of Contents

1. [Result and Option Types](#result-and-option-types)
2. [The ? Operator](#the--operator)
3. [Custom Error Types](#custom-error-types)
4. [thiserror Crate](#thiserror-crate)
5. [anyhow Crate](#anyhow-crate)
6. [Panic vs Result](#panic-vs-result)
7. [Error Conversion](#error-conversion)
8. [Async Error Handling](#async-error-handling)

## Result and Option Types

### Basic Result Usage

```rust
use std::fs::File;
use std::io::Read;

fn read_file(path: &str) -> Result<String, std::io::Error> {
    let mut file = File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

// Matching on Result
match read_file("data.txt") {
    Ok(contents) => println!("File contents: {}", contents),
    Err(error) => eprintln!("Error reading file: {}", error),
}
```

### Option Type

```rust
fn find_user(id: u32) -> Option<User> {
    database.get(&id).cloned()
}

// Matching on Option
match find_user(123) {
    Some(user) => println!("Found user: {}", user.name),
    None => println!("User not found"),
}

// Using unwrap_or and unwrap_or_else
let user = find_user(123).unwrap_or_default();
let user = find_user(123).unwrap_or_else(|| create_default_user());
```

### Converting Option to Result

```rust
fn get_user(id: u32) -> Result<User, String> {
    find_user(id).ok_or_else(|| format!("User {} not found", id))
}

// Or with a specific error type
fn get_user(id: u32) -> Result<User, NotFoundError> {
    find_user(id).ok_or(NotFoundError::new("User", &id.to_string()))
}
```

## The ? Operator

### Basic ? Usage

```rust
use std::fs::File;
use std::io::{self, Read};

fn read_file(path: &str) -> io::Result<String> {
    let mut file = File::open(path)?;  // Returns early if error
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;  // Returns early if error
    Ok(contents)
}
```

### ? with Option

```rust
fn get_user_email(id: u32) -> Option<String> {
    let user = find_user(id)?;  // Returns None if user not found
    let email = user.email?;    // Returns None if email is None
    Some(email)
}
```

### Chaining with ?

```rust
fn process_user(id: u32) -> Result<ProcessedUser, Error> {
    let user = fetch_user(id)?;
    let validated = validate_user(&user)?;
    let processed = process_data(&validated)?;
    save_to_database(&processed)?;
    Ok(processed)
}
```

## Custom Error Types

### Manual Error Implementation

```rust
use std::fmt;

#[derive(Debug)]
pub struct NotFoundError {
    resource: String,
    identifier: String,
}

impl NotFoundError {
    pub fn new(resource: &str, identifier: &str) -> Self {
        Self {
            resource: resource.to_string(),
            identifier: identifier.to_string(),
        }
    }
}

impl fmt::Display for NotFoundError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{} not found: {}", self.resource, self.identifier)
    }
}

impl std::error::Error for NotFoundError {}

// Usage
fn get_user(id: u32) -> Result<User, NotFoundError> {
    database.get(&id)
        .ok_or_else(|| NotFoundError::new("User", &id.to_string()))
}
```

### Enum Error Type

```rust
use std::fmt;
use std::io;

#[derive(Debug)]
pub enum AppError {
    NotFound { resource: String, id: String },
    Validation { field: String, message: String },
    Database(String),
    Io(io::Error),
    External { service: String, message: String },
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            AppError::NotFound { resource, id } => {
                write!(f, "{} not found: {}", resource, id)
            }
            AppError::Validation { field, message } => {
                write!(f, "Validation error on {}: {}", field, message)
            }
            AppError::Database(msg) => write!(f, "Database error: {}", msg),
            AppError::Io(err) => write!(f, "IO error: {}", err),
            AppError::External { service, message } => {
                write!(f, "{} error: {}", service, message)
            }
        }
    }
}

impl std::error::Error for AppError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            AppError::Io(err) => Some(err),
            _ => None,
        }
    }
}

// Conversion from io::Error
impl From<io::Error> for AppError {
    fn from(err: io::Error) -> Self {
        AppError::Io(err)
    }
}

// Usage
fn read_user_file(id: u32) -> Result<User, AppError> {
    let path = format!("users/{}.json", id);
    let contents = std::fs::read_to_string(&path)?;  // Auto-converts io::Error

    serde_json::from_str(&contents)
        .map_err(|e| AppError::Validation {
            field: "user_data".to_string(),
            message: e.to_string(),
        })
}
```

## thiserror Crate

### Basic thiserror Usage

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Not found: {resource} with id {id}")]
    NotFound { resource: String, id: String },

    #[error("Validation failed on field {field}: {message}")]
    Validation { field: String, message: String },

    #[error("Database error: {0}")]
    Database(String),

    #[error("IO error")]
    Io(#[from] std::io::Error),

    #[error("JSON parsing error")]
    Json(#[from] serde_json::Error),

    #[error("External service {service} failed: {message}")]
    External { service: String, message: String },
}

// Usage
fn process_user_file(id: u32) -> Result<User, AppError> {
    let path = format!("users/{}.json", id);

    // io::Error automatically converts to AppError::Io
    let contents = std::fs::read_to_string(&path)?;

    // serde_json::Error automatically converts to AppError::Json
    let user: User = serde_json::from_str(&contents)?;

    if !user.is_valid() {
        return Err(AppError::Validation {
            field: "email".to_string(),
            message: "Invalid email format".to_string(),
        });
    }

    Ok(user)
}
```

### Nested Error Chaining

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DatabaseError {
    #[error("Connection failed: {0}")]
    Connection(String),

    #[error("Query failed: {0}")]
    Query(String),

    #[error("Transaction failed: {0}")]
    Transaction(String),
}

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Database error")]
    Database(#[from] DatabaseError),

    #[error("Not found: {0}")]
    NotFound(String),

    #[error("Validation error: {0}")]
    Validation(String),
}

// Usage
fn get_user(id: u32) -> Result<User, AppError> {
    let user = db::find_user(id)?;  // DatabaseError -> AppError

    user.ok_or_else(|| AppError::NotFound(format!("User {}", id)))
}
```

## anyhow Crate

### Basic anyhow Usage

```rust
use anyhow::{Context, Result};

fn read_config() -> Result<Config> {
    let contents = std::fs::read_to_string("config.toml")
        .context("Failed to read config file")?;

    let config: Config = toml::from_str(&contents)
        .context("Failed to parse config")?;

    Ok(config)
}

// Error messages are chained
match read_config() {
    Ok(config) => println!("Config loaded"),
    Err(err) => {
        eprintln!("Error: {}", err);
        // Prints:
        // Failed to parse config
        // Caused by:
        //     invalid TOML value
    }
}
```

### anyhow with Custom Context

```rust
use anyhow::{anyhow, bail, ensure, Context, Result};

fn process_user(id: u32) -> Result<ProcessedUser> {
    // Create error with message
    let user = find_user(id)
        .ok_or_else(|| anyhow!("User {} not found", id))?;

    // Early return with error
    if !user.is_active {
        bail!("User {} is not active", id);
    }

    // Assertion with error
    ensure!(user.age >= 18, "User {} is under 18", id);

    // Add context to errors
    let profile = fetch_profile(&user)
        .context("Failed to fetch user profile")?;

    let processed = process_data(&profile)
        .with_context(|| format!("Failed to process user {}", id))?;

    Ok(processed)
}
```

### Downcast Errors with anyhow

```rust
use anyhow::Result;

fn process() -> Result<()> {
    if let Err(err) = risky_operation() {
        // Check if error is a specific type
        if let Some(not_found) = err.downcast_ref::<NotFoundError>() {
            println!("Resource not found: {}", not_found.resource);
        } else if let Some(validation) = err.downcast_ref::<ValidationError>() {
            println!("Validation failed: {:?}", validation.fields);
        } else {
            println!("Unknown error: {}", err);
        }
    }
    Ok(())
}
```

## Panic vs Result

### When to Use Result

```rust
// Use Result for expected errors
fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        Err("Division by zero".to_string())
    } else {
        Ok(a / b)
    }
}

// Use Result for recoverable errors
fn read_config() -> Result<Config, ConfigError> {
    // Config file might not exist - this is expected
    let contents = std::fs::read_to_string("config.toml")
        .map_err(|e| ConfigError::FileNotFound)?;

    parse_config(&contents)
}
```

### When to Use Panic

```rust
// Panic for programming errors (bugs)
fn get_user_at_index(users: &[User], index: usize) -> &User {
    // Out of bounds is a programming error
    &users[index]  // Will panic if out of bounds
}

// Panic for unrecoverable errors
fn initialize_app() {
    let config = read_config()
        .expect("Config file is required for app to run");

    let db = connect_database(&config.db_url)
        .expect("Cannot run without database");
}

// Use panic! for invariants
fn process_data(data: &[u8]) {
    assert!(!data.is_empty(), "Data must not be empty");
    assert!(data.len() <= MAX_SIZE, "Data exceeds maximum size");

    // Process data...
}
```

### Custom Panic Messages

```rust
// panic! with message
if critical_condition {
    panic!("Critical condition occurred: {}", details);
}

// expect with context
let user = find_user(id)
    .expect("User must exist at this point");

// unwrap for development (remove in production)
let value = some_option.unwrap();  // Bad: loses error context

// Better: use expect
let value = some_option
    .expect("Value should be present after initialization");
```

## Error Conversion

### Manual Error Conversion

```rust
impl From<std::io::Error> for AppError {
    fn from(err: std::io::Error) -> Self {
        AppError::Io(err.to_string())
    }
}

impl From<serde_json::Error> for AppError {
    fn from(err: serde_json::Error) -> Self {
        AppError::Validation {
            field: "json".to_string(),
            message: err.to_string(),
        }
    }
}

// Now ? operator works automatically
fn read_and_parse(path: &str) -> Result<Data, AppError> {
    let contents = std::fs::read_to_string(path)?;  // io::Error -> AppError
    let data = serde_json::from_str(&contents)?;     // serde::Error -> AppError
    Ok(data)
}
```

### map_err for Ad-hoc Conversion

```rust
fn process_file(path: &str) -> Result<Data, AppError> {
    let contents = std::fs::read_to_string(path)
        .map_err(|e| AppError::Io(e.to_string()))?;

    let data: Data = serde_json::from_str(&contents)
        .map_err(|e| AppError::Validation {
            field: "json".to_string(),
            message: e.to_string(),
        })?;

    Ok(data)
}
```

## Async Error Handling

### Async Result

```rust
use tokio::fs::File;
use tokio::io::AsyncReadExt;

async fn read_file_async(path: &str) -> Result<String, std::io::Error> {
    let mut file = File::open(path).await?;
    let mut contents = String::new();
    file.read_to_string(&mut contents).await?;
    Ok(contents)
}

// Usage
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let contents = read_file_async("data.txt").await?;
    println!("File contents: {}", contents);
    Ok(())
}
```

### Async Error Propagation

```rust
async fn fetch_user_async(id: u32) -> Result<User, AppError> {
    let response = reqwest::get(&format!("https://api.example.com/users/{}", id))
        .await
        .map_err(|e| AppError::External {
            service: "User API".to_string(),
            message: e.to_string(),
        })?;

    if response.status() == 404 {
        return Err(AppError::NotFound {
            resource: "User".to_string(),
            id: id.to_string(),
        });
    }

    let user = response.json::<User>()
        .await
        .map_err(|e| AppError::Validation {
            field: "response".to_string(),
            message: e.to_string(),
        })?;

    Ok(user)
}
```

### Concurrent Async Operations

```rust
use tokio::try_join;

async fn fetch_user_data(id: u32) -> Result<(User, Profile, Settings), AppError> {
    // Execute in parallel, fail fast on first error
    let (user, profile, settings) = try_join!(
        fetch_user(id),
        fetch_profile(id),
        fetch_settings(id)
    )?;

    Ok((user, profile, settings))
}

// With partial success
async fn fetch_multiple_users(ids: Vec<u32>) -> (Vec<User>, Vec<AppError>) {
    let futures = ids.into_iter().map(fetch_user);
    let results = futures::future::join_all(futures).await;

    let mut users = Vec::new();
    let mut errors = Vec::new();

    for result in results {
        match result {
            Ok(user) => users.push(user),
            Err(err) => errors.push(err),
        }
    }

    (users, errors)
}
```

## Best Practices Summary

1. **Prefer Result over panic**: Use Result for expected/recoverable errors
2. **Use ? operator**: Propagate errors cleanly instead of explicit matching
3. **Use thiserror for libraries**: Define precise error types
4. **Use anyhow for applications**: Simplify error handling with context
5. **Implement From traits**: Enable automatic error conversion
6. **Add context**: Use `.context()` to add helpful error messages
7. **Don't unwrap in production**: Use proper error handling
8. **Match on errors**: Handle different error cases appropriately
9. **Document errors**: Document which errors functions can return
10. **Test error paths**: Write tests for all error scenarios

## Comparison: thiserror vs anyhow

**Use thiserror when:**
- Writing a library
- Need precise error types for callers
- Want exhaustive error matching
- Errors are part of public API

**Use anyhow when:**
- Writing an application
- Don't need to expose error types
- Want to add context easily
- Want simpler error handling

**Example combining both:**

```rust
// Library code: Use thiserror for precise errors
use thiserror::Error;

#[derive(Error, Debug)]
pub enum LibraryError {
    #[error("Configuration error: {0}")]
    Config(String),

    #[error("Database error: {0}")]
    Database(String),
}

pub fn library_function() -> Result<(), LibraryError> {
    // ...
}

// Application code: Use anyhow for convenience
use anyhow::{Context, Result};

fn app_function() -> Result<()> {
    library_function()
        .context("Failed to execute library function")?;

    Ok(())
}
```
