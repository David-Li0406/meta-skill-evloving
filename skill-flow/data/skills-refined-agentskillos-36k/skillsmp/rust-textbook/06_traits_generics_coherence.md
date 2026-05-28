# 06 — Traits, Generics, Coherence (Contract Surface and SemVer Hazards)

[HAZARD: RSK-0601] Public Generics Multiply Downstream Compile Cost.
- TRIGGER: new type parameters on public APIs; new blanket trait layers; derive-heavy public types.
- FAILURE MODE: downstream compile time regression; code size inflation; monomorphization bloat.
- REJECT IF: public generic surface is expanded without an explicit justification (performance, expressivity, safety).
- ENFORCE BY: keep generics local; hide helper traits/types; prefer concrete public types for widely used APIs when acceptable.
[PROVENANCE] rustc monomorphization model (background); Rust Reference: no codegen guarantees.
[VERIFICATION] Track compile-time and code-size budgets in CI for foundational crates.

[CONTRACT: CTR-0601] Trait Bounds Are Part of the Public API.
- REJECT IF: bounds are tightened without an explicit semver decision.
- REJECT IF: bounds force allocations, `Send`/`Sync`, `'static`, or `Unpin` without necessity.
- ENFORCE BY: constrain at the narrowest boundary; push bounds inward; document bounds that encode safety or performance contracts.
[PROVENANCE] Rust Reference: trait bounds are part of type signatures and affect type checking and inference.

[INVARIANT: INV-0601] Coherence and Orphan Rules Must Hold.
- REJECT IF: a crate introduces overlapping impls or orphan-rule violations (even if "it seems fine" under current usage).
- ENFORCE BY: newtype wrappers to regain coherence control; avoid broad impls for foreign traits/types.
[PROVENANCE] Rust Reference: implementations (coherence, overlap, orphan rules).
[VERIFICATION] Compile in a feature matrix; add compile-fail tests for intended coherence boundaries when using macros.

[HAZARD: RSK-0602] Blanket Impl and Impl Addition Can Be SemVer-Breaking.
- TRIGGER: `impl<T> Trait for T where ...`, new impls for public types, new default methods that change resolution, extension traits.
- FAILURE MODE: downstream overlap errors; method resolution changes; trait-selection ambiguity.
- REJECT IF: new impls are added to public crates without a semver impact analysis.
- ENFORCE BY: prefer sealed traits for extension points; keep impl domains narrow; avoid "catch-all" impls.
[PROVENANCE] Rust Reference: overlapping impl definition; orphan rules; method call resolution is affected by available impls.
[VERIFICATION] Semver-check tooling where available; downstream integration tests for ecosystem-facing crates.

[CONTRACT: CTR-0602] Auto Traits (`Send`, `Sync`, `Unpin`) Are Observable Contracts.
- REJECT IF: field changes on public types unintentionally change auto-trait derivation.
- REJECT IF: `unsafe impl Send/Sync` lacks explicit invariants and a protocol description.
- ENFORCE BY: make auto-trait intent explicit in docs; add compile-time assertions in tests for expected auto-traits; isolate `unsafe impl` in small modules.
[PROVENANCE] Rust Reference: auto traits and implementations; data races are UB.
[VERIFICATION] Compile-time trait assertion tests; Loom for concurrent protocols that justify `Send/Sync`.

[CONTRACT: CTR-0603] Trait Objects Are Allocation and Lifetime Boundaries.
- REJECT IF: a `dyn Trait` return type hides allocation, lifetime ownership, or thread-safety constraints.
- ENFORCE BY: document allocation strategy; document ownership and lifetime ties; prefer generics for hot paths and `dyn` for heterogeneity.
[PROVENANCE] Rust Reference: trait objects and object safety constraints.

## References (Normative Anchors)

- Rust Reference: Implementations (coherence; orphan rules): https://doc.rust-lang.org/reference/items/implementations.html
- Rust Reference: Traits and trait objects: https://doc.rust-lang.org/reference/types/trait-object.html
- Rust Reference: Behavior considered undefined (data races): https://doc.rust-lang.org/reference/behavior-considered-undefined.html
- rustc-dev-guide: https://rustc-dev-guide.rust-lang.org/
