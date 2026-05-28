---
name: aptos-framework
description: Use this skill when you need expertise in the Aptos Framework (0x1 standard library) for developing and managing core modules like accounts, coins, and events.
---

# Skill body

## Overview

Expert on the Aptos Framework (0x1 address) - the standard library of core modules essential for all Aptos development.

## Triggers

- aptos framework, 0x1::, aptos_framework::
- account module, table, smart_table
- event, timestamp, randomness
- aggregator, resource account

## Framework Architecture

### Core Modules (0x1::)

```
aptos_framework/
├── account.move           - Account management
├── coin.move              - Fungible token standard (v1)
├── fungible_asset.move    - Fungible asset standard (v2)
├── object.move            - Object model primitives
├── timestamp.move         - Block timestamp access
├── table.move             - Key-value storage
├── smart_table.move       - Auto-split table
├── event.move             - Event emission
├── randomness.move        - Secure randomness (VRF)
├── aggregator_v2.move     - Parallel execution
├── resource_account.move  - Deterministic deployment
```

### Standard Library (std::)

```
move-stdlib/
├── vector.move      - Dynamic arrays
├── option.move      - Optional values
├── string.move      - UTF8 strings
├── signer.move      - Signer operations
├── error.move       - Error codes
```

## Key Modules

### account.move

```move
use aptos_framework::account;

// Create account
account::create_account(new_address);

// Get sequence number
account::get_sequence_number(addr);

// Check existence
account::exists_at(addr);

// SignerCapability pattern
let (resource_signer, signer_cap) = account::create_resource_account(deployer, b"SEED");
```

### table.move / smart_table.move

```move
use aptos_framework::table::{Self, Table};

struct Registry has key {
    data: Table<address, UserData>
}

table::add(&mut t, key, value);
table::borrow(&t, key);
table::borrow_mut(&mut t, key);
table::remove(&mut t, key);
table::contains(&t, key);
```

### event.move (V2 - Recommended)

```move
#[event]
struct TransferEvent has drop, store {
    from: address,
    to: address,
    amount: u64,
}

event::emit(TransferEvent { from, to, amount });
```

### timestamp.move

```move
use aptos_framework::timestamp;

timestamp::now_seconds();
timestamp::now_millis();
```