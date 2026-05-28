# Error Handling Patterns

## Using thiserror (Libraries)

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum UserError {
    #[error("user not found: {0}")]
    NotFound(String),

    #[error("invalid email format")]
    InvalidEmail,

    #[error("database error")]
    Database(#[from] sqlx::Error),

    #[error("validation failed: {field} - {message}")]
    Validation { field: String, message: String },
}

// Usage
fn find_user(id: &str) -> Result<User, UserError> {
    let user = db.find(id).map_err(UserError::Database)?;
    user.ok_or_else(|| UserError::NotFound(id.to_string()))
}
```

## Using anyhow (Applications)

```rust
use anyhow::{Context, Result, bail};

fn process_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .context("failed to read config file")?;

    let config: Config = serde_json::from_str(&content)
        .context("failed to parse config")?;

    if config.port == 0 {
        bail!("port cannot be zero");
    }

    Ok(config)
}

// In main
fn main() -> Result<()> {
    let config = process_config("config.json")?;
    run_server(config)?;
    Ok(())
}
```

## Error Conversion

```rust
// From trait for automatic conversion
impl From<std::io::Error> for AppError {
    fn from(err: std::io::Error) -> Self {
        AppError::Io(err.to_string())
    }
}

// Or use #[from] with thiserror
#[derive(Error, Debug)]
pub enum AppError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Parse error: {0}")]
    Parse(#[from] serde_json::Error),
}
```

## Pattern Matching Errors

```rust
match result {
    Ok(value) => println!("Success: {}", value),
    Err(UserError::NotFound(id)) => println!("User {} not found", id),
    Err(UserError::InvalidEmail) => println!("Invalid email"),
    Err(e) => println!("Other error: {}", e),
}

// Or with if let
if let Err(UserError::NotFound(id)) = result {
    // handle not found
}
```
