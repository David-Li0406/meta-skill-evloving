# rustdoc (Rust)

Documentation convention for Rust codebases.

## Overview

Rust uses doc comments (`///` for items, `//!` for modules) that support Markdown. Documentation is tightly integrated with the language—examples are compiled and tested, and docs are generated with `cargo doc`.

## Basic Syntax

```rust
/// Calculate shipping cost for an order.
///
/// Uses tiered pricing based on weight and destination:
/// - Domestic orders under 5kg: standard rates
/// - Larger packages: dimensional weight pricing
/// - International: carrier-specific rate tables
///
/// # Arguments
///
/// * `order` - The order containing items to ship
/// * `dest` - Shipping destination address
///
/// # Returns
///
/// Cost in cents, or `None` if destination is not serviceable.
///
/// # Errors
///
/// Returns `ShippingError::InvalidAddress` if the destination
/// cannot be validated with the postal service.
///
/// # Examples
///
/// ```
/// let order = Order::new(vec![item1, item2]);
/// let dest = Address::new("US", "90210");
/// let cost = calculate_shipping(&order, &dest)?;
/// assert!(cost > 0);
/// ```
pub fn calculate_shipping(order: &Order, dest: &Address) -> Result<u32, ShippingError> {
    // ...
}
```

## Common Sections

| Section | Purpose |
|---------|---------|
| `# Arguments` | Document function parameters |
| `# Returns` | Document return value |
| `# Errors` | Document error conditions |
| `# Panics` | Document panic conditions |
| `# Safety` | Document unsafe preconditions |
| `# Examples` | Show usage (compiled and tested!) |
| `# See Also` | Link to related items |

## Applying Core Principles

### Use Different Vocabulary

```rust
// Bad: Restates the function name
/// Gets a user by their ID.
pub fn get_user(id: UserId) -> Option<User>

// Good: Explains the abstraction
/// Retrieve a user's complete profile from the database.
///
/// The returned `User` includes loaded associations (orders, preferences).
/// Returns `None` if no user exists with the given ID.
///
/// Deactivated accounts are excluded; use [`get_user_admin`] for those.
pub fn get_user(id: UserId) -> Option<User>
```

### Document Non-Obvious Behavior

```rust
/// Process items in batches to manage memory usage.
///
/// Items are loaded lazily from the iterator and processed in groups.
/// Processing continues until the iterator is exhausted or the callback
/// returns `ControlFlow::Break`.
///
/// # Performance
///
/// Memory usage is O(batch_size) regardless of total item count.
/// For very large datasets, prefer smaller batch sizes.
///
/// # Examples
///
/// ```
/// let items = fetch_all_orders();
/// let count = process_in_batches(items, 100, |batch| {
///     for order in batch {
///         order.fulfill()?;
///     }
///     ControlFlow::Continue(())
/// });
/// ```
pub fn process_in_batches<T, F>(
    items: impl Iterator<Item = T>,
    batch_size: usize,
    f: F,
) -> usize
where
    F: FnMut(&[T]) -> ControlFlow<()>,
```

### Document Safety Requirements

```rust
/// Transmute bytes directly into a value of type `T`.
///
/// # Safety
///
/// Callers must ensure:
/// - `bytes.len() == size_of::<T>()`
/// - The byte pattern represents a valid `T`
/// - `T` has no padding bytes that could be uninitialized
///
/// Violating these requirements causes undefined behavior.
///
/// # Examples
///
/// ```
/// let bytes = [0x01, 0x00, 0x00, 0x00];
/// // SAFETY: 4 bytes is correct size for u32, all bit patterns valid
/// let value: u32 = unsafe { transmute_bytes(&bytes) };
/// assert_eq!(value, 1);
/// ```
pub unsafe fn transmute_bytes<T>(bytes: &[u8]) -> T {
    // ...
}
```

## Module Documentation

Use `//!` for inner doc comments:

```rust
//! User authentication and session management.
//!
//! This module provides authentication via OAuth 2.0, SAML,
//! and username/password. Sessions are stored in Redis with
//! configurable TTL.
//!
//! # Quick Start
//!
//! ```
//! use auth::{Authenticator, Credentials};
//!
//! let auth = Authenticator::new(config);
//! let session = auth.authenticate(credentials).await?;
//! let is_valid = auth.validate(&session.token).await?;
//! ```
//!
//! # Feature Flags
//!
//! - `oauth`: Enable OAuth 2.0 support (enabled by default)
//! - `saml`: Enable SAML support
//!
//! # See Also
//!
//! - [`Session`]: Session data and lifecycle
//! - [`Store`]: Custom session storage backends

pub mod oauth;
pub mod password;
pub mod session;
```

## Struct Documentation

```rust
/// A pool of reusable database connections.
///
/// Connections are created lazily up to `max_size`, then reused.
/// Idle connections are validated periodically and recycled if stale.
///
/// # Thread Safety
///
/// `ConnectionPool` is `Send + Sync` and can be shared across threads.
/// Internally uses a mutex for connection checkout/checkin.
///
/// # Examples
///
/// ```
/// let pool = ConnectionPool::builder()
///     .max_size(10)
///     .idle_timeout(Duration::from_secs(300))
///     .build()?;
///
/// let conn = pool.get().await?;
/// conn.execute("SELECT 1").await?;
/// // Connection returned to pool when `conn` is dropped
/// ```
pub struct ConnectionPool {
    // ...
}

impl ConnectionPool {
    /// Create a new connection pool builder.
    ///
    /// Use the builder to configure pool settings before calling
    /// [`Builder::build`].
    pub fn builder() -> Builder {
        // ...
    }

    /// Acquire a connection from the pool.
    ///
    /// If no connections are available and the pool is at capacity,
    /// this method waits until one becomes available.
    ///
    /// # Errors
    ///
    /// Returns [`PoolError::Timeout`] if no connection becomes
    /// available within the configured timeout.
    ///
    /// # Cancel Safety
    ///
    /// This method is cancel-safe. If the future is dropped before
    /// completion, no connection is leaked.
    pub async fn get(&self) -> Result<PooledConnection<'_>, PoolError> {
        // ...
    }
}
```

## Trait Documentation

```rust
/// A backend for storing user sessions.
///
/// Implementations must be thread-safe (`Send + Sync`).
/// The default implementation uses Redis; see [`RedisStore`].
///
/// # Implementing
///
/// ```
/// impl Store for MyStore {
///     async fn get(&self, token: &str) -> Result<Option<Session>, StoreError> {
///         // Look up session by token
///     }
///     // ...
/// }
/// ```
pub trait Store: Send + Sync {
    /// Retrieve a session by its token.
    ///
    /// Returns `Ok(None)` if the session doesn't exist.
    /// Returns `Err` if the storage backend fails.
    async fn get(&self, token: &str) -> Result<Option<Session>, StoreError>;

    /// Store a session with the given TTL.
    ///
    /// If a session with this token exists, it is overwritten.
    async fn set(&self, session: &Session, ttl: Duration) -> Result<(), StoreError>;
}
```

## Linking to Other Items

```rust
/// See [`other_function`] for the async version.
/// Uses the [`Config`] struct for settings.
/// Implements the [`std::fmt::Display`] trait.
/// Related to [`crate::other_module::Thing`].
```

## Tools

- **cargo doc**: Generate documentation (`cargo doc --open`)
- **cargo test**: Runs doc examples as tests
- **rustdoc**: Underlying documentation tool
- **docs.rs**: Automatic documentation hosting for crates.io packages
