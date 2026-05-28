# 17 — Verification Protocols (Tests, Fuzzing, Miri, Loom, Kani)

[CONTRACT: CTR-1701] Verification Plan Is Mandatory for Risk Anchors.
- REJECT IF: a change touches any risk anchor (unsafe, atomics, parsing, FFI, cfg matrix) without an explicit verification plan.
- ENFORCE BY: map each risk anchor to a tool gate and a test shape.
[PROVENANCE] Rust Reference: UB classes exist that compile cleanly; verification requires independent checks.

[VERIFICATION] Tool Selection (Minimum Requirements).
- Unsafe/raw pointers/validity: Miri.
- Custom synchronization / atomics protocols: Loom.
- Stateful invariants (allocators, parsers, protocols): Proptest (model/property tests).
- Bounded proofs (small-state logic, arithmetic invariants): Kani (when applicable).

[INVARIANT: INV-1701] Tests Encode Invariants, Not Only Examples.
- REJECT IF: a state machine change adds only happy-path tests.
- ENFORCE BY: negative tests; boundary tests; regression tests that fail without the fix.
[PROVENANCE] Correctness requires invariants; tests are executable constraints.

[HAZARD: RSK-1701] "Passes Tests" Is Not a Soundness Proof for Unsafe.
- REJECT IF: unsafe changes land without Miri coverage.
- ENFORCE BY: run Miri on the relevant test suite; isolate unsafe and add targeted tests that exercise the unsafe boundary.
[PROVENANCE] Rust Reference: UB can remain latent under native execution.
[VERIFICATION] `cargo miri test` (project-specific invocations vary); enable strict checks where supported.

[HAZARD: RSK-1702] Concurrency Bugs Require Schedule Exploration.
- REJECT IF: custom sync primitives rely only on stress tests.
- ENFORCE BY: Loom models for core primitives; stress tests as a supplement.
[PROVENANCE] Weak memory and interleavings create behaviors absent from naive tests.
[VERIFICATION] Loom model tests that explore interleavings and reorderings.

[HAZARD: RSK-1703] Parsers Need Fuzzing and Size/Depth Caps.
- REJECT IF: parser changes ship without fuzz coverage when parsing untrusted inputs.
- ENFORCE BY: fuzz targets that accept bytes and drive parsing; keep fuzz targets deterministic; maintain corpus of regressions.
[PROVENANCE] Parsing is a DoS surface even under memory safety.
[VERIFICATION] `cargo fuzz run <target>` (or equivalent harness).

[INVARIANT: INV-1702] Zero-Cost Verification via Compile-Time Assertions.
- REJECT IF: runtime-only assertions are used for invariants that can be proven at compile time.
- ENFORCE BY:
  - const-evaluated asserts for size/layout invariants (when stable for the MSRV)
  - type-level assertions (trait bounds) in tests
  - optional `static_assertions` for richer diagnostics when dependency policy allows
[PROVENANCE] Compile-time checking reduces runtime attack surface and removes unreachable branches.
[VERIFICATION] `cargo test` (compile-time assertions fail at build time).

```text
Compile-time assertion patterns (examples)
1) Size/layout invariants (no runtime cost)
   const _: () = { assert!(core::mem::size_of::<T>() == N); };
2) Trait assertions (tests-only)
   fn _assert_send_sync<T: Send + Sync>() {}
   #[test] fn send_sync_contract() { _assert_send_sync::<MyType>(); }
```

## References (Normative Anchors)

- Rust Reference: Behavior considered undefined: https://doc.rust-lang.org/reference/behavior-considered-undefined.html
- Rustdoc (doctests): https://doc.rust-lang.org/rustdoc/
- Miri: https://github.com/rust-lang/miri
- Loom: https://github.com/tokio-rs/loom
- Proptest: https://docs.rs/proptest/
- Kani: https://model-checking.github.io/kani/
