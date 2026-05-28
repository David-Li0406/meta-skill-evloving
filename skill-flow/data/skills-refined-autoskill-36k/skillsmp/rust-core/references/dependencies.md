# Dependency Management in Rust

Best practices for managing dependencies in Cargo-based projects.

## Cargo.toml Basics

### Version Specification

```toml
[dependencies]
# Caret requirement (default): ^1.2.3 means >=1.2.3, <2.0.0
serde = "1.0"

# Tilde requirement: ~1.2.3 means >=1.2.3, <1.3.0
regex = "~1.5"

# Exact version
libc = "=0.2.95"

# Version range
rand = ">0.8, <0.9"

# Wildcard
log = "0.4.*"

# Multiple constraints
openssl = ">=1.0, <2.0"
```

**Recommendation**: Use caret (default) for semantic versioning.

### Features

```toml
[dependencies]
# Specific features
serde = { version = "1.0", features = ["derive"] }

# Optional dependency (becomes a feature)
tokio = { version = "1.0", optional = true }

# No default features
reqwest = { version = "0.11", default-features = false, features = ["json"] }
```

### Source Alternatives

```toml
[dependencies]
# Git dependency
my-lib = { git = "https://github.com/user/my-lib" }

# Specific branch/tag/commit
my-lib = { git = "https://github.com/user/my-lib", branch = "main" }
my-lib = { git = "https://github.com/user/my-lib", tag = "v0.1.0" }
my-lib = { git = "https://github.com/user/my-lib", rev = "abc123" }

# Local path
my-lib = { path = "../my-lib" }

# Alternative registry
my-lib = { version = "1.0", registry = "my-registry" }
```

## Dependency Categories

### Regular Dependencies

Runtime dependencies required by your code.

```toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1.0", features = ["full"] }
anyhow = "1.0"
```

### Dev Dependencies

Only used for tests, benches, and examples.

```toml
[dev-dependencies]
criterion = "0.5"
proptest = "1.0"
mockall = "0.12"
```

### Build Dependencies

Used by `build.rs` scripts.

```toml
[build-dependencies]
cc = "1.0"
bindgen = "0.69"
```

## Feature Management

### Defining Features

```toml
[features]
# Default features
default = ["std", "serde"]

# Feature that enables dependencies
std = []
serde = ["dep:serde", "dep:serde_json"]

# Feature composition
full = ["std", "serde", "async"]
async = ["tokio"]

[dependencies]
serde = { version = "1.0", optional = true }
serde_json = { version = "1.0", optional = true }
tokio = { version = "1.0", optional = true }
```

### Using Features

```rust
#[cfg(feature = "serde")]
use serde::{Serialize, Deserialize};

#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
pub struct MyStruct {
    field: String,
}
```

## Workspace Dependencies

Centralize dependency versions across a workspace.

```toml
# Root Cargo.toml
[workspace]
members = ["crate-a", "crate-b"]

[workspace.dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1.0", features = ["full"] }
anyhow = "1.0"

# Member Cargo.toml
[dependencies]
serde.workspace = true
tokio.workspace = true
anyhow.workspace = true

# Override workspace dependency
tokio = { workspace = true, features = ["macros"] }
```

## Version Management

### Semantic Versioning

- **0.0.x**: Initial development, anything can change
- **0.x.y**: Pre-1.0, minor version can break compatibility
- **x.y.z**: Stable API
  - **x**: Breaking changes
  - **y**: New features, backwards compatible
  - **z**: Bug fixes

### Updating Dependencies

```bash
# Show outdated dependencies
cargo outdated

# Update to latest compatible versions
cargo update

# Update specific dependency
cargo update -p serde

# Update to latest (may break)
cargo update --aggressive
```

### Cargo.lock

- **Libraries**: Add `Cargo.lock` to `.gitignore`
- **Applications**: Commit `Cargo.lock` to ensure reproducible builds

```gitignore
# For libraries
Cargo.lock

# For applications, do NOT ignore Cargo.lock
```

## Security Best Practices

### Using cargo-audit

