# Performance Optimization in Rust

Guide to writing high-performance Rust code and identifying bottlenecks.

## Profiling

### CPU Profiling with cargo-flamegraph

```bash
cargo install flamegraph
cargo flamegraph --bin my-app
# Opens flamegraph in browser
```

### Benchmarking with Criterion

```toml
[dev-dependencies]
criterion = "0.5"

[[bench]]
name = "my_benchmark"
harness = false
```

```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn fibonacci(n: u64) -> u64 {
    match n {
        0 | 1 => 1,
        n => fibonacci(n - 1) + fibonacci(n - 2),
    }
}

fn benchmark(c: &mut Criterion) {
    c.bench_function("fib 20", |b| b.iter(|| fibonacci(black_box(20))));
}

criterion_group!(benches, benchmark);
criterion_main!(benches);
```

## Memory Optimization

### Avoid Unnecessary Clones

```rust
// Bad
fn process(data: Vec<String>) {
    for item in &data {
        println!("{}", item.clone());  // Unnecessary
    }
}

// Good
fn process(data: &[String]) {
    for item in data {
        println!("{}", item);
    }
}
```

### Use `Cow` for Conditional Ownership

```rust
use std::borrow::Cow;

fn process<'a>(input: &'a str) -> Cow<'a, str> {
    if input.contains("bad") {
        Cow::Owned(input.replace("bad", "good"))
    } else {
        Cow::Borrowed(input)
    }
}
```

### Stack vs Heap

```rust
// Heap allocation (slower)
let vec = vec![1, 2, 3, 4, 5];

// Stack allocation (faster) when size is known
let arr = [1, 2, 3, 4, 5];

// Use SmallVec for small collections
use smallvec::{SmallVec, smallvec};
let small: SmallVec<[i32; 8]> = smallvec![1, 2, 3];  // Stack if <= 8 items
```

## Algorithm Optimization

### Use Iterators

```rust
// Bad: Allocates intermediate vectors
let result: Vec<_> = data.iter()
    .map(|x| x * 2)
    .collect::<Vec<_>>()
    .iter()
    .filter(|x| x > &10)
    .collect();

// Good: Lazy evaluation, no intermediate allocations
let result: Vec<_> = data.iter()
    .map(|x| x * 2)
    .filter(|x| x > &10)
    .collect();
```

### Parallel Processing

```toml
[dependencies]
rayon = "1.8"
```

```rust
use rayon::prelude::*;

// Sequential
let sum: i32 = data.iter().map(|x| expensive(x)).sum();

// Parallel
let sum: i32 = data.par_iter().map(|x| expensive(x)).sum();
```

## Data Structure Selection

```rust
// O(1) lookup
use std::collections::HashMap;
let map: HashMap<String, Value> = HashMap::new();

// Ordered O(log n) lookup
use std::collections::BTreeMap;
let btree: BTreeMap<String, Value> = BTreeMap::new();

// Fast for small collections
use smallvec::SmallVec;

// Fast hash function
use rustc_hash::FxHashMap;
let fast_map: FxHashMap<String, Value> = FxHashMap::default();
```

## Compilation Optimization

### Release Profile

```toml
[profile.release]
opt-level = 3           # Maximum optimization
lto = "fat"             # Link-time optimization
codegen-units = 1       # Better optimization, slower compile
strip = true            # Remove debug symbols
```

### Target CPU

```bash
# Optimize for current CPU
RUSTFLAGS="-C target-cpu=native" cargo build --release
```

## Common Patterns

### String Building

```rust
// Bad: Reallocates
let mut s = String::new();
for i in 0..1000 {
    s = s + &i.to_string();
}

// Good: Pre-allocate
let mut s = String::with_capacity(4000);
for i in 0..1000 {
    s.push_str(&i.to_string());
}

// Better: Use format!
let s = (0..1000).map(|i| i.to_string()).collect::<String>();
```

### Avoiding Bounds Checks

```rust
// With bounds check
for i in 0..vec.len() {
    process(vec[i]);
}

// Iterator eliminates bounds checks
for item in &vec {
    process(*item);
}

// Or use get_unchecked (unsafe but fast)
unsafe {
    for i in 0..vec.len() {
        process(*vec.get_unchecked(i));
    }
}
```

## Best Practices

1. **Profile first**: Don't optimize without measuring
2. **Use release builds**: Always benchmark in release mode
3. **Prefer iterators**: Lazy, composable, optimized
4. **Avoid clones**: Use references when possible
5. **Pre-allocate**: Use `with_capacity` for collections
6. **Choose right data structure**: HashMap vs BTreeMap vs Vec
7. **Use parallel iterators**: Rayon for CPU-bound work
8. **Enable LTO**: Link-time optimization for release builds
9. **Benchmark changes**: Verify optimizations work
10. **Read assembly**: `cargo asm` to see generated code
