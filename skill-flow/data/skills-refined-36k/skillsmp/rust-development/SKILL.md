---
name: rust-development
description: Use when writing Rust code for memory safety, performance, and systems programming
---

# Rust Development

Guidelines for safe, performant, and idiomatic Rust code.

## When to Use

- Writing new Rust modules or crates
- Refactoring Rust code
- Systems programming tasks
- Performance-critical components
- Concurrent/parallel programming

## Core Principles

1. **Memory Safety** - Leverage ownership system for zero-cost safety
2. **Performance** - Zero-cost abstractions and efficient code
3. **Fearless Concurrency** - Safe parallel programming
4. **Explicit Error Handling** - Use Result<T, E> and Option<T>
5. **Idiomatic Patterns** - Follow Rust conventions

## Ownership and Borrowing

### Basic Ownership Rules
```rust
// Rule 1: Each value has a single owner
let s1 = String::from("hello");
let s2 = s1; // s1 is moved, no longer valid

// Rule 2: Use references to borrow without taking ownership
fn calculate_length(s: &String) -> usize {
    s.len()
} // s goes out of scope but doesn't own the data

// Rule 3: Mutable references are exclusive
let mut s = String::from("hello");
let r1 = &mut s;
// let r2 = &mut s; // ❌ Cannot have two mutable references
```

### Borrowing Patterns
```rust
// Immutable borrows (multiple allowed)
let s = String::from("hello");
let r1 = &s;
let r2 = &s; // ✅ Multiple immutable borrows OK

// Mutable borrow (exclusive access)
let mut s = String::from("hello");
{
    let r1 = &mut s;
    r1.push_str(", world");
} // r1 goes out of scope
println!("{}", s); // ✅ Can use s again
```

## Error Handling

### Result<T, E> Pattern
```rust
use std::fs::File;
use std::io::Read;

// ❌ Don't use unwrap() in production
fn read_file_bad(path: &str) -> String {
    let mut file = File::open(path).unwrap(); // Panics on error
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();
    contents
}

// ✅ Proper error handling
fn read_file_good(path: &str) -> Result<String, std::io::Error> {
    let mut file = File::open(path)?; // ? operator for early return
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

// ✅ Custom error types
#[derive(Debug)]
enum ConfigError {
    Io(std::io::Error),
    Parse(String),
}

impl From<std::io::Error> for ConfigError {
    fn from(err: std::io::Error) -> Self {
        ConfigError::Io(err)
    }
}
```

### Option<T> Pattern
```rust
// ✅ Safe option handling
fn find_user(id: u32) -> Option<User> {
    // Implementation
}

match find_user(123) {
    Some(user) => println!("Found: {}", user.name),
    None => println!("User not found"),
}

// ✅ Combinators for transformation
let user_name = find_user(123)
    .map(|user| user.name)
    .unwrap_or_else(|| "Unknown".to_string());
```

## Memory Management

### Smart Pointers
```rust
use std::rc::Rc;
use std::sync::Arc;
use std::cell::RefCell;

// Reference counting for shared ownership
let data = Rc::new(vec![1, 2, 3]);
let data_clone = Rc::clone(&data); // Increment reference count

// Thread-safe reference counting
let shared_data = Arc::new(vec![1, 2, 3]);
let thread_data = Arc::clone(&shared_data);

// Interior mutability pattern
let data = RefCell::new(vec![1, 2, 3]);
data.borrow_mut().push(4); // Runtime borrow checking
```

### Lifetimes
```rust
// ✅ Explicit lifetime annotations
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

// ✅ Struct with lifetime
struct ImportantExcerpt<'a> {
    part: &'a str,
}

impl<'a> ImportantExcerpt<'a> {
    fn level(&self) -> i32 {
        3
    }
}
```

## Concurrency and Parallelism

### Thread Safety
```rust
use std::sync::{Arc, Mutex};
use std::thread;

// ✅ Shared mutable state with Arc<Mutex<T>>
let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    let handle = thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}
```

### Async/Await
```rust
use tokio;

// ✅ Async function
async fn fetch_data(url: &str) -> Result<String, reqwest::Error> {
    let response = reqwest::get(url).await?;
    let body = response.text().await?;
    Ok(body)
}

// ✅ Concurrent async operations
async fn fetch_multiple() -> Result<Vec<String>, Box<dyn std::error::Error>> {
    let urls = vec!["https://api1.com", "https://api2.com"];
    
    let futures: Vec<_> = urls
        .iter()
        .map(|&url| fetch_data(url))
        .collect();
    
    let results = futures::future::try_join_all(futures).await?;
    Ok(results)
}
```

## Performance Optimization

