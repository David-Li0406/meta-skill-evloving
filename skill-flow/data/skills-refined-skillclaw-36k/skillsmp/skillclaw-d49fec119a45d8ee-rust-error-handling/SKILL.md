---
name: rust-error-handling
description: Use this skill when you need to handle errors in Rust applications using `anyhow` for application-level errors and `thiserror` for library-specific errors.
---

# Rust Error Handling Skill

## Overview
This skill covers error handling patterns in Rust using `anyhow` for application code and `thiserror` for library/domain-specific errors. It provides guidelines on when to use each crate and examples of their usage.

## When to Use Each

| Crate      | Use Case                                                        | Returns                     |
|------------|-----------------------------------------------------------------|-----------------------------|
| **anyhow** | Application code, internal functions, quick prototyping        | `anyhow::Result<T>`         |
| **thiserror** | Public APIs, domain errors, when callers need to match on variants | Custom error enum           |

**Rule of thumb**: If the error needs to cross a module boundary or callers might want to handle specific cases differently, use `thiserror`. Otherwise, use `anyhow`.

## Using `anyhow`

`anyhow` provides a flexible error type for application-level error handling. It wraps any `std::error::Error` and adds context.

### Core API Example
```rust
use anyhow::{anyhow, bail, Context, Result};

fn load_config() -> Result<Config> {
    let content = std::fs::read_to_string("config.json")?;
    let config: Config = serde_json::from_str(&content)?;
    Ok(config)
}
```

### Key Macros
```rust
// Create an ad-hoc error
return Err(anyhow!("Failed to parse shortcut: {}", shortcut));

// Early return with error
if id.is_empty() {
    bail!("Entry not found: {}", id);
}

// Return error if condition is false
ensure!(count > 0, "Count must be positive, got {}", count);
```

### Adding Context
Always add context to low-level errors for better debugging:
```rust
let conn = Connection::open(&db_path)
    .context("Failed to open AI chats database")?;
```

## Using `thiserror`

`thiserror` provides derive macros for implementing `std::error::Error`. Use it when you need structured, matchable errors.

### Basic Usage Example
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum MyError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Parse error: {0}")]
    Parse(String),
}
```

## Best Practices
- **Avoid `unwrap`/`expect` in Production**: Instead, use error handling patterns.
  ```rust
  // BAD
  let value = some_option.unwrap();

  // GOOD
  let value = some_option.ok_or(MyError::MissingValue)?;
  ```

### Review Severity
- **CRITICAL**: `unwrap`/`expect` without justification
- **MAJOR**: Missing error handling
- **MINOR**: Could use `?` operator