# 20 — `cfg`, Feature Flags, Build Matrix (Dark-Code Control)

[INVARIANT: INV-2001] `#[cfg]` Is Source Rewriting.
- False predicate: the item/expression is removed from the program; it is not type-checked.
- True predicate: the attribute is removed and the item remains.
- REJECT IF: correctness relies on excluded code "still being checked."
[PROVENANCE] Rust Reference: conditional compilation attribute effect.

[HAZARD: RSK-2001] Dark Code Rot (Untested cfg/feature permutations).
- TRIGGER: new `#[cfg]` branches; feature-gated modules; platform-gated code.
- FAILURE MODE: excluded code compiles only in theory; public API breaks in non-default feature sets; release-time failures.
- REJECT IF: new cfg branches are not covered by at least one CI build.
- ENFORCE BY: explicit build matrix; targeted CI jobs per platform/feature; eliminate dead cfg branches.
[PROVENANCE] Rust Reference: cfg removes code; Cargo features alter the compiled program.
[VERIFICATION] CI builds: defaults, `--no-default-features`, `--all-features`, and curated permutations; platform runners when applicable.

[CONTRACT: CTR-2001] Feature Flags Must Be Additive and Contracted.
- REJECT IF: a feature flips core semantics without a documented contract and dedicated tests.
- REJECT IF: public API differs across feature sets unintentionally (missing items, different trait impl sets) without an explicit design.
- ENFORCE BY: additive capability features; stable default set; feature-gated APIs that remain coherent under semver.
[PROVENANCE] Cargo feature resolution is global; trait impl sets affect method resolution and coherence.

[HAZARD: RSK-2002] `cfg_attr` Can Change Semantics (Not Only Visibility).
- TRIGGER: `cfg_attr` applying `repr`, linking attributes, lint levels, `path`, `inline`, `target_feature`.
- FAILURE MODE: ABI/layout drift; linking drift; lint policy drift across configurations.
- REJECT IF: `cfg_attr` changes semantic attributes without a configuration-specific test.
[PROVENANCE] Rust Reference: attributes (active/inert; meta processing order); conditional compilation.
[VERIFICATION] Compile/link tests per affected configuration.

[HAZARD: RSK-2003] `cfg!()` Is Not `#[cfg]`.
- `cfg!()` yields a boolean; both branches are still type-checked.
- REJECT IF: `cfg!()` is used to guard code that must not exist for unsupported targets (missing symbols, unsupported syscalls).
- ENFORCE BY: use `#[cfg]` for compilation gating; use `cfg!()` only for in-code selection among universally available APIs.
[PROVENANCE] Rust Reference: conditional compilation; `cfg!` is a built-in macro evaluated at compile time.

[CONTRACT: CTR-2002] Public API Must Be Stable Across cfg/feature Sets or Explicitly Partitioned.
- REJECT IF: `#[cfg(feature = ...)]` code introduces APIs that silently disappear under `#[cfg(not(feature = ...))]` in ways that break downstream.
- ENFORCE BY: facade modules that provide a stable API with feature-gated implementations; explicit cfg-gated modules only when the API itself is cfg-specific.
[PROVENANCE] SemVer hazards include cfg-dependent API drift.
[VERIFICATION] Downstream compilation under supported feature sets.

[CONTRACT: CTR-2003] Fail-Closed Feature Flags.
- REJECT IF: feature flags controlling security-sensitive behavior default to enabled (fail-open).
- ENFORCE BY: default to disabled; require explicit opt-in via environment or feature flag.
[PROVENANCE] APM2 Security Policy; CTR-FLAG001.

## References (Normative Anchors)

- Rust Reference: Conditional compilation: https://doc.rust-lang.org/reference/conditional-compilation.html
- Rust Reference: Attributes: https://doc.rust-lang.org/reference/attributes.html
- Cargo features: https://doc.rust-lang.org/cargo/reference/features.html
