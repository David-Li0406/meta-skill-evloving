---
name: aptos-token-standards
description: Use this skill when you need expertise on Aptos token standards, including fungible and non-fungible tokens, their frameworks, and operations.
---

# Aptos Token Standards Expert

Expert on Aptos token standards for fungible tokens (Coin framework, Fungible Asset) and non-fungible tokens (Digital Asset standard, Token V1/V2).

## Triggers

- token, nft, fungible asset
- coin, digital asset, collection
- mint, burn, metadata, royalty
- Token V1, Token V2

## Token Frameworks Overview

| Framework | Type | Status | Use For |
|-----------|------|--------|---------|
| Coin (0x1::coin) | Fungible | Current | Simple tokens, APT |
| Fungible Asset | Fungible | Current | Advanced features |
| Token V1 (0x3) | NFT | Deprecated | Legacy only |
| Digital Asset (0x4) | NFT | Current | All new NFTs |

## Coin Framework

### Create Coin

```move
module my_addr::my_coin {
    use aptos_framework::coin;
    
    struct MyCoin {}
    
    struct Caps has key {
        mint_cap: coin::MintCapability<MyCoin>,
        burn_cap: coin::BurnCapability<MyCoin>,
    }
    
    fun init_module(sender: &signer) {
        let (burn_cap, freeze_cap, mint_cap) = coin::initialize<MyCoin>(
            sender,
            string::utf8(b"My Coin"),
            string::utf8(b"MYC"),
            8,    // decimals
            true, // monitor_supply
        );
        move_to(sender, Caps { mint_cap, burn_cap });
    }
}
```

### Coin Operations

```move
// Mint
let coins = coin::mint(amount, &caps.mint_cap);
coin::deposit(recipient, coins);

// Burn
let coins = coin::withdraw<MyCoin>(account, amount);
coin::burn(coins, &caps.burn_cap);

// Transfer
coin::transfer<MyCoin>(from, to, amount);

// Balance
coin::balance<MyCoin>(account);

// Register to receive
coin::register<MyCoin>(account);
```

## Fungible Asset Framework

### Create Fungible Asset

```move
use aptos_framework::fungible_asset::{Self, MintRef, BurnRef, TransferRef};
use aptos_framework::primary_fungible_store;

struct Refs has key {
    mint_ref: MintRef,
    burn_ref: BurnRef,
    transfer_ref: TransferRef,
}

fun init_module(admin: &signer) {
    let constructor_ref = &object::create_named_object(admin, b"MY_FA");
    
    primary_fungible_store::create_primary_store_enabled_fungible_asset(
        constructor_ref,
        option::none(),  // max_supply
        string::utf8(b"My FA"),
        8, // decimals
    );
}
```