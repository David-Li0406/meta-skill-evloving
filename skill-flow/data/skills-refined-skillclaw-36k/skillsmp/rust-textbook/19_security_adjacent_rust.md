# 19 — Security-Adjacent Rust (What Memory Safety Does Not Solve)

[CONTRACT: CTR-1901] Threat Model Must Include Non-Memory-Safety Failures.
- REJECT IF: security posture assumes "memory safe == secure."
- ENFORCE BY: explicit threat model for:
  - resource exhaustion (CPU, memory, file descriptors)
  - panic-as-DoS
  - logic bugs (authz, integrity)
  - nondeterminism (reproducibility, consensus drift)
  - supply chain and build-time code execution
[PROVENANCE] Rust guarantees memory safety in safe code; it does not guarantee availability or correctness.

[HAZARD: RSK-1901] Resource Exhaustion via Untrusted Inputs.
- TRIGGER: parsing, decompression, regex, recursion, unbounded allocations, uncontrolled concurrency.
- FAILURE MODE: OOM, CPU spikes, thread exhaustion.
- REJECT IF: boundary code lacks size/depth/time caps.
- ENFORCE BY: explicit caps; checked arithmetic; streaming/iterative algorithms; backpressure.
[PROVENANCE] Availability is not guaranteed by type safety.
[VERIFICATION] Fuzzing with size amplification corpora; load tests; property tests for bounded resource usage.

[HAZARD: RSK-1902] Panic-as-DoS.
- REJECT IF: attacker-controlled inputs can trigger panics (see RSK-0701).
- ENFORCE BY: fallible parsing; boundary checks; avoid indexing panics in untrusted paths.
[PROVENANCE] Panic semantics are observable and can abort tasks/processes.

[HAZARD: RSK-1903] Unsafe Code Escalates to Security-Critical.
- REJECT IF: unsafe changes ship without Miri coverage and explicit safety preconditions (CTR-0902).
- ENFORCE BY: minimize unsafe; isolate unsafe; add tests that exercise the unsafe boundary.
[PROVENANCE] Rust Reference: unsafe does not relax UB; UB enables miscompilation and exploitation.
[VERIFICATION] Miri; fuzzers for unsafe boundary glue.

[HAZARD: RSK-1904] Supply Chain and Build-Time Code Execution.
- TRIGGER: new dependencies; build scripts; proc macros; code generation.
- FAILURE MODE: malicious code execution at build time; dependency confusion; transitive vulnerability surface.
- REJECT IF: dependency additions lack policy review (license, audit, MSRV, minimal features).
- ENFORCE BY: minimize dependencies; disable default features; pin and audit critical crates; restrict build scripts and proc macros.
[PROVENANCE] Cargo executes build scripts and proc macros on the build host.
[VERIFICATION] Dependency audit gates; reproducible build checks where required.

[HAZARD: RSK-1905] Unicode Normalization and Confusables.
- REJECT IF: identifiers or security-relevant keys are compared without an explicit Unicode policy (see RSK-1402).
- ENFORCE BY: define normalization/case-folding; treat as bytes where Unicode semantics are not required.
[PROVENANCE] Unicode security issues exist independent of memory safety.

[HAZARD: RSK-1906] Nondeterminism as Integrity Failure.
- TRIGGER: wall-clock time in core logic, RNG without explicit seeding, hash iteration order, `cfg`-dependent behavior drift.
- FAILURE MODE: divergent outputs across nodes; reproducibility failure; consensus drift.
- REJECT IF: nondeterminism enters a domain that requires deterministic outputs (signatures, hashing, consensus state machines).
- ENFORCE BY: deterministic time sources (see Chapter 25); explicit seeding; sort before hashing; build-matrix coverage for cfg.
[PROVENANCE] Determinism is a system contract; Rust does not enforce determinism.
[VERIFICATION] Deterministic test harnesses; CI build matrix; property tests for determinism.

[CONTRACT: CTR-1907] Complete Audit and Ledger Data (Anti-Information Loss).
- Audit trails and ledger events MUST capture all possible associated values to prevent information loss.
- REJECT IF: audit/ledger fields use `Option<T>` when multiplicity (multiple associated items) is possible.
- ENFORCE BY: use `Vec<T>` instead of `Option<T>` for associated identifiers (e.g., `pr_numbers: Vec<u64>` instead of `pr_number: Option<u64>`).
[PROVENANCE] APM2 Security Policy; RSK-1906 (Nondeterminism/Integrity).

[CONTRACT: CTR-1908] Serialization in Crypto Contexts.
- REJECT IF: serialization errors are swallowed when the output feeds into a hash or signature.
- ENFORCE BY: propagate all serialization failures to prevent silent corruption of hash chains.
[PROVENANCE] APM2 Implementation Standard; CTR-0701.

## References (Normative Anchors)

- Rust Reference: Behavior considered undefined: https://doc.rust-lang.org/reference/behavior-considered-undefined.html
- Cargo build scripts: https://doc.rust-lang.org/cargo/reference/build-scripts.html
- Rust Reference: Conditional compilation: https://doc.rust-lang.org/reference/conditional-compilation.html
