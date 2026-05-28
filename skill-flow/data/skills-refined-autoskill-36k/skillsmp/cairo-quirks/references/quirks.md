# Cairo Quirks Reference

## Operator Limitations

### No Bit Shift Operators

Cairo does not have `>>` or `<<` operators. Use division/multiplication by powers of 2:

```cairo
// WRONG - won't compile
let high = value >> 64;

// CORRECT - use division
const TWO_POW_64: u128 = 0x1_0000_0000_0000_0000_u128;
let high = value / TWO_POW_64;

// For left shift, use multiplication
let shifted = value * TWO_POW_64;
```

### Unary Negation Parsing Issues

In some contexts, unary minus doesn't parse correctly:

```cairo
// WRONG - may not parse correctly
return -u256_cmp(a.mag, b.mag);

// CORRECT - use subtraction from zero
return 0_i32 - u256_cmp(a.mag, b.mag);
```

This is especially common in return statements and when the negation would be at the start of an expression.

## Array and Collection Quirks

### No Runtime Array Indexing

Fixed-size arrays `[T; N]` cannot be indexed with a runtime variable:

```cairo
// WRONG - won't compile
let arr: [u64; 4] = [1, 2, 3, 4];
let idx: u32 = 2;
let val = arr[idx];  // Error!

// CORRECT - convert to Span first
let val = arr.span().get(idx);  // Returns Option<@T>
// or
let val = *arr.span().at(idx);  // Returns T, panics if out of bounds
```

### Span for Iteration

```cairo
// Convert fixed array to span for iteration
let values: [SQ128x128; 5] = [MIN, NEG_ONE, ZERO, ONE, MAX];
let mut i: u32 = 0;
while i < 5 {
    let val = *values.span().at(i);
    // use val...
    i += 1;
};
```

## Scope and Declaration Issues

### No `use` Inside Functions

Import statements must be at the module level:

```cairo
// WRONG - won't compile
fn my_function() {
    use core::num::traits::Zero;  // Error!
    // ...
}

// CORRECT - import at module level
use core::num::traits::Zero;

fn my_function() {
    // now Zero is available
}
```

### Reserved Keywords

`type` is reserved even in lowercase:

```cairo
// WRONG
let type = "foo";  // Error!

// CORRECT
let kind = "foo";
let ty = "foo";
```

## Trait and Method Issues

### Ambiguous `unwrap`

When both `Option` and `Result` are in scope, `unwrap` can be ambiguous:

```cairo
// WRONG - may be ambiguous
let val = result.unwrap();

// CORRECT - specify the trait explicitly
let val = OptionTrait::unwrap(result);
// or
let val = ResultTrait::unwrap(result);
```

### PartialEq Takes Snapshot Parameters

Cairo's `PartialEq` trait uses snapshots, not owned values:

```cairo
// WRONG
impl MyTypePartialEq of PartialEq<MyType> {
    fn eq(lhs: MyType, rhs: MyType) -> bool {  // Error!
        // ...
    }
}

// CORRECT - use snapshots (@) and dereference (*)
impl MyTypePartialEq of PartialEq<MyType> {
    fn eq(lhs: @MyType, rhs: @MyType) -> bool {
        *lhs.field == *rhs.field  // Dereference with *
    }
}
```

### Trait Methods Need Import

To call a trait method, the trait must be in scope:

```cairo
// WRONG - Zero trait not in scope
fn test() {
    let x = SQ128x128::zero();  // Error: method not found
}

// CORRECT - import the trait
use core::num::traits::Zero;

fn test() {
    let x = SQ128x128::zero();  // Works now
}
```

## Numeric Type Quirks

### No Implicit Conversions

All type conversions must be explicit:

```cairo
// WRONG
let a: u64 = 5;
let b: u128 = a;  // Error!

// CORRECT
let a: u64 = 5;
let b: u128 = a.into();  // Infallible conversion

// For potentially failing conversions
let c: u128 = 1000;
let d: u64 = c.try_into().unwrap();  // May panic
```

### Comparison Functions Return i32

For ordering comparisons, return `i32` (-1, 0, 1) not bool:

```cairo
fn u256_cmp(a: U256, b: U256) -> i32 {
    if a.limb3 < b.limb3 { return -1_i32; }
    if a.limb3 > b.limb3 { return 1_i32; }
    // ... continue for other limbs
    0_i32
}

// Usage
let result = u256_cmp(a, b);
if result < 0_i32 { /* a < b */ }
if result == 0_i32 { /* a == b */ }
if result > 0_i32 { /* a > b */ }
```

### Integer Literal Suffixes

Always use explicit suffixes to avoid ambiguity:

```cairo
let a = 5_u64;      // u64
let b = -3_i32;     // i32
let c = 0_u128;     // u128
let d = 1_felt252;  // felt252
```

## Testing Quirks

### Assert Messages Must Be String Literals

```cairo
// WRONG - variable message
let msg = "test failed";
assert!(condition, msg);  // Error!

// CORRECT - literal message
assert!(condition, "test failed");

// Also correct - format with values
assert!(x == y, "Expected {} but got {}", expected, actual);
```

### Tests Need Attributes

```cairo
#[test]
fn test_addition() {
    // test code
}

#[test]
#[should_panic(expected: "overflow")]
fn test_overflow_panics() {
    // code that should panic
}

#[test]
#[available_gas(1000000)]  // Required for loops/recursion
fn test_with_loop() {
    let mut i = 0;
    while i < 100 {
        i += 1;
    };
}

#[test]
#[ignore]  // Skip by default, run with --include-ignored
fn slow_test() {
    // expensive test
}
```

## Struct and Type Issues

### Derive Macros

Common derives for data types:

```cairo
#[derive(Copy, Drop, Serde, Debug)]
pub struct MyType {
    pub field: u64,
}
```

- `Copy`: Type can be copied (required for most numeric types)
- `Drop`: Type can be dropped (most types need this)
- `Serde`: Serialization/deserialization
- `Debug`: Debug formatting

### Public Fields and Functions

```cairo
// Public struct with public fields
pub struct MyType {
    pub raw: i256,  // Public field
}

// Public function
pub fn my_function() -> u64 {
    // ...
}
```

## Memory and Ownership

### Snapshots vs References

Cairo uses snapshots (`@T`) for immutable borrows:

```cairo
fn read_value(value: @MyType) -> u64 {
    *value.field  // Dereference with *
}

// For mutable access, use ref
fn modify_value(ref value: MyType) {
    value.field = 42;
}
```

### No Mutable Closures

Cairo closures are more limited than Rust:

```cairo
// Closures can capture, but mutation is limited
let x = 5;
let f = || x + 1;  // Captures x by value

// For mutation, use explicit loops/recursion instead
```
