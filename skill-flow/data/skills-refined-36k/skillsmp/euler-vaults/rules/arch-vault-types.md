---
title: Understanding Vault Types (Governed, Ungoverned, Escrowed Collateral)
impact: HIGH
impactDescription: Critical for selecting appropriate vault type for your use case
tags: architecture, vault, governed, ungoverned, escrow, perspective
---

## Understanding Vault Types (Governed, Ungoverned, Escrowed Collateral)

Euler V2 vaults fall into two main categories based on governance: **Governed** (with active governance) and **Ungoverned** (governance renounced). Escrowed Collateral vaults are a special subtype of ungoverned vaults designed for collateral-only use cases.

**Incorrect (treating all vaults the same):**

```solidity
// WRONG: Not all vaults support borrowing or have the same features
IEVault vault = IEVault(anyVault);
vault.borrow(amount, receiver); // May revert for escrow vaults!
vault.setInterestRateModel(irm); // May not be configurable!
```

**Correct (understanding vault types):**

### 1. Governed Vaults

Full-featured lending vaults with active governance (risk management). The governor can update parameters like LTV, caps, IRM, and oracle configuration over time.

> ⚠️ **Trust Warning:** Users must fully trust the governor address. The governor has significant power over vault parameters and could potentially act maliciously (e.g., setting dangerous LTVs, changing oracles, or extracting fees). Always verify who controls governance before depositing - whether it's an EOA, multisig, DAO, or limited governor contract.

```solidity
import {GenericFactory} from "evk/GenericFactory/GenericFactory.sol";
import {IEVault} from "evk/EVault/IEVault.sol";

// Governed vaults have full configuration capabilities
IEVault vault = IEVault(vaultAddress);

// Has governor for ongoing management
address governor = vault.governorAdmin();
require(governor != address(0), "This is a governed vault");

// Governor can update configuration
vault.setInterestRateModel(newIRM);
vault.setLTV(collateral, borrowLTV, liquidationLTV, rampDuration);
vault.setCaps(supplyCap, borrowCap);

// Supports all operations: deposit, withdraw, borrow, repay
vault.deposit(amount, receiver);
vault.borrow(amount, receiver);
```

**Limited Governor Pattern:**

Instead of a full EOA or multisig as governor, you can set a **limited governor contract** that only allows specific parameter changes. This provides a middle ground between full governance and complete immutability.

```solidity
// Example: CapRiskSteward only allows cap adjustments within limits
import {CapRiskSteward} from "evk-periphery/Governor/CapRiskSteward.sol";

// Deploy a limited governor that can only adjust caps
CapRiskSteward steward = new CapRiskSteward(
    evc,
    admin,           // Who can call the steward
    3 days,          // Cooldown between adjustments
    0.1e18           // Max 10% change per adjustment
);

// Set the steward as the vault's governor
vault.setGovernorAdmin(address(steward));

// Now only cap changes (within limits) are possible
// Other governance functions like setLTV, setIRM will revert
steward.setSupplyCap(vaultAddress, newSupplyCap);
steward.setBorrowCap(vaultAddress, newBorrowCap);
```

This pattern is useful when you want restricted, predictable governance rather than full control or complete immutability.

### 2. Ungoverned Vaults

Vaults with governance permanently renounced (`governorAdmin == address(0)`). Configuration is fixed at deployment and cannot be changed. This provides immutability guarantees but no flexibility.

```solidity
// Ungoverned vaults have fixed configuration
IEVault vault = IEVault(vaultAddress);

// Governor is address(0) - no one can change parameters
require(vault.governorAdmin() == address(0), "Ungoverned vault");

// These calls will revert with E_Unauthorized:
// vault.setInterestRateModel(newIRM);  // Cannot change
// vault.setLTV(collateral, ltv, ltv, 0);  // Cannot change
// vault.setCaps(cap, cap);  // Cannot change

// Normal operations still work
vault.deposit(amount, receiver);
vault.borrow(amount, receiver);  // If borrowing is configured
```

### 3. Escrowed Collateral Vaults (Ungoverned Subtype)

Special ungoverned vaults designed purely for holding collateral. They have no oracle, no IRM, and no borrowing capability and are neutral (can be reused by anyone). One escrow vault exists per asset (singleton pattern).

```solidity
import {EscrowedCollateralPerspective} from "evk-periphery/Perspectives/deployed/EscrowedCollateralPerspective.sol";

// Escrow vaults are singletons per asset - only one per token
EscrowedCollateralPerspective perspective = EscrowedCollateralPerspective(perspectiveAddress);
address escrowVault = perspective.singletonLookup(assetAddress);

// If not deployed, deploy new escrow vault
if (escrowVault == address(0)) {
    bytes memory trailingData = abi.encodePacked(asset, address(0), address(0));
    escrowVault = GenericFactory(factory).createProxy(address(0), true, trailingData);
    
    // Escrow vaults have minimal config and renounced governance
    IEVault(escrowVault).setHookConfig(address(0), 0);
    IEVault(escrowVault).setGovernorAdmin(address(0));
    
    // Verify in perspective so that others can reuse this vault later
    perspective.perspectiveVerify(escrowVault, true);
}

// Escrow vault properties:
// - No oracle (address(0))
// - No unit of account (address(0))
// - No IRM (address(0))
// - No caps
// - No hooks
// - No LTV list (cannot be borrowed against directly)
// - Governance renounced (address(0))
```

**Correct (using Perspectives to verify vault type):**

```typescript
import { getContract } from 'viem';

// Perspectives verify vault properties
const governedPerspective = getContract({
  address: governedPerspectiveAddress,
  abi: perspectiveABI,
  client: publicClient,
});

const escrowPerspective = getContract({
  address: escrowPerspectiveAddress,
  abi: perspectiveABI,
  client: publicClient,
});

// Check if vault is in a perspective
const isGoverned = await governedPerspective.read.isVerified([vaultAddress]);
const isEscrow = await escrowPerspective.read.isVerified([vaultAddress]);

// Check governance status directly
const vault = getContract({
  address: vaultAddress,
  abi: evaultABI,
  client: publicClient,
});
const governor = await vault.read.governorAdmin();
const isUngoverned = governor === '0x0000000000000000000000000000000000000000';

// Perspectives provide trust guarantees:
// - GovernedPerspective: whitelisted by Euler
// - EscrowedCollateralPerspective: verified collateral-only vault
// - EVKFactoryPerspective: deployed by official factory
```

| Feature | Governed Vault | Ungoverned Vault | Escrowed Collateral |
|---------|----------------|------------------|---------------------|
| Borrowing | ✓ | ✓ (if configured) | ✗ |
| Governance | ✓ | ✗ (renounced) | ✗ (renounced) |
| Oracle | ✓ | ✓ (fixed) | ✗ |
| IRM | ✓ | ✓ (fixed) | ✗ |
| Caps | ✓ | ✓ (fixed) | ✗ |
| Can be collateral | ✓ | ✓ | ✓ |
| Config changeable | ✓ | ✗ | ✗ |

Reference: [EscrowedCollateralPerspective.sol](https://github.com/euler-xyz/evk-periphery/blob/master/src/Perspectives/deployed/EscrowedCollateralPerspective.sol)
