---
name: rust
description: "Rust development process and idiomatic code review. Use when writing Rust code, reviewing Rust PRs, debugging ownership or lifetime issues, implementing error handling with thiserror/anyhow, or writing concurrent code. Also use when code uses `.unwrap()` liberally, Clone is used to satisfy the borrow checker, or lifetimes are explicit when they could be elided. Essential for async/await patterns, trait design, iterators, and clippy configuration."
---

# Rust Skill

## Overview

Rust's ownership system is your ally, not your enemy. This skill guides writing idiomatic Rust that works with the compiler, not against it.

**Core principle:** If it compiles, it's probably correct. Rust's strictness is a feature. Don't fight the borrow checker—understand what it's telling you.

## The Rust Development Process

### Phase 1: Design with Ownership

**Before writing implementation:**

1. **Think About Data Ownership**
   - Who owns this data?
   - Who needs to read it?
   - Who needs to mutate it?

2. **Choose the Right Type**
   - Owned: `String`, `Vec<T>`, `Box<T>`
   - Borrowed: `&str`, `&[T]`, `&T`
   - Mutable borrow: `&mut T`

3. **Plan Error Handling**
   - What can fail?
   - Use `Result<T, E>` for recoverable errors
   - Use `Option<T>` for absence of value

### Phase 2: Implement Idiomatically

**Write Rust, not C-in-Rust:**

1. **Propagate Errors with `?`**
   ```rust
   // ✅ Idiomatic error propagation
   fn read_config(path: &str) -> Result<Config, ConfigError> {
       let content = std::fs::read_to_string(path)?;
       let config: Config = toml::from_str(&content)?;
       Ok(config)
   }

   // ❌ Manual error handling
   fn read_config(path: &str) -> Result<Config, ConfigError> {
       let content = match std::fs::read_to_string(path) {
           Ok(c) => c,
           Err(e) => return Err(e.into()),
       };
       // ... more verbose code
   }
   ```

2. **Use Iterators, Not Loops**
   ```rust
   // ✅ Idiomatic
   let sum: i32 = numbers.iter().filter(|&n| n > 0).sum();

   // ❌ Imperative
   let mut sum = 0;
   for n in &numbers {
       if n > 0 {
           sum += n;
       }
   }
   ```

3. **Accept Borrowed, Return Owned**
   ```rust
   // ✅ Flexible API
   fn greet(name: &str) -> String {
       format!("Hello, {}!", name)
   }

   // ❌ Forces allocation on caller
   fn greet(name: String) -> String {
       format!("Hello, {}!", name)
   }
   ```

### Phase 3: Review for Idioms

**Before approving:**

1. **Check Error Handling**
   - No `.unwrap()` in production code?
   - Errors wrapped with context?
   - Custom error types where appropriate?

2. **Check Ownership**
   - Minimal cloning?
   - Borrows instead of moves where possible?
   - Lifetimes elided when possible?

3. **Check Concurrency**
   - `Send` and `Sync` bounds understood?
   - No data races possible?
   - Appropriate sync primitives?

## Red Flags - STOP and Fix

### Error Handling Red Flags

```rust
// Unwrap in production code
let value = something.unwrap();  // Will panic!

// Expect without meaningful message
let value = something.expect("failed");  // Unhelpful

// Ignoring Result
let _ = file.write_all(data);  // Silent failure!

// String error types
fn process() -> Result<(), String> {  // Use proper error types
```

### Ownership Red Flags

```rust
// Clone to satisfy borrow checker
let data = expensive.clone();  // Usually wrong approach
process(data);

// Unnecessary lifetime annotations
fn first<'a>(s: &'a str) -> &'a str {  // Elision works here
    &s[..1]
}

// Rc/RefCell for single-threaded ownership confusion
let data = Rc::new(RefCell::new(vec![]));  // Smell: rethink design

// Box<dyn Trait> when generics work
fn process(handler: Box<dyn Handler>) {  // Prefer generics
```

### Concurrency Red Flags

```rust
// Mutex without Arc in multithreaded context
let mutex = Mutex::new(data);  // Can't share across threads

// Holding lock across await
let guard = mutex.lock().await;
async_operation().await;  // Lock held! Use async-aware mutex

// Thread::spawn without join
thread::spawn(|| work());  // Fire and forget = bug
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "I'll remove the unwraps later" | You won't. Handle errors now. |
| "Clone makes the compiler happy" | Clone hides design problems. Rethink ownership. |
| "Lifetimes are too confusing" | Lifetimes ARE the design. Understand them. |
| "It's just a script" | Scripts become production. Write it right. |
| "unsafe is fine here" | unsafe requires proof of safety. Document it. |
| "The borrow checker is wrong" | The borrow checker is right. Your model is wrong. |

## Rust Quality Checklist

Before approving Rust code:

- [ ] **No unwrap**: `?` operator or proper error handling
- [ ] **Errors contextual**: Using `anyhow` or `thiserror` properly
- [ ] **Minimal cloning**: Borrows preferred where possible
- [ ] **Idiomatic APIs**: Accept &str, return String; accept &[T], return Vec<T>
- [ ] **Iterators used**: Not manual loops for transforms
- [ ] **Clippy clean**: `cargo clippy -- -D warnings`
- [ ] **Tests present**: Unit and integration tests

## Quick Patterns

### Error Handling

```rust
// ✅ With thiserror
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Parse error at line {line}: {message}")]
    Parse { line: usize, message: String },

    #[error("Not found: {0}")]
    NotFound(String),
}

// ✅ With anyhow for applications
use anyhow::{Context, Result};

fn load_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .context("Failed to read config file")?;
    let config: Config = toml::from_str(&content)
        .context("Failed to parse config")?;
    Ok(config)
}
```

### Ownership Patterns

```rust
// ✅ Builder pattern
#[derive(Default)]
pub struct RequestBuilder {
    url: Option<String>,
    timeout: Option<Duration>,
}

impl RequestBuilder {
    pub fn url(mut self, url: impl Into<String>) -> Self {
        self.url = Some(url.into());
        self
    }

    pub fn build(self) -> Result<Request, BuildError> {
        Ok(Request {
            url: self.url.ok_or(BuildError::MissingUrl)?,
            timeout: self.timeout.unwrap_or(Duration::from_secs(30)),
        })
    }
}
```

### Concurrent Patterns

```rust
// ✅ Shared state with Arc<Mutex<T>>
use std::sync::{Arc, Mutex};

let counter = Arc::new(Mutex::new(0));
let handles: Vec<_> = (0..10).map(|_| {
    let counter = Arc::clone(&counter);
    thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    })
}).collect();

for handle in handles {
    handle.join().unwrap();
}
```

## Quick Commands

```bash
# Format
cargo fmt

# Lint (strict)
cargo clippy -- -D warnings

# Test with output
cargo test -- --nocapture

# Check without building
cargo check

# Security audit
cargo audit

# Documentation
cargo doc --open

# Release build
cargo build --release
```

## References

Detailed patterns and examples in `references/`:
- `ownership-patterns.md` - Ownership and borrowing deep dive
- `error-handling.md` - Error handling patterns
- `async-rust.md` - Async/await patterns
