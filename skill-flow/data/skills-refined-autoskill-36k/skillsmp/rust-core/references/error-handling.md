# Error Handling in Rust

Rust's error handling system is explicit and type-safe, distinguishing between recoverable and unrecoverable errors.

## Core Concepts

### Recoverable vs Unrecoverable Errors

**Unrecoverable Errors**: Use `panic!` for bugs and invariant violations.

```rust
// Unrecoverable: programming error
if index >= vec.len() {
    panic!("Index out of bounds: {} >= {}", index, vec.len());
}

// Or use assertions
assert!(index < vec.len(), "Index out of bounds");
debug_assert!(expensive_check()); // Only in debug builds
```

**Recoverable Errors**: Use `Result<T, E>` for expected failures.

```rust
use std::fs::File;
use std::io::Error;

fn open_file(path: &str) -> Result<File, Error> {
    File::open(path)
}
```

## Result<T, E>

### Basic Usage

```rust
fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("Division by zero".to_string())
    } else {
        Ok(a / b)
    }
}

// Pattern matching
match divide(10.0, 2.0) {
    Ok(result) => println!("Result: {}", result),
    Err(e) => eprintln!("Error: {}", e),
}

// Or use if let
if let Ok(result) = divide(10.0, 2.0) {
    println!("Result: {}", result);
}
```

### Error Propagation

**The `?` operator**: Propagates errors up the call stack.

```rust
use std::fs::File;
use std::io::{self, Read};

fn read_file_contents(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?; // Returns early if Err
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}
```

The `?` operator:
1. If `Ok(v)`, unwraps to `v`
2. If `Err(e)`, returns `Err(e.into())` (with automatic conversion)

### Combining Results

```rust
// Multiple fallible operations
fn process_data(path: &str) -> Result<Data, Error> {
    let contents = read_file(path)?;
    let parsed = parse_data(&contents)?;
    let validated = validate_data(parsed)?;
    Ok(validated)
}
```

## Option<T>

### When to Use Option

Use `Option<T>` for values that might be absent (not an error condition).

```rust
fn find_user(id: u64) -> Option<User> {
    users.get(&id).cloned()
}

// Pattern matching
match find_user(42) {
    Some(user) => println!("Found: {}", user.name),
    None => println!("User not found"),
}

// Chaining with combinators
let user_name = find_user(42)
    .map(|u| u.name)
    .unwrap_or_else(|| "Unknown".to_string());
```

### Option Combinators

```rust
let maybe_number = Some(5);

// map: transform the inner value
let squared = maybe_number.map(|n| n * n); // Some(25)

// and_then (flatMap): chain operations that return Option
let result = maybe_number
    .and_then(|n| if n > 3 { Some(n) } else { None }); // Some(5)

// or: provide alternative Option
let x = None.or(Some(5)); // Some(5)

// filter: conditional inclusion
let even = maybe_number.filter(|&n| n % 2 == 0); // None
```

### Converting Between Option and Result

```rust
let opt: Option<i32> = Some(5);

// Option -> Result
let res: Result<i32, &str> = opt.ok_or("Value was None");

// Result -> Option
let opt2: Option<i32> = res.ok();
```

## Error Type Design

### Simple Errors: Using String

For prototypes and simple cases:

```rust
fn parse_number(s: &str) -> Result<i32, String> {
    s.parse().map_err(|e| format!("Parse error: {}", e))
}
```

**Limitations**: No programmatic error handling, just for display.

### Custom Error Enums

For libraries and production code:

```rust
#[derive(Debug)]
enum DataError {
    Io(std::io::Error),
    Parse(std::num::ParseIntError),
    Validation(String),
}

impl std::fmt::Display for DataError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            DataError::Io(e) => write!(f, "I/O error: {}", e),
            DataError::Parse(e) => write!(f, "Parse error: {}", e),
            DataError::Validation(msg) => write!(f, "Validation error: {}", msg),
        }
    }
}

impl std::error::Error for DataError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            DataError::Io(e) => Some(e),
            DataError::Parse(e) => Some(e),
            DataError::Validation(_) => None,
        }
    }
}

// Enable ? operator conversions
impl From<std::io::Error> for DataError {
    fn from(error: std::io::Error) -> Self {
        DataError::Io(error)
    }
}

impl From<std::num::ParseIntError> for DataError {
    fn from(error: std::num::ParseIntError) -> Self {
        DataError::Parse(error)
    }
}
```

