# Rust Project Structure

Best practices for organizing Rust projects, from simple binaries to complex workspaces.

## Basic Project Structure

### Binary Project

```
my-app/
├── Cargo.toml
├── Cargo.lock
├── src/
│   ├── main.rs
│   └── lib.rs (optional)
├── tests/
│   └── integration_test.rs
├── benches/
│   └── benchmark.rs
└── examples/
    └── example.rs
```

### Library Project

```
my-lib/
├── Cargo.toml
├── src/
│   ├── lib.rs
│   └── module.rs
├── tests/
│   └── integration_test.rs
├── examples/
│   └── usage.rs
└── benches/
    └── performance.rs
```

## Module Organization

### Inline Modules

```rust
// src/lib.rs or src/main.rs
mod database {
    pub fn connect() -> Connection {
        // ...
    }
}

mod api {
    pub fn handle_request() {
        // ...
    }
}
```

### File-Based Modules

```
src/
├── lib.rs
├── database.rs
└── api.rs
```

```rust
// src/lib.rs
mod database;
mod api;

pub use database::Database;
pub use api::Router;
```

### Directory-Based Modules

```
src/
├── lib.rs
├── database/
│   ├── mod.rs
│   ├── connection.rs
│   └── query.rs
└── api/
    ├── mod.rs
    ├── routes.rs
    └── middleware.rs
```

```rust
// src/database/mod.rs
mod connection;
mod query;

pub use connection::Connection;
pub use query::Query;

// src/lib.rs
mod database;
mod api;

pub use database::Database;
```

### Modern Module Structure (Rust 2018+)

Instead of `mod.rs`, use the directory name:

```
src/
├── lib.rs
├── database.rs  (or database/)
└── database/
    ├── connection.rs
    └── query.rs
```

```rust
// src/database.rs (replaces database/mod.rs)
mod connection;
mod query;

pub use connection::Connection;
```

## Visibility and API Design

### Public API

```rust
// src/lib.rs
pub mod database {
    pub struct Connection { /* private fields */ }

    impl Connection {
        pub fn new() -> Self { /* ... */ }
        pub fn query(&self, sql: &str) -> Result<Rows> { /* ... */ }

        // Private method
        fn internal_execute(&self, sql: &str) { /* ... */ }
    }
}

// External usage
use my_lib::database::Connection;
```

### Re-exports for Clean API

```rust
// src/lib.rs
mod database;
mod api;
mod utils;

// Flatten the public API
pub use database::{Connection, Query};
pub use api::{Router, Request, Response};
// utils is private

// External usage (clean)
use my_lib::{Connection, Router};
```

### Prelude Pattern

```rust
// src/prelude.rs
pub use crate::database::{Connection, Query};
pub use crate::api::{Router, Request, Response};
pub use crate::error::Error;
pub use crate::Result;

// src/lib.rs
pub mod prelude;

// External usage
use my_lib::prelude::*;
```

## Cargo Workspace

For multi-crate projects.

### Workspace Structure

```
my-workspace/
├── Cargo.toml (workspace manifest)
├── crates/
│   ├── core/
│   │   ├── Cargo.toml
│   │   └── src/
│   ├── api/
│   │   ├── Cargo.toml
│   │   └── src/
│   └── cli/
│       ├── Cargo.toml
│       └── src/
└── Cargo.lock (shared)
```

### Workspace Cargo.toml

```toml
[workspace]
members = [
    "crates/core",
    "crates/api",
    "crates/cli",
]

# Shared dependencies
[workspace.dependencies]
tokio = { version = "1.0", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
anyhow = "1.0"

[workspace.package]
version = "0.1.0"
edition = "2021"
license = "MIT"
authors = ["Your Name <you@example.com>"]
```

### Member Cargo.toml

```toml
[package]
name = "my-workspace-api"
version.workspace = true
edition.workspace = true

[dependencies]
# Use workspace dependency
tokio.workspace = true
serde.workspace = true

# Internal dependency
my-workspace-core = { path = "../core" }

# Crate-specific dependency
axum = "0.7"
```

## Project Layout Examples

### Web Application

```
my-web-app/
├── Cargo.toml
├── src/
│   ├── main.rs
│   ├── lib.rs
│   ├── config.rs
│   ├── error.rs
│   ├── models/
│   │   ├── mod.rs
│   │   ├── user.rs
│   │   └── post.rs
│   ├── db/
│   │   ├── mod.rs
│   │   ├── connection.rs
│   │   └── migrations.rs
│   ├── handlers/
│   │   ├── mod.rs
│   │   ├── auth.rs
│   │   └── posts.rs
│   ├── middleware/
│   │   ├── mod.rs
│   │   ├── auth.rs
│   │   └── logging.rs
│   └── utils/
│       ├── mod.rs
│       └── validation.rs
├── migrations/
│   └── 001_initial.sql
├── tests/
│   └── api_tests.rs
└── static/
    └── index.html
```

### CLI Application

```
my-cli/
├── Cargo.toml
├── src/
│   ├── main.rs
│   ├── cli.rs (argument parsing)
│   ├── commands/
│   │   ├── mod.rs
│   │   ├── init.rs
│   │   └── run.rs
│   ├── config.rs
│   └── utils/
│       ├── mod.rs
│       └── fs.rs
├── tests/
│   └── cli_tests.rs
└── README.md
```

