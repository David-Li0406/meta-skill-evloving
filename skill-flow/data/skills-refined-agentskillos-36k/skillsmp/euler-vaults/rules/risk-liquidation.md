---
title: How Liquidation Works on Euler
impact: HIGH
impactDescription: Understanding liquidation mechanics and math
tags: risk, liquidation, health, discount, debt-socialization
---

## How Liquidation Works on Euler

Liquidation protects the protocol by allowing anyone to take over an unhealthy account's debt in exchange for their collateral at a discount. The discount is dynamically calculated based on how unhealthy the position is.

**Key difference from other protocols:** Euler liquidation is a **position transfer**, not a debt repayment. The liquidator inherits the debt AND receives the collateral - no debt tokens are pulled from the liquidator upfront.

**Liquidation Math (from Liquidation.sol):**

```solidity
// Health score (discountFactor) = risk-adjusted collateral / liability
// discountFactor = 1.0 means healthy, < 1.0 means liquidatable
uint256 discountFactor = collateralAdjustedValue * 1e18 / liabilityValue;

// Discount = 1 - discountFactor (i.e., 1 - health score)
// Example: health = 0.85 → discount = 15%

// Cap discount at maxLiquidationDiscount (set by governor)
uint256 minDiscountFactor = 1e18 - (1e18 * maxLiquidationDiscount / 1e4);
if (discountFactor < minDiscountFactor) {
    discountFactor = minDiscountFactor;  // Cap the discount
}

// Yield value = repay value / discountFactor (more yield at lower health)
uint256 maxYieldValue = maxRepayValue * 1e18 / discountFactor;
```

**Practical Example:**

```
Position:
- Debt: 1000 USDC (value: $1000)
- Collateral: 1 ETH (value: $1200)
- Liquidation LTV: 90%
- Max Liquidation Discount: 15%

Health Score:
- Adjusted Collateral = $1200 * 90% = $1080
- Health = $1080 / $1000 = 1.08 → HEALTHY (>1.0)

After ETH drops to $1050:
- Adjusted Collateral = $1050 * 90% = $945
- Health = $945 / $1000 = 0.945 → LIQUIDATABLE (<1.0)
- Discount Factor = 0.945
- Discount = 1 - 0.945 = 5.5%

Liquidation:
- Debt inherited: $1000
- Collateral received: $1000 / 0.945 = $1058 worth of ETH
- Liquidator profit: $58 (5.5% discount)
```

**Checking liquidation opportunity:**

```solidity
// checkLiquidation returns (0, 0) if account is healthy
(uint256 maxRepay, uint256 maxYield) = IEVault(vault).checkLiquidation(
    liquidator,   // who will receive collateral
    violator,     // unhealthy account
    collateral    // which collateral to seize
);
```

**Executing liquidation:**

```solidity
// liquidate(violator, collateral, repayAssets, minYieldBalance)
// - violator: the unhealthy account
// - collateral: which collateral vault to seize from
// - repayAssets: how much debt to take over (use type(uint256).max for all)
// - minYieldBalance: minimum collateral to receive (slippage protection)

// LIQUIDATOR MUST BE PREPARED LIKE A BORROWER:
// 1. The vault must be enabled as the liquidator's controller (explicitly)
// 2. The seized collateral must be enabled for the liquidator's account

IEVC(evc).enableController(liquidator, vault);
IEVC(evc).enableCollateral(liquidator, collateral);

IEVault(vault).liquidate(violator, collateral, repayAmount, minYieldBalance);

// After: liquidator has collateral shares AND owes the debt
// Profit is realized by repaying the debt (worth less than collateral received)
```

**Liquidation Constraints:**

```solidity
// 1. Cannot self-liquidate
require(violator != liquidator, "E_SelfLiquidation");

// 2. Collateral must have LTV configured
require(isRecognizedCollateral(collateral), "E_BadCollateral");

// 3. Vault must be violator's controller
validateController(violator);

// 4. Violator must have enabled this collateral
require(isCollateralEnabled(violator, collateral), "E_CollateralDisabled");

// 5. No deferred status checks (prevents batch manipulation)
require(!isAccountStatusCheckDeferred(violator), "E_ViolatorLiquidityDeferred");

// 6. Must wait for cool-off period after last status check
require(!isInLiquidationCoolOff(violator), "E_LiquidationCoolOff");
```

**Debt Socialization (bad debt handling):**

When a position has debt remaining but no collateral left, the debt is "socialized":
- Remaining debt is written off (removed from the system)
- Loss is spread across all depositors (share value decreases)
- This protects the pool from accumulating bad debt that can never be repaid

Conditions: liability >= 1e6 in unit of account, `CFG_DONT_SOCIALIZE_DEBT` flag not set.

**Key Parameters:**

| Parameter | Getter | Description |
|-----------|--------|-------------|
| maxLiquidationDiscount | `maxLiquidationDiscount()` | Max discount (e.g., 0.15e4 = 15%) |
| liquidationCoolOffTime | `liquidationCoolOffTime()` | Seconds after status check before liquidatable |
| liquidationLTV | `LTVLiquidation(collateral)` | LTV threshold for liquidation |

Reference: [Liquidation.sol Source](https://github.com/euler-xyz/euler-vault-kit/blob/master/src/EVault/modules/Liquidation.sol)
