# 01 — rustc Compilation Pipeline (Semantic Phase Protocol)

[INVARIANT: INV-0101] Phase-Aware Reasoning.
- REJECT IF: correctness depends on the surface syntax instead of the expanded + lowered semantics.
- ENFORCE BY: reason about expanded code (macros/attributes/cfg), then about MIR-level effects (drops, borrows).
[PROVENANCE] rustc pipeline background: rustc-dev-guide; Rust Reference: attributes and conditional compilation semantics.

[HAZARD: RSK-0101] Macro Expansion Is a Semantic Transform.
- TRIGGER: `macro_rules!`, derive macros, attribute macros, `cfg_attr`, `#[doc = include_str!(...)]`.
- FAILURE MODE: small diff, large semantic delta (new items, new impls, new `unsafe`, new cfg surfaces).
- REJECT IF: macro changes are not accompanied by at least one expansion inspection path in a trusted environment.
- ENFORCE BY: inspect expansion (tooling such as `cargo expand`); add compile-fail/compile-pass tests for macro surfaces.
[PROVENANCE] Rust Reference: attributes (active vs inert; meta expansion ordering); Conditional compilation (cfg rewriting rules).
[VERIFICATION] Compile macro-expanded surfaces in CI on representative configurations.

[HAZARD: RSK-0102] Attribute Processing Removes and Rewrites Code.
- TRIGGER: new `#[cfg]`, `#[cfg_attr]`, `#[path]`, `#[repr(...)]`, linking attributes.
- FAILURE MODE: "dark code" (excluded code not type-checked) and configuration-dependent semantics drift.
- REJECT IF: new cfg branches are not covered by at least one CI build/test configuration.
[PROVENANCE] Rust Reference: attributes (activity); Conditional compilation (cfg attr effect).
[VERIFICATION] CI build matrix includes cfg/feature permutations; deny unused cfg branches when feasible.

[HAZARD: RSK-0103] Drop and Borrow Semantics Are Checked Over Lowered Forms.
- TRIGGER: refactors that move `;`, change block shapes, or alter pattern binding modes.
- FAILURE MODE: drop-scope changes; temporary lifetime changes; moved-from use changes; borrow region shifts.
- REJECT IF: a refactor is accepted without checking whether it changes drop scopes or borrow regions.
[PROVENANCE] Rust Reference: expressions (temporaries); destructors (drop scopes).
[VERIFICATION] Regression tests that lock drop timing when observable; Miri for unsafe drop-scope interactions.

[CONTRACT: CTR-0101] Diagnostics Are Not Proof.
- REJECT IF: "it compiles" is used as a correctness argument for unsafe, concurrency protocols, or parsing.
- ENFORCE BY: encode invariants in types; add negative tests; use tool-backed verification for risk anchors.
[PROVENANCE] Rust Reference: Behavior considered undefined (classes of UB compile cleanly).

[HAZARD: RSK-0104] Compile-Time Resource Exhaustion (Variety Explosion).
- TRIGGER: new generic layers on public APIs; large derive expansions; heavy proc-macro graphs.
- FAILURE MODE: downstream compile-time regression; code size inflation.
- REJECT IF: public generic surface is expanded without an explicit compile-time cost rationale.
- ENFORCE BY: keep generics local; hide helper traits/types; prefer non-generic public wrappers where acceptable.
[PROVENANCE] rustc-dev-guide: query system and incremental compilation model (background).
[VERIFICATION] Track compile-time metrics (CI timing budgets or perf harness) for foundational crates.

## References (Normative Anchors)

- Rust Reference: https://doc.rust-lang.org/reference/
- Rust Reference: Attributes: https://doc.rust-lang.org/reference/attributes.html
- Rust Reference: Conditional compilation: https://doc.rust-lang.org/reference/conditional-compilation.html
- Rust Reference: Expressions (temporaries): https://doc.rust-lang.org/reference/expressions.html
- Rust Reference: Destructors (drop scopes): https://doc.rust-lang.org/reference/destructors.html
- rustc-dev-guide: https://rustc-dev-guide.rust-lang.org/
