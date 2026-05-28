---
title: Repay Borrowed Debt
impact: HIGH
impactDescription: Essential for managing debt and avoiding liquidation
tags: vault, repay, debt, interest
---

## Repay Borrowed Debt

Repaying debt reduces your borrow balance and improves your health factor. Interest accrues continuously, so the debt amount increases over time.

**Incorrect (repaying exact original borrow amount):**

```solidity
// Interest has accrued - this won't fully repay the debt
uint256 originalBorrow = 1000e18;
IERC20(asset).approve(vault, originalBorrow);
IEVault(vault).repay(originalBorrow, account);
// Still has dust debt remaining!
```

**Correct (partial repay - specify exact amount):**

```solidity
// Get current debt to understand position
uint256 currentDebt = IEVault(vault).debtOf(account);

// Repay a specific amount (must be <= current debt, otherwise reverts)
uint256 repayAmount = currentDebt / 2; // repay half
IERC20(asset).approve(vault, repayAmount);
IEVault(vault).repay(repayAmount, account);
```

**Correct (full repay - use type(uint256).max):**

```solidity
// To repay ALL debt, use type(uint256).max
// This is the only safe way to clear debt completely (handles interest accrual)
// IMPORTANT: Repaying more than owed will REVERT - do not add buffers

// Approve enough to cover debt
uint256 currentDebt = IEVault(vault).debtOf(account);
IERC20(asset).approve(vault, currentDebt + (currentDebt / 100)); // small buffer for approval only

// Use max value to repay - pulls exactly what's owed
IEVault(vault).repay(type(uint256).max, account);
```

**Correct (repay with vault shares instead of underlying):**

```solidity
// repayWithShares burns your vault shares to repay debt
// Useful when you have shares but not the underlying asset

// Get current debt and share balance
uint256 myDebt = IEVault(vault).debtOf(account);
uint256 myShares = IEVault(vault).balanceOf(account);

// Repay using shares - returns (shares burned, assets repaid)
// amount = type(uint256).max uses all shares
(uint256 sharesBurned, uint256 assetsRepaid) = IEVault(vault).repayWithShares(
    type(uint256).max,  // or specific amount of assets to repay
    account             // whose debt to repay
);

// If shares value > debt, only burns shares worth the debt
// The conversion uses toAssetsDown for shares, toSharesUp for rounding
```

**TypeScript: repayWithShares example:**

```typescript
const vault = getContract({
  address: vaultAddress,
  abi: evaultABI,
  client: walletClient
});

// Check balances
const myDebt = await vault.read.debtOf([account]);
const myShares = await vault.read.balanceOf([account]);
const shareValue = await vault.read.convertToAssets([myShares]);

console.log(`Debt: ${myDebt}, Shares: ${myShares}, Share Value: ${shareValue}`);

// Repay with all shares (up to debt amount)
const [sharesBurned, assetsRepaid] = await vault.write.repayWithShares([
  MaxUint256,  // use all available shares
  account
]);

console.log(`Burned ${sharesBurned} shares, repaid ${assetsRepaid} debt`);
```

After fully repaying:
- The controller can be released, freeing your collateral
- You can withdraw collateral or use it elsewhere
- Sub-account becomes available for new positions

Reference: [EVault Borrowing Module](https://github.com/euler-xyz/euler-vault-kit/blob/master/src/EVault/modules/Borrowing.sol)
