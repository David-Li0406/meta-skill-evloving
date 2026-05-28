---
title: Lens Contracts for Data Queries
impact: MEDIUM
impactDescription: Essential for reading comprehensive vault and account data
tags: lens, query, data, vault, account, oracle, irm
---

## Lens Contracts for Data Queries

Lens contracts provide read-only aggregated views of Euler protocol data. They simplify complex multi-call queries into single function calls, returning structured data about vaults, accounts, oracles, and interest rate models.

**Available Lens Contracts:**

| Lens | Purpose |
|------|---------|
| AccountLens | Account positions, liquidity, health, TTL |
| VaultLens | Vault configuration, state, LTVs, IRM info |
| OracleLens | Oracle configuration and validation |
| IRMLens | Interest rate model parameters |
| UtilsLens | APY calculations, token balances, price queries |
| EulerEarnVaultLens | EulerEarn vault strategies and allocations |

**Incorrect (making many individual calls):**

```typescript
// WRONG: Multiple calls easy to miss data
const totalAssets = await vault.read.totalAssets();
const totalBorrows = await vault.read.totalBorrows();
const cash = await vault.read.cash();
const governor = await vault.read.governorAdmin();
const irm = await vault.read.interestRateModel();
// ... many more calls needed
```

**Correct (using VaultLens for comprehensive vault data):**

```typescript
import { getContract } from 'viem';
import lens from '@eulerxyz/euler-interfaces/addresses/1/LensAddresses.json';
import vaultLensABI from '@eulerxyz/euler-interfaces/abis/VaultLens.json';

const vaultLens = getContract({
  address: lens.vaultLens as Address,
  abi: vaultLensABI,
  client: publicClient
});

// Get all vault info in one call
const vaultInfo = await vaultLens.read.getVaultInfoFull([vaultAddress]);

console.log(`Vault: ${vaultInfo.vaultName} (${vaultInfo.vaultSymbol})`);
console.log(`Asset: ${vaultInfo.assetName} (${vaultInfo.assetDecimals} decimals)`);
console.log(`Total Assets: ${vaultInfo.totalAssets}`);
console.log(`Total Borrowed: ${vaultInfo.totalBorrowed}`);
console.log(`Supply Cap: ${vaultInfo.supplyCap}`);
console.log(`Borrow Cap: ${vaultInfo.borrowCap}`);
console.log(`Governor: ${vaultInfo.governorAdmin}`);
console.log(`Oracle: ${vaultInfo.oracle}`);
console.log(`IRM: ${vaultInfo.interestRateModel}`);

// LTV info for each collateral
for (const ltv of vaultInfo.collateralLTVInfo) {
  console.log(`Collateral ${ltv.collateral}: borrow=${ltv.borrowLTV}, liq=${ltv.liquidationLTV}`);
}
```

**Correct (using AccountLens for position data):**

```typescript
import accountLensABI from '@eulerxyz/euler-interfaces/abis/AccountLens.json';

const accountLens = getContract({
  address: lens.accountLens as Address,
  abi: accountLensABI,
  client: publicClient
});

// Get full account info for a specific vault
const accountInfo = await accountLens.read.getAccountInfo([account, vaultAddress]);

// EVC account state
const evcInfo = accountInfo.evcAccountInfo;
console.log(`Owner: ${evcInfo.owner}`);
console.log(`Controllers: ${evcInfo.enabledControllers}`);
console.log(`Collaterals: ${evcInfo.enabledCollaterals}`);
console.log(`Lockdown Mode: ${evcInfo.isLockdownMode}`);

// Vault position
const vaultInfo = accountInfo.vaultAccountInfo;
console.log(`Shares: ${vaultInfo.shares}`);
console.log(`Assets (deposits): ${vaultInfo.assets}`);
console.log(`Borrowed: ${vaultInfo.borrowed}`);
console.log(`Is Controller: ${vaultInfo.isController}`);
console.log(`Is Collateral: ${vaultInfo.isCollateral}`);

// Liquidity and health
const liq = vaultInfo.liquidityInfo;
console.log(`Collateral Value (borrow): ${liq.collateralValueBorrowing}`);
console.log(`Collateral Value (liq): ${liq.collateralValueLiquidation}`);
console.log(`Liability Value: ${liq.liabilityValueLiquidation}`);
console.log(`Time to Liquidation: ${liq.timeToLiquidation}`);
```

**Correct (using AccountLens for liquidity info only):**

