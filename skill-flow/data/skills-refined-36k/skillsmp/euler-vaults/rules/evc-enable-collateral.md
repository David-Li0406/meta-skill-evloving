---
title: Enable Vault as Collateral
impact: CRITICAL
impactDescription: Required before collateral can back borrows
tags: evc, collateral, enable, controller, ltv
---

## Enable Vault as Collateral

Before vault deposits can be used as collateral for borrowing, you must explicitly enable the vault in your account's collateral set via EVC.

**Incorrect (borrowing without enabling collateral):**

```solidity
// Deposit into vault
IEVault(collateralVault).deposit(amount, account);

// Try to borrow - fails because collateral not recognized
IEVC(evc).enableController(account, borrowVault);
IEVault(borrowVault).borrow(borrowAmount, account);
// Error: E_AccountLiquidity - no recognized collateral
```

**Correct (enable collateral before borrowing):**

```solidity
// Step 1: Deposit into the collateral vault
IERC20(asset).approve(collateralVault, amount);
IEVault(collateralVault).deposit(amount, account);

// Step 2: Enable this vault as collateral for your account
// This adds the vault to your account's collateral set
IEVC(evc).enableCollateral(account, collateralVault);

// Step 3: Now you can borrow against this collateral
IEVC(evc).enableController(account, borrowVault);
IEVault(borrowVault).borrow(borrowAmount, account);
```

**Correct (batch enable multiple collaterals):**

```solidity
IEVC.BatchItem[] memory items = new IEVC.BatchItem[](3);

// Enable WETH vault as collateral
// NOTE: When target is EVC itself, onBehalfOfAccount MUST be address(0)
items[0] = IEVC.BatchItem({
    onBehalfOfAccount: address(0),
    targetContract: address(evc),
    value: 0,
    data: abi.encodeCall(IEVC.enableCollateral, (account, wethVault))
});

// Enable WBTC vault as collateral
items[1] = IEVC.BatchItem({
    onBehalfOfAccount: address(0),
    targetContract: address(evc),
    value: 0,
    data: abi.encodeCall(IEVC.enableCollateral, (account, wbtcVault))
});

// Enable wstETH vault as collateral
items[2] = IEVC.BatchItem({
    onBehalfOfAccount: address(0),
    targetContract: address(evc),
    value: 0,
    data: abi.encodeCall(IEVC.enableCollateral, (account, wstethVault))
});

IEVC(evc).batch(items);
```

**Correct (checking and disabling collateral):**

```solidity
// Check if vault is enabled as collateral
bool isCollateral = IEVC(evc).isCollateralEnabled(account, vault);

// Get all enabled collaterals for an account
address[] memory collaterals = IEVC(evc).getCollaterals(account);

// Disable collateral (only works if not needed for health)
// WARNING: Will fail if removing would make account unhealthy
IEVC(evc).disableCollateral(account, vault);
```

Important considerations:
- Collateral vault must be accepted by the borrow vault's LTV configuration
- Each vault can have different LTV ratios (borrow LTV vs liquidation LTV)
- Disabling collateral fails if it would make account unhealthy
- Maximum 10 collaterals per account (SET_MAX_ELEMENTS)

Reference: [EVC Whitepaper - Collateral Validity](https://github.com/euler-xyz/ethereum-vault-connector/blob/master/docs/whitepaper.md#collateral-validity)
