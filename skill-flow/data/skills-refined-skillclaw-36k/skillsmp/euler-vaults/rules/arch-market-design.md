---
title: Understanding Euler Market Design
impact: HIGH
impactDescription: Fundamental knowledge for building on Euler V2
tags: architecture, market, design, vault, modular
---

## Understanding Euler Market Design

Euler V2 uses a modular "vault kit" architecture where each market is an independent ERC-4626 vault with its own configuration for oracle, interest rate model, and collateral relationships.

**Incorrect (assuming monolithic pool like Compound/Aave):**

```solidity
// WRONG: There's no single "Euler pool" to interact with
// Each asset has its own vault(s) with independent configuration
address eulerPool = 0x...;
IPool(eulerPool).deposit(USDC, amount); // This doesn't exist!
```

**Correct (understanding independent vault architecture):**

```solidity
import {IEVault} from "evk/EVault/IEVault.sol";
import {IEVC} from "ethereum-vault-connector/interfaces/IEVC.sol";

// Each vault is independent - there can be multiple USDC vaults
// with different configurations (oracle, IRM, collaterals and risk profile)
address usdcVault = 0x...; // A specific USDC vault

// Vaults are standard ERC-4626 with extensions
IEVault vault = IEVault(usdcVault);

// Key vault properties
address asset = vault.asset();           // Underlying token
address oracle = vault.oracle();         // Price oracle (EulerRouter)
address irm = vault.interestRateModel(); // Interest rate model
address unitOfAccount = vault.unitOfAccount(); // Price denomination

// Collateral relationships are vault-to-vault
// This vault accepts another vaults' shares (not vaults' assets) as collateral
address[] memory collaterals = vault.LTVList(); // this is an append only list and may contain addresses that are no longer accepted as collateral
(uint16 borrowLTV, uint16 liquidationLTV, , ) = vault.LTVFull(collateralVault);
```

**Correct (understanding the EVC layer):**

```solidity
// The EVC (Ethereum Vault Connector) orchestrates cross-vault operations
IEVC evc = IEVC(0x0C9a3dd6b8F28529d72d7f9cE918D493519EE383); // this address is different on each chain

// Accounts enable a vault as collateral for their positions
evc.enableCollateral(account, collateralVault);

// Accounts enable a vault as controller (to borrow from)
evc.enableController(account, borrowVault);

// The controller vault checks all collateral vaults to ensure solvency
// This happens automatically at the end of the operation/batch of operations
```

**Key Architecture Concepts:**

1. **Vaults are ERC-4626**: Standard deposit/withdraw interface plus borrowing extensions
2. **Oracles per vault**: Each vault has its own EulerRouter for price resolution
3. **Unit of Account**: Common price denomination (usually USD or ETH) for LTV calculations
4. **Collateral is vault shares**: When you deposit, you get vault shares that can be accepted as collateral
5. **Controller relationship**: The vault you borrow from is your "controller". It decides if the position is healthy or requires a liquidation. It controls how much collateral user can withdraw when having an active borrow position
6. **LTV is vault-to-vault**: Each collateral-controller pair has specific LTV settings

```typescript
// TypeScript example: querying vault configuration
import { getContract } from 'viem';

const vault = getContract({
  address: vaultAddress,
  abi: evaultABI,
  client: publicClient,
});

// Get all accepted collaterals for this vault (this is an append only list and may contain addresses that are no longer accepted as collateral)
const ltvList = await vault.read.LTVList();

// For each collateral, get LTV configuration
for (const collateral of ltvList) {
  const [borrowLTV, liquidationLTV, initialLTV, targetTimestamp, rampDuration] = 
    await vault.read.LTVFull([collateral]);
  
  console.log(`Collateral ${collateral}:`);
  console.log(`  Borrow LTV: ${borrowLTV / 100}%`);
  console.log(`  Liquidation LTV: ${liquidationLTV / 100}%`);
}
```

**Market Design Patterns:**

Euler's modular architecture enables various market structures. Choose based on capital efficiency vs risk isolation tradeoffs:

| Design | Description | Similar To | Capital Efficiency | Risk Isolation |
|--------|-------------|------------|-------------------|----------------|
| Simple collateral-debt pairs | One collateral vault, one borrow vault | Morpho, FraxLend, Kashi | Low | High |
| Rehypothecation pairs | Both vaults lend and serve as collateral for each other | Silo, Fluid | Medium | Medium |
| Multiple collaterals | Many collateral vaults borrow from one lending vault | Compound | Medium-High | Medium |
| Cross-collateralised clusters | Multiple vaults all lend and collateralize each other | Aave | High | Low |
| Fully customisable | Any configuration, including vaults from existing markets | Unique to Euler | Variable | Variable |

```solidity
// Example: Simple isolated pair (Morpho-style)
// - WETH vault holds collateral in escrow only
// - USDC vault is the lending/borrowing vault
// - WETH vault has no borrowing enabled

// Example: Rehypothecation pair (Silo-style)  
// - WETH vault: accepts USDC as collateral, lends WETH
// - USDC vault: accepts WETH as collateral, lends USDC
// - Assets earn yield while backing loans

// Example: Multiple collateral vaults (Compound-style)
// - USDC vault: accepts WETH, WBTC, DAI, etc. as collateral
// - Only USDC is supplied and borrowed
// - Users can deposit various assets as collateral to borrow/supply USDC
// - Each collateral type can have different LTV and risk parameters

// Example: Cross-collateralised cluster (Aave-style)
// - WETH, WBTC, USDC, DAI vaults all interconnected
// - Each can lend and serve as collateral for others
// - Higher contagion risk if one vault defaults
```

**Creating Custom Markets:**

```solidity
// Vaults can accept collateral from ANY existing vault
// This enables composability with the broader Euler ecosystem

// Step 1: Deploy your vault
address myVault = EVaultFactory.createProxy(
    asset,
    false,  // not upgradeable
    ""      // no trailing data (only for the example; otherwise it's required)
);

// Step 2: Configure to accept existing vault shares as collateral
IEVault(myVault).setLTV(
    existingPopularVault,  // e.g., an established USDC vault
    0.85e4,                // 85% borrow LTV
    0.90e4,                // 90% liquidation LTV
    0                      // ramp duration
);

// Now users with deposits in existingPopularVault
// can borrow from your new vault without moving funds!
```

This modular design allows for permissionless market creation - anyone can deploy a vault with custom parameters while the EVC provides the security layer for cross-vault interactions.

References:
- [Euler Markets Documentation](https://docs.euler.finance/concepts/core/markets)
- [EVK Whitepaper](https://github.com/euler-xyz/euler-vault-kit/blob/master/docs/whitepaper.md)
