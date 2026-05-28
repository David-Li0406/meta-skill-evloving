# 07 — Errors, Panics, Diagnostics (Failure Semantics as Contract)

[CONTRACT: CTR-0701] Failure Channel Selection.
- `Option`: absence is expected and non-diagnostic.
- `Result`: fallibility with diagnosable cause.
- panic: bug boundary only; never an input-driven control-flow mechanism in library code.
- REJECT IF: untrusted input can trigger panic.
- ENFORCE BY: parse/validate as `Result`; keep panics behind impossible-by-construction invariants.
[PROVENANCE] Rust Reference: panic is not UB; UB list remains relevant for unsafe even when panics occur.

[HAZARD: RSK-0701] Panic-as-DoS in Public/Untrusted Paths.
- TRIGGER: `unwrap`, `expect`, `panic!`, `unreachable!`, indexing (`v[i]`), `str` slicing by byte offsets.
- FAILURE MODE: attacker-controlled inputs crash the process or abort a task.
- REJECT IF: a panic site is reachable from untrusted inputs or external boundary conditions.
- ENFORCE BY: fallible APIs (`get`, checked indexing, `Result`); input caps; explicit error variants.
[PROVENANCE] std docs: indexing and slicing can panic; Rust Reference: panic semantics.

[CONTRACT: CTR-0702] Panic Surface Audit Is Mandatory for Foundational Code.
- REJECT IF: a change introduces a new panic site without a classification.
- Classification: unreachable-by-construction; debug-only; unacceptable.
- ENFORCE BY: local proofs (types, invariants); tests that would fail if the panic becomes reachable.
[PROVENANCE] Rust Reference: panics are not UB; correctness still requires explicit failure semantics.
[VERIFICATION] `cargo test` with negative cases; fuzzers for parsing paths; property tests for state machines.

[INVARIANT: INV-0701] Panic Safety for Unsafe-Backed State (Unwind Safety).
- REJECT IF: panic/unwind can leave a value in a state where later safe code can trigger UB (double-free, invalid reference, use-after-free).
- ENFORCE BY: commit/rollback protocols; poisoning; two-phase initialization; ensure `Drop` sees a consistent state.
[PROVENANCE] Rust Reference: destructors run during unwinding; unsafe code remains subject to UB rules.
[VERIFICATION] Unwind tests under `panic=unwind`; Miri for unsafe invariants; fault-injection tests for mid-operation panics.

[HAZARD: RSK-0702] Panicking `Drop` Escalates Failures.
- FAILURE MODE: double panic during unwinding aborts the process; partial cleanup; corrupted global invariants.
- REJECT IF: `Drop::drop` can panic (directly or via fallible operations that panic).
- ENFORCE BY: `Drop` is infallible; move fallible cleanup into explicit `close()`/`shutdown()` APIs.
[PROVENANCE] Rust Reference: destructor execution during unwinding; panic behavior is observable and may abort.
[VERIFICATION] Tests that run under `panic=unwind` and induce drop during unwinding.

[CONTRACT: CTR-0703] Error Types Must Be Structured When Callers Branch on Cause.
- REJECT IF: public APIs return opaque strings when callers must distinguish error causes.
- ENFORCE BY: enums for error kinds; include actionable context (indices, ranges, sizes); stable `Display` messages.
[PROVENANCE] std error traits and conventions; public API stability expectations.

```rust
// Pattern: Typed Error Model
#[derive(Debug, thiserror::Error)]
pub enum FsEditError {
    #[error("path rejected: {0}")]
    PathRejected(String),
    #[error("payload too large: {size} > {max}")]
    TooLarge { size: u64, max: u64 },
    #[error(transparent)]
    Io(#[from] std::io::Error),
}
```

[CONTRACT: CTR-0704] `#[must_use]` on Values That Carry Correctness Obligations.
- REJECT IF: dropping a value can silently discard an error, guard, token, or pending operation required for correctness.
- ENFORCE BY: `#[must_use]` on results/guards/tokens; clippy lint policy that denies unused results where appropriate.
[PROVENANCE] Rust Reference: diagnostics attributes (`must_use`).
[VERIFICATION] Clippy with warnings denied; tests that assert guard drop behavior when relevant.

[CONTRACT: CTR-0705] Lint Policy Is a Contract.
- REJECT IF: `allow(...)` is introduced without a local rationale and scope minimization.
- ENFORCE BY: workspace lint policy; local suppressions only with precise targets.
[PROVENANCE] Rust Reference: attributes (lint attributes).

[CONTRACT: CTR-0706] Non-Critical Error Visibility (Tracing over Printing).
- REJECT IF: library code uses `println!`, `eprintln!`, or `dbg!` for diagnostics or non-critical errors.
- ENFORCE BY: use the `tracing` crate (or `log`) for warnings and info; allow callers to decide on collection/visibility.
[PROVENANCE] APM2 Implementation Standard.

## References (Normative Anchors)

- Rust Reference: Attributes (`must_use`, lint attributes): https://doc.rust-lang.org/reference/attributes.html
- Rust Reference: Destructors (drop during unwinding): https://doc.rust-lang.org/reference/destructors.html
- Rust Reference: Behavior considered undefined: https://doc.rust-lang.org/reference/behavior-considered-undefined.html
- std error docs: https://doc.rust-lang.org/std/error/
