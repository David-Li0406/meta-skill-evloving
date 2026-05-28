# Cairo Numeric Types Reference

> **Reference Implementation**: [Ekubo's i129](https://github.com/EkuboProtocol/starknet-contracts/blob/main/src/types/i129.cairo) - the gold standard for signed integers in Cairo.

## Invariant Enforcement

Ekubo's `i129` implementation demonstrates the gold standard for numeric type invariants in Cairo. The key insight is using a constructor function that enforces invariants, preventing invalid states from ever being created.

From Ekubo's i129:
```cairo
fn i129_new(mag: u128, sign: bool) -> i129 {
    i129 { mag, sign: sign & (mag != 0) }
}
```

### The i256_new Pattern

```cairo
/// Creates an I256 with invariant enforcement.
/// Invariant: When mag is zero, neg must be false (no negative zero).
fn i256_new(mag: U256, neg: bool) -> I256 {
    I256 { mag, neg: neg && !u256_is_zero(mag) }
}
```

This single-line constructor ensures:
- Negative zero is impossible (if mag is zero, neg is always false)
- All code paths that create I256 go through this function
- Invariants are enforced at construction, not checked everywhere

### Normalize Function

For working with potentially invalid external data:

```cairo
fn i256_normalize(value: I256) -> I256 {
    i256_new(value.mag, value.neg)
}
```

## Defensive Normalization in Comparisons

Even with careful construction, `eq`, `cmp`, and `Hash` should defensively normalize to handle edge cases:

```cairo
fn i256_eq(a: I256, b: I256) -> bool {
    // Defensive normalization: treat mag=0 as neg=false
    let a_neg = a.neg && !u256_is_zero(a.mag);
    let b_neg = b.neg && !u256_is_zero(b.mag);
    a_neg == b_neg && u256_eq(a.mag, b.mag)
}

fn i256_cmp(a: I256, b: I256) -> i32 {
    // Defensive normalization
    let a_neg = a.neg && !u256_is_zero(a.mag);
    let b_neg = b.neg && !u256_is_zero(b.mag);

    if a_neg != b_neg {
        if a_neg { return -1_i32; }
        return 1_i32;
    }
    if !a_neg {
        return u256_cmp(a.mag, b.mag);
    }
    0_i32 - u256_cmp(a.mag, b.mag)
}
```

## API Safety: Checked vs Unchecked

### Naming Convention

```cairo
// UNSAFE: No validation, caller must ensure valid input
pub fn from_raw_unchecked(raw: i256) -> SQ128x128 {
    SQ128x128 { raw: i256_normalize(raw) }
}

// SAFE: Returns None for invalid input
pub fn from_raw_checked(raw: i256) -> Option<SQ128x128> {
    let normalized = i256_normalize(raw);
    if normalized.neg {
        if u256_cmp(normalized.mag, U256_MAX_NEG_MAG) > 0_i32 {
            return Option::None;
        }
    } else if u256_cmp(normalized.mag, U256_MAX_POS_MAG) > 0_i32 {
        return Option::None;
    }
    Option::Some(SQ128x128 { raw: normalized })
}
```

### Checked Arithmetic Pattern

Implement checked versions first, panicking versions as wrappers:

```cairo
/// Core implementation returns Option
fn i256_checked_add(a: I256, b: I256) -> Option<I256> {
    if a.neg == b.neg {
        let (sum, overflow) = u256_add(a.mag, b.mag);
        if overflow { return Option::None; }
        // ... range validation
        return Option::Some(i256_new(sum, a.neg));
    }
    // ... handle different signs
}

/// Panicking wrapper
fn i256_add_internal(a: I256, b: I256) -> I256 {
    i256_checked_add(a, b).expect('i256 add overflow')
}
```

## Handling Neg Overflow

The MIN value cannot be negated (would produce a value outside the representable range):

```cairo
pub fn checked_neg(a: SQ128x128) -> Option<SQ128x128> {
    // Negating MIN (-2^127) would produce +2^127 which exceeds MAX
    if a.raw.neg && u256_eq(a.raw.mag, U256_MAX_NEG_MAG) {
        return Option::None;
    }
    Option::Some(SQ128x128 { raw: i256_new(a.raw.mag, !a.raw.neg) })
}

pub impl SQ128x128Neg of Neg<SQ128x128> {
    fn neg(a: SQ128x128) -> SQ128x128 {
        checked_neg(a).expect('neg overflow')
    }
}
```

## Standard Trait Implementations

### PartialEq (Note: Snapshot Parameters)

```cairo
pub impl SQ128x128PartialEq of PartialEq<SQ128x128> {
    fn eq(lhs: @SQ128x128, rhs: @SQ128x128) -> bool {
        i256_eq(*lhs.raw, *rhs.raw)  // Dereference snapshots
    }
}
```

### PartialOrd

```cairo
pub impl SQ128x128PartialOrd of PartialOrd<SQ128x128> {
    fn lt(lhs: SQ128x128, rhs: SQ128x128) -> bool {
        i256_cmp(lhs.raw, rhs.raw) < 0_i32
    }
    fn le(lhs: SQ128x128, rhs: SQ128x128) -> bool {
        i256_cmp(lhs.raw, rhs.raw) <= 0_i32
    }
    fn gt(lhs: SQ128x128, rhs: SQ128x128) -> bool {
        i256_cmp(lhs.raw, rhs.raw) > 0_i32
    }
    fn ge(lhs: SQ128x128, rhs: SQ128x128) -> bool {
        i256_cmp(lhs.raw, rhs.raw) >= 0_i32
    }
}
```

### Arithmetic Operators

```cairo
pub impl SQ128x128Add of Add<SQ128x128> {
    fn add(lhs: SQ128x128, rhs: SQ128x128) -> SQ128x128 {
        add_internal(lhs, rhs)  // Panics on overflow
    }
}

pub impl SQ128x128Sub of Sub<SQ128x128> {
    fn sub(lhs: SQ128x128, rhs: SQ128x128) -> SQ128x128 {
        sub_internal(lhs, rhs)
    }
}

/// Document rounding behavior for Mul
pub impl SQ128x128Mul of Mul<SQ128x128> {
    fn mul(lhs: SQ128x128, rhs: SQ128x128) -> SQ128x128 {
        mul_internal(lhs, rhs, false)  // Uses floor rounding
    }
}
```

### Zero and One Traits

```cairo
pub impl SQ128x128Zero of core::num::traits::Zero<SQ128x128> {
    fn zero() -> SQ128x128 { ZERO }
    fn is_zero(self: @SQ128x128) -> bool { i256_is_zero(*self.raw) }
    fn is_non_zero(self: @SQ128x128) -> bool { !i256_is_zero(*self.raw) }
}

pub impl SQ128x128One of core::num::traits::One<SQ128x128> {
    fn one() -> SQ128x128 { ONE }
    fn is_one(self: @SQ128x128) -> bool { i256_eq(*self.raw, I256_SCALE) }
    fn is_non_one(self: @SQ128x128) -> bool { !i256_eq(*self.raw, I256_SCALE) }
}
```

### Hash (Must Be Consistent with Eq)

```cairo
pub impl SQ128x128Hash<S, +HashStateTrait<S>, +Drop<S>> of Hash<SQ128x128, S> {
    fn update_state(state: S, value: SQ128x128) -> S {
        // Normalize to ensure Hash consistency with Eq
        let normalized = i256_normalize(value.raw);
        let state = state.update(normalized.mag.limb0.into());
        let state = state.update(normalized.mag.limb1.into());
        let state = state.update(normalized.mag.limb2.into());
        let state = state.update(normalized.mag.limb3.into());
        let neg_val: felt252 = if normalized.neg { 1 } else { 0 };
        state.update(neg_val)
    }
}
```

## Limb-Based Wide Arithmetic

### Helper Functions for Limb Access

```cairo
fn u512_get_limb(value: @U512, idx: u32) -> u64 {
    if idx == 0 { *value.limb0 }
    else if idx == 1 { *value.limb1 }
    else if idx == 2 { *value.limb2 }
    else if idx == 3 { *value.limb3 }
    else if idx == 4 { *value.limb4 }
    else if idx == 5 { *value.limb5 }
    else if idx == 6 { *value.limb6 }
    else { *value.limb7 }
}

fn u512_set_limb(ref value: U512, idx: u32, limb: u64) {
    if idx == 0 { value.limb0 = limb; return; }
    if idx == 1 { value.limb1 = limb; return; }
    // ... etc
}
```

### Division by 2^64 (No Shift Operator)

Cairo lacks the `>>` operator. Use division by a constant:

```cairo
const TWO_POW_64: u128 = 0x1_0000_0000_0000_0000_u128;

fn u128_split_to_u64(value: u128) -> (u64, u64) {
    let low: u64 = (value & 0xFFFFFFFFFFFFFFFF_u128).try_into().unwrap();
    let high: u64 = (value / TWO_POW_64).try_into().unwrap();
    (low, high)
}
```

### Loop-Based Carry Propagation

Instead of copy-pasting for each limb:

```cairo
fn u512_add_one_from(mut acc: U512, start: u32) -> U512 {
    let mut carry: u64 = 1;
    let mut i: u32 = start;
    while i < 8 && carry != 0 {
        let limb = u512_get_limb(@acc, i);
        let (new_limb, new_carry) = add_u64_with_carry(limb, 0, carry);
        u512_set_limb(ref acc, i, new_limb);
        carry = new_carry;
        i += 1;
    };
    acc
}
```

## Cairo Quirks to Remember

1. **No `>>` operator**: Use `/ TWO_POW_64` instead of `>> 64`
2. **Array indexing**: Can't index `[T; N]` with runtime index, use `.span().get(i)`
3. **`use` in functions**: Not allowed, move to module level
4. **Unary minus parsing**: Use `0_i32 - value` instead of `-value` in some contexts
5. **Ambiguous unwrap**: Use `OptionTrait::unwrap(x)` when compiler complains