```typescript
// Quick health check without full account info
const liquidityInfo = await accountLens.read.getAccountLiquidityInfo([
  account,
  controllerVault
]);

if (liquidityInfo.queryFailure) {
  console.error('Query failed:', liquidityInfo.queryFailureReason);
  return;
}

// Calculate health factor
const health = liquidityInfo.liabilityValueLiquidation > 0n
  ? (liquidityInfo.collateralValueLiquidation * 10n ** 18n) / liquidityInfo.liabilityValueLiquidation
  : MaxUint256;

console.log(`Health Factor: ${formatUnits(health, 18)}`);

// Time to liquidation (special int256 values)
const TTL_INFINITY = (2n ** 255n) - 1n;        // type(int256).max - no debt or safe indefinitely
const TTL_MORE_THAN_ONE_YEAR = (2n ** 255n) - 2n; // safe for at least one year
const TTL_LIQUIDATION = -1n;                   // already liquidatable
const TTL_ERROR = -2n;                         // computation error

const ttl = liquidityInfo.timeToLiquidation;
if (ttl === TTL_INFINITY || ttl === TTL_MORE_THAN_ONE_YEAR) {
  console.log('Safe: No liquidation risk');
} else if (ttl === TTL_LIQUIDATION) {
  console.log('DANGER: Already liquidatable!');
} else if (ttl === TTL_ERROR) {
  console.log('Error computing TTL');
} else if (ttl > 0n) {
  console.log(`Time to liquidation: ${ttl} seconds`);
}
```

**Correct (using AccountLens for all EVC-enabled vaults):**

```typescript
// Get info for ALL vaults an account has enabled (collaterals + controllers)
const multiVaultInfo = await accountLens.read.getAccountEnabledVaultsInfo([
  evcAddress,
  account
]);

// EVC state
console.log(`Owner: ${multiVaultInfo.evcAccountInfo.owner}`);
console.log(`Controllers: ${multiVaultInfo.evcAccountInfo.enabledControllers.length}`);
console.log(`Collaterals: ${multiVaultInfo.evcAccountInfo.enabledCollaterals.length}`);

// Position in each vault
for (const vaultInfo of multiVaultInfo.vaultAccountInfo) {
  console.log(`\nVault: ${vaultInfo.vault}`);
  console.log(`  Deposited: ${vaultInfo.assets}`);
  console.log(`  Borrowed: ${vaultInfo.borrowed}`);
  console.log(`  Is Controller: ${vaultInfo.isController}`);
  console.log(`  Is Collateral: ${vaultInfo.isCollateral}`);
}
```

**Correct (using AccountLens with no-validation mode):**

```typescript
// getAccountLiquidityInfoNoValidation handles certain query failures gracefully
// Useful for accounts without active debt or when vault is not a controller
const liquidityInfo = await accountLens.read.getAccountLiquidityInfoNoValidation([
  account,
  vaultAddress
]);

// Returns zeroed values instead of failing for:
// - E_TransientState (mid-batch checks)
// - E_NoLiability (no debt)
// - E_NotController (vault not enabled as controller)
// - E_NoPriceOracle (oracle not configured)
```

**Correct (using AccountLens for on-chain reward info):**

