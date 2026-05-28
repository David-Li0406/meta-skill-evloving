---
name: aptos-object-model
description: Use this skill when you need expertise on the Aptos Object Model for building composable and transferable on-chain assets.
---

# Skill body

## Triggers

- object model, objectcore, Object<T>
- constructorref, extendref, deleteref, transferref
- named object, generated object
- object ownership, composable object
- soul-bound, nesting

## Core Concepts

The Object Model enables:
- **Transferable resources** - Objects can move between accounts.
- **Composability** - Objects can own other objects.
- **Lifecycle management** - Create, extend, delete via refs.
- **Ownership separation** - Owner address != object address.

## ObjectCore

Every object has an `ObjectCore`:

```move
struct ObjectCore has key {
    owner: address,
    allow_ungated_transfer: bool,
}
```

## Object<T> Wrapper

```move
struct Object<phantom T> has copy, drop, store {
    inner: address  // Pointer to object
}
```

## Object Creation

### Named Objects (Deterministic)

```move
let constructor_ref = object::create_named_object(creator, b"SEED");
// Address = hash(creator_address, seed)
```

### Generated Objects (Random)

```move
let constructor_ref = object::create_object(creator);
// Non-deterministic address
```

### Sticky Objects (Cannot Delete)

```move
let constructor_ref = object::create_sticky_object(creator);
```

## References (Capabilities)

### ConstructorRef - Master Key (Creation Only)

```move
let constructor_ref = object::create_object(creator);

// Generate all other refs during creation
let extend_ref = object::generate_extend_ref(&constructor_ref);
let transfer_ref = object::generate_transfer_ref(&constructor_ref);
let delete_ref = object::generate_delete_ref(&constructor_ref);
let object_signer = object::generate_signer(&constructor_ref);

// Store refs at object address
move_to(&object_signer, Refs { extend_ref, transfer_ref, delete_ref });
```

### ExtendRef - Access Later

```move
// Get signer after creation
let object_signer = object::generate_signer_for_extending(&refs.extend_ref);
```

### TransferRef - Control Transfers

```move
// Disable transfers (soul-bound)
object::disable_transfers(&refs.transfer_ref);
```