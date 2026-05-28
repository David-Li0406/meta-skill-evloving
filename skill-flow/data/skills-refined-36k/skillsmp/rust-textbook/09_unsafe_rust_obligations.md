# 09 — Unsafe Rust (Obligation Ledger and Proof Discipline)

[INVARIANT: INV-0901] `unsafe` Does Not Relax UB Rules.
- REJECT IF: an argument relies on "it is inside unsafe" as justification.
- ENFORCE BY: treat every unsafe operation as a local proof obligation against the Rust Abstract Machine invariants (INV-0001..0009).
[PROVENANCE] Rust Reference: `unsafe` shifts responsibility; UB remains forbidden.

[CONTRACT: CTR-0901] Unsafe Surface Classification.
- `unsafe fn`: caller must uphold preconditions.
- `unsafe trait`: implementer and/or caller must uphold extra conditions.
- `unsafe impl`: asserts those conditions for a concrete type.
- `unsafe { ... }`: local scope contains unsafe operations; local proof required.
- REJECT IF: safety preconditions are implicit or scattered.
[PROVENANCE] Rust Reference: the `unsafe` keyword (unsafe fn/blocks/traits/impls).

[CONTRACT: CTR-0902] `// SAFETY:` Comment Format (Post-Condition Form).
- REJECT IF: an `unsafe { ... }` block lacks a local `// SAFETY:` comment.
- REJECT IF: the comment does not state preconditions, provenance/aliasing assumptions, and post-condition.
- FORMAT:
  - "This block is safe because [Pre-condition] is upheld by [Caller/Previous Step] and results in [Post-condition]."
- ENFORCE BY: one `// SAFETY:` per unsafe block; keep unsafe blocks minimal.
[PROVENANCE] Rust Reference: unsafe operations list defines the boundary; proof must cover the operation’s preconditions.

[INVARIANT: INV-0902] Unsafe Obligation Checklist (Fail-Closed).
- REJECT IF: any item is unproven for an unsafe operation that depends on it.
- Validity: values read/dropped as `T` are valid `T` (INV-0001, INV-0802).
- Alignment: typed access is aligned, or unaligned ops are used (INV-0003, INV-0801).
- Initialization: memory is initialized before typed read (INV-0002).
- Aliasing: reference exclusivity and shared immutability rules are upheld (INV-0005).
- Bounds: pointer arithmetic and slice lengths stay in-bounds; size math is checked.
- Provenance: dereferenceable pointers retain provenance (INV-0006).
- Drop discipline: initialized values dropped exactly once; uninitialized never dropped (INV-0008, INV-0804).
- Panic safety: unwinding cannot expose UB later (INV-0009, INV-0701).
[PROVENANCE] Rust Reference: Behavior considered undefined; Expressions and destructors define many preconditions.
[VERIFICATION] Miri for UB classes; Proptest for state machines; Loom for concurrent unsafe protocols.

[CONTRACT: CTR-0903] APM2 Unsafe Policy (Lints + Justification).
- REJECT IF: new unsafe code is introduced without:
  - workspace lint visibility (`unsafe_code = "warn"`),
  - minimal unsafe scope (unsafe wraps only the unsafe op),
  - a local `// SAFETY:` comment (CTR-0902),
  - and a local `#[allow(unsafe_code)]` (or equivalent lint suppression) with a justification comment.
- ENFORCE BY:
  - keep `[workspace.lints.rust] unsafe_code = "warn"` enabled in root `Cargo.toml`,
  - isolate unsafe behind safe APIs,
  - treat new unsafe sites as security-critical (Chapter 19).
[PROVENANCE] Rust Reference: lint attributes; `unsafe` shifts responsibility, not rules.

