---
name: aptos-move-language
description: Use this skill when you need deep expertise in the Move programming language for the Aptos blockchain, covering its core concepts and advanced features.
---

# Move Language Expert

Deep expertise on the Move programming language for Aptos blockchain.

## Triggers

- move language, abilities, generics
- phantom type, borrow_global
- signer, friend, inline
- copy, drop, store, key
- move_to, move_from, acquires

## Abilities

The four abilities control what can be done with types:

| Ability | Meaning | Use Case |
|---------|---------|----------|
| `copy` | Can be copied | Primitives, configs |
| `drop` | Can be discarded | Temporary data |
| `store` | Can be stored in structs | Most data types |
| `key` | Can be top-level resource | Account resources |

```move
struct Resource has key, store { value: u64 }
struct Point has copy, drop, store { x: u64, y: u64 }
struct Capability {}  // No abilities - hot potato
```

### Critical Rules

1. Fields must have compatible abilities.
2. Structs without `drop` must be explicitly handled.
3. `copy` requires all fields to have `copy`.

## Generics

```move
struct Box<T: store> has store {
    value: T
}

public fun create<T: store>(value: T): Box<T> {
    Box { value }
}
```

### Phantom Types (Zero-Cost Type Safety)

```move
struct Coin<phantom CoinType> has store {
    value: u64  // CoinType doesn't appear here
}

struct BTC {}
struct ETH {}

// Coin<BTC> != Coin<ETH> at compile time
```

## References

```move
// Immutable reference
fun read(x: &u64): u64 { *x }

// Mutable reference
fun increment(x: &mut u64) { *x = *x + 1; }
```

### Reference Rules

- Can't have mutable + immutable refs simultaneously.
- Only one mutable reference at a time.
- References can't outlive values.

## Global Storage

```move
// Store resource
move_to(account, MyResource { value: 0 });

// Remove resource
let resource = move_from<MyResource>(addr);

// Immutable borrow
let r = borrow_global<MyResource>(addr);

// Mutable borrow
let r = borrow_global_mut<MyResource>(addr);

// Check existence
exists<MyResource>(addr);
```

### The `acquires` Annotation

```move
public fun get_value(addr: address): u64 acquires MyResource {
    borrow_global<MyResource>(addr).value
}
```