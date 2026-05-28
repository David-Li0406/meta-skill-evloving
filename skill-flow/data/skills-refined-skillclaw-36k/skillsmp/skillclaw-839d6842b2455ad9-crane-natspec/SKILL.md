---
name: crane-natspec
description: Use this skill when you need guidance on documenting Crane contracts with NatSpec and AsciiDoc include-tags, including details on custom tags and their usage.
---

# Crane NatSpec & Documentation Standards

Crane uses NatSpec combined with AsciiDoc include-tags for accurate, extractable documentation.

## AsciiDoc Include-Tags

Wrap documented symbols with include-tags for documentation extraction:

```solidity
// tag::MySymbol[]
/// @notice Description of the symbol
function myFunction() external { ... }
// end::MySymbol[]
```

### Tag Format Rules

- Tag markers must match exactly (no extra spaces inside `[]`)
- Tag name should match the symbol being documented
- Use PascalCase for tag names matching type names
- Use camelCase for function tag names

### Example Usage

```solidity
// tag::transfer[]
/// @notice Transfers tokens to a recipient
/// @param to_ The recipient address
/// @param amount_ The amount to transfer
/// @return success True if transfer succeeded
/// @custom:signature transfer(address,uint256)
/// @custom:selector 0xa9059cbb
function transfer(address to_, uint256 amount_) external returns (bool success);
// end::transfer[]
```

## Custom NatSpec Tags

### Functions

| Tag | Purpose | Example |
|-----|---------|---------|
| `@custom:signature` | Canonical signature string | `transfer(address,uint256)` |
| `@custom:selector` | bytes4 selector | `0xa9059cbb` |

```solidity
/// @notice Transfers tokens
/// @custom:signature transfer(address,uint256)
/// @custom:selector 0xa9059cbb
function transfer(address to_, uint256 amount_) external returns (bool);
```

### Errors

| Tag | Purpose | Example |
|-----|---------|---------|
| `@custom:signature` | Canonical error signature | `NotOwner(address)` |
| `@custom:selector` | bytes4 selector | `0x30cd7471` |

```solidity
/// @notice Thrown when caller is not the owner
/// @custom:signature NotOwner(address)
/// @custom:selector 0x30cd7471
error NotOwner(address caller);
```

### Events

| Tag | Purpose | Example |
|-----|---------|---------|
| `@custom:signature` | Canonical event signature | `Transfer(address,address,uint256)` |
| `@custom:topiczero` | bytes32 topic0 hash | `0xddf252ad...` |

```solidity
/// @notice Emitted on token transfer
/// @custom:signature Transfer(address,address,uint256)
/// @custom:topiczero 0xddf252ad...
event Transfer(address indexed from, address indexed to, uint256 value);
```