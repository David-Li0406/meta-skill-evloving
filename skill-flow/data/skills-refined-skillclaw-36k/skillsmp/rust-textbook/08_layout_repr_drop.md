# 08 — Layout, `repr`, Attributes, Drop (Representation Invariants)

[CONTRACT: CTR-0801] Layout Is Not a Property of `repr(Rust)`.
- REJECT IF: any code depends on field order, padding, niche layout, or enum discriminant placement under `repr(Rust)`.
- ENFORCE BY: `repr(C)` for FFI; `repr(transparent)` for wrapper layout promises; explicit serialization formats that do not depend on Rust layout.
[PROVENANCE] Rust Reference: type layout is largely unspecified unless constrained by `repr`.

[INVARIANT: INV-0801] Alignment and Layout Are Preconditions for Typed Access.
- REJECT IF: typed loads/stores can occur at misaligned addresses.
- REJECT IF: a reference is created to a packed/unaligned field.
- ENFORCE BY: raw borrows for packed fields; `read_unaligned`/`write_unaligned`; allocate with correct `Layout`.
[PROVENANCE] Rust Reference: Behavior considered undefined (misaligned pointer dereference); Expressions (raw borrows motivation).
[VERIFICATION] Miri (alignment + invalid reference checks).

[INVARIANT: INV-0802] Primitive Validity (Bit-Pattern Requirements).
- REJECT IF: unsafe code can produce an invalid primitive value (including via `transmute`, `mem::zeroed`, union reads, or byte reinterprets).
[PROVENANCE] Rust Reference: Behavior considered undefined (invalid values).

```text
Type; Valid values; Invalid values; Notes
uN/iN/usize/isize; all bit patterns; none; validity != arithmetic overflow behavior
f32/f64; all bit patterns; none; NaN payloads are valid values
bool; 0x00 or 0x01; 0x02..0xFF; invalid bool is UB to observe as bool
char; 0x0000..0xD7FF and 0xE000..0x10FFFF; 0xD800..0xDFFF and >0x10FFFF; Unicode scalar value
&T; non-null, aligned, dereferenceable, points to valid T for lifetime; null/misaligned/dangling/invalid T; reference validity is strict
&mut T; &T validity plus exclusivity for lifetime; any aliasing that violates exclusivity; mutation through shared refs requires UnsafeCell
*const/*mut T; any bit pattern; none; dereferenceability requires provenance+alignment+validity (INV-0003/0006)
fn(...) -> R; non-null code pointer; null/invalid address; Option uses niche to represent null
NonZero*; any non-zero; zero; used for niche optimization in Option
```

[HAZARD: RSK-0801] `repr(packed)` Field References Are UB.
- TRIGGER: `#[repr(packed)]` structs; taking `&packed.field` or `&mut packed.field`.
- FAILURE MODE: creating an unaligned reference; immediate UB on dereference.
- REJECT IF: code creates references to packed fields.
- ENFORCE BY: raw borrows + `read_unaligned`/`write_unaligned` or copy bytes out first.
[PROVENANCE] Rust Reference: expressions (raw borrows exist to avoid invalid references).
[VERIFICATION] Miri.

[CONTRACT: CTR-0802] `repr` Selection Matrix (FFI and Wrapper Discipline).

```text
repr; Guarantees; Primary hazards; Reject condition
repr(Rust); none stable; layout drift; reliance on field order/padding/niches
repr(C); C-like field order/alignment; still not a stable wire format; using for persistence/serialization
repr(transparent); single-field layout promise; only for one non-zero-sized field (plus ZSTs); multiple fields or relying on padding
repr(packed); removes alignment padding; invalid references; any reference to packed fields
repr(align(N)); increases alignment; may change size and ABI; FFI without matching C alignment
```

[HAZARD: RSK-0802] Unsafe Attributes Change ABI/Linking/Codegen.
- TRIGGER: `no_mangle`, `export_name`, `link_section`, `naked`, `target_feature`, `repr(packed)`, and other unsafe-to-apply attributes.
- FAILURE MODE: UB via ABI mismatch; linker-level symbol collision; platform-specific breakage.
- REJECT IF: unsafe attributes are applied without an explicit boundary contract and tests on at least one target that exercises the attribute.
[PROVENANCE] Rust Reference: attributes (unsafe attributes; active attributes); functions (ABI).
[VERIFICATION] Targeted integration tests; compile/link tests per target.

[INVARIANT: INV-0803] Drop Order Is Observable Behavior.
- REJECT IF: a change modifies drop order (via declaration order, block structure, or expression shape) without a compatibility decision.
- ENFORCE BY: scope resources explicitly; add tests when drop timing is part of the contract.
[PROVENANCE] Rust Reference: destructors (drop scopes; reverse declaration/creation order).

[INVARIANT: INV-0804] Partial Initialization Must Not Drop Uninitialized State.
- REJECT IF: manual initialization can drop uninitialized fields or skip drops for initialized fields.
- ENFORCE BY: field-by-field init with `MaybeUninit`; guard drops during partial init.
[PROVENANCE] Rust Reference: destructors (partial initialization drop behavior).
[VERIFICATION] Miri; tests that exercise early-return and panic during initialization.

## References (Normative Anchors)

- Rust Reference: Attributes: https://doc.rust-lang.org/reference/attributes.html
- Rust Reference: Destructors: https://doc.rust-lang.org/reference/destructors.html
- Rust Reference: Behavior considered undefined: https://doc.rust-lang.org/reference/behavior-considered-undefined.html
- Rust Reference: Operator expressions (raw borrows): https://doc.rust-lang.org/reference/expressions/operator-expr.html
- std pointer docs: https://doc.rust-lang.org/std/primitive.pointer.html
