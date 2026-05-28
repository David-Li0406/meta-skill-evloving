---
name: cairo-numeric-types
description: Guide implementing custom numeric types in Cairo with invariant enforcement, overflow safety, and standard trait implementations; use when implementing fixed-point, signed integers, or other numeric primitives.
---

# Cairo Numeric Types

## Overview
Guide implementing production-quality custom numeric types (fixed-point, big integers, signed integers) in Cairo following Ekubo-style patterns.

## Quick Use
- Read `references/numeric-types.md` before answering.
- Study Ekubo's i129 - the gold standard for signed integers in Cairo.
- Use constructor functions to enforce invariants (e.g., no negative zero).
- Provide both checked (returns Option) and unchecked (panics) API variants.
- Implement standard traits: PartialEq, PartialOrd, Add, Sub, Mul, Neg, Zero, One.

## Response Checklist

### Invariant Enforcement
- Use a private constructor function that enforces invariants (Ekubo i129 pattern).
- Example: `fn i256_new(mag: U256, neg: bool) -> I256 { I256 { mag, neg: neg && !u256_is_zero(mag) } }`
- Never allow invalid states like negative zero.

### Defensive Normalization
- In `eq`, `cmp`, and `Hash`, normalize inputs defensively to handle potentially invalid states.
- Example: `let a_neg = a.neg && !u256_is_zero(a.mag);` before comparing.

### API Safety
- Name unsafe functions explicitly: `from_raw_unchecked`, not just `from_raw`.
- Provide `from_raw_checked` returning `Option<T>` for untrusted input.
- Document safety requirements with `/// # Safety` sections.

### Checked vs Panicking Arithmetic
- Implement checked versions first (return `Option<T>`).
- Panicking versions should be thin wrappers: `checked_op(...).expect('error msg')`.
- Handle edge cases: `Neg` on MIN value overflows (returns None in checked).

### Standard Trait Implementations
- `PartialEq`: Takes `@Self` (snapshot) parameters, dereference with `*`.
- `PartialOrd`: Implement `lt`, `le`, `gt`, `ge` for full ordering.
- `Add`, `Sub`, `Mul`: Return owned values, panic on overflow.
- `Neg`: Must handle MIN value overflow.
- `Zero`, `One`, `Default`: Return constant values.
- `Into<SourceType>`: For converting from smaller types.
- `Hash`: Must be consistent with `Eq` (normalize before hashing).
- Use `#[derive(Copy, Drop, Serde, Debug)]` for automatic implementations.

### Limb-Based Arithmetic
- Prefer 64-bit limbs for Cairo (U256 = 4 x u64, U512 = 8 x u64).
- Use helper functions for limb access instead of copy-paste branches.
- For division by 2^64, use `value / TWO_POW_64` (Cairo lacks `>>` operator).
- Loop-based operations reduce code size vs unrolled branches.

### Code Organization
- Keep checked arithmetic as the core implementation.
- Panicking wrappers call checked versions with `.expect()`.
- Group related operations: constructors, arithmetic, traits, tests.

## Cairo-Specific Quirks
- No `>>` bit shift operator - use division by power-of-2 constant.
- Can't index fixed-size arrays with runtime index - use `.span()`.
- `use` statements cannot appear inside functions.
- Unary negation parsing issues - use `0_i32 - value` instead of `-value` in some contexts.
- Ambiguous `unwrap` - use `OptionTrait::unwrap(result)` to disambiguate.

## Example Requests
- "How do I implement a signed integer type in Cairo?"
- "How do I enforce invariants like no negative zero?"
- "How do I implement operator overloading for my numeric type?"
- "How do I handle overflow in custom arithmetic?"

## Reference Implementations
- [Ekubo i129](https://github.com/EkuboProtocol/starknet-contracts/blob/main/src/types/i129.cairo) - Production signed integer (the gold standard)

## Cairo by Example
- [Operator Overloading](https://cairo-by-example.xyz/trait/ops)
- [Traits](https://cairo-by-example.xyz/trait)
- [Derive](https://cairo-by-example.xyz/trait/derive)
