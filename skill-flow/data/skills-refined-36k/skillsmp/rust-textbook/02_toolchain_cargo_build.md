# 02 — Toolchain, Cargo, Builds (Reproducibility and Build-Surface Control)

[CONTRACT: CTR-0201] Toolchain Baseline (MSRV).
- REJECT IF: MSRV is implicit or unenforced.
- REJECT IF: dependency or syntax changes effectively raise MSRV without an explicit contract update.
- ENFORCE BY: `package.rust-version`; CI job pinned to MSRV; dependency policy that tracks transitive MSRV.
[PROVENANCE] Cargo book: rust-version; Rust 2024 edition guidance (edition baseline is not an MSRV substitute).
[VERIFICATION] CI: build + test under MSRV; `cargo update -Z minimal-versions` in a dedicated policy job when used.

[HAZARD: RSK-0201] Feature Unification and Hidden `std`/Build Surfaces.
- FAILURE MODE: dependency default-features pull `std`, heavy graphs, build scripts, proc macros.
- REJECT IF: dependency default-features are enabled without explicit justification.
- ENFORCE BY: `default-features = false` on dependencies; explicit feature wiring; minimal feature sets tested.
[PROVENANCE] Cargo book: features and feature resolution.
[VERIFICATION] CI: `--no-default-features`, defaults, `--all-features`, plus curated feature combinations for complex graphs.

[INVARIANT: INV-0201] Profile-Independent Correctness.
- REJECT IF: correctness depends on debug-only behavior (`debug_assert!`, overflow-checking expectations, `cfg(debug_assertions)`).
- ENFORCE BY: treat `debug_assert!` as diagnostics only; enforce invariants at runtime where required; design APIs so invalid states are unrepresentable.
[PROVENANCE] Rust Reference: no optimization/codegen guarantees; behavior differences exist across profiles.
[VERIFICATION] CI: test in debug and release for crates with unsafe/concurrency risk anchors.

[HAZARD: RSK-0202] Build Scripts Are Host Code Execution.
- TRIGGER: `build.rs`, `links = ...`, `cargo:rustc-cfg=...`, `cargo:rustc-env=...`, bindgen.
- FAILURE MODE: nondeterministic builds; supply-chain risk; environment-dependent compilation.
- REJECT IF: build scripts read ambient environment or filesystem without a declared input set.
- REJECT IF: build scripts perform network I/O.
- ENFORCE BY: strict input surface (Cargo-provided env only); deterministic outputs; minimized dependencies; documented `cargo:` outputs.
[PROVENANCE] Cargo book: build scripts (`cargo:` output protocol; rerun-if-* semantics).
[VERIFICATION] CI in a restricted environment; diff-based check for generated outputs when committed.

[HAZARD: RSK-0203] Proc Macros Are Host Code Execution + Code Generation.
- TRIGGER: proc-macro crates; derive/attribute macros.
- FAILURE MODE: hidden allocations/IO; hidden `unsafe`; expansion drift across versions.
- REJECT IF: proc macros introduce semantic logic that cannot be validated by compile tests.
- ENFORCE BY: minimal proc-macro dependency graph; expansion tests; keep proc macros syntactic where possible.
[PROVENANCE] Rust Reference: procedural macros (conceptual); Cargo book: proc-macro crates and build phases.
[VERIFICATION] CI: compile-pass/compile-fail tests; expansion snapshot in trusted CI when used.

[CONTRACT: CTR-0202] rustdoc and Doctests Are Public API.
- REJECT IF: public APIs lack usage examples when the safe usage protocol is non-obvious.
- REJECT IF: doctests are not executed in CI.
- ENFORCE BY: doctestable examples that encode correct usage; lint policy for rustdoc warnings set by project.
[PROVENANCE] Rustdoc documentation (doctest execution model).
[VERIFICATION] `cargo test --doc` in CI.

[CONTRACT: CTR-0203] CI Is the Ground-Truth Execution Environment.
- REJECT IF: acceptance depends on local execution of untrusted code.
- ENFORCE BY: CI-only verification for PRs; signed artifacts where required; dependency governance gates.
[PROVENANCE] Project security posture (fail-closed; supply-chain controls) is a contract surface.

## References (Normative Anchors)

- Cargo book: https://doc.rust-lang.org/cargo/
- Cargo build scripts: https://doc.rust-lang.org/cargo/reference/build-scripts.html
- Rust Reference: Conditional compilation: https://doc.rust-lang.org/reference/conditional-compilation.html
- Rustdoc: https://doc.rust-lang.org/rustdoc/
