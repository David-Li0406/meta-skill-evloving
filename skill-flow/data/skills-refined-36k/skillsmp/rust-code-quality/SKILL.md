---
name: rust-code-quality
description: Rust code quality standards and documentation practices. Use when reviewing Rust code, cleaning up churn, writing docstrings, or following rustdoc conventions.
license: AGPL-3.0
metadata:
  triggers:
    type: domain
    enforcement: suggest
    priority: high
    keywords:
      - rustdoc
      - doc comment
      - documentation
      - intra-doc link
      - deslop
      - code quality
      - code review
    intent-patterns:
      - \bdocument(ing|ation)?\b.*?\b(rust|function|type|struct|enum|trait|module)\b
      - \b(write|add|create)\b.*?\bdoc\s*comment\b
      - \b#\s*(Errors|Panics|Examples|Arguments)\b
      - \b(clean|review|deslop)\b.*?\b(rust|code)\b
---

# Rust Code Quality

## Required: Code Churn Review

Before finalizing any Rust changes, inspect what you are actually changing:

`git add -N .; git diff` if diff is relatively small, or, if changes are very large, manually read files of interest.

Separate behavioural changes from churn. As you review, actively avoid Rust-shaped noise:

### Remove

✗ Inline comments that don't match the project's tone or that narrate obvious control flow
✗ Defensive branches that assume impossible states on trusted codepaths (extra `match _ =>`, redundant `if let Some` guards, spurious fallbacks) unless you can point to a concrete invariant break
✗ Error handling that's performative: turning simple `?` propagation into verbose `map_err` chains, adding "just in case" `catch_unwind`, or plumbing new error enums when an existing error type already expresses the failure. Consider that it may be better to let some code paths that should theoretically be invalid panic clearly
✗ Type escape hatches (`Box<dyn Any>`, casts to silence the compiler) unless the area already uses that pattern and you can justify it mechanically
✗ Tramp data and excessive named variables where they should really be inlined
✗ Section markers/decorative comments (organization is implied by code structure and naming, not adhoc separators)

### Keep

✓ Comprehensive, technical docstrings (important for rustdoc, required on all public API)
✓ Rustdoc best practices (intra-doc links for type ref, standard headings e.g. `# Errors`, `# Arguments`)
✓ All existing docstrings, even if they seem repetitive (do not remove docstrings, especially for pubs!)

### Principles

Once non-essential lines are identified, clean them up while keeping identical observable behaviour. Prefer minimal diffs: keep signatures stable, keep error shapes stable, keep logging consistent, keep module and crate boundaries clean.

______________________________________________________________________

## Documentation Practices

### Do

✓ Begin every doc comment with single-line summary
✓ Use intra-doc links for all type references
✓ Document all error conditions with `# Errors`
✓ Include practical examples for public APIs
✓ Link standard library types: \[`Vec`\], \[`HashMap`\], etc.
✓ Use inline parameter descriptions for simple functions (0-2 params)
✓ Describe return values in main text, not separate sections

### Don't

✗ Document standard trait implementations (`Debug`, `Display`, `From`)
✗ Add separate `# Returns` sections (inline instead)
✗ Mention variable types already in signatures
✗ Use comments on same line as code
✗ Skip error documentation for fallible functions
✗ Sprinkle small inline `//` comments; merge these into a comprehensive docstring if useful, otherwise remove them completely

## Quick Reference

### Basic Doc Comment

```rust
/// Retrieves an entity by its UUID.
///
/// Loads the entity from the store and verifies access permissions.
/// Returns the [`Entity`] if found and accessible.
///
/// # Errors
///
/// - [`NotFound`] if the entity doesn't exist
/// - [`AuthorizationError`] if access is denied
///
/// [`NotFound`]: EntityError::NotFound
/// [`AuthorizationError`]: EntityError::Authorization
pub fn get_entity(&self, id: EntityId) -> Result<Entity, Report<EntityError>> {
```

### Intra-Doc Links

```rust
/// Updates the [`User`] using [`UserUpdateStrategy`].
///
/// See [`validation::user`] for validation rules.
///
/// [`validation::user`]: crate::validation::user
```

## Documentation Patterns

### Simple Functions (0-2 params)

Describe parameters inline:

```rust
/// Processes the `input` elements and returns filtered results.
///
/// Takes a collection of `input` elements, applies the `filter_fn`,
/// and returns a [`Vec`] containing only matching elements.
```

### Complex Functions (3+ params)

Use explicit `# Arguments` section:

```rust
/// Merges multiple data sources with transformation rules.
///
/// # Arguments
///
/// * `sources` - Collection of data sources to merge
/// * `rules` - Transformation rules to apply
/// * `options` - Configuration controlling merge behavior
/// * `callback` - Optional function for each merged item
```

### Error Docs

```rust
/// # Errors
///
/// - [`WebAlreadyExists`] if web ID is taken
/// - [`AuthorizationError`] if permission denied
///
/// [`WebAlreadyExists`]: WebError::WebAlreadyExists
/// [`AuthorizationError`]: WebError::Authorization
```

### Module Docs

````rust
//! Entity management functionality.
//!
//! Main types:
//! - [`Entity`] - Core entity type
//! - [`EntityStore`] - Storage trait
//!
//! # Examples
//!
//! ```
//! use hash_graph::entity::Entity;
//! ```
````

### Examples with Error Handling

````rust
/// # Examples
///
/// ```rust
/// let entities = get_entities_by_type(type_id)?;
/// assert_eq!(entities.len(), 2);
/// # Ok::<(), Box<dyn core::error::Error>>(())
/// ```
````

## Verification

```bash
cargo doc --no-deps --all-features
```

## References

For doc-heavy tasks, READ as needed (don't assume you 'already know'):

- [function-documentation.md](references/function-documentation.md) - functions/methods
- [type-documentation.md](references/type-documentation.md) - structs/enums/traits
- [error-documentation.md](references/error-documentation.md) - errors/panics
- [examples-and-links.md](references/examples-and-links.md) - examples/intra-doc links
