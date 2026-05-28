# 03 — Core Language Semantics (Places, Values, Moves, Drops, Patterns)

[CONTRACT: CTR-0301] Place Model (Operational Definition).
- Place = `(addr, metadata, provenance)`.
- `addr`: integer address usable for non-dereferenceable comparisons/logging only.
- `metadata`: slice length, `dyn` vtable, or `()` for sized types.
- `provenance`: allocation identity required for dereferenceability (see `INV-0006`).
[PROVENANCE] Rust Reference: expressions (place and value expressions); std pointer docs (provenance APIs).

[INVARIANT: INV-0301] Move Semantics Are Deinitialization.
- REJECT IF: a moved-from place is treated as initialized.
- REJECT IF: "move" is modeled as a bitwise copy in safety reasoning.
- ENFORCE BY: model move as "source place becomes uninitialized"; use `MaybeUninit<T>` for manual init protocols.
[PROVENANCE] Rust Reference: expressions (move semantics; deinitialization).
[VERIFICATION] Miri for unsafe move/drop protocols; tests for partial-move paths.

[HAZARD: RSK-0301] Semicolon Changes Drop Scopes.
- TRIGGER: refactors that add/remove/move `;`, change block tails, or inline `let` bindings.
- FAILURE MODE: destructor timing changes; guard lifetimes change; temporary drop scope changes.
- REJECT IF: observable drop timing can change without a regression test.
[PROVENANCE] Rust Reference: destructors (drop scopes); expressions (temporaries).
[VERIFICATION] Regression tests that assert ordering when externally observable; Miri for unsafe drop interactions.

[HAZARD: RSK-0302] Temporary Lifetime Truncation at Statement Boundaries.
- TRIGGER: borrowing a value expression (`&foo()`, `&iter().next().unwrap()`), taking references to temporaries, chaining method calls that produce temporaries.
- FAILURE MODE: borrow does not outlive the statement; refactor flips borrow-check outcome or behavior.
- REJECT IF: a borrow is intended to outlive a statement but is formed from a temporary.
- ENFORCE BY: bind temporaries to named locals; split expressions at lifetime boundaries.
[PROVENANCE] Rust Reference: expressions (temporaries; borrow operators).

[HAZARD: RSK-0303] Macro-Dependent Temporary Lifetime Extension.
- TRIGGER: reliance on "super macro" temporary lifetime extension (notably `format_args!` internals).
- FAILURE MODE: compiler-version-dependent lifetime behavior; refactor-induced breakage.
- REJECT IF: correctness depends on temporary lifetime extension unless defended by a regression test and isolated from public API contracts.
[PROVENANCE] Rust Reference: expressions (super macro notes and unspecified internal temporary behavior).
[VERIFICATION] Compile and test across MSRV and current stable; add targeted regression test.

[CONTRACT: CTR-0302] Pattern Binding Mode Is Semantics.
- REJECT IF: pattern changes (including adding/removing `ref`/`ref mut`) are treated as "style-only."
- ENFORCE BY: document whether bindings move or borrow; prefer explicit bindings when changes affect ownership.
[PROVENANCE] Rust Reference: patterns (binding modes; refutability; identifier precedence).

[HAZARD: RSK-0304] Accidental Moves and Partial Moves From Patterns.
- TRIGGER: destructuring patterns over non-`Copy` types; pattern changes on `Drop` types; `let` bindings that destructure.
- FAILURE MODE: moved-out fields make the parent unusable; partial-move restrictions for `Drop` types.
- REJECT IF: a pattern introduces a move where a borrow is intended.
- ENFORCE BY: use `ref` bindings or destructure through references; avoid partial moves of `Drop` types.
[PROVENANCE] Rust Reference: expressions (movable places; move restrictions); patterns (binding modes).

[INVARIANT: INV-0302] Reference Creation Requires Validity (No "Convenience References" in Unsafe).
- REJECT IF: `&T`/`&mut T` is created from a place that may be unaligned, uninitialized, or aliasing-unsafe.
- ENFORCE BY: use raw borrows (`&raw const`, `&raw mut`) + explicit `read`/`write` (or unaligned variants) until reference validity holds.
[PROVENANCE] Rust Reference: expressions (raw borrows motivation; borrow operators); Behavior considered undefined (invalid reference dereference).
[VERIFICATION] Miri (invalid reference and provenance checks).

## Matrix: Expression Kind vs Place/Value Risk

```text
Expression kind; Typical role; Hazard
Local/field place; Place; move/deinit rules (INV-0301), drop order (RSK-0301)
Deref/index place; Place; alignment/validity/provenance (INV-0003/0004/0006)
Function/method call; Value; temporary lifetime truncation (RSK-0302)
Macro expansion; Any; hidden drops/borrows/unsafe (RSK-0101/0103)
```

## References (Normative Anchors)

- Rust Reference: Expressions: https://doc.rust-lang.org/reference/expressions.html
- Rust Reference: Operator expressions (borrow operators; raw borrows): https://doc.rust-lang.org/reference/expressions/operator-expr.html
- Rust Reference: Patterns: https://doc.rust-lang.org/reference/patterns.html
- Rust Reference: Destructors: https://doc.rust-lang.org/reference/destructors.html
- std pointer docs: https://doc.rust-lang.org/std/primitive.pointer.html
