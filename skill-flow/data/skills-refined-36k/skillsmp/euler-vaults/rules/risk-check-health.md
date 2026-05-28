---
title: Check Account Health Factor
impact: HIGH
impactDescription: Critical for avoiding liquidation
tags: risk, health, liquidation, ltv, collateral
---

## Check Account Health Factor

Health factor determines how close an account is to liquidation. A health factor below 1.0 means the account can be liquidated. Monitoring health is essential for safe position management.

**Incorrect (only checking debt amount):**

```solidity
// Debt amount alone doesn't indicate liquidation risk
uint256 debt = IEVault(vault).debtOf(account);
// This tells you nothing about health - need to compare against collateral value
```

**Correct (using AccountLens for health check):**

```typescript
import { AccountLens } from '@eulerxyz/evk-periphery';

// Get comprehensive account health info
// accountLens.getAccountInfo(account, vault) returns AccountInfo struct
const accountInfo = await accountLens.read.getAccountInfo([account, controller]);

// Access liquidity info from vaultAccountInfo
const liquidityInfo = accountInfo.vaultAccountInfo.liquidityInfo;

// Check if query succeeded (liquidityInfo.queryFailure === false)
if (liquidityInfo.queryFailure) {
  console.error('Liquidity query failed:', liquidityInfo.queryFailureReason);
  return;
}

// For liquidation health: collateralValueLiquidation / liabilityValueLiquidation
const collateralValueLiq = liquidityInfo.collateralValueLiquidation;
const liabilityValueLiq = liquidityInfo.liabilityValueLiquidation;

// Calculate health: > 1.0 = healthy, < 1.0 = can be liquidated
const health = liabilityValueLiq > 0n 
  ? (collateralValueLiq * BigInt(1e18)) / liabilityValueLiq 
  : BigInt(2n ** 256n - 1n); // Infinite if no debt

// timeToLiquidation: estimated SECONDS until liquidation (int256)
// Computed via binary search over 0 to 400 days, assuming static prices/rates
// Binary search precision: ±1 day (exits when interval <= 1 day)
// NOTE: Only considers Euler lending/borrowing rates, NOT external yield (e.g., wstETH, DAI)
// Special int256 values:
const TTL_INFINITY = (2n ** 255n) - 1n;        // type(int256).max - no debt, zero rate, or collateral interest >= debt interest
const TTL_MORE_THAN_ONE_YEAR = (2n ** 255n) - 2n; // type(int256).max - 1 - safe for at least one year
const TTL_LIQUIDATION = -1n;                   // already liquidatable (health <= 1)
const TTL_ERROR = -2n;                         // computation overflow or failure

const ttl = liquidityInfo.timeToLiquidation;

console.log(`Health: ${Number(health) / 1e18}`);
console.log(`Liability: ${liabilityValueLiq}`);
console.log(`Collateral: ${collateralValueLiq}`);
console.log(`Time to Liquidation: ${ttl}`);
```

**Correct (on-chain health check via accountLiquidity):**

```solidity
// Use accountLiquidity to check health on-chain

// Get liquidity values with liquidation LTV
(uint256 collateralValue, uint256 liabilityValue) = IEVault(controller).accountLiquidity(
    account,
    true  // liquidation = true for liquidation LTV
);

// Check if account is healthy (collateral >= liability)
bool isHealthy = collateralValue >= liabilityValue;

// Check if account is liquidatable
bool isLiquidatable = liabilityValue > 0 && collateralValue < liabilityValue;

// Calculate health factor (1e18 scale)
uint256 healthFactor = liabilityValue > 0 
    ? (collateralValue * 1e18) / liabilityValue 
    : type(uint256).max;
```

**Correct (detailed breakdown with accountLiquidityFull):**

```solidity
// accountLiquidityFull returns per-collateral breakdown
(
    address[] memory collaterals,
    uint256[] memory collateralValues,
    uint256 liabilityValue
) = IEVault(controller).accountLiquidityFull(account, true);

// Analyze each collateral's contribution
for (uint256 i = 0; i < collaterals.length; i++) {
    console.log("Collateral:", collaterals[i]);
    console.log("Value:", collateralValues[i]);
    
    // Calculate this collateral's contribution percentage
    uint256 totalCollateral = sumArray(collateralValues);
    uint256 contribution = collateralValues[i] * 100 / totalCollateral;
    console.log("Contribution:", contribution, "%");
}

console.log("Total Liability:", liabilityValue);
```

**TypeScript: Using accountLiquidity:**