```bash
# Install
cargo install cargo-audit

# Check for vulnerabilities
cargo audit

# Fix vulnerabilities
cargo audit fix
```

### Using cargo-deny

```toml
# deny.toml
[advisories]
vulnerability = "deny"
unmaintained = "warn"

[licenses]
unlicensed = "deny"
allow = ["MIT", "Apache-2.0", "BSD-3-Clause"]

[bans]
multiple-versions = "warn"
deny = [
    { name = "openssl", wrappers = ["native-tls"] }
]
```

```bash
cargo install cargo-deny
cargo deny check
```

## Dependency Minimization

### Audit Dependencies

```bash
# Show dependency tree
cargo tree

# Show specific dependency
cargo tree -p serde

# Show duplicates
cargo tree --duplicates

# Reverse dependencies
cargo tree -i serde
```

### Avoiding Duplicate Dependencies

**Problem**: Multiple versions of the same crate.

```bash
$ cargo tree --duplicates
serde v1.0.130
serde v1.0.125
```

**Solution**: Use `[patch]` or update dependencies.

```toml
[patch.crates-io]
# Force all crates to use same version
serde = "1.0.130"
```

### Opt Out of Default Features

```toml
[dependencies]
# Large dependency with many features
reqwest = { version = "0.11", default-features = false, features = ["json"] }
```

## Dependency Groups Pattern

Organize related dependencies.

```toml
[dependencies]
# Core
serde = { version = "1.0", features = ["derive"] }
anyhow = "1.0"

# Async
tokio = { version = "1.0", features = ["full"] }
async-trait = "0.1"

# Web
axum = "0.7"
tower = "0.4"

# Database
sqlx = { version = "0.7", features = ["postgres"] }

# Testing (dev-only)
[dev-dependencies]
tokio-test = "0.4"
mockall = "0.12"
```

## Vendoring Dependencies

For offline builds or security.

```bash
# Create vendor directory
cargo vendor

# Configure .cargo/config.toml
mkdir -p .cargo
cat > .cargo/config.toml <<EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF
```

## Dependency Anti-Patterns

### Kitchen Sink Dependencies

**Bad**: Including large dependencies for single functions.

```toml
[dependencies]
tokio = { version = "1.0", features = ["full"] }  # Huge dependency
```

**Good**: Only enable needed features.

```toml
[dependencies]
tokio = { version = "1.0", features = ["rt-multi-thread", "macros"] }
```

### Transitive Dependencies

**Bad**: Relying on transitive dependencies.

```rust
// Using serde::Serialize from transitive dependency
use serde::Serialize;  // serde comes from another crate
```

**Good**: Explicitly declare all direct dependencies.

```toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }
```

### Outdated Dependencies

**Bad**: Never updating dependencies.

**Good**: Regular updates, security audits.

```bash
# Check for updates weekly
cargo outdated
cargo audit
```

## Best Practices Summary

1. **Use semantic versioning**: Specify versions with caret (^)
2. **Minimize features**: Only enable what you need
3. **Audit regularly**: Use `cargo-audit` and `cargo-deny`
4. **Avoid duplicates**: Check `cargo tree --duplicates`
5. **Lock for applications**: Commit `Cargo.lock` for binaries
6. **Don't lock for libraries**: Ignore `Cargo.lock` in libraries
7. **Document MSRV**: Specify minimum Rust version in `Cargo.toml`
8. **Use workspace dependencies**: Share versions across workspace
9. **Feature gates**: Make heavy dependencies optional
10. **Regular updates**: Keep dependencies current for security

## Useful Commands Reference

```bash
# Check for outdated deps
cargo outdated

# Update dependencies
cargo update

# Security audit
cargo audit

# Check licenses and bans
cargo deny check

# Show dependency tree
cargo tree

# Find duplicates
cargo tree --duplicates

# Find why a dep is included
cargo tree -i <dependency-name>

# Build with specific features
cargo build --features "serde async"

# Build with all features
cargo build --all-features

# Build with no default features
cargo build --no-default-features
```
