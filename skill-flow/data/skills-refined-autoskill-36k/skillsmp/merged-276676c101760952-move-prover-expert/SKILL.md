---
name: move-prover-expert
description: Use this skill for formal verification of Move smart contracts using Move Prover, including writing specifications, debugging verification failures, and understanding the Move Specification Language (MSL).
---

# Move Prover Expert

Formal verification for Move smart contracts - mathematically prove your code is correct.

## When to Use

- Writing specifications for Move functions
- Proving correctness properties (invariants, access control)
- Debugging verification failures or timeouts
- Understanding MSL (Move Specification Language)

## Core Constructs

### Preconditions - `requires`

Conditions that must be true BEFORE function runs:

```move
spec withdraw {
    requires exists<Balance>(addr);
    requires global<Balance>(addr).coins >= amount;
}
```

### Postconditions - `ensures`

Conditions that must be true AFTER function runs:

```move
spec transfer {
    ensures global<Balance>(from).coins == old(global<Balance>(from).coins) - amount;
    ensures global<Balance>(to).coins == old(global<Balance>(to).coins) + amount;
}
```

### Abort Conditions - `aborts_if`

When function should abort:

```move
spec withdraw {
    aborts_if !exists<Balance>(addr) with ERROR_NOT_FOUND;
    aborts_if global<Balance>(addr).coins < amount with ERROR_INSUFFICIENT;
}
```

### Modified Resources - `modifies`

Which global resources change:

```move
spec transfer {
    modifies global<Balance>(from);
    modifies global<Balance>(to);
}
```

### The `old()` Operator

Access pre-execution values:

```move
spec increment {
    ensures counter.value == old(counter.value) + 1;
}
```

## Invariants

### Struct Invariants

Properties that always hold for a struct:

```move
struct Balance has key {
    coins: u64,
    locked: u64,
}

spec Balance {
    invariant coins >= locked;
}
```

### Module Invariants

Properties that hold across the module:

```move
spec module {
    invariant [global]
        forall addr: address:
            exists<Balance>(addr) ==> global<Balance>(addr).coins >= 0;
}
```

## Quantifiers

### Universal - `forall`

Property holds for ALL values:

```move
spec transfer {
    ensures forall addr: address where addr != from && addr != to:
        global<Balance>(addr).coins == old(global<Balance>(addr).coins);
}
```

### Existential - `exists`

Property holds for AT LEAST ONE value:

```move
spec module {
    invariant exists addr: address: exists<AdminCap>(addr);
}
```

## Schemas (Reusable Specs)

```move
spec schema BalanceExists {
    addr: address;
    requires exists<Balance>(addr);
}

spec schema SufficientBalance {
    addr: address;
    amount: u64;
    requires global<Balance>(addr).coins >= amount;
}

// Reuse in functions
spec withdraw {
    include BalanceExists;
    include SufficientBalance;
}
```

## Pragmas

```move
spec module {
    pragma verify = true;           // Enable verification
    pragma aborts_if_is_strict;     // Require complete abort specs
    pragma timeout = 120;           // Timeout in seconds
}
```

## Common Patterns

### Access Control

```move
spec admin_only_function {
    requires exists<AdminCap>(signer::address_of(admin));
    aborts_if !exists<AdminCap>(signer::address_of(admin));
}
```

### Overflow Prevention

```move
spec deposit {
    requires global<Balance>(addr).coins + amount <= MAX_U64;
    ensures global<Balance>(addr).coins == old(global<Balance>(addr).coins) + amount;
}
```

## Running the Prover

```bash
# Verify all modules
aptos move prove

# Verify specific module
aptos move prove --filter MyModule

# Verbose output
aptos move prove --verbose
```

## Debugging Failures

### Reading Errors

```
error: post-condition does not hold
```

**Solution:** Add overflow precondition.

### Common Issues

**Missing precondition:**
```move
spec withdraw {
    ensures global<Balance>(addr).coins == old(global<Balance>(addr).coins) - amount;
}
```

**Incomplete abort specs:**
```move
spec transfer {
    aborts_if !exists<Balance>(from);
}
```

## Complete Example

```move
module 0x1::coin {
    struct Coin has key {
        value: u64
    }

    const ERROR_NOT_FOUND: u64 = 1;
    const ERROR_INSUFFICIENT: u64 = 2;

    public fun transfer(from: &signer, to: address, amount: u64) acquires Coin {
        let from_addr = signer::address_of(from);
        assert!(exists<Coin>(from_addr), ERROR_NOT_FOUND);
        assert!(exists<Coin>(to), ERROR_NOT_FOUND);

        let from_coin = borrow_global_mut<Coin>(from_addr);
        assert!(from_coin.value >= amount, ERROR_INSUFFICIENT);
        from_coin.value = from_coin.value - amount;

        let to_coin = borrow_global_mut<Coin>(to);
        to_coin.value = to_coin.value + amount;
    }

    spec transfer {
        let from_addr = signer::address_of(from);
        requires exists<Coin>(from_addr);
        requires exists<Coin>(to);
        requires global<Coin>(from_addr).value >= amount;

        aborts_if !exists<Coin>(from_addr) with ERROR_NOT_FOUND;
        aborts_if !exists<Coin>(to) with ERROR_NOT_FOUND;
        aborts_if global<Coin>(from_addr).value < amount with ERROR_INSUFFICIENT;

        ensures global<Coin>(from_addr).value == old(global<Coin>(from_addr).value) - amount;
        ensures global<Coin>(to).value == old(global<Coin>(to).value) + amount;

        modifies global<Coin>(from_addr);
        modifies global<Coin>(to);
    }
}
```

## Specification Checklist

For critical functions, verify:

- [ ] **Preconditions** - What must be true before?
- [ ] **Postconditions** - What must be true after?
- [ ] **Abort conditions** - When should it fail?
- [ ] **Modified resources** - What state changes?
- [ ] **Invariants** - What always holds?
- [ ] **Conservation** - Are resources conserved?
- [ ] **Access control** - Is authorization correct?
- [ ] **Overflow** - Are bounds checked?

## Resources

- **Aptos Move Prover Docs:** https://aptos.dev/move/prover/
- **Move Specification Language:** https://github.com/move-language/move/blob/main/language/move-prover/doc/user/spec-lang.md