### Zero-Cost Abstractions
```rust
// ✅ Iterator chains are zero-cost
let sum: i32 = (0..1_000_000)
    .filter(|x| x % 2 == 0)
    .map(|x| x * x)
    .sum();

// ✅ Avoid unnecessary allocations
fn process_data(data: &[u8]) -> Vec<u8> {
    data.iter()
        .copied()
        .filter(|&b| b > 0)
        .collect()
}
```

### Memory Efficiency
```rust
// ✅ Use slices instead of Vec when possible
fn analyze_data(data: &[f64]) -> f64 {
    data.iter().sum::<f64>() / data.len() as f64
}

// ✅ Use Box for large stack data
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(Box<[u8; 1024]>), // Box large arrays
}
```

## Testing

### Unit Tests
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calculation() {
        let result = calculate(2, 2);
        assert_eq!(result, 4);
    }

    #[test]
    #[should_panic(expected = "divide by zero")]
    fn test_divide_by_zero() {
        divide(10, 0);
    }

    #[test]
    fn test_result_handling() -> Result<(), Box<dyn std::error::Error>> {
        let result = risky_operation()?;
        assert_eq!(result, "success");
        Ok(())
    }
}
```

### Property-Based Testing
```rust
use quickcheck::quickcheck;

#[quickcheck]
fn prop_reverse_involutive(xs: Vec<u32>) -> bool {
    let reversed: Vec<_> = xs.iter().rev().rev().cloned().collect();
    xs == reversed
}
```

## Best Practices Checklist

- [ ] Use `cargo clippy` for linting
- [ ] Run `cargo fmt` for formatting
- [ ] Handle all Result/Option cases explicitly
- [ ] Prefer borrowing over taking ownership
- [ ] Use iterators over manual loops
- [ ] Implement proper Error types for libraries
- [ ] Add comprehensive documentation with `///`
- [ ] Use `#[deny(missing_docs)]` for public APIs
- [ ] Profile with `cargo flamegraph` for performance
- [ ] Test with `cargo test` and property-based tests

## Common Patterns

### Builder Pattern
```rust
pub struct Config {
    host: String,
    port: u16,
    timeout: Duration,
}

pub struct ConfigBuilder {
    host: Option<String>,
    port: Option<u16>,
    timeout: Option<Duration>,
}

impl ConfigBuilder {
    pub fn new() -> Self {
        Self {
            host: None,
            port: None,
            timeout: None,
        }
    }

    pub fn host(mut self, host: impl Into<String>) -> Self {
        self.host = Some(host.into());
        self
    }

    pub fn port(mut self, port: u16) -> Self {
        self.port = Some(port);
        self
    }

    pub fn build(self) -> Result<Config, String> {
        Ok(Config {
            host: self.host.ok_or("host is required")?,
            port: self.port.unwrap_or(8080),
            timeout: self.timeout.unwrap_or(Duration::from_secs(30)),
        })
    }
}
```

### State Machine with Types
```rust
pub struct Pending;
pub struct Running;
pub struct Completed;

pub struct Task<State = Pending> {
    id: u32,
    _state: PhantomData<State>,
}

impl Task<Pending> {
    pub fn new(id: u32) -> Self {
        Task {
            id,
            _state: PhantomData,
        }
    }

    pub fn start(self) -> Task<Running> {
        Task {
            id: self.id,
            _state: PhantomData,
        }
    }
}

impl Task<Running> {
    pub fn complete(self) -> Task<Completed> {
        Task {
            id: self.id,
            _state: PhantomData,
        }
    }
}
```

## Anti-Patterns to Avoid

### Don't Fight the Borrow Checker
```rust
// ❌ Over-using Clone to avoid borrowing issues
fn bad_example(data: Vec<String>) -> Vec<String> {
    data.clone() // Unnecessary allocation
}

// ✅ Work with borrowing
fn good_example(data: &[String]) -> Vec<&str> {
    data.iter().map(|s| s.as_str()).collect()
}
```

### Don't Overuse unwrap()
```rust
// ❌ Panic-prone code
let value = risky_operation().unwrap();

// ✅ Handle errors properly
let value = risky_operation().unwrap_or_else(|e| {
    eprintln!("Operation failed: {}", e);
    default_value()
});
```

## Tooling Commands

```bash
# Create new project
cargo new myproject
cargo new mylib --lib

# Check without building
cargo check

# Lint and fix
cargo clippy
cargo clippy -- -W clippy::pedantic

# Format code
cargo fmt

# Run tests
cargo test
cargo test --release

# Benchmark
cargo bench

# Documentation
cargo doc --open

# Profile
cargo install flamegraph
cargo flamegraph --bin mybin
```

## Performance Debugging

```bash
# Compile with optimizations
cargo build --release

# Profile binary size
cargo bloat --release

# Check assembly output
cargo asm myfunction --release

# Memory profiling
valgrind ./target/release/mybin
```

## Remember

> The compiler is your friend. When fighting the borrow checker, step back and consider if your design could be improved rather than working around the constraints.