## Using `thiserror`

`thiserror` eliminates boilerplate for custom error types.

```rust
use thiserror::Error;

#[derive(Error, Debug)]
enum DataError {
    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Parse error: {0}")]
    Parse(#[from] std::num::ParseIntError),

    #[error("Validation failed: {0}")]
    Validation(String),

    #[error("Invalid configuration: {key} = {value}")]
    InvalidConfig { key: String, value: String },
}
```

**Benefits**:
- Automatic `Display` implementation using `#[error]` attribute
- Automatic `From` implementations using `#[from]`
- Implements `std::error::Error` automatically
- No runtime cost

**When to use**: Libraries and applications that need well-typed errors.

## Using `anyhow`

`anyhow` provides ergonomic error handling for applications.

```rust
use anyhow::{Result, Context, bail, ensure};

fn process_file(path: &str) -> Result<Data> {
    let contents = std::fs::read_to_string(path)
        .context("Failed to read input file")?;

    ensure!(!contents.is_empty(), "File is empty");

    let data: Data = serde_json::from_str(&contents)
        .context("Failed to parse JSON")?;

    if data.version != EXPECTED_VERSION {
        bail!("Unsupported version: {}", data.version);
    }

    Ok(data)
}
```

**Key Features**:
- `anyhow::Result<T>` = `Result<T, anyhow::Error>`
- `.context()` adds context to errors
- `bail!()` for early return with error
- `ensure!()` like assert but returns error
- Automatic error conversion from any `std::error::Error`

**When to use**: Applications (not libraries) where you want ergonomic error handling.

## thiserror vs anyhow

### Use `thiserror` for Libraries

```rust
// Library code: expose well-typed errors
use thiserror::Error;

#[derive(Error, Debug)]
pub enum MyLibError {
    #[error("Database connection failed")]
    ConnectionFailed(#[from] sqlx::Error),

    #[error("Invalid user ID: {0}")]
    InvalidUserId(String),
}

pub fn library_function() -> Result<(), MyLibError> {
    // Library functions return typed errors
    Err(MyLibError::InvalidUserId("abc".into()))
}
```

### Use `anyhow` for Applications

```rust
// Application code: prioritize ergonomics
use anyhow::{Result, Context};

fn main() -> Result<()> {
    let config = load_config()
        .context("Failed to load configuration")?;

    let db = connect_database(&config.db_url)
        .context("Failed to connect to database")?;

    run_app(db)?;

    Ok(())
}
```

### Mixing Both

```rust
// Library returns typed errors
use my_lib::MyLibError;

// Application converts to anyhow
use anyhow::Result;

fn app_function() -> Result<()> {
    // Automatic conversion from MyLibError to anyhow::Error
    my_lib::library_function()?;
    Ok(())
}
```

## Error Handling Patterns

### Early Returns

```rust
fn validate_user(user: &User) -> Result<(), ValidationError> {
    if user.name.is_empty() {
        return Err(ValidationError::EmptyName);
    }
    if user.age < 18 {
        return Err(ValidationError::Underage);
    }
    if !user.email.contains('@') {
        return Err(ValidationError::InvalidEmail);
    }
    Ok(())
}
```

### Collecting Results

```rust
// Stop at first error
let numbers: Result<Vec<i32>, _> = vec!["1", "2", "three", "4"]
    .iter()
    .map(|s| s.parse::<i32>())
    .collect();

// Partition successes and failures
let results: Vec<Result<i32, _>> = vec!["1", "2", "three", "4"]
    .iter()
    .map(|s| s.parse::<i32>())
    .collect();

let (successes, failures): (Vec<_>, Vec<_>) = results
    .into_iter()
    .partition(Result::is_ok);
```

### Fallback Chains

```rust
fn get_config() -> Config {
    load_config_from_env()
        .or_else(|_| load_config_from_file("config.toml"))
        .or_else(|_| load_config_from_file("/etc/myapp/config.toml"))
        .unwrap_or_else(|_| Config::default())
}
```

### Error Context