### Library Crate

```
my-lib/
├── Cargo.toml
├── README.md
├── src/
│   ├── lib.rs
│   ├── prelude.rs
│   ├── error.rs
│   ├── core/
│   │   ├── mod.rs
│   │   ├── types.rs
│   │   └── traits.rs
│   ├── io/
│   │   ├── mod.rs
│   │   ├── reader.rs
│   │   └── writer.rs
│   └── utils/
│       ├── mod.rs
│       └── helpers.rs
├── tests/
│   ├── integration_test.rs
│   └── common/
│       └── mod.rs
├── benches/
│   └── performance.rs
└── examples/
    ├── basic.rs
    └── advanced.rs
```

## Common Patterns

### Feature Flags Organization

```
src/
├── lib.rs
├── sync/      # Always available
│   └── mod.rs
└── async/     # Behind "async" feature
    └── mod.rs
```

```rust
// src/lib.rs
pub mod sync;

#[cfg(feature = "async")]
pub mod async;
```

```toml
[features]
default = ["sync"]
async = ["tokio", "async-trait"]
```

### Platform-Specific Code

```
src/
├── lib.rs
├── platform/
│   ├── mod.rs
│   ├── unix.rs
│   └── windows.rs
```

```rust
// src/platform/mod.rs
#[cfg(unix)]
mod unix;
#[cfg(unix)]
pub use unix::*;

#[cfg(windows)]
mod windows;
#[cfg(windows)]
pub use windows::*;
```

### Build Scripts

```
my-project/
├── Cargo.toml
├── build.rs
└── src/
    └── main.rs
```

```rust
// build.rs
fn main() {
    println!("cargo:rerun-if-changed=build.rs");

    // Generate code
    generate_bindings();

    // Set environment variables
    println!("cargo:rustc-env=BUILD_TIME={}", timestamp());

    // Link to C library
    println!("cargo:rustc-link-lib=mylib");
}
```

## Naming Conventions

### Crate Names

- Use kebab-case: `my-awesome-crate`
- Be descriptive but concise
- Avoid generic names

### Module Names

- Use snake_case: `user_management`
- Group related functionality
- Keep hierarchy shallow (3 levels max)

### File Names

- Match module names: `user_management.rs`
- Use snake_case
- Be specific: `database_connection.rs` not `db.rs`

## Documentation Structure

```
my-project/
├── README.md (project overview)
├── CHANGELOG.md
├── LICENSE
├── docs/
│   ├── architecture.md
│   ├── api.md
│   └── contributing.md
└── src/
    └── lib.rs (API documentation)
```

### lib.rs Documentation

```rust
//! # My Library
//!
//! This library provides tools for working with data processing.
//!
//! ## Features
//!
//! - Fast data parsing
//! - Flexible transformation pipeline
//! - Type-safe API
//!
//! ## Examples
//!
//! ```
//! use my_lib::Parser;
//!
//! let parser = Parser::new();
//! let result = parser.parse("input data");
//! ```

#![warn(missing_docs)]
#![warn(rustdoc::broken_intra_doc_links)]

pub mod parser;
pub mod transformer;
```

## Cargo.toml Best Practices

### Complete Manifest

```toml
[package]
name = "my-crate"
version = "0.1.0"
authors = ["Your Name <you@example.com>"]
edition = "2021"
rust-version = "1.70"  # Minimum Rust version
description = "A short description of my crate"
documentation = "https://docs.rs/my-crate"
homepage = "https://github.com/username/my-crate"
repository = "https://github.com/username/my-crate"
license = "MIT OR Apache-2.0"
keywords = ["data", "parsing", "utility"]
categories = ["parsing", "data-structures"]
readme = "README.md"
include = [
    "src/**/*",
    "Cargo.toml",
    "LICENSE*",
    "README.md",
]

[dependencies]
serde = { version = "1.0", features = ["derive"], optional = true }
tokio = { version = "1.0", optional = true }

[dev-dependencies]
criterion = "0.5"
proptest = "1.0"

[features]
default = []
serde-support = ["serde"]
async = ["tokio"]

[[bin]]
name = "my-tool"
path = "src/bin/tool.rs"

[profile.release]
lto = true
codegen-units = 1
strip = true
```

## Anti-Patterns

### Deep Module Nesting

**Bad**:
```
src/api/v1/handlers/users/profile/settings/privacy.rs
```

**Good**:
```
src/api/
├── handlers.rs
└── users/
    ├── profile.rs
    └── settings.rs
```

### Large Single Files

**Bad**: `src/main.rs` with 3000+ lines

**Good**: Split into logical modules

### Circular Dependencies

**Bad**:
```rust
// user.rs
use crate::post::Post;

// post.rs
use crate::user::User;
```

**Good**: Extract shared types
```rust
// types.rs
pub struct UserId(u64);
pub struct PostId(u64);

// user.rs
use crate::types::PostId;

// post.rs
use crate::types::UserId;
```

## Key Takeaways

1. **Keep it flat**: Avoid deep module hierarchies
2. **Use workspaces**: For multi-crate projects
3. **Public API design**: Use re-exports for clean interfaces
4. **Feature flags**: For optional dependencies
5. **Documentation**: Keep README updated, use doc comments
6. **Follow conventions**: snake_case modules, CamelCase types
7. **Organize by feature**: Not by layer (models/, controllers/)
