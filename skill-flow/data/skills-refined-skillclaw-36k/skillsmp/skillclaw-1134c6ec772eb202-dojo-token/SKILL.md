---
name: dojo-token
description: Use this skill when implementing ERC20 and ERC721 token standards in your Dojo game using the Origami library for fungible tokens, NFTs, or token-based game mechanics.
---

# Dojo Token Standards

Implement ERC20 fungible tokens and ERC721 NFTs in your Dojo game using the Origami library.

## When to Use This Skill

- "Implement ERC20 token for game currency"
- "Create NFT items with ERC721"
- "Add token standard to my game"
- "Use Origami for tokens"

## What This Skill Does

Implements token standards:
- ERC20 fungible tokens (currency, resources)
- ERC721 non-fungible tokens (items, characters)
- Token minting and burning
- Transfer mechanics
- Balance tracking
- Integration with Origami library

## Quick Start

**ERC20 (fungible):**
```plaintext
"Implement ERC20 token for gold currency"
```

**ERC721 (NFT):**
```plaintext
"Create ERC721 for equipment items"
```

**With Origami:**
```plaintext
"Use Origami library to add token support"
```

## Token Standards

### ERC20 - Fungible Tokens

For interchangeable assets:
- Game currency (gold, gems)
- Resources (wood, stone)
- Experience points

**Properties:**
- Divisible (can have fractions)
- Interchangeable (any token = any other)
- Track balances per account

### ERC721 - Non-Fungible Tokens

For unique assets:
- Character NFTs
- Equipment/items
- Land plots
- Achievements

**Properties:**
- Unique (each has token ID)
- Indivisible (whole units only)
- Individual ownership tracking

## Using Origami Library

### Installation

Add to `Scarb.toml`:
```toml
[dependencies]
origami_token = { git = "https://github.com/dojoengine/origami", tag = "v1.0.0" }
```

### Origami Components

Origami provides reusable token components:
- `Balance` - Token balances
- `ERC20Allowance` - Spending approvals
- `ERC20Metadata` - Token info
- `ERC721Owner` - NFT ownership
- `ERC721TokenApproval` - NFT approvals

## ERC20 Implementation

### Basic ERC20 Model

```cairo
use origami_token::components::token::erc20::erc20_balance::{
    ERC20Balance, ERC20BalanceTrait
};

#[derive(Copy, Drop, Serde)]
#[dojo::model]
pub struct Gold {
    #[key]
    pub player: ContractAddress,
    pub amount: u256,
}
```

### ERC20 System

```cairo
use dojo::model::{ModelStorage, ModelValueStorage};
use origami_token::components::token::erc20::erc20_balance::ERC20Balance;

#[dojo::interface]
trait IGoldToken {
    fn mint(ref self: ContractState, to: ContractAddress, amount: u256);
    fn transfer(ref self: ContractState, to: ContractAddress, amount: u256);
    fn balance_of(self: @ContractState, account: ContractAddress) -> u256;
}
```