---
name: rust-performance-optimization
description: Use this skill when you want to optimize Rust applications for performance through techniques like avoiding unnecessary clones and preallocating collections.
---

# Rust Performance Optimization Skill

## Avoid Unnecessary Clones
```rust
// BAD
fn process(s: String) -> String {
    let s_copy = s.clone();  // Unnecessary!
    s_copy.to_uppercase()
}

// GOOD
fn process(s: String) -> String {
    s.to_uppercase()
}

// OR borrow if you don't need ownership
fn process(s: &str) -> String {
    s.to_uppercase()
}
```

## Preallocate Collections
```rust
// BAD - many reallocations
let mut vec = Vec::new();
for i in 0..1000 {
    vec.push(i);
}

// GOOD - single allocation
let vec: Vec<_> = (0..1000).collect();

// OR with_capacity
let mut vec = Vec::with_capacity(1000);
```

## Zero-Cost Abstractions
Iterators are as fast as loops due to inlining and optimization.

## Review Severity
- **MAJOR**: Unnecessary clones in hot path
- **MINOR**: Could preallocate collection
- **SUGGESTION**: Could use iterator instead of loop