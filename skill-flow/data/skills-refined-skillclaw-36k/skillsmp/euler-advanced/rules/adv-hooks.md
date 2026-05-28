---
title: Vault Hooks and Use Cases
impact: MEDIUM
impactDescription: Enabling custom vault logic and access control
tags: hooks, guardian, pause, access-control, customization
---

## Vault Hooks and Use Cases

Euler vaults support a hooking system that allows custom logic to be executed before operations. Hooks can implement access control, pausing, or reject operations that violate custom invariants.

**Incorrect (ignoring hook configuration on new vaults):**

```solidity
// WRONG: New vaults start with all operations disabled!
// Hooks are enabled with hookTarget = address(0), which reverts
IEVault vault = IEVault(newVaultAddress);
vault.deposit(amount, receiver); // Reverts with E_OperationDisabled!
```

**Correct (understanding hook architecture):**

```solidity
import {IEVault} from "evk/EVault/IEVault.sol";

IEVault vault = IEVault(vaultAddress);

// Get current hook configuration
(address hookTarget, uint32 hookedOps) = vault.hookConfig();

// hookedOps is a bitfield of operations that trigger the hook
// If hookTarget == address(0) and operation is hooked, it reverts

// Operation flags (from Constants.sol):
uint32 OP_DEPOSIT            = 1 << 0;   // deposit
uint32 OP_MINT               = 1 << 1;   // mint
uint32 OP_WITHDRAW           = 1 << 2;   // withdraw
uint32 OP_REDEEM             = 1 << 3;   // redeem
uint32 OP_TRANSFER           = 1 << 4;   // transfer, transferFrom
uint32 OP_SKIM               = 1 << 5;   // skim
uint32 OP_BORROW             = 1 << 6;   // borrow
uint32 OP_REPAY              = 1 << 7;   // repay
uint32 OP_REPAY_WITH_SHARES  = 1 << 8;   // repayWithShares
uint32 OP_PULL_DEBT          = 1 << 9;   // pullDebt
uint32 OP_CONVERT_FEES       = 1 << 10;  // convertFees
uint32 OP_LIQUIDATE          = 1 << 11;  // liquidate
uint32 OP_FLASHLOAN          = 1 << 12;  // flashLoan
uint32 OP_TOUCH              = 1 << 13;  // touch
uint32 OP_VAULT_STATUS_CHECK = 1 << 14;  // checkVaultStatus

// To enable all operations, disable all hooks:
vault.setHookConfig(address(0), 0);
```

**Correct (implementing Access Control):**

```solidity
import {HookTargetAccessControl} from "evk-periphery/HookTarget/HookTargetAccessControl.sol";

// Access control hook for permissioned vaults
HookTargetAccessControl accessControl = new HookTargetAccessControl(
    eVaultFactory,
    admin
);

// Grant roles to addresses
accessControl.grantRole(accessControl.WILD_CARD(), allowedAddress);

// Configure vault
vault.setHookConfig(address(accessControl), OP_DEPOSIT | OP_BORROW);

// Now only addresses with WILD_CARD role can deposit/borrow
```

**Correct (custom hook implementation):**

```solidity
import {BaseHookTarget} from "evk-periphery/HookTarget/BaseHookTarget.sol";

contract CustomHook is BaseHookTarget {
    mapping(address => bool) public allowed;
    
    constructor(address factory) BaseHookTarget(factory) {}
    
    // Hook receives same calldata as vault function
    // with the authenticated caller appended
    function deposit(uint256 assets, address receiver) external view {
        address caller = _msgSender();
        require(allowed[caller], "Not allowed");
        // If this doesn't revert, the deposit proceeds
    }
    
    function borrow(uint256 assets, address receiver) external view {
        address caller = _msgSender();
        require(allowed[caller], "Not allowed");
    }
    
    // Fallback for other operations - allow them
    fallback() external {}
}
```

**Correct (checking vault status with hooks):**

```solidity
// OP_VAULT_STATUS_CHECK hooks into the EVC status check
// This runs at the end of batches to verify post-conditions

contract InvariantChecker is BaseHookTarget {
    constructor(address factory) BaseHookTarget(factory) {}
    
    // Called when EVC checks vault status
    function checkVaultStatus() external view {
        IEVault vault = IEVault(msg.sender);
        
        // Example: ensure utilization stays below 95%
        uint256 totalAssets = vault.totalAssets();
        uint256 totalBorrows = vault.totalBorrows();
        
        if (totalAssets > 0) {
            uint256 utilization = (totalBorrows * 1e18) / totalAssets;
            require(utilization < 0.95e18, "Utilization too high");
        }
    }
    
    fallback() external {}
}
```

**TypeScript: Checking hook configuration:**

```typescript
import { getContract } from 'viem';

const vault = getContract({
  address: vaultAddress,
  abi: evaultABI,
  client: publicClient,
});

const [hookTarget, hookedOps] = await vault.read.hookConfig();

// Decode hooked operations (correct bit positions)
const operations = {
  DEPOSIT: (hookedOps & (1 << 0)) !== 0,
  MINT: (hookedOps & (1 << 1)) !== 0,
  WITHDRAW: (hookedOps & (1 << 2)) !== 0,
  REDEEM: (hookedOps & (1 << 3)) !== 0,
  TRANSFER: (hookedOps & (1 << 4)) !== 0,
  SKIM: (hookedOps & (1 << 5)) !== 0,
  BORROW: (hookedOps & (1 << 6)) !== 0,
  REPAY: (hookedOps & (1 << 7)) !== 0,
  REPAY_WITH_SHARES: (hookedOps & (1 << 8)) !== 0,
  PULL_DEBT: (hookedOps & (1 << 9)) !== 0,
  CONVERT_FEES: (hookedOps & (1 << 10)) !== 0,
  LIQUIDATE: (hookedOps & (1 << 11)) !== 0,
  FLASHLOAN: (hookedOps & (1 << 12)) !== 0,
  TOUCH: (hookedOps & (1 << 13)) !== 0,
  VAULT_STATUS_CHECK: (hookedOps & (1 << 14)) !== 0,
};

console.log(`Hook Target: ${hookTarget}`);
console.log('Hooked Operations:', operations);

// If hookTarget is zero and operation is hooked, it's DISABLED
const isDepositDisabled = operations.DEPOSIT && hookTarget === '0x0000000000000000000000000000000000000000';
```

**Use Cases:**

| Hook Type | Purpose | Example |
|-----------|---------|---------|
| Access Control | Permissioned vaults | KYC/AML compliance |
| Rate Limiter | Prevent large movements | Limit deposit/withdraw per block |
| Invariant Checker | Post-condition validation | Ensure utilization bounds |
| Whitelist | Restrict interactions | Institutional-only vaults |

[EVK Whitepaper - Hooks](https://github.com/euler-xyz/euler-vault-kit/blob/master/docs/whitepaper.md)