```rust
use anyhow::{Context, Result};

fn load_user_data(user_id: u64) -> Result<UserData> {
    let db = connect_db()
        .context("Database connection failed")?;

    let user = db.find_user(user_id)
        .with_context(|| format!("User {} not found", user_id))?;

    let settings = db.load_settings(user_id)
        .with_context(|| format!("Failed to load settings for user {}", user_id))?;

    Ok(UserData { user, settings })
}
```

### Error Recovery

```rust
fn fetch_with_retry(url: &str, max_attempts: u32) -> Result<Response> {
    let mut last_error = None;

    for attempt in 1..=max_attempts {
        match fetch(url) {
            Ok(response) => return Ok(response),
            Err(e) => {
                eprintln!("Attempt {} failed: {}", attempt, e);
                last_error = Some(e);
                if attempt < max_attempts {
                    std::thread::sleep(Duration::from_secs(2u64.pow(attempt)));
                }
            }
        }
    }

    Err(last_error.unwrap())
}
```

## Testing Error Cases

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_division_by_zero() {
        let result = divide(10.0, 0.0);
        assert!(result.is_err());
        assert_eq!(result.unwrap_err(), "Division by zero");
    }

    #[test]
    fn test_error_context() {
        let result = process_file("nonexistent.txt");
        assert!(result.is_err());

        let err = result.unwrap_err();
        let err_msg = format!("{:#}", err); // Pretty-print error chain
        assert!(err_msg.contains("Failed to read input file"));
    }

    #[test]
    #[should_panic(expected = "Index out of bounds")]
    fn test_panic() {
        access_invalid_index();
    }
}
```

## Best Practices

### Do's

1. **Use `Result` for expected failures**: File I/O, network, parsing, validation
2. **Use `Option` for absent values**: Map lookups, first/last element, search
3. **Use `panic!` for programming errors**: Array index out of bounds, invariant violations
4. **Add context to errors**: Use `.context()` or `.with_context()` liberally
5. **Use `?` operator**: Cleaner than manual error propagation
6. **Define custom error types for libraries**: Let consumers handle errors programmatically
7. **Use `anyhow` for applications**: Ergonomic error handling with good error messages

### Don'ts

1. **Don't use `.unwrap()` in production code**: Only in tests, examples, or when you've proven it can't fail
2. **Don't ignore errors**: Always handle or propagate
3. **Don't use `.expect()` without a good message**: The message should explain why it's safe
4. **Don't return generic errors from libraries**: Use typed errors so consumers can handle them
5. **Don't overuse `panic!`**: Reserve for truly unrecoverable situations
6. **Don't catch panics for control flow**: Use `Result` instead

### When to Use What

| Scenario | Use |
|----------|-----|
| Library public API | `Result<T, CustomError>` with `thiserror` |
| Application logic | `anyhow::Result<T>` |
| Value might be absent | `Option<T>` |
| Programming error | `panic!` or `assert!` |
| Prototype/example | `Result<T, Box<dyn Error>>` or `.unwrap()` |
| Error needs context | `.context()` from `anyhow` |
| Performance critical | Custom error enum (no heap allocation) |

## Common Patterns Summary

```rust
// Pattern 1: Simple error propagation
fn f1() -> Result<T, E> {
    let x = operation1()?;
    let y = operation2(x)?;
    Ok(y)
}

// Pattern 2: Error with context
fn f2() -> anyhow::Result<T> {
    let x = operation1()
        .context("Step 1 failed")?;
    let y = operation2(x)
        .with_context(|| format!("Step 2 failed for {}", x))?;
    Ok(y)
}

// Pattern 3: Custom error with From conversion
#[derive(Error, Debug)]
enum MyError {
    #[error("IO error")]
    Io(#[from] std::io::Error),
}

fn f3() -> Result<T, MyError> {
    let file = File::open("file.txt")?; // Auto-converts io::Error
    Ok(process(file))
}

// Pattern 4: Fallible iterator
fn f4() -> Result<Vec<T>, E> {
    items.iter()
        .map(|item| process(item))
        .collect() // Stops at first error
}

// Pattern 5: Option to Result
fn f5(maybe: Option<T>) -> Result<T, MyError> {
    maybe.ok_or(MyError::NotFound)
}
```
