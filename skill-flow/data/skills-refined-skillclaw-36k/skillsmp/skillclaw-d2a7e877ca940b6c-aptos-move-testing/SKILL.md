---
name: aptos-move-testing
description: Use this skill when you need to test Move smart contracts on the Aptos blockchain, including unit tests, integration tests, formal verification, and debugging strategies.
---

# Skill body

## Triggers

- move test, unit test, integration test
- move prover, formal verification
- debug, coverage, assert, expect
- test failure, debugging

## Test Attributes

```move
#[test]
fun test_basic() { }

#[test(account = @0x1)]
fun test_with_signer(account: &signer) { }

#[test(alice = @0x123, bob = @0x456)]
fun test_multi_signer(alice: &signer, bob: &signer) { }

#[test]
#[expected_failure(abort_code = ERROR_CODE)]
fun test_should_fail() { }

#[test_only]
fun helper_function() { }
```

## Basic Testing Pattern

```move
#[test(account = @0x123)]
fun test_resource_creation(account: &signer) {
    let addr = signer::address_of(account);
    
    // Create resource
    create_resource(account);
    
    // Verify exists
    assert!(exists<MyResource>(addr), 0);
    
    // Verify state
    let resource = borrow_global<MyResource>(addr);
    assert!(resource.value == expected, 1);
}
```

## Test Commands

```bash
# Run all tests
aptos move test

# Run specific test
aptos move test --filter test_name

# With coverage
aptos move test --coverage

# With gas profiling
aptos move test --gas

# Verbose
aptos move test --verbose
```

## Multi-Signer Testing

```move
#[test(alice = @0x123, bob = @0x456)]
fun test_transfer(alice: &signer, bob: &signer) {
    let alice_addr = signer::address_of(alice);
    let bob_addr = signer::address_of(bob);
    
    initialize(alice);
    initialize(bob);
    
    transfer(alice, bob_addr, 100);
    
    assert!(get_balance(alice_addr) == 900, 0);
    assert!(get_balance(bob_addr) == 100, 1);
}
```

## Error Testing

```move
#[test]
#[expected_failure(abort_code = ERROR_INSUFFICIENT_BALANCE)]
fun test_insufficient_balance() {
    transfer(from, to, amount_too_large);
}

#[test]
#[expected_failure]  // Any failure
fun test_any_failure() {
    assert!(false, 0);
}
```

## Test-Only Helpers

```move
#[test_only]
module test_helpers {
    public fun setup_account(account: &signer): address {
        let addr = signer::address_of(account);
        // Setup logic
        addr
    }
}
```