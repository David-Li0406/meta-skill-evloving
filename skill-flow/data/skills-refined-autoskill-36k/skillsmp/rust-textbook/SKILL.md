---
name: rust-textbook
description: Agent-native Rust protocol specification for high-assurance systems programming.
---

# Rust Agent Protocol Specification (Rust 2024; MSRV 1.85)

Fail-closed protocol spec for agents producing standard-library-grade Rust (core/std/tokio/serde class).

Rust has no single formal language spec. Normative anchors are the Rust Reference and standard library documentation. Where
behavior is underspecified, treat reliance as a defect unless it is isolated, documented, and defended by verification.

## Taxonomy

Every rule uses tagged lines:

- `[INVARIANT]`: always-true property required for soundness/correctness.
- `[HAZARD]`: compiler/hardware/runtime behavior that causes UB or logic failures.
- `[CONTRACT]`: interface boundary requirement (public API, trait boundary, FFI).
- `[PROVENANCE]`: normative citation requirement (Rust Reference/std docs section anchor).
- `[VERIFICATION]`: mandated tool evidence (Miri, Kani, Loom, Proptest).

## Rule Block Format

Each rule uses a fail-closed structure:

- `[INVARIANT: INV-XXXX]` / `[HAZARD: RSK-XXXX]` / `[CONTRACT: CTR-XXXX]`
- `REJECT IF: ...` (non-negotiable rejection conditions)
- `ENFORCE BY: ...` (types, patterns, wrappers)
- `[PROVENANCE] ...` (URLs + section anchors)
- `[VERIFICATION] ...` (tool + minimal invocation)

No Markdown tables. Use code-fenced matrices (aligned columns or delimited rows).

ID scheme: `XXXX = CCSS` where `CC` is the chapter number and `SS` is a within-chapter sequence.

## Assumptions

- Edition: 2024
- MSRV baseline: rustc 1.85 (enforce in CI)
- Target: foundational crates and high-assurance systems code

## Chapters

- 00_contract_and_truth.md
- 01_compilation_pipeline.md
- 02_toolchain_cargo_build.md
- 03_core_language_semantics.md
- 04_ownership_borrowing_model.md
- 05_lifetimes_variance_hrtb.md
- 06_traits_generics_coherence.md
- 07_errors_panics_diagnostics.md
- 08_layout_repr_drop.md
- 09_unsafe_rust_obligations.md
- 10_concurrency_atomics_memory_order.md
- 11_async_pin_cancellation.md
- 12_api_design_stdlib_quality.md
- 13_collections_allocation_models.md
- 14_unicode_text_graphemes.md
- 15_paths_filesystem_os.md
- 16_io_protocol_boundaries.md
- 17_testing_fuzz_miri_evidence.md
- 18_performance_measurement.md
- 19_security_adjacent_rust.md
- 20_cfg_features_build_matrix.md
- 21_msrv_editions_maintenance.md
- 22_macros_buildscripts_proc_macros.md
- 23_ffi_and_abi.md
- 24_hazard_catalog_checklists.md
- 25_time_monotonicity_determinism.md
- 26_apm2_safe_patterns_and_anti_patterns.md
