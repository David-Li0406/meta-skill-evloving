# 00 — Rust Abstract Machine: Primitive Invariants and Contract Surfaces

[CONTRACT: CTR-0001] Fail-Closed Acceptance.
- REJECT IF: any soundness/correctness claim lacks an explicit enforcement mechanism (types, checks, tests, or a verification tool).
- REJECT IF: behavior depends on underspecified language/library behavior without isolation + regression tests.
- ENFORCE BY: smallest possible trusted surface; explicit contracts at boundaries; tool-backed verification for risk anchors.

[CONTRACT: CTR-0002] Rule Vocabulary (Stable Terms).
- ENFORCE BY: use these terms with the defined meaning; treat ambiguous usage as a defect.
- Place: `(addr, metadata, provenance)` identifying a storage location.
- Value: a typed datum produced by evaluating an expression.
- Move: semantic deinitialization of a place; not a bitwise operation.
- Validity: bit-pattern and structural constraints required for a value to be a valid `T`.
- Soundness: no safe Rust usage can cause Undefined Behavior (UB).
- Correctness: behavior matches specification, even if not UB.

## Primitive Invariants (Rust Abstract Machine)

[INVARIANT: INV-0001] Type Validity.
- REJECT IF: bytes are reinterpreted as `T` without proving `T` validity.
- REJECT IF: a value is dropped as `T` unless it is valid for `T`.
- ENFORCE BY: validated constructors; `TryFrom`; typestates; `MaybeUninit<T>` for uninitialized storage.
[PROVENANCE] Rust Reference: Behavior considered undefined (invalid values).
[VERIFICATION] Miri for unsafe boundaries; Proptest/Kani for constructor/model invariants.

[INVARIANT: INV-0002] Initialization Before Read.
- REJECT IF: any code path reads uninitialized memory as a typed value.
- ENFORCE BY: `MaybeUninit<T>` + explicit initialization protocol; avoid `mem::zeroed()` for non-zeroable types.
[PROVENANCE] Rust Reference: Behavior considered undefined (reading uninitialized memory; invalid values).
[VERIFICATION] Miri with strict checks; targeted tests that exercise partial-init paths.

[INVARIANT: INV-0003] Alignment for Typed Access.
- REJECT IF: dereference or reference creation can target a misaligned address for `T`.
- ENFORCE BY: `ptr::read_unaligned`/`write_unaligned` for unaligned accesses; `Layout`-correct allocation; avoid `#[repr(packed)]` field references.
[PROVENANCE] Rust Reference: Behavior considered undefined (misaligned pointer dereference); Expressions (borrow operators and reference creation).
[VERIFICATION] Miri; targeted tests for packed/byte-buffer paths.

[INVARIANT: INV-0004] Reference Validity (`&T`, `&mut T`).
- REJECT IF: any `&T`/`&mut T` can be created to unaligned, uninitialized, or non-dereferenceable memory.
- REJECT IF: `&mut T` aliasing cannot be proven exclusive for the reference lifetime.
- ENFORCE BY: raw borrows (`&raw const`, `&raw mut`) when reference validity cannot be established; keep raw pointers raw until validity holds.
[PROVENANCE] Rust Reference: Expressions (borrow operators; raw borrows motivation); Behavior considered undefined (dangling/unaligned references).
[VERIFICATION] Miri; negative tests for invalid-reference construction.

[INVARIANT: INV-0005] Aliasing Discipline (Safe Rust Model).
- REJECT IF: safe code observes mutation through shared references without `UnsafeCell`.
- REJECT IF: `&mut` exclusivity is violated (including via reborrows) in a way that could be observed by safe code.
- ENFORCE BY: confine mutation behind `UnsafeCell`-based primitives; keep `unsafe` blocks small; avoid creating references from raw pointers unless exclusivity holds.
[PROVENANCE] Rust Reference: Expressions (borrow operators; mutable borrow restrictions); Behavior considered undefined (data races; invalid dereference).
[VERIFICATION] Miri (stacked-borrows model); Loom for concurrent aliasing protocols.

[INVARIANT: INV-0006] Provenance for Dereference (Strict Provenance).
- REJECT IF: pointer provenance is discarded and the resulting pointer is dereferenced.
- ENFORCE BY: preserve provenance across address manipulation via `ptr::addr`, `ptr::with_addr`, `ptr::map_addr`; avoid pointer-int-pointer roundtrips for dereferenceable pointers.
[PROVENANCE] std docs: primitive pointer methods (`addr`, `with_addr`, `map_addr`) provenance notes; Rust Reference: Behavior considered undefined (invalid pointer dereference).
[VERIFICATION] Miri with strict provenance checking where supported.

[INVARIANT: INV-0007] Data Race Freedom.
- REJECT IF: concurrent access can produce a data race.
- ENFORCE BY: locks; atomics with a named protocol; ownership transfer; `Send`/`Sync` invariants for shared types.
[PROVENANCE] Rust Reference: Behavior considered undefined (data races).
[VERIFICATION] Loom for custom synchronization; stress tests for high-contention paths.

[INVARIANT: INV-0008] Drop Discipline (Exactly Once for Initialized State).
- REJECT IF: a value can be dropped twice or leaked in a way that violates the type contract.
- REJECT IF: partial initialization can lead to dropping uninitialized fields.
- ENFORCE BY: `MaybeUninit` field-by-field init; `ManuallyDrop` only with an explicit drop protocol; avoid `Vec::set_len` without a proof of element initialization.
[PROVENANCE] Rust Reference: Destructors (drop scopes; partial initialization); Behavior considered undefined (use-after-free; invalid values).
[VERIFICATION] Miri; tests covering early-return/panic paths that cross initialization boundaries.

[INVARIANT: INV-0009] Panic Safety for Unsafe-Backed Types.
- REJECT IF: panic/unwind can leave an unsafe-backed value in a state where later safe code can trigger UB (double-free, use-after-free, invariant break).
- ENFORCE BY: commit/rollback protocols; poison-on-panic; `catch_unwind` at FFI boundaries where unwind may cross; prefer `panic=abort` only with an explicit abort contract.
[PROVENANCE] Rust Reference: functions (ABI categories including unwinding); FFI boundaries require explicit unwind containment strategy.
[VERIFICATION] Unwind tests under `panic=unwind`; targeted fault-injection tests.

## Risk Anchors (Escalate Verification)

[HAZARD: RSK-0001] Soundness Escalators.
- TRIGGER: `unsafe`, raw pointers, `MaybeUninit`, `ManuallyDrop`, `transmute`, `from_raw_parts`, `set_len`, `unsafe impl Send/Sync`, custom atomics, FFI, `#[cfg]` permutations.
- REJECT IF: verification plan is absent (tests + tool choice) for triggered areas.
[PROVENANCE] Rust Reference: Unsafety (unsafe operations list); Conditional compilation (cfg semantics).
[VERIFICATION] Miri for unsafe; Loom for concurrency; Proptest for state machines/parsers; Kani for bounded proofs where applicable.

## References (Normative Anchors)

- Rust Reference: Behavior considered undefined: https://doc.rust-lang.org/reference/behavior-considered-undefined.html
- Rust Reference: Unsafety: https://doc.rust-lang.org/reference/unsafety.html
- Rust Reference: Expressions (borrow operators; raw borrows): https://doc.rust-lang.org/reference/expressions/operator-expr.html
- Rust Reference: Destructors (drop scopes; partial init): https://doc.rust-lang.org/reference/destructors.html
- std pointer docs (strict provenance APIs): https://doc.rust-lang.org/std/primitive.pointer.html
