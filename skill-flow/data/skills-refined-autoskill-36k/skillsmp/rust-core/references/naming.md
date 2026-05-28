# Rust Naming Conventions

Follow Rust's naming conventions for consistent, idiomatic code.

## General Rules

### CamelCase for Types

```rust
// Types: struct, enum, trait
struct UserAccount {}
enum HttpStatus {}
trait Drawable {}

// Type aliases
type UserId = u64;

// Generics
struct Container<T> {}
trait Iterator<Item> {}
```

### snake_case for Values

```rust
// Functions
fn calculate_total() -> f64 {}
fn send_email() -> Result<()> {}

// Variables
let user_name = "Alice";
let max_connections = 100;

// Modules
mod user_management;
mod http_client;
```

### SCREAMING_SNAKE_CASE for Constants

```rust
// Constants
const MAX_BUFFER_SIZE: usize = 1024;
const DEFAULT_TIMEOUT: Duration = Duration::from_secs(30);

// Static variables
static GLOBAL_CONFIG: Mutex<Config> = Mutex::new(Config::default());
```

## Specific Conventions

### Module Names

```rust
// Short, descriptive, singular
mod user;
mod config;
mod database;

// Multi-word: snake_case
mod user_manager;
mod http_client;
mod data_store;
```

### Crate Names

```toml
# Cargo.toml: kebab-case
[package]
name = "my-awesome-library"

# In code: snake_case
use my_awesome_library::Parser;
```

### Feature Names

```toml
[features]
# kebab-case
serde-support = ["dep:serde"]
full-crypto = ["sha2", "aes"]
```

### Method Names

```rust
impl User {
    // Constructors: new, with_*, from_*, default
    fn new(name: String) -> Self {}
    fn with_email(mut self, email: String) -> Self {}
    fn from_id(id: u64) -> Result<Self> {}

    // Conversions: into_*, as_*, to_*
    fn into_bytes(self) -> Vec<u8> {}  // Consumes self
    fn as_str(&self) -> &str {}         // Cheap borrow
    fn to_string(&self) -> String {}    // Expensive clone

    // Getters: just the field name
    fn name(&self) -> &str {}
    fn age(&self) -> u32 {}

    // Setters: set_*
    fn set_name(&mut self, name: String) {}

    // Predicates: is_*, has_*
    fn is_valid(&self) -> bool {}
    fn has_permission(&self, perm: &str) -> bool {}
}
```

### Type Conversions

```rust
// From/Into (infallible)
impl From<String> for Email {
    fn from(s: String) -> Self {
        Email(s)
    }
}

// TryFrom/TryInto (fallible)
impl TryFrom<String> for Email {
    type Error = ValidationError;

    fn try_from(s: String) -> Result<Self, Self::Error> {
        if s.contains('@') {
            Ok(Email(s))
        } else {
            Err(ValidationError::InvalidEmail)
        }
    }
}

// AsRef (cheap reference conversion)
impl AsRef<str> for Email {
    fn as_ref(&self) -> &str {
        &self.0
    }
}
```

### Iterator Methods

```rust
impl MyCollection {
    // Return iterator: iter, iter_mut, into_iter
    fn iter(&self) -> Iter<'_, T> {}
    fn iter_mut(&mut self) -> IterMut<'_, T> {}
    fn into_iter(self) -> IntoIter<T> {}  // Implement IntoIterator trait
}
```

### Builder Pattern

```rust
struct ConfigBuilder;

impl ConfigBuilder {
    fn new() -> Self {}

    // Setters return Self for chaining
    fn host(self, host: String) -> Self {}
    fn port(self, port: u16) -> Self {}

    // Terminal method
    fn build(self) -> Config {}
}
```

### Error Types

```rust
// Error enums: *Error suffix
enum DatabaseError {}
enum ParseError {}

// Result aliases
type Result<T> = std::result::Result<T, Error>;
```

## Trait Naming

### Common Trait Patterns

```rust
// Capability traits: *able suffix
trait Drawable {}
trait Serializable {}
trait Comparable {}

// Conversion traits
trait From<T> {}
trait Into<T> {}
trait TryFrom<T> {}

// Operator traits
trait Add<Rhs = Self> {}
trait Sub<Rhs = Self> {}
```

## Avoiding Stuttering

```rust
// Bad: repetitive names
user::UserManager
http::HttpClient
database::DatabaseConnection

// Good: context is clear from module
user::Manager
http::Client
database::Connection

// Usage makes it clear
use database::Connection as DbConnection;
```

## Abbreviations

### Common Abbreviations (Acceptable)

```rust
fn to_json() -> String {}  // JSON
fn from_xml() -> Self {}   // XML
fn connect_db() -> Conn {} // Database
fn calc_hash() -> u64 {}   // Calculate
fn init_app() {}           // Initialize
```

### Avoid Unclear Abbreviations

```rust
// Bad
fn proc_msg() {}  // Process message?
fn chk_val() {}   // Check value?

// Good
fn process_message() {}
fn validate_value() {}
```

## Lifetime Names

```rust
// Short: 'a, 'b for simple cases
fn first<'a>(s: &'a str) -> &'a str {}

// Descriptive for complex cases
fn merge<'input, 'output>(
    input: &'input Data,
    output: &'output mut Data,
) {}

// Common conventions
'static  // Static lifetime
'_       // Elided lifetime
```

## Generic Type Parameters

```rust
// Single letter for simple cases
struct Container<T> {}
fn map<T, U>(input: T, f: impl Fn(T) -> U) -> U {}

// Descriptive for complex cases
struct Parser<Input, Output, Error> {}

// Common conventions
T: generic type
E: error type
K, V: key, value (for maps)
R: result/return type
```

## Anti-Patterns

### Don't Use get_ Prefix

```rust
// Bad
fn get_name(&self) -> &str {}

// Good
fn name(&self) -> &str {}

// Exception: when there's also a setter
fn name(&self) -> &str {}
fn set_name(&mut self, name: String) {}
```

### Don't Hungarian Notation

```rust
// Bad
let str_name = "Alice";
let i_count = 42;

// Good
let name = "Alice";
let count = 42;
```

### Don't Encode Type in Name

```rust
// Bad
struct UserStruct {}
enum StatusEnum {}

// Good
struct User {}
enum Status {}
```

## Quick Reference

| Item | Convention | Example |
|------|------------|---------|
| Types | `CamelCase` | `UserAccount` |
| Functions | `snake_case` | `calculate_total` |
| Variables | `snake_case` | `user_name` |
| Constants | `SCREAMING_SNAKE_CASE` | `MAX_SIZE` |
| Modules | `snake_case` | `user_manager` |
| Crate names | `kebab-case` | `my-crate` |
| Features | `kebab-case` | `serde-support` |
| Lifetimes | `'lowercase` | `'a`, `'static` |
| Type params | `CamelCase` | `T`, `Error` |
