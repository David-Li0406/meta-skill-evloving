# Essential Rust Crates

Guide to commonly used crates across all Rust projects.

## Error Handling

### anyhow
**Application-level error handling**

```toml
anyhow = "1.0"
```

```rust
use anyhow::{Result, Context, bail, ensure};

fn load_config() -> Result<Config> {
    let contents = std::fs::read_to_string("config.toml")
        .context("Failed to read config file")?;

    let config: Config = toml::from_str(&contents)
        .context("Failed to parse config")?;

    ensure!(config.port > 1024, "Port must be > 1024");

    Ok(config)
}
```

### thiserror
**Library-level custom errors**

```toml
thiserror = "1.0"
```

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DataError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Parse error: {0}")]
    Parse(#[from] serde_json::Error),

    #[error("Invalid data: {0}")]
    Invalid(String),

    #[error("Not found: {field} = {value}")]
    NotFound { field: String, value: String },
}
```

## Serialization

### serde
**Serialize/deserialize data**

```toml
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
```

```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
struct User {
    name: String,
    age: u32,
    #[serde(skip_serializing_if = "Option::is_none")]
    email: Option<String>,
    #[serde(rename = "userId")]
    id: u64,
}

// JSON
let json = serde_json::to_string(&user)?;
let user: User = serde_json::from_str(&json)?;

// Other formats: toml, yaml, bincode, msgpack
```

## Async Runtime

### tokio
**Async runtime**

```toml
tokio = { version = "1.0", features = ["full"] }
```

```rust
#[tokio::main]
async fn main() {
    let result = async_operation().await;
}

// Spawn tasks
let handle = tokio::spawn(async {
    expensive_work().await
});

// Timeouts
use tokio::time::{timeout, Duration};
let result = timeout(Duration::from_secs(5), operation()).await?;

// Channels
use tokio::sync::mpsc;
let (tx, mut rx) = mpsc::channel(32);
```

## HTTP Clients

### reqwest
**HTTP client**

```toml
reqwest = { version = "0.11", features = ["json"] }
```

```rust
// GET request
let response = reqwest::get("https://api.example.com/data")
    .await?
    .json::<ApiResponse>()
    .await?;

// POST request
let client = reqwest::Client::new();
let response = client
    .post("https://api.example.com/users")
    .json(&user)
    .send()
    .await?;
```

## Date/Time

### chrono
**Date and time handling**

```toml
chrono = "0.4"
```

```rust
use chrono::{DateTime, Utc, Duration};

let now = Utc::now();
let tomorrow = now + Duration::days(1);

// Parse
let dt = DateTime::parse_from_rfc3339("2024-01-01T12:00:00Z")?;

// Format
println!("{}", now.format("%Y-%m-%d %H:%M:%S"));
```

## UUIDs

### uuid
**Generate UUIDs**

```toml
uuid = { version = "1.0", features = ["v4", "serde"] }
```

```rust
use uuid::Uuid;

let id = Uuid::new_v4();
println!("{}", id);  // e.g., 550e8400-e29b-41d4-a716-446655440000
```

## Regular Expressions

### regex
**Regular expressions**

```toml
regex = "1.10"
```

```rust
use regex::Regex;

let re = Regex::new(r"^\d{4}-\d{2}-\d{2}$").unwrap();
assert!(re.is_match("2024-01-01"));

// Capture groups
let re = Regex::new(r"(\d+)-(\d+)-(\d+)").unwrap();
let caps = re.captures("2024-01-01").unwrap();
let year = &caps[1];
```

## Collections

### indexmap
**Ordered HashMap**

```toml
indexmap = "2.2"
```

```rust
use indexmap::IndexMap;

let mut map = IndexMap::new();
map.insert("first", 1);
map.insert("second", 2);

// Maintains insertion order
for (key, value) in &map {
    println!("{}: {}", key, value);
}
```

## Utilities

### itertools
**Iterator extras**

```toml
itertools = "0.12"
```

```rust
use itertools::Itertools;

// Chunks
let chunks: Vec<_> = data.iter().chunks(3).collect();

// Unique
let unique: Vec<_> = data.iter().unique().collect();

// Cartesian product
for (a, b) in (0..3).cartesian_product(0..3) {
    println!("{}, {}", a, b);
}
```

### once_cell
**Lazy statics**

```toml
once_cell = "1.19"
```

```rust
use once_cell::sync::Lazy;

static CONFIG: Lazy<Config> = Lazy::new(|| {
    Config::load().expect("Failed to load config")
});
```

## Random Numbers

### rand
**Random number generation**

```toml
rand = "0.8"
```

```rust
use rand::{thread_rng, Rng};

let mut rng = thread_rng();
let n: u32 = rng.gen();
let n: u32 = rng.gen_range(0..100);

// Shuffle
let mut nums = vec![1, 2, 3, 4, 5];
nums.shuffle(&mut rng);
```

## CLI

### clap
**Command-line parsing**

```toml
clap = { version = "4.5", features = ["derive"] }
```

```rust
use clap::Parser;

#[derive(Parser)]
struct Cli {
    #[arg(short, long)]
    input: String,
}

let cli = Cli::parse();
```

## Quick Reference

| Category | Crate | Use Case |
|----------|-------|----------|
| Errors (apps) | `anyhow` | Application error handling |
| Errors (libs) | `thiserror` | Library error types |
| Serialization | `serde` + `serde_json` | JSON, TOML, YAML |
| Async runtime | `tokio` | Async/await |
| HTTP client | `reqwest` | Making HTTP requests |
| Date/time | `chrono` | Working with dates |
| UUIDs | `uuid` | Generating UUIDs |
| Regex | `regex` | Pattern matching |
| CLI parsing | `clap` | Command-line arguments |
| Logging | `tracing` | Structured logging |
| Testing | `proptest` | Property-based testing |
| Benchmarking | `criterion` | Performance benchmarks |
