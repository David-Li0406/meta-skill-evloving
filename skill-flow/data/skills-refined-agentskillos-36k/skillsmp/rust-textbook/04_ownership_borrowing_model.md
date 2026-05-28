# 04 — Ownership and Borrowing (Alias and Resource Protocol)

[INVARIANT: INV-0401] Ownership Determines Destruction Authority.
- REJECT IF: more than one independent code path can free/drop the same resource.
- ENFORCE BY: single-owner types; move-based transfer; RAII guards for scoped ownership.
[PROVENANCE] Rust Reference: destructors (drop scopes); expressions (moves and deinitialization).
[VERIFICATION] Miri for unsafe drop protocols; tests that exercise early-return and panic paths.

[INVARIANT: INV-0402] Move Transfers Ownership and Deinitializes the Source Place.
- REJECT IF: moved-from state is accessed as initialized state.
- ENFORCE BY: treat moved-from places as uninitialized; use `Option<T>`/`MaybeUninit<T>` to model "present/absent."
[PROVENANCE] Rust Reference: expressions (move semantics; deinitialization).

[INVARIANT: INV-0403] Shared vs Mutable Borrow Is an Exclusivity Protocol.
- Shared borrow: mutation through the borrowed place is forbidden unless mediated by `UnsafeCell`.
- Mutable borrow: all access to the borrowed place is forbidden for the borrow lifetime except through the `&mut`.
- REJECT IF: safe code relies on "it seems not to alias" rather than explicit lifetime/borrow structure.
[PROVENANCE] Rust Reference: operator expressions (borrow lifetime and mutable borrow semantics).

[HAZARD: RSK-0401] Interior Mutability as Hidden Global Invariant.
- TRIGGER: `Cell`, `RefCell`, `Mutex`, `RwLock`, `Atomic*`, `UnsafeCell` in public types.
- FAILURE MODE: action-at-a-distance invariants; implicit synchronization protocols; latent deadlocks.
- REJECT IF: interior mutability appears without an explicit protocol (who mutates, when, and under what synchronization).
- ENFORCE BY: narrow mutation surface; document lock/atomic protocol; encapsulate interior mutability behind safe APIs.
[PROVENANCE] std docs: `UnsafeCell` is the foundation of interior mutability; Rust Reference: data race UB.
[VERIFICATION] Loom for custom synchronization; stress tests for lock ordering; Miri for aliasing-unsafe patterns.

[HAZARD: RSK-0402] Stable Reference Into Moving Storage (Use-After-Realloc).
- TRIGGER: returning `&T` into `Vec`/`String` storage while also exposing mutation that can reallocate.
- FAILURE MODE: reference invalidation after reallocation (logic bug in safe code; UB if unsafe code dereferences stale raw pointers).
- REJECT IF: an API returns references that can be invalidated by later safe operations without lifetime coupling that prevents mutation.
- ENFORCE BY: borrow tying lifetimes to `&self`/`&mut self` correctly; use indices/handles; use chunked arenas or slab handles for stable identity.
[PROVENANCE] std docs: `Vec`/`String` reallocation semantics; Rust Reference: aliasing and reference validity requirements.

[CONTRACT: CTR-0401] Public API Borrowing Discipline.
- REJECT IF: public APIs force cloning/allocating to read.
- REJECT IF: public APIs hide allocation or synchronization as a side effect of a getter.
- ENFORCE BY: provide borrowed views (`&[T]`, `&str`, iterators); make allocation explicit in method naming and docs; expose mutation as a narrow, audited surface.
[PROVENANCE] Rust API Guidelines (background); std patterns (`as_slice`, iterators).

[HAZARD: RSK-0403] Borrow Across Suspension (Async Interaction).
- TRIGGER: holding a reference/guard across `.await`.
- FAILURE MODE: invariants remain broken at a yield point; cancellation drops the future mid-protocol.
- REJECT IF: a borrow/guard spans `.await` unless explicitly required and proven cancellation-safe.
- ENFORCE BY: split critical sections; move owned data into the future; use scoped locks that are dropped before `.await`.
[PROVENANCE] Rust Reference: await expressions are suspension points; cancellation is drop of the future.
[VERIFICATION] Async tests with cancellation/timeout; Loom for combined sync+async protocols when modeled.

## References (Normative Anchors)

- Rust Reference: Expressions (moves; places): https://doc.rust-lang.org/reference/expressions.html
- Rust Reference: Operator expressions (borrows): https://doc.rust-lang.org/reference/expressions/operator-expr.html
- Rust Reference: Destructors (drop scopes): https://doc.rust-lang.org/reference/destructors.html
- Rust Reference: Behavior considered undefined (data races; invalid dereference): https://doc.rust-lang.org/reference/behavior-considered-undefined.html
- std `Vec` docs: https://doc.rust-lang.org/std/vec/struct.Vec.html
- std `String` docs: https://doc.rust-lang.org/std/string/struct.String.html
