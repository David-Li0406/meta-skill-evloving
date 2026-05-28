---
name: Rust Core
description: Rust language fundamentals, ownership, error handling, and project patterns.
metadata:
  labels: [rust, core, language]
  triggers:
    files: ['Cargo.toml', '**/*.rs']
    keywords: [fn, impl, struct, enum, Result, Option]
---

# Rust Core Standards

## Ownership & Borrowing

1. **Ownership Rules**:
   - Each value has exactly one owner
   - Value dropped when owner goes out of scope
   - **Do**: Move or clone explicitly when needed
   - **Don't**: Fight the borrow checker with unsafe

2. **Borrowing**:
   - Immutable: `&T` - multiple allowed
   - Mutable: `&mut T` - only one, no immutable refs
   - **Rule**: References must not outlive data

## Error Handling

```rust
// Use Result for recoverable errors
fn parse_config(path: &str) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)?;
    toml::from_str(&content).map_err(ConfigError::Parse)
}

// Use Option for optional values
fn find_user(id: u64) -> Option<User> { /* ... */ }

// Custom error types
#[derive(Debug, thiserror::Error)]
enum AppError {
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),
    #[error("not found: {0}")]
    NotFound(String),
}
```

**Patterns**:
- `?` operator for propagation
- `thiserror` for library errors
- `anyhow` for application errors
- **Never**: `unwrap()` in production code (use `expect` with context)

## Async/Await

- **Runtime**: Tokio for production
- **Rule**: Async functions return `Future`, need executor

```rust
#[tokio::main]
async fn main() {
    let result = fetch_data().await;
}

async fn fetch_data() -> Result<Data, Error> {
    let response = reqwest::get("https://api.example.com").await?;
    response.json().await.map_err(Into::into)
}
```

**Concurrency Patterns**:
- `tokio::spawn` for background tasks
- `tokio::select!` for racing futures
- `tokio::sync::Mutex` for shared async state
- **Warning**: `std::sync::Mutex` blocks; use `tokio::sync` in async

## Traits & Generics

```rust
// Define trait bounds
fn process<T: Serialize + Debug>(item: T) -> String { /* ... */ }

// Impl blocks
impl<T: Clone> Container<T> {
    fn duplicate(&self) -> Self { /* ... */ }
}

// Associated types for clarity
trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}
```

**Best Practices**:
- Prefer `impl Trait` for return types
- Use `where` clauses for complex bounds
- `#[derive]` for common traits: `Debug, Clone, PartialEq`

## Project Structure

```
my-project/
├── Cargo.toml
├── src/
│   ├── main.rs          # Entry point
│   ├── lib.rs           # Library root (optional)
│   ├── config.rs        # Configuration
│   ├── error.rs         # Error types
│   ├── handlers/        # Request handlers
│   │   └── mod.rs
│   └── models/          # Data structures
│       └── mod.rs
└── tests/
    └── integration.rs   # Integration tests
```

**Conventions**:
- `mod.rs` for module roots
- `pub` only what's needed
- Re-export with `pub use` at module root

## Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse() {
        let result = parse("valid");
        assert_eq!(result, Ok(Expected));
    }

    #[tokio::test]
    async fn test_async_fn() {
        let data = fetch().await;
        assert!(data.is_ok());
    }
}
```

- Unit tests in same file with `#[cfg(test)]`
- Integration tests in `tests/` directory
- Use `mockall` for mocking traits

## Security

1. **Input Validation**: Validate all external input before processing
2. **SQL Injection**: Use parameterized queries (sqlx, diesel)
3. **Dependencies**: Run `cargo audit` regularly
4. **Unsafe**: Minimize `unsafe` blocks, document invariants
5. **Secrets**: Use `secrecy` crate for sensitive data in memory
