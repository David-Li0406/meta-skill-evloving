---
name: crane-architecture
description: Use this skill when you need guidance on Crane's core architectural patterns for building modular, upgradeable smart contracts, including facets, targets, repos, and related concepts.
---

# Crane Architecture Patterns

Crane is a Diamond-first (ERC2535) Solidity development framework for building modular, upgradeable smart contracts. This skill provides guidance on the core architectural patterns.

## Core Pattern: Facet-Target-Repo

Every feature in Crane follows a three-tier architecture:

| Layer | File Pattern | Purpose |
|-------|--------------|---------|
| **Repo** | `*Repo.sol` | Storage library with assembly-based slot binding. Defines `Storage` struct and dual `_layout()` functions. No state variables. |
| **Target** | `*Target.sol` | Implementation contract with business logic. Uses Repo for storage access. Inherits interfaces. |
| **Facet** | `*Facet.sol` | Diamond facet. Extends Target and implements `IFacet` for metadata (name, interfaces, selectors). |

### When to Create Each Layer

- **Repo**: Always create first. Contains all storage and internal helper functions.
- **Target**: Create when business logic needs to be shared or tested independently.
- **Facet**: Create when exposing functionality through the Diamond proxy.

## Storage Slot Pattern

All Repos use the Diamond storage pattern with dual function overloads:

```solidity
library ExampleRepo {
    bytes32 internal constant STORAGE_SLOT = keccak256(abi.encode("crane.feature.name"));

    struct Storage {
        mapping(address => bool) isOperator;
    }

    // Parameterized version - allows custom slot
    function _layout(bytes32 slot) internal pure returns (Storage storage layout) {
        assembly { layout.slot := slot }
    }

    // Default version - uses STORAGE_SLOT
    function _layout() internal pure returns (Storage storage) {
        return _layout(STORAGE_SLOT);
    }
}
```

### Dual Function Overload Pattern

Every Repo function has TWO overloads:

```solidity
// 1. Parameterized: takes Storage as first param
function _isOperator(Storage storage layout, address query) internal view returns (bool) {
    return layout.isOperator[query];
}

// 2. Default: calls parameterized with _layout()
function _isOperator(address query) internal view returns (bool) {
    return _isOperator(_layout(), query);
}
```