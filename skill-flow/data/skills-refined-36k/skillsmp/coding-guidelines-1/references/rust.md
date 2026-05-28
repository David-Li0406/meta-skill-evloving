# Rust Patterns

Patterns and conventions for Rust projects.

## General Principles

- **Simplicity**: Straightforward solutions. No unnecessary intermediate variables—directly invoke/access if used once
- **Functional**: Prefer functional style with iterators, closures, immutability
- **No duplication**: Extract to reusable functions or modules
- **Dependencies**: Check existing crates before adding new. Prefer well-maintained. Document rationale for major ones

## Rust Practices

### Ownership & Borrowing
Prefer borrowing over cloning. Use references when ownership transfer isn't needed:

```rust
// Preferred
fn process(data: &str) -> Result<Output> { ... }

// Avoid unnecessary cloning
fn process(data: String) -> Result<Output> { ... }
```

### Error Handling
Use `Result` and `?` operator. Prefer `thiserror` for library errors, `anyhow` for applications:

```rust
// Library code
#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("invalid input: {0}")]
    InvalidInput(String),
    #[error("io error: {0}")]
    Io(#[from] std::io::Error),
}

// Application code
fn main() -> anyhow::Result<()> {
    let data = std::fs::read_to_string("config.toml")?;
    Ok(())
}
```

### Option Handling
Use combinators over match when simple:

```rust
// Preferred
let name = user.map(|u| u.name).unwrap_or_default();

// Only use match for complex logic
match user {
    Some(u) if u.is_active => process(u),
    Some(_) => skip(),
    None => default(),
}
```

### Type Inference
Let the compiler infer when obvious. Annotate when clarity helps:

```rust
// Infer
let items = vec![1, 2, 3];
let map: HashMap<_, _> = items.into_iter().collect();

// Annotate for clarity
let timeout: Duration = config.timeout.unwrap_or(Duration::from_secs(30));
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Types/Structs/Enums | PascalCase | `OrderEvent`, `UserConfig` |
| Functions/Variables | snake_case | `process_order`, `max_retries` |
| Constants | SCREAMING_SNAKE | `MAX_CONNECTIONS`, `DEFAULT_TIMEOUT` |
| Modules | snake_case | `order_processor.rs` |
| Traits | PascalCase | `Serialize`, `IntoIterator` |

**Descriptive names**: Full names, not abbreviations. Exceptions: `i` (index), `e`/`err` (error), single-letter generics (`T`, `K`, `V`).

## Modules & Visibility

### Module Organization
- One module per file, named after the module
- Use `mod.rs` only for re-exports from submodules
- Prefer flat structure over deep nesting

### Visibility
Minimize public API. Use `pub(crate)` for internal sharing:

```rust
// Public API
pub fn create_order(input: OrderInput) -> Result<Order> { ... }

// Internal only
pub(crate) fn validate_input(input: &OrderInput) -> Result<()> { ... }

// Private helper
fn compute_total(items: &[Item]) -> Decimal { ... }
```

## Functions & Control Flow

### Iterator Chains
Prefer iterators over loops:

```rust
// Preferred
let names: Vec<_> = users
    .iter()
    .filter(|u| u.is_active)
    .map(|u| &u.name)
    .collect();

// Avoid
let mut names = Vec::new();
for u in &users {
    if u.is_active {
        names.push(&u.name);
    }
}
```

### Early Returns
Use early returns to reduce nesting:

```rust
fn process(user: Option<&User>) -> Result<Output> {
    let user = user.ok_or(Error::NotFound)?;
    if !user.is_active {
        return Err(Error::Inactive);
    }
    // Main logic here
    Ok(output)
}
```

### Closures
Use closures for short inline logic. Extract to functions when reused or complex:

```rust
// Inline closure
items.iter().filter(|x| x.value > threshold)

// Extracted for reuse
fn above_threshold(threshold: i32) -> impl Fn(&Item) -> bool {
    move |item| item.value > threshold
}
```

## Struct Patterns

### Field Ordering
Group by purpose: identifiers first, then data, then metadata:

```rust
struct Order {
    // Identifiers
    id: OrderId,
    user_id: UserId,
    // Data
    items: Vec<Item>,
    total: Decimal,
    // Metadata
    created_at: DateTime<Utc>,
    updated_at: DateTime<Utc>,
}
```

### Builder Pattern
Use for structs with many optional fields:

```rust
let config = ConfigBuilder::new()
    .timeout(Duration::from_secs(30))
    .retries(3)
    .build()?;
```

### Default Implementation
Implement `Default` for structs with sensible defaults:

```rust
#[derive(Default)]
struct Config {
    timeout: Duration,  // Uses Duration::default()
    retries: u32,       // Uses 0
}

// Or custom defaults
impl Default for Config {
    fn default() -> Self {
        Self {
            timeout: Duration::from_secs(30),
            retries: 3,
        }
    }
}
```

## Comments

- **When**: Explain "why" not "what"—business logic, workarounds, non-obvious decisions
- **Avoid**: Never restate code. If self-explanatory, no comment needed
- **TODOs**: `// TODO:` with context (optional ticket ref)
- **Doc comments**: Use `///` for public API, include examples when helpful

```rust
/// Processes an order and returns the confirmation.
///
/// # Errors
/// Returns `Error::InvalidInput` if the order is empty.
pub fn process_order(order: Order) -> Result<Confirmation> { ... }
```

## Config & Environment

- Use `std::env` or `dotenvy` for environment variables
- Validate at startup, fail fast on missing config
- Use strongly-typed config structs:

```rust
#[derive(Debug)]
struct Config {
    database_url: String,
    api_key: String,
    port: u16,
}

impl Config {
    fn from_env() -> Result<Self> {
        Ok(Self {
            database_url: std::env::var("DATABASE_URL")?,
            api_key: std::env::var("API_KEY")?,
            port: std::env::var("PORT")?.parse()?,
        })
    }
}
```
