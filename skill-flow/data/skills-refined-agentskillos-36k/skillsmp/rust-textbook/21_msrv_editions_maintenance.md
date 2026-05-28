# 21 — MSRV, Editions, Maintenance (Compatibility as Protocol)

[CONTRACT: CTR-2101] MSRV Is a Compatibility Contract.
- REJECT IF: MSRV is implicit.
- REJECT IF: code changes effectively bump MSRV without an explicit contract update (syntax, std APIs, dependency MSRV).
- ENFORCE BY: `rust-version`; CI job pinned to MSRV; dependency policy that tracks transitive MSRV.
[PROVENANCE] Cargo `rust-version` defines the declared toolchain floor; dependency MSRV propagates to consumers.
[VERIFICATION] CI build/test under MSRV; optional minimal-versions policy checks.

[CONTRACT: CTR-2102] Edition Upgrades Are Planned Migrations.
- REJECT IF: edition is upgraded without a migration plan and CI coverage across supported toolchains.
- ENFORCE BY: explicit edition decision; apply migration tooling; audit macro/cfg/unsafe surfaces after upgrade.
[PROVENANCE] Rust editions change parsing/resolution and some lint/keyword rules; semantics can still evolve in underspecified areas.
[VERIFICATION] CI against MSRV and current stable; compile macro-heavy crates across the matrix.

[CONTRACT: CTR-2103] Deprecation and Behavior Changes Require Compatibility Strategy.
- REJECT IF: behavior changes land without a deprecation path when consumers depend on the behavior.
- ENFORCE BY: additive APIs; deprecation attributes; migration docs; compatibility tests.
[PROVENANCE] Public API stability is a library contract; Rust provides deprecation attributes.

## References (Normative Anchors)

- Rust 2024 Edition Guide: https://doc.rust-lang.org/edition-guide/rust-2024/index.html
- Cargo `rust-version`: https://doc.rust-lang.org/cargo/reference/manifest.html#the-rust-version-field
