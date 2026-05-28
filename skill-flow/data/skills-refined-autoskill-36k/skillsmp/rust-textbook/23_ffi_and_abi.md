# 23 — FFI and ABI (Unsafe Boundaries With Long Tails)

[CONTRACT: CTR-2301] `extern` Declarations Are Assertions.
- REJECT IF: external declarations are treated as "imports" rather than unchecked ABI assertions.
- ENFORCE BY: keep extern declarations in a single module; expose safe wrappers that validate all preconditions.
[PROVENANCE] Rust Reference: external blocks declare foreign items; signatures are unchecked by the compiler.

[CONTRACT: CTR-2302] Rust 2024: `unsafe extern` Is Required.
- REJECT IF: external blocks are not marked `unsafe extern` under Rust 2024.
[PROVENANCE] Rust Reference: edition 2024 requires `unsafe` on extern blocks.

[CONTRACT: CTR-2303] ABI and Unwinding Must Be Explicit.
- REJECT IF: panic/unwind can cross a non-unwinding foreign boundary.
- ENFORCE BY: use `"C-unwind"` only when the foreign caller supports unwinding; otherwise contain panics (`catch_unwind`) or enforce abort-at-boundary policy.
[PROVENANCE] Rust Reference: function ABIs include unwinding categories; unwinding across incompatible ABIs is forbidden.
[VERIFICATION] Integration tests that force panics at the boundary under `panic=unwind`; platform-specific harnesses where applicable.

[CONTRACT: CTR-2304] Ownership Transfer Protocol Must Be Stated.
- REJECT IF: allocation/free responsibilities are implicit.
- Required contract fields:
  - which side allocates
  - which side deallocates
  - which allocator must be used
  - lifetime rules for pointers/slices/strings
- ENFORCE BY: opaque handles; explicit `*_free` functions; length-delimited buffers; avoid "C string" APIs unless required.
[PROVENANCE] Ownership and allocator choice are not inferable by the compiler; FFI correctness depends on explicit conventions.

[INVARIANT: INV-2301] FFI Pointer Validity Must Satisfy Rust Validity When Constructing Rust Types.
- REJECT IF: `&T`/`&mut T`/`&str` is constructed from FFI pointers without proving:
  - alignment (INV-0003)
  - initialization (INV-0002)
  - validity for `T` (INV-0001, INV-0802)
  - provenance for dereference (INV-0006)
- ENFORCE BY: validate before constructing Rust references; keep raw pointers raw until validity holds.
[PROVENANCE] Rust Reference: invalid reference dereference is UB; `str` requires UTF-8 validity (std).
[VERIFICATION] Miri for unsafe conversions; fuzzers for boundary parsing of byte buffers.

[HAZARD: RSK-2301] Layout and Padding Assumptions in FFI.
- REJECT IF: FFI relies on `repr(Rust)` layout or enum niche layout.
- ENFORCE BY: `repr(C)`/`repr(transparent)`; explicit field-by-field marshaling; wire-format encoding independent of layout.
[PROVENANCE] Rust Reference: type layout is unspecified unless constrained by `repr`.
[VERIFICATION] ABI tests against C headers; bindgen checks in CI when used.

[CONTRACT: CTR-2305] Safe Wrapper Pattern (stdlib-grade).
- Structure:
  - `mod ffi { unsafe extern { ... } }`
  - `pub fn safe_api(...) -> Result<...>` wrappers that validate inputs and translate outputs.
- REJECT IF: unsafe FFI calls are scattered across the codebase.
- ENFORCE BY: one module owns the boundary; wrappers define the contract.
[PROVENANCE] Rust Reference: extern blocks are unsafe operations; unsafe must be locally justified.

## References (Normative Anchors)

- Rust Reference: External blocks: https://doc.rust-lang.org/reference/items/external-blocks.html
- Rust Reference: Unsafety: https://doc.rust-lang.org/reference/unsafety.html
- Rust Reference: Functions (ABI and unwinding): https://doc.rust-lang.org/reference/items/functions.html
- std `ffi`: https://doc.rust-lang.org/std/ffi/
- Rustonomicon (FFI): https://doc.rust-lang.org/nomicon/ffi.html