```typescript
const vault = getContract({
  address: controllerAddress,
  abi: evaultABI,
  client: publicClient
});

// Get liquidity with borrow LTV
const [collateralBorrow, liabilityBorrow] = await vault.read.accountLiquidity([
  account,
  false  // borrow LTV
]);

// Get liquidity with liquidation LTV
const [collateralLiq, liabilityLiq] = await vault.read.accountLiquidity([
  account,
  true   // liquidation LTV
]);

// Calculate both health factors
const borrowHealth = liabilityBorrow > 0n 
  ? (collateralBorrow * 10n ** 18n) / liabilityBorrow 
  : MaxUint256;

const liquidationHealth = liabilityLiq > 0n
  ? (collateralLiq * 10n ** 18n) / liabilityLiq
  : MaxUint256;

console.log(`Borrow Health: ${formatUnits(borrowHealth, 18)}`);
console.log(`Liquidation Health: ${formatUnits(liquidationHealth, 18)}`);

// Full breakdown
const [collaterals, values, liability] = await vault.read.accountLiquidityFull([
  account,
  true
]);

for (let i = 0; i < collaterals.length; i++) {
  console.log(`${collaterals[i]}: ${formatUnits(values[i], 18)} value`);
}
```

**Correct (disabling controller after full repayment):**

```solidity
// After fully repaying debt, you can disable the controller
// This releases your collateral from the vault's control

// First, ensure debt is zero
uint256 debt = IEVault(controller).debtOf(account);
require(debt == 0, "Outstanding debt");

// Disable controller - must be called by the account owner
// Note: This is called ON the controller vault, not the EVC
IEVault(controller).disableController();

// Now you can withdraw freely without health checks
```

**TypeScript: Full repay and disable flow:**

```typescript
const batchItems: BatchItem[] = [
  // Repay all debt
  {
    onBehalfOfAccount: account,
    targetContract: controllerVault,
    value: 0n,
    data: encodeFunctionData({
      abi: evaultABI,
      functionName: 'repay',
      args: [MaxUint256, account],
    }),
  },
  // Disable controller (releases collateral from health checks)
  {
    onBehalfOfAccount: account,
    targetContract: controllerVault,
    value: 0n,
    data: encodeFunctionData({
      abi: evaultABI,
      functionName: 'disableController',
      args: [],
    }),
  },
  // Withdraw collateral (no health check now that controller is disabled)
  {
    onBehalfOfAccount: account,
    targetContract: collateralVault,
    value: 0n,
    data: encodeFunctionData({
      abi: evaultABI,
      functionName: 'withdraw',
      args: [MaxUint256, account, account],
    }),
  },
];

await evc.batch(batchItems);
```

**Understanding checkAccountStatus and checkVaultStatus (EVC internals):**

These are EVC callback functions - **NOT meant to be called directly**. The EVC calls them automatically during deferred checks at the end of batches:

- `checkAccountStatus(account, collaterals)`: Called by EVC to verify account health. Reverts if unhealthy (collateral < liability). Returns magic selector on success.
- `checkVaultStatus()`: Called by EVC to verify vault caps aren't exceeded and triggers interest rate recalculation.

**For health checks in your code, use `accountLiquidity()` instead** (shown above).

Key concepts:
- Health > 1.0 = safe from liquidation
- Borrow LTV: max health when taking new borrows
- Liquidation LTV: health at which liquidation can occur
- Always maintain buffer above 1.0 for price volatility
- `accountLiquidity(account, false)` = borrow LTV values
- `accountLiquidity(account, true)` = liquidation LTV values
- Call `disableController()` after full repayment to release position

Time to Liquidation (TTL) - **unit: seconds**, **precision: ±1 day** (int256):
- Positive values = seconds until liquidation (binary search over 0-400 days, ±1 day precision)
- `TTL_INFINITY` = `type(int256).max`: No debt, zero borrow rate, or collateral interest >= debt interest
- `TTL_MORE_THAN_ONE_YEAR` = `type(int256).max - 1`: Safe for at least one year
- `TTL_LIQUIDATION` = `-1`: Already liquidatable (health <= 1)
- `TTL_ERROR` = `-2`: Computation overflow or failure
- ⚠️ TTL only considers **Euler lending/borrowing rates** - does NOT include external yield (wstETH, DAI etc.)
- ⚠️ TTL assumes **static prices** - real price volatility may cause liquidation sooner

See also: [Lens Contracts](tools-lens) - AccountLens provides `getAccountLiquidityInfo()` and `getTimeToLiquidation()` for comprehensive health monitoring.

Reference: [EVK Risk Manager Module](https://github.com/euler-xyz/euler-vault-kit/blob/master/src/EVault/modules/RiskManager.sol)
