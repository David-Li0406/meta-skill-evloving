# Type Documentation Guide

## Struct Documentation

### Basic Structure

```rust
/// Unique identifier for an entity in the system.
///
/// Combines entity UUID and web ID for precise references across the API.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct EntityId {
    pub entity_uuid: EntityUuid,
    pub web_id: WebId,
}
```

### When to Document Fields

Document when field purpose is NOT obvious:

```rust
pub struct EntityQuery {
    /// Maximum number of results to return (default: 100)
    pub limit: Option<usize>,

    /// Include deleted entities in results
    pub include_deleted: bool,
}
```

Don't document obvious fields:

```rust
pub struct User {
    pub id: UserId,        // ID is obvious
    pub name: String,      // name is obvious
    pub email: String,     // email is obvious
}
```

______________________________________________________________________

## Enum Documentation

### Document WHY, not WHAT

Good - explains purpose:

```rust
/// Entity lifecycle state.
///
/// Controls validation rules and access permissions at each stage.
pub enum EntityState {
    Draft,      // No docs needed - obvious
    Published,
    Archived,
    Deleted,
}
```

Bad - restates the obvious:

```rust
pub enum EntityState {
    /// The draft state        // Redundant
    Draft,
    /// The published state    // Redundant
    Published,
}
```

### When Variants Need Docs

Document variants only when they:

- Have non-obvious behavior
- Affect system state in special ways
- Have constraints or invariants

```rust
pub enum CacheStrategy {
    /// Never cache (always fetch fresh)
    None,

    /// Cache with TTL expiration
    Timed { seconds: u64 },

    /// Cache until explicitly invalidated
    Persistent,

    /// Adaptive caching based on access patterns (experimental)
    Adaptive,
}
```

______________________________________________________________________

## Trait Documentation

Focus on contract and guarantees, not restating method signatures:

```rust
/// Store for entity data with transactional guarantees.
///
/// All operations are atomic and maintain consistency even under
/// concurrent access.
pub trait EntityStore: Send + Sync {
    /// Retrieves entity if it exists and caller has access.
    ///
    /// # Errors
    ///
    /// - [`NotFound`] if entity doesn't exist
    /// - [`AccessDenied`] if caller lacks permission
    ///
    /// [`NotFound`]: StoreError::NotFound
    /// [`AccessDenied`]: StoreError::AccessDenied
    fn get_entity(&self, id: EntityId) -> Result<Entity, Report<StoreError>>;
}
```

______________________________________________________________________

## Newtype Pattern

Document invariants and guarantees, not the wrapping itself:

Good:

```rust
/// Non-empty string validated at construction.
///
/// Guaranteed to contain at least one non-whitespace character.
#[derive(Debug, Clone)]
pub struct NonEmptyString(String);
```

Bad:

```rust
/// A string wrapper
pub struct NonEmptyString(String);
```

______________________________________________________________________

## Generic Types

Document constraints and behavior, not type parameters themselves:

```rust
/// LRU cache with configurable eviction.
///
/// Evicts least-recently-used items when capacity is reached.
/// All operations are O(1) amortized.
pub struct LruCache<K, V>
where
    K: Hash + Eq,
{
    // fields...
}
```

______________________________________________________________________

## Complex Types

Add sections only when behavior is non-obvious:

```rust
/// Temporal entity with complete version history.
///
/// # Version Storage
///
/// Versions are stored as deltas from previous state for space efficiency.
/// Full reconstruction requires replaying deltas (O(n) where n = versions).
///
/// # Querying
///
/// - `current()` - O(1), returns latest version
/// - `at_time(t)` - O(log n + m), binary search + delta replay
///
/// For frequent historical queries, use snapshot API instead.
pub struct TemporalEntity {
    // fields...
}
```

______________________________________________________________________

## What NOT to Document

Skip docs for:

- Obvious structs: `struct Point { x: f64, y: f64 }`
- Standard trait impls: `Debug`, `From`, etc.
- Self-explanatory type aliases
- Obvious field names (`id`, `name`, etc.)

______________________________________________________________________

## When TO Document

Document when:

- Non-obvious invariants: `/// Validated email (RFC 5322 compliant)`
- Performance characteristics: `/// Sorted vector with O(log n) lookup`
- Special behavior: `/// Cache that prefetches adjacent keys on miss`
- Complex state machines: `/// Transitions: Idle -> Active -> Closing -> Closed`

______________________________________________________________________

## Related

- [function-documentation.md](function-documentation.md) - Functions and methods
- [error-documentation.md](error-documentation.md) - Error types
- [examples-and-links.md](examples-and-links.md) - Examples and links
- [SKILL.md](../SKILL.md) - Overview
