---
name: crane-access
description: Use this skill when you need to implement access control mechanisms in Crane Diamond contracts, including ownership transfer, operator permissions, and reentrancy protection.
---

# Crane Access Control Components

Crane provides three access control patterns for Diamond proxies: MultiStepOwnable (ERC-8023), Operable, and ReentrancyLock.

## Component Selection

| Need | Component | Purpose |
|------|-----------|---------|
| Ownership with time-lock | MultiStepOwnable | Two-step ownership transfer with buffer period |
| Delegated permissions | Operable | Global and function-level operator authorization |
| Reentrancy protection | ReentrancyLock | Transient storage lock for cross-function reentrancy |

## Quick Start: Add Access Control

```solidity
// Import modifiers
import {MultiStepOwnableModifiers} from "@crane/contracts/access/ERC8023/MultiStepOwnableModifiers.sol";
import {OperableModifiers} from "@crane/contracts/access/operable/OperableModifiers.sol";
import {ReentrancyLockModifiers} from "@crane/contracts/access/reentrancy/ReentrancyLockModifiers.sol";

// Use in your Target contract
contract MyTarget is MultiStepOwnableModifiers, OperableModifiers, ReentrancyLockModifiers {
    function adminOnly() external onlyOwner {
        // Only owner can call
    }

    function operatorOnly() external onlyOperator {
        // Global operators or function-specific operators
    }

    function ownerOrOperator() external onlyOwnerOrOperator {
        // Either owner or operator can call
    }

    function noReentrant() external nonReentrant {
        // Protected from reentrancy
    }
}
```

## MultiStepOwnable (ERC-8023)

Time-locked two-step ownership transfer with buffer period.

### Storage

```solidity
struct Storage {
    address owner;
    address pendingOwner;
    bool pendingOwnerConfirmed;
    uint256 ownershipBufferPeriod;  // e.g., 1 days
    uint256 bufferPeriodEnd;
}
```

### Ownership Transfer Flow

1. **Initiate**: Owner calls `initiateOwnershipTransfer(newOwner)`
2. **Wait**: Buffer period must elapse
3. **Confirm**: Owner calls `confirmOwnershipTransfer(newOwner)`
4. **Accept**: New owner calls `acceptOwnershipTransfer()`

```solidity
// Step 1: Current owner initiates
MultiStepOwnableRepo._initiateOwnershipTransfer(newOwner);

// Step 2: Wait for buffer period (e.g., 1 day)
```