> **Note:** The balance tracking and reward-streams mechanism (`TrackingRewardStreams`) is embedded in the EVK but has seen limited adoption. Most Euler rewards are distributed via **off-chain mechanisms like [Merkl](https://merkl.xyz/)**. The on-chain reward-streams may not be supported in all UIs. Check the specific vault's reward distribution method before relying on this data.

```typescript
// On-chain reward info (legacy mechanism - limited adoption)
// Most rewards are distributed off-chain via Merkl instead
const accountInfo = await accountLens.read.getAccountInfo([account, vaultAddress]);
const rewardInfo = accountInfo.accountRewardInfo;

// balanceTracker will be address(0) if no on-chain rewards configured
if (rewardInfo.balanceTracker !== zeroAddress) {
  console.log(`Balance Tracker: ${rewardInfo.balanceTracker}`);
  console.log(`Balance Forwarder Enabled: ${rewardInfo.balanceForwarderEnabled}`);
  console.log(`Tracked Balance: ${rewardInfo.balance}`);

  // Earned rewards (on-chain mechanism)
  for (const reward of rewardInfo.enabledRewardsInfo) {
    console.log(`\nReward Token: ${reward.reward}`);
    console.log(`  Earned: ${reward.earnedReward}`);
  }
} else {
  console.log('No on-chain rewards configured - check Merkl for off-chain rewards');
}
```

**Correct (using VaultLens for IRM curve data):**

```typescript
// Get interest rate model info with custom utilization points
const utilizationPoints = [
  { cash: 90n * 10n ** 18n, borrows: 10n * 10n ** 18n },   // 10% utilization
  { cash: 50n * 10n ** 18n, borrows: 50n * 10n ** 18n },   // 50% utilization
  { cash: 10n * 10n ** 18n, borrows: 90n * 10n ** 18n },   // 90% utilization
  { cash: 5n * 10n ** 18n, borrows: 95n * 10n ** 18n },    // 95% utilization
];

const cashArray = utilizationPoints.map(p => p.cash);
const borrowsArray = utilizationPoints.map(p => p.borrows);

const irmInfo = await vaultLens.read.getVaultInterestRateModelInfo([
  vaultAddress,
  cashArray,
  borrowsArray
]);

// Plot the interest rate curve
for (let i = 0; i < irmInfo.interestRateInfo.length; i++) {
  const info = irmInfo.interestRateInfo[i];
  const utilization = (info.borrows * 100n) / (info.cash + info.borrows);
  console.log(`${utilization}% util: Borrow APY=${info.borrowAPY}, Supply APY=${info.supplyAPY}`);
}

// For kink IRM, get standard curve points
const kinkIrmInfo = await vaultLens.read.getVaultKinkInterestRateModelInfo([vaultAddress]);
console.log(`IRM Type: ${kinkIrmInfo.interestRateModelInfo.interestRateModelType}`);
```

**Correct (using OracleLens for oracle validation):**

```typescript
import oracleLensABI from '@eulerxyz/euler-interfaces/abis/OracleLens.json';

const oracleLens = getContract({
  address: lens.oracleLens as Address,
  abi: oracleLensABI,
  client: publicClient
});

// Get oracle info for multiple base/quote pairs
const bases = [wethAddress, wbtcAddress, linkAddress];
const quotes = [usdAddress, usdAddress, usdAddress];

const oracleInfo = await oracleLens.read.getOracleInfo([
  routerAddress,
  bases,
  quotes
]);

console.log(`Oracle: ${oracleInfo.name}`);
console.log(`Oracle Address: ${oracleInfo.oracle}`);
// oracleInfo.oracleInfo contains encoded adapter-specific info
```

**Correct (using UtilsLens for calculations):**

```typescript
import utilsLensABI from '@eulerxyz/euler-interfaces/abis/UtilsLens.json';

const utilsLens = getContract({
  address: lens.utilsLens as Address,
  abi: utilsLensABI,
  client: publicClient
});

// Get APYs for a vault
const [borrowAPY, supplyAPY] = await utilsLens.read.getAPYs([vaultAddress]);
console.log(`Borrow APY: ${formatUnits(borrowAPY, 25)}%`);  // 1e27 scale
console.log(`Supply APY: ${formatUnits(supplyAPY, 25)}%`);

// Batch token balances
const tokens = [wethAddress, usdcAddress, daiAddress];
const balances = await utilsLens.read.tokenBalances([account, tokens]);
tokens.forEach((token, i) => {
  console.log(`${token}: ${balances[i]}`);
});

// Batch token allowances
const allowances = await utilsLens.read.tokenAllowances([
  spenderAddress,
  account,
  tokens
]);

// Get ERC4626 vault info (works for any 4626 vault)
const vaultInfo = await utilsLens.read.getVaultInfoERC4626([vaultAddress]);
console.log(`Is EVault: ${vaultInfo.isEVault}`);
console.log(`Share/Asset ratio: ${vaultInfo.totalAssets / vaultInfo.totalShares}`);

// Calculate time to liquidation
const ttl = await utilsLens.read.calculateTimeToLiquidation([
  liabilityVault,
  liabilityValue,
  collateralAddresses,
  collateralValues
]);
```

**Correct (using IRMLens for interest rate model details):**

```typescript
import irmLensABI from '@eulerxyz/euler-interfaces/abis/IRMLens.json';

const irmLens = getContract({
  address: lens.irmLens as Address,
  abi: irmLensABI,
  client: publicClient
});

// Get detailed IRM info including type and parameters
const irmInfo = await irmLens.read.getInterestRateModelInfo([irmAddress]);

console.log(`IRM Address: ${irmInfo.interestRateModel}`);
console.log(`IRM Type: ${irmInfo.interestRateModelType}`);
// Types: 0=UNKNOWN, 1=KINK, 2=ADAPTIVE_CURVE, 3=KINKY, 4=FIXED_CYCLICAL_BINARY

// Decode params based on type
if (irmInfo.interestRateModelType === 1) { // KINK
  const params = decodeAbiParameters(
    [{ type: 'tuple', components: [
      { name: 'baseRate', type: 'uint256' },
      { name: 'slope1', type: 'uint256' },
      { name: 'slope2', type: 'uint256' },
      { name: 'kink', type: 'uint256' }
    ]}],
    irmInfo.interestRateModelParams
  )[0];
  console.log(`Kink IRM: baseRate=${params.baseRate}, slope1=${params.slope1}, slope2=${params.slope2}, kink=${params.kink}`);
} else if (irmInfo.interestRateModelType === 2) { // ADAPTIVE_CURVE
  const params = decodeAbiParameters(
    [{ type: 'tuple', components: [
      { name: 'targetUtilization', type: 'int256' },
      { name: 'initialRateAtTarget', type: 'int256' },
      { name: 'minRateAtTarget', type: 'int256' },
      { name: 'maxRateAtTarget', type: 'int256' },
      { name: 'curveSteepness', type: 'int256' },
      { name: 'adjustmentSpeed', type: 'int256' }
    ]}],
    irmInfo.interestRateModelParams
  )[0];
  console.log(`Adaptive Curve IRM: target=${params.targetUtilization}`);
}
```

**Correct (using EulerEarnVaultLens for yield strategies):**

```typescript
import eulerEarnLensABI from '@eulerxyz/euler-interfaces/abis/EulerEarnVaultLens.json';

const eulerEarnLens = getContract({
  address: lens.eulerEarnVaultLens as Address,
  abi: eulerEarnLensABI,
  client: publicClient
});

// Get full EulerEarn vault info including strategies
const earnInfo = await eulerEarnLens.read.getVaultInfoFull([earnVaultAddress]);

console.log(`EulerEarn Vault: ${earnInfo.vaultName}`);
console.log(`Total Assets: ${earnInfo.totalAssets}`);
console.log(`Available (unallocated): ${earnInfo.availableAssets}`);
console.log(`Lost Assets: ${earnInfo.lostAssets}`);
console.log(`Performance Fee: ${earnInfo.performanceFee / 100}%`);
console.log(`Curator: ${earnInfo.curator}`);
console.log(`Guardian: ${earnInfo.guardian}`);
console.log(`Timelock: ${earnInfo.timelock} seconds`);

// Strategy breakdown
console.log(`\nStrategies (${earnInfo.strategies.length}):`);
for (const strategy of earnInfo.strategies) {
  console.log(`  ${strategy.strategy}:`);
  console.log(`    Allocated: ${strategy.allocatedAssets}`);
  console.log(`    Available: ${strategy.availableAssets}`);
  console.log(`    Cap: ${strategy.currentAllocationCap}`);
  console.log(`    Is EVault: ${strategy.info.isEVault}`);
}

// Get specific strategy info
const strategyInfo = await eulerEarnLens.read.getStrategyInfo([
  earnVaultAddress,
  strategyAddress
]);
```

**Important: Lens contracts are for off-chain queries only**

Lens contracts are optimized for convenience, not gas efficiency. They aggregate multiple calls and return large structs, which is expensive on-chain. For on-chain integrations, call vault methods directly:

```solidity
// DON'T use Lens on-chain - it's not gas efficient
// IAccountLens(lens).getAccountLiquidityInfo(account, vault); // Expensive!

// DO call vault methods directly for on-chain checks
(uint256 collateralValue, uint256 liabilityValue) = IEVault(vault).accountLiquidity(account, true);
bool isHealthy = collateralValue >= liabilityValue;
```

**Key Lens Functions Summary:**

| Lens | Function | Returns |
|------|----------|---------|
| AccountLens | `getAccountInfo(account, vault)` | Full account position + EVC state + rewards |
| AccountLens | `getAccountEnabledVaultsInfo(evc, account)` | Info for ALL enabled vaults |
| AccountLens | `getAccountLiquidityInfo(account, vault)` | Health, collateral values, TTL |
| AccountLens | `getAccountLiquidityInfoNoValidation(account, vault)` | Same as above, handles errors gracefully |
| AccountLens | `getTimeToLiquidation(account, vault)` | Seconds until liquidatable (int256) |
| AccountLens | `getEVCAccountInfo(evc, account)` | EVC state: controllers, collaterals, lockdown |
| AccountLens | `getVaultAccountInfo(account, vault)` | Position: shares, assets, borrowed, allowances |
| AccountLens | `getRewardAccountInfo(account, vault)` | On-chain reward tracking (legacy, limited adoption) |
| VaultLens | `getVaultInfoFull(vault)` | Complete vault config + state |
| VaultLens | `getVaultInfoDynamic(vault)` | Current state only |
| VaultLens | `getVaultInfoStatic(vault)` | Immutable config only |
| VaultLens | `getRecognizedCollateralsLTVInfo(vault)` | LTV for all collaterals |
| VaultLens | `getVaultKinkInterestRateModelInfo(vault)` | IRM curve data |
| OracleLens | `getOracleInfo(oracle, bases, quotes)` | Oracle configuration |
| OracleLens | `isStalePullOracle(oracle, reason)` | Check for stale Pyth/RedStone |
| IRMLens | `getInterestRateModelInfo(irm)` | IRM type + decoded parameters |
| UtilsLens | `getAPYs(vault)` | Current borrow/supply APY |
| UtilsLens | `tokenBalances(account, tokens)` | Batch balance query |
| EulerEarnLens | `getVaultInfoFull(vault)` | Earn vault with strategies |

Reference: [EVK Periphery Lens](https://github.com/euler-xyz/evk-periphery/tree/master/src/Lens)
