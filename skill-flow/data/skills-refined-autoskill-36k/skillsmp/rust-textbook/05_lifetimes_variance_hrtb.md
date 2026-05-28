# 05 — Lifetimes, Variance, HRTBs, Pin (Type-Level Protocols)

[CONTRACT: CTR-0501] Lifetime Parameters Are Compile-Time Constraints.
- REJECT IF: an API relies on a runtime interpretation of lifetimes (timers, wall clock, cancellation).
- ENFORCE BY: model runtime timeouts/cancellation explicitly via values (tokens, deadlines) and state machines.
[PROVENANCE] Rust lifetime parameters exist only at compile time; runtime behavior is not specified by lifetime syntax.

[CONTRACT: CTR-0502] Reference-Returning APIs Must State Ties.
- REJECT IF: an output reference lifetime is unclear (which input or internal storage owns it).
- ENFORCE BY: explicit lifetime parameters when elision hides meaning; document storage/move hazards when returning references into internal buffers.
[PROVENANCE] Rust Reference: lifetime elision rules; borrowing and reference validity requirements.

[INVARIANT: INV-0501] Variance Determines Allowed Substitutions.
- REJECT IF: variance changes accidentally (often via introducing `UnsafeCell`, `&mut`, or `PhantomData` adjustments) without an explicit usability/soundness rationale.
- ENFORCE BY: audit variance when changing fields or phantom markers of public types.
[PROVENANCE] Rust Reference: subtyping and variance rules (generics).

## Matrix: Common Variance Constructors

```text
Type constructor; Parameter; Variance; Primary hazard
&'a T; 'a; covariant; returning references tied to internal mutation (RSK-0402)
&'a T; T; covariant; exposing borrowed view of unstable storage (RSK-0402)
&'a mut T; 'a; covariant; borrow spans yield points (RSK-0403)
&'a mut T; T; invariant; accidental invariance reduces usability; often correct for mutation
*const T; T; covariant; pointer casts hide validity/provenance obligations (INV-0006)
*mut T; T; invariant; writing through pointer requires exact type/validity (INV-0001)
UnsafeCell<T>; T; invariant; interior mutability requires explicit protocol (RSK-0401)
PhantomData<T>; T; covariant; dropck/ownership modeling must match reality (RSK-0502)
fn(T) -> U; T; contravariant; wrong variance breaks API substitutability
fn(T) -> U; U; covariant; returning owned values may leak invariants if not validated
```

[HAZARD: RSK-0501] Accidental Invariance and API Lock-In.
- TRIGGER: adding `UnsafeCell<T>`, `&mut T`, `PhantomData<*mut T>`, `PhantomData<&'a mut T>` to public types.
- FAILURE MODE: callers cannot coerce lifetimes/types as expected; downstream breakage.
- REJECT IF: variance changes without explicit intent and a migration strategy (if public).
[PROVENANCE] Rust variance/subtyping rules are structural; field changes propagate to public type variance.

[HAZARD: RSK-0502] PhantomData Mismatch (Dropck and Auto-Trait Drift).
- TRIGGER: raw pointers/FFI handles in a struct; `PhantomData` added/removed/changed; manual `Send`/`Sync`.
- FAILURE MODE:
  - dropck allows a value to outlive borrowed/owned state it logically depends on
  - auto-trait derivation (`Send`/`Sync`) becomes incorrect for the logical ownership model
  - variance becomes incorrect for the intended lifetime contract
- REJECT IF: the logical ownership/borrowing model of a type is not reflected in its fields and phantom markers.
- ENFORCE BY:
  - logical ownership: `PhantomData<T>`
  - logical borrow: `PhantomData<&'a T>` (or `&'a mut T` for exclusivity/invariance as required)
  - explicit invariance: `PhantomData<*mut T>` or `UnsafeCell<T>` when mutation/aliasing protocols require it
[PROVENANCE] std `PhantomData` docs; Rustonomicon dropck and ownership modeling guidance.
[VERIFICATION] Compile-time assertions for expected auto-traits; Miri for drop-time pointer validity when unsafe is involved.

[CONTRACT: CTR-0503] HRTBs (`for<'a>`) Declare Universality.
- REJECT IF: an HRTB is introduced to "make the compiler accept it" without a semantic explanation.
- ENFORCE BY: document the universal quantification meaning; add compile-time examples that demonstrate capture constraints.
[PROVENANCE] Rust Reference: higher-ranked trait bounds (`for<...>`) semantics.
[VERIFICATION] Compile-fail tests that demonstrate forbidden captures; compile-pass tests for intended usage.

[INVARIANT: INV-0502] Pin Contracts Prevent Moves; Pin Does Not Provide Valid Self-References.
- REJECT IF: self-referential pointers/references are created without a pinned invariant that makes them valid.
- REJECT IF: pin projection is implemented with ad-hoc `unsafe` without a proof of field pinning invariants.
- ENFORCE BY: avoid self-references; prefer indices/offsets into stable storage; use proven pin-projection patterns; keep pinned surface minimal.
[PROVENANCE] std docs: `Pin` contract; Rust Reference: moves and drop semantics.
[VERIFICATION] Miri for unsafe pin projection; tests that move values to confirm pin invariants are enforced.

## References (Normative Anchors)

- Rust Reference: https://doc.rust-lang.org/reference/
- Rust Book (baseline lifetime syntax): https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html
- std `Pin`: https://doc.rust-lang.org/std/pin/struct.Pin.html
- std `PhantomData`: https://doc.rust-lang.org/std/marker/struct.PhantomData.html
- Rustonomicon (unsafe patterns; pin): https://doc.rust-lang.org/nomicon/
