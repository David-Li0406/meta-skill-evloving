---
name: crane-code-style
description: Use this skill when you need guidance on Crane's code conventions, including code style, naming conventions, imports, section headers, and formatting.
---

# Crane Code Style Guide

Crane follows strict code conventions for consistency and maintainability. This skill covers section headers, imports, naming, and critical compilation rules.

## Section Headers

Use 78-character wide comment blocks for major sections:

```solidity
/* -------------------------------------------------------------------------- */
/*                             Section Name                                   */
/* -------------------------------------------------------------------------- */
```

Shorter form for subsections:

```solidity
/* ------ Feature Name ------ */
```

## Import Organization

Group imports by source, with import aliases:

```solidity
// External libraries
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@solady/utils/SafeERC20.sol";

// Crane interfaces
import {IFacet} from "@crane/contracts/interfaces/IFacet.sol";
import {IOperable} from "@crane/contracts/access/operable/interfaces/IOperable.sol};

// Crane contracts
import {OperableRepo} from "@crane/contracts/access/operable/OperableRepo.sol";
import {OperableTarget} from "@crane/contracts/access/operable/OperableTarget.sol";

// Test utilities (in test files)
import {Test} from "forge-std/Test.sol";
import {Vm, VM_ADDRESS} from "forge-std/Vm.sol";
```

### Import Aliases

Defined in `foundry.toml` and `remappings.txt`:

| Alias | Path |
|-------|------|
| `@crane/` | Crane framework contracts |
| `@solady/` | Solady library |
| `@openzeppelin/` | OpenZeppelin contracts |
| `forge-std/` | Foundry test utilities |

## Function Organization

Order functions by visibility:

1. Constructor
2. Receive
3. Fallback
4. External
5. Public
6. Internal
7. Private

## Naming Conventions

| Pattern | Usage | Example |
|---------|-------|---------|
| `_layout()` | Storage access | `_layout()`, `_layout(bytes32 slot_)` |
| `_initialize()` | Storage setup | `_initialize(address owner_)` |
| `_functionName()` | Internal Repo functions | `_isOperator()`, `_setOperator()` |
| `_onlyXxx()` | Guard functions in Repos | `_onlyOwner()`, `_onlyOperator()` |
| `onlyXxx` | Modifiers | `onlyOwner`, `onlyOperator` |
| `layout` | Storage parameters | `layout` |