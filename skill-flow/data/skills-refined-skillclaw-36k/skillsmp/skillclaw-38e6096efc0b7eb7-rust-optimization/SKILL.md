---
name: rust-optimization
description: Use this skill when you need to optimize Rust code for performance, memory usage, caching strategies, or parallel computation.
---

# Rust Optimization Skill

## Applicable Scope
- Rust performance and memory optimization
- Caching and parallel computation strategies
- Linear programming and numerical computation acceleration

## Critical Rules
- Prioritize caching high-frequency static data using `moka`
- Use `rayon` for CPU-intensive tasks or `tokio::task::spawn_blocking` for blocking operations
- Avoid unnecessary cloning; prefer borrowing slices and references
- Avoid blocking calls in asynchronous contexts

## Quick Templates
### Moka Caching
```rust
use moka::future::Cache;
use std::time::Duration;

pub struct MaterialCache {
    cache: Cache<String, crate::material::material::Material>,
}

impl MaterialCache {
    pub fn new() -> Self {
        Self {
            cache: Cache::builder()
                .max_capacity(1000)
                .time_to_live(Duration::from_secs(3600))
                .build(),
        }
    }
}
```

### Rayon Parallelism
```rust
use rayon::prelude::*;

let totals: Vec<f64> = materials
    .par_iter()
    .map(|m| m.price)
    .collect();
```

### Blocking Computation Offloading
```rust
let result = tokio::task::spawn_blocking(move || heavy_calc(input))
    .await?;
```

## Optimization Checklist
- [ ] Is there any repeated computation that can be cached?
- [ ] Are CPU-intensive tasks parallelized?
- [ ] Are there any blocking calls in asynchronous paths?
- [ ] Are clones explicit and necessary?