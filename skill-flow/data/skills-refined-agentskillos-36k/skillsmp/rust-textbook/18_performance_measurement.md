# 18 — Performance (Cost Model, Measurement, Regression Control)

[CONTRACT: CTR-1801] Performance Is a Public Contract When It Defines Feasibility.
- REJECT IF: performance-sensitive APIs change asymptotic complexity or allocation behavior without an explicit contract decision.
- ENFORCE BY: document complexity and allocation points for hot APIs; keep fast paths allocation-free when required.
[PROVENANCE] Rust makes no performance guarantees beyond semantics; performance contracts are library-level.

[HAZARD: RSK-1801] Hidden Allocation and Formatting in Hot Paths.
- TRIGGER: `clone()` in loops, `format!`, `to_string()`, iterator `collect()` on critical paths, repeated `Vec` growth.
- FAILURE MODE: latency and throughput regression; allocator contention.
- REJECT IF: hidden allocations are introduced without explicit justification.
- ENFORCE BY: borrowed inputs (`&[u8]`, `&str`); `Cow` for dual ownership; explicit preallocation and capacity control.
[PROVENANCE] Allocation behavior is part of std type contracts; formatting allocates by default.
[VERIFICATION] Benchmarks; allocation profiling where available.

[CONTRACT: CTR-1802] Benchmark Methodology Must Control Noise.
- REJECT IF: performance claims ship without a reproducible benchmark harness when regression risk exists.
- ENFORCE BY: stable harness; fixed inputs; warmup; regression thresholds; isolate workloads.
[PROVENANCE] Microbenchmarks are sensitive to environment; correctness of claims requires method discipline.
[VERIFICATION] `cargo bench` with pinned methodology; CI benchmark gates for critical crates.

[HAZARD: RSK-1802] Code Size and Monomorphization Bloat.
- TRIGGER: aggressive inlining, heavy generic abstraction, blanket impl layers.
- FAILURE MODE: larger binaries; worse I-cache locality; downstream compile-time regression.
- REJECT IF: generic/inlining changes are introduced without a size/compile-time rationale for foundational crates.
- ENFORCE BY: keep generics local; avoid exposing large generic surfaces; prefer dynamic dispatch only where justified.
[PROVENANCE] rustc monomorphizes generics; codegen is implementation-defined.
[VERIFICATION] Size tracking (`-Z print-type-sizes` in trusted CI when applicable); compile-time and binary-size metrics.

## References (Normative Anchors)

- Cargo bench: https://doc.rust-lang.org/cargo/commands/cargo-bench.html
- Rust Reference: no codegen guarantees: https://doc.rust-lang.org/reference/
