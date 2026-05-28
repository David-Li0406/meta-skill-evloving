---
name: rust-error-handling
description: Use this skill for effective error handling in Rust applications using `anyhow` and `thiserror`.
---

# Rust Error Handling Skill

This skill covers error handling patterns in Rust using `anyhow` for application code and `thiserror` for library/domain-specific errors.

## Result Type
```rust
fn parse_number(s: &str) -> Result<i32, ParseIntError> {
    s.parse()
}

// Use ? operator for propagation
fn process() -> Result<(), Box<dyn std::error::Error>> {
    let num = parse_number("42")?;
    Ok(())
}
```

## Custom Errors with thiserror
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

## When to Use Each

| Crate | Use Case | Returns |
|-------|----------|---------|
| **anyhow** | Application code, internal functions, quick prototyping | `anyhow::Result<T>` |
| **thiserror** | Public APIs, domain errors, when callers need to match on variants | Custom error enum |

**Rule of thumb**: If the error needs to cross a module boundary or callers might want to handle specific cases differently, use `thiserror`. Otherwise, use `anyhow`.

## anyhow

`anyhow` provides a flexible error type for application-level error handling. It wraps any `std::error::Error` and adds context.

### Core API
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
// anyhow! - Create an ad-hoc error
return Err(anyhow!("Failed to parse shortcut: {}", shortcut));

// bail! - Early return with error
if id.is_empty() {
    bail!("Entry not found: {}", id);
}

// ensure! - Return error if condition is false
ensure!(count > 0, "Count must be positive, got {}", count);
```

### Adding Context
Always add context to low-level errors:
```rust
let conn = Connection::open(&db_path)
    .context("Failed to open AI chats database")?;
```

## thiserror

`thiserror` provides derive macros for implementing `std::error::Error`. Use it when you need structured, matchable errors.

### Basic Usage
```rust
#[derive(Error, Debug)]
pub enum ShortcutParseError {
    #[error("shortcut string is empty")]
    Empty,
    
    #[error("shortcut has no key, only modifiers")]
    MissingKey,
    
    #[error("unknown token '{0}' in shortcut")]
    UnknownToken(String),
    
    #[error("unknown key '{0}'")]
    UnknownKey(String),
}
```

### Attributes
| Attribute | Purpose | Example |
|-----------|---------|---------|
| `#[error("...")]` | Display message with interpolation | `#[error("Not found: {0}")]` |
| `#[from]` | Auto-implement `From<T>` for `?` | `Io(#[from] io::Error)` |
| `#[source]` | Mark error source for chaining | `#[source] source: io::Error` |

## Best Practices
1. **Choose the Right Tool**: Use `anyhow` for internal functions and `thiserror` for public APIs.
2. **Always Add Context**: Provide helpful context for I/O operations.
3. **Use bail! for Early Returns**: Simplifies error handling.
4. **Make thiserror Variants Actionable**: Provide clear messages for users.

## Anti-patterns
- Avoid unwrapping in library code.
- Don't lose error context.
- Use specific error messages instead of generic ones.

## Debug Macro
For "impossible" states, use the `debug_panic!` macro:
```rust
debug_panic!("Invariant violated: counter was {}", counter);
```