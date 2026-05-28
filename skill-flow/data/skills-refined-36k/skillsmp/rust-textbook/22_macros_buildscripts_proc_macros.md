# 22 — Macros, Build Scripts, Proc Macros (Expansion and Execution Surfaces)

[CONTRACT: CTR-2201] Macros Are Code Generation; Treat as Semantics.
- REJECT IF: macros implement core logic that cannot be audited in expanded form.
- ENFORCE BY: prefer functions/types for semantics; restrict macros to syntactic convenience.
[PROVENANCE] rustc expands macros before type checking and borrow checking.

[HAZARD: RSK-2201] Hygiene and Name-Resolution Traps.
- TRIGGER: `macro_rules!` without `$crate::` paths; identifier generation; `concat_idents`-style patterns; shadowing.
- FAILURE MODE: cross-crate resolution drift; collision; surprising visibility.
- REJECT IF: a macro relies on caller scope names or ambiguous paths.
- ENFORCE BY: `$crate::` for internal paths; `macro_rules!` scoping discipline; minimal identifier synthesis.
[PROVENANCE] Rust Reference: macro hygiene and name resolution rules.
[VERIFICATION] Compile-pass tests across crates; feature/cfg permutations for macro exports.

[HAZARD: RSK-2202] Hidden `unsafe` and Hidden Contracts in Macro Expansion.
- TRIGGER: macros that emit `unsafe`, raw pointers, `transmute`, `from_raw_parts`, or FFI.
- FAILURE MODE: unsafe obligations are invisible at call sites; callers cannot uphold hidden preconditions.
- REJECT IF: macros emit unsafe operations without emitting an explicit safety boundary (unsafe fn/unsafe block with `// SAFETY:`).
- ENFORCE BY: keep unsafe out of macros; if unavoidable, confine unsafe to a single expanded site with explicit documentation.
[PROVENANCE] Rust Reference: unsafe operations list; unsafe blocks require local proof.
[VERIFICATION] Expansion inspection; Miri on macro-generated unsafe paths.

[HAZARD: RSK-2203] Macro Expansion Ordering and Attribute Interaction.
- TRIGGER: macros inside attributes (doc includes, cfg_attr with macros), nested meta items.
- FAILURE MODE: configuration-dependent expansion; surprising evaluation order; missing cfg coverage.
- REJECT IF: correctness depends on subtle attribute expansion ordering without tests.
[PROVENANCE] Rust Reference: attributes (active/inert; meta processing and ordering notes).
[VERIFICATION] Compile matrix; tests that exercise affected attribute/macro combinations.

[HAZARD: RSK-2204] Build-Time Code Execution (Build Scripts and Proc Macros).
- REJECT IF: build scripts or proc macros perform network I/O.
- REJECT IF: build output depends on ambient environment without declared inputs.
- ENFORCE BY: deterministic inputs; minimal dependency graphs; documented `cargo:` outputs; restricted CI environment.
[PROVENANCE] Cargo executes build scripts and proc macros on the build host.
[VERIFICATION] CI in a restricted environment; diff-based checks for committed generated outputs.

[CONTRACT: CTR-2202] Variety Budget Escalation (Decomposition Required).
- REJECT IF: a macro/proc-macro/build change exceeds reviewability constraints (large expansion, many cfg branches, many unsafe sites) without decomposition.
- ENFORCE BY: split macros; generate inspectable artifacts in trusted CI; isolate unsafe and cfg-heavy code behind narrow interfaces.
[PROVENANCE] Complexity increases error rate; fail-closed posture rejects underspecified expansion surfaces.

## References (Normative Anchors)

- Rust Reference: Macros: https://doc.rust-lang.org/reference/macros.html
- Rust Reference: Attributes: https://doc.rust-lang.org/reference/attributes.html
- Cargo build scripts: https://doc.rust-lang.org/cargo/reference/build-scripts.html