[CONTRACT: CTR-0904] Unsafe Is Not a Convenience or Speculation Optimization.
- REJECT IF: unsafe is used for tasks that have safe primitives in std/ecosystem (collections/memory mgmt, pointer math, unchecked indexing, type coercion/transmute).
- REJECT IF: unsafe is introduced for "performance" without profiling evidence and an evaluated safe alternative.
- ALLOW IF: required for a boundary with no safe alternative (syscalls/FFI) AND isolated behind a safe API with targeted tests.
- ENFORCE BY: measure first; isolate; add negative tests and (when applicable) Miri coverage (Chapter 17).
[PROVENANCE] Rust Reference: unsafe does not relax UB; miscompilation is a correctness and security risk.

[INVARIANT: INV-0903] Unsafe Review Checklist (Minimum Bar).
- REJECT IF: any item is missing for new/modified unsafe:
  - local safety proof (CTR-0902) + obligation checklist (INV-0902),
  - minimal scope + justified `#[allow(unsafe_code)]` (CTR-0903),
  - correct cfg/platform gating (Chapter 20),
  - panic/unwind safety is addressed (INV-0701),
  - verification exists (Miri when applicable; Chapter 17).
[VERIFICATION] `cargo test`; Miri for unsafe/memory/provenance hazards; fuzz/property tests for protocols/state machines.

NOTE (APM2): Unix daemonization uses `unsafe { fork() }` and is intentionally isolated; see `crates/apm2-daemon/src/main.rs`.

[HAZARD: RSK-0901] Invalid Reference Creation (Immediate UB When Used as Reference).
- TRIGGER: `&*ptr`, `&mut *ptr`, references to packed fields, references to uninitialized memory, references into freed/allocation-unknown memory.
- REJECT IF: unsafe code creates references without proving reference validity and aliasing exclusivity for the full reference lifetime.
- ENFORCE BY: raw borrows + pointer reads/writes until validity holds; avoid producing references as "convenience values."
[PROVENANCE] Rust Reference: borrow operators; raw borrows exist to avoid invalid references; UB list includes invalid reference dereference.
[VERIFICATION] Miri.

[HAZARD: RSK-0902] Provenance Loss via Pointer-Integer-Pointer Roundtrip.
- TRIGGER: `ptr as usize`, arithmetic on the integer, `usize as *mut T`, then dereference.
- FAILURE MODE: dereference of a pointer without required provenance; UB under strict provenance.
- REJECT IF: a pointer is formed from an integer and later dereferenced without an explicit provenance-preserving mechanism.
- ENFORCE BY: `ptr::addr()` to extract address for non-dereference uses; `ptr::with_addr`/`ptr::map_addr` to adjust addresses while preserving provenance.
[PROVENANCE] std docs: pointer provenance notes on `addr`/`with_addr`/`map_addr`.
[VERIFICATION] Miri with strict provenance checking where supported.

[HAZARD: RSK-0903] Manual Drop/Init APIs Have Hidden Exactly-Once Contracts.
- TRIGGER: `MaybeUninit::assume_init`, `ManuallyDrop`, `mem::forget`, `mem::transmute`, `ptr::read`, `Vec::set_len`, `from_raw_parts`.
- FAILURE MODE: double drop, drop uninitialized, leak required drop, read uninitialized, out-of-bounds, misaligned access.
- REJECT IF: these operations are used without a local proof that covers INV-0902 checklist items.
[PROVENANCE] Rust Reference: unsafety (unsafe operations list); destructors (drop semantics); Behavior considered undefined.
[VERIFICATION] Miri; fuzz for boundary/size cases; property tests for stateful init protocols.

## References (Normative Anchors)

- Rust Reference: The `unsafe` keyword: https://doc.rust-lang.org/reference/unsafe-keyword.html
- Rust Reference: Unsafety (unsafe operations list): https://doc.rust-lang.org/reference/unsafety.html
- Rust Reference: Behavior considered undefined: https://doc.rust-lang.org/reference/behavior-considered-undefined.html
- Rust Reference: Operator expressions (raw borrows): https://doc.rust-lang.org/reference/expressions/operator-expr.html
- Rust Reference: Destructors: https://doc.rust-lang.org/reference/destructors.html
- std pointer docs (strict provenance APIs): https://doc.rust-lang.org/std/primitive.pointer.html
