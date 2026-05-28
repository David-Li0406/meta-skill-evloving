# Rust Error Handling Patterns

## Result and Option

### Basic Result Usage

```rust
use std::fs::File;
use std::io::{self, Read};

// Explicit error handling
fn read_file_explicit(path: &str) -> Result<String, io::Error> {
    let mut file = match File::open(path) {
        Ok(f) => f,
        Err(e) => return Err(e),
    };

    let mut contents = String::new();
    match file.read_to_string(&mut contents) {
        Ok(_) => Ok(contents),
        Err(e) => Err(e),
    }
}

// Idiomatic with ? operator
fn read_file(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}
```

### Option for Absence

```rust
fn find_user(id: u64) -> Option<User> {
    USERS.get(&id).cloned()
}

// Chaining Option operations
fn get_user_email(id: u64) -> Option<String> {
    find_user(id)
        .filter(|u| u.is_active)
        .map(|u| u.email.clone())
}

// Converting Option to Result
fn get_user_or_error(id: u64) -> Result<User, UserError> {
    find_user(id).ok_or(UserError::NotFound(id))
}
```

## Custom Error Types

### Using thiserror

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Parse error: {0}")]
    Parse(#[from] serde_json::Error),

    #[error("Database error: {source}")]
    Database {
        #[from]
        source: sqlx::Error,
    },

    #[error("Validation error: {field} - {message}")]
    Validation { field: String, message: String },

    #[error("Not found: {0}")]
    NotFound(String),

    #[error("Unauthorized")]
    Unauthorized,
}

// Usage
fn process_data(path: &str) -> Result<Data, AppError> {
    let content = std::fs::read_to_string(path)?;  // Auto-converts io::Error
    let data: Data = serde_json::from_str(&content)?;  // Auto-converts parse error

    if !data.is_valid() {
        return Err(AppError::Validation {
            field: "data".to_string(),
            message: "Invalid format".to_string(),
        });
    }

    Ok(data)
}
```

### Using anyhow for Applications

```rust
use anyhow::{anyhow, bail, Context, Result};

// Application code with anyhow
fn process_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .context("Failed to read config file")?;

    let config: Config = toml::from_str(&content)
        .context("Failed to parse config")?;

    if config.name.is_empty() {
        bail!("Config name cannot be empty");
    }

    Ok(config)
}

// Main function with anyhow
fn main() -> Result<()> {
    let config = process_config("config.toml")?;
    run_app(config)?;
    Ok(())
}
```

## Error Checking Patterns

### errors::Is and errors::As

```rust
use std::io;

fn handle_error(err: &AppError) {
    // Check error type
    if let AppError::Io(io_err) = err {
        match io_err.kind() {
            io::ErrorKind::NotFound => println!("File not found"),
            io::ErrorKind::PermissionDenied => println!("Permission denied"),
            _ => println!("IO error: {}", io_err),
        }
    }
}

// With std::error::Error trait
fn handle_dyn_error(err: &dyn std::error::Error) {
    if let Some(io_err) = err.downcast_ref::<io::Error>() {
        println!("IO: {}", io_err);
    } else if let Some(app_err) = err.downcast_ref::<AppError>() {
        println!("App: {}", app_err);
    }
}
```

### Error Chain Inspection

```rust
use anyhow::Result;

fn inspect_error_chain(err: &anyhow::Error) {
    println!("Error: {}", err);

    for (i, cause) in err.chain().enumerate() {
        println!("  Cause {}: {}", i, cause);
    }
}

// Finding root cause
fn find_io_error(err: &anyhow::Error) -> Option<&io::Error> {
    err.chain()
        .find_map(|e| e.downcast_ref::<io::Error>())
}
```

## Propagation Patterns

### Early Return with ?

```rust
fn validate_and_process(input: &str) -> Result<Output, AppError> {
    // Each ? returns early on error
    let parsed = parse_input(input)?;
    let validated = validate(parsed)?;
    let processed = process(validated)?;
    Ok(processed)
}
```

### Try Block (Nightly)

```rust
#![feature(try_blocks)]

fn complex_operation() -> Result<(), AppError> {
    let result: Result<(), AppError> = try {
        let a = operation_a()?;
        let b = operation_b(a)?;
        operation_c(b)?;
    };

    result.map_err(|e| {
        log::error!("Complex operation failed: {}", e);
        e
    })
}
```

### Combining Results

```rust
// Collect all results
fn process_all(items: Vec<Item>) -> Result<Vec<Output>, AppError> {
    items.into_iter()
        .map(process_item)
        .collect()  // Stops at first error
}

// Collect successes and failures
fn process_all_with_errors(items: Vec<Item>) -> (Vec<Output>, Vec<AppError>) {
    let (successes, failures): (Vec<_>, Vec<_>) = items
        .into_iter()
        .map(process_item)
        .partition(Result::is_ok);

    (
        successes.into_iter().map(Result::unwrap).collect(),
        failures.into_iter().map(Result::unwrap_err).collect(),
    )
}
```

## Panic Handling

### When to Panic

```rust
// ✅ Panic: Unrecoverable programming errors
fn get_index(slice: &[i32], index: usize) -> i32 {
    slice[index]  // Panic if out of bounds - bug in caller
}

// ✅ Panic: Invariant violations
fn new_positive(value: i32) -> Positive {
    assert!(value > 0, "Value must be positive");
    Positive(value)
}

// ❌ Don't panic: Recoverable errors
fn read_config(path: &str) -> Result<Config, Error> {
    // Don't panic if file doesn't exist - return Result
}
```

### Catching Panics

```rust
use std::panic;

fn risky_operation() -> Result<(), String> {
    let result = panic::catch_unwind(|| {
        // Code that might panic
        might_panic();
    });

    match result {
        Ok(_) => Ok(()),
        Err(_) => Err("Operation panicked".to_string()),
    }
}
```

## Testing Errors

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_error_type() {
        let result = process("invalid");
        assert!(matches!(result, Err(AppError::Validation { .. })));
    }

    #[test]
    fn test_error_message() {
        let result = process("invalid");
        let err = result.unwrap_err();
        assert!(err.to_string().contains("validation"));
    }

    #[test]
    #[should_panic(expected = "invariant violated")]
    fn test_panic() {
        violate_invariant();
    }
}
```

## Best Practices

| Do | Don't |
|-----|-------|
| Use `?` for propagation | Use `.unwrap()` in production |
| Add context with `.context()` | Return bare errors without context |
| Use `thiserror` for libraries | Use `anyhow` for libraries |
| Use `anyhow` for applications | Create custom errors for apps |
| Panic only for bugs | Panic for user input errors |
| Log errors at boundaries | Log same error multiple times |
