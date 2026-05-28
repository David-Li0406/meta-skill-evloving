---
title: Configure EulerRouter for Price Resolution
impact: HIGH
impactDescription: Central oracle routing for vault pricing
tags: oracle, router, configuration, governance
---

## Configure EulerRouter for Price Resolution

EulerRouter is the central price resolution contract that routes price queries to appropriate oracle adapters. It supports direct pricing and ERC-4626 vault share pricing via `convertToAssets`.

**Incorrect (hardcoding oracle in vault):**

```solidity
// Don't hardcode individual oracles in vaults
// This makes upgrades and fixes impossible
IEVault(vault).setOracle(specificOracleAdapter);
// If oracle has issues, vault is stuck
```

**Correct (deploy and configure EulerRouter):**

```solidity
import {EulerRouter} from "euler-price-oracle/EulerRouter.sol";
import {EulerRouterFactory} from "evk-periphery/EulerRouterFactory/EulerRouterFactory.sol";

// Deploy router via factory
// Note: Factory was initialized with EVC address in its constructor
address router = EulerRouterFactory(factory).deploy(governor);

// Configure pricing for asset pairs
EulerRouter eulerRouter = EulerRouter(router);

// Set direct oracle for ETH/USD
// Note: Assets are lexicographically sorted internally
eulerRouter.govSetConfig(
    weth,                    // Base asset
    usd,                     // Quote asset  
    chainlinkEthUsdOracle    // Oracle adapter address
);

// Set direct oracle for BTC/USD
eulerRouter.govSetConfig(
    wbtc,
    usd,
    chainlinkBtcUsdOracle
);
```

**Correct (understanding resolution - NO automatic cross-pricing):**

```solidity
// IMPORTANT: EulerRouter does NOT automatically chain oracles!
// For TOKEN/USD pricing, you must EITHER:
// 1. Configure a direct TOKEN/USD oracle, OR
// 2. Use a CrossAdapter that handles the cross-pricing internally

// Resolution order in resolveOracle():
// 1. base == quote? Return inAmount (same asset)
// 2. Direct oracle configured for base/quote? Use it
// 3. Base is a resolved ERC4626 vault? Convert via convertToAssets, recurse
// 4. Fallback oracle set? Use it
// 5. Revert with PriceOracle_NotSupported

// Example: If you need TOKEN/USD via TOKEN/ETH and ETH/USD,
// use a CrossAdapter, not multiple govSetConfig calls
import {CrossAdapter} from "euler-price-oracle/adapter/CrossAdapter.sol";

// Deploy cross adapter that chains TOKEN/ETH -> ETH/USD
// Constructor: (base, cross, quote, oracleBaseCross, oracleCrossQuote)
// Note: Both cross oracles MUST be bidirectional. Does not support bid/ask pricing.
CrossAdapter crossAdapter = new CrossAdapter(
    tokenAddress,     // base: the asset you want to price
    weth,             // cross: intermediate asset (e.g., WETH)
    usd,              // quote: the unit of account
    tokenEthOracle,   // oracleBaseCross: TOKEN/ETH oracle (must be bidirectional)
    ethUsdOracle      // oracleCrossQuote: ETH/USD oracle (must be bidirectional)
);

// Configure router with the cross adapter
eulerRouter.govSetConfig(tokenAddress, usd, crossAdapter);
```

**Correct (ERC-4626 vault share pricing):**

```solidity
// For pricing vault shares in terms of underlying
// Router uses convertToAssets() for automatic share->asset conversion

// Configure underlying asset pricing first
eulerRouter.govSetConfig(
    underlyingAsset,
    usd,
    underlyingOracle
);

// Enable vault share resolution
// Router will call vault.convertToAssets() and recurse
eulerRouter.govSetResolvedVault(
    vaultAddress,
    true  // Enable automatic share->asset conversion
);

// To disable later:
eulerRouter.govSetResolvedVault(vaultAddress, false);

// Now queries for vault shares work:
// vaultShares -> convertToAssets -> underlying -> USD
uint256 shareValueUsd = eulerRouter.getQuote(1e18, vaultAddress, usd);

// IMPORTANT: Verify vault's convertToAssets is secure before configuring!
// Per ERC4626 spec, convert* ignores liquidity, fees, slippage
// The reported price may not be realizable through redeem/withdraw
```

**Example: Pricing sUSDS (ERC4626 vault for USDS) as collateral**

For yield-bearing tokens like sUSDS used as collateral in an Euler vault, you need to configure the full pricing chain:

```solidity
// sUSDS is an ERC4626 vault wrapping USDS
// To use sUSDS as collateral and price the Euler vault shares, the router needs:
// 1. USDS/USD pricing (the base asset)
// 2. sUSDS registered as a resolved vault (for pricing sUSDS)
// 3. The Euler vault registered as a resolved vault (for pricing vault shares)

// Step 1: Configure USDS/USD pricing
eulerRouter.govSetConfig(
    usds,                  // base: USDS token
    usd,                   // quote: USD reference
    usdsUsdOracle          // oracle: e.g., Chainlink USDS/USD feed
);

// Step 2: Register sUSDS as a resolved vault
// This allows pricing sUSDS collateral via convertToAssets → USDS → USD
eulerRouter.govSetResolvedVault(
    susds,                 // sUSDS vault address
    true                   // enable resolution
);

// Step 3: Register the Euler vault as a resolved vault
// This allows pricing the Euler vault's shares (e.g., for use as collateral elsewhere)
eulerRouter.govSetResolvedVault(
    eulerVaultSUSDS,       // Euler vault that accepts sUSDS deposits
    true                   // enable resolution
);

// Now the router can price at each level:

// Price sUSDS directly:
// Query: getQuote(1e18, sUSDS, USD)
// Path: sUSDS → convertToAssets → USDS → USDS/USD oracle → USD
uint256 susdsValueInUsd = eulerRouter.getQuote(1e18, susds, usd);

// Price Euler vault shares:
// Query: getQuote(1e18, eulerVaultSUSDS, USD)
// Path: eVault → convertToAssets → sUSDS → convertToAssets → USDS → USD
uint256 eVaultShareValueInUsd = eulerRouter.getQuote(1e18, eulerVaultSUSDS, usd);
```

**Correct (TypeScript router configuration):**

```typescript
import { encodeFunctionData, getContract } from 'viem';

const eulerRouter = getContract({
  address: routerAddress,
  abi: eulerRouterABI,
  client: walletClient
});

// Configure oracle for asset pair
// Note: gov functions require being called by governor via EVC context
await eulerRouter.write.govSetConfig([
  wethAddress,        // base
  usdAddress,         // quote  
  chainlinkOracle     // oracle adapter
]);

// Configure resolved vault for share pricing
await eulerRouter.write.govSetResolvedVault([
  vaultAddress,
  true  // set = true to enable, false to disable
]);

// Query prices
const quote = await eulerRouter.read.getQuote([
  parseEther('1'),    // inAmount
  wethAddress,        // base
  usdAddress          // quote
]);

// Get bid/ask quotes
const [bid, ask] = await eulerRouter.read.getQuotes([
  parseEther('1'),
  wethAddress,
  usdAddress
]);

// Check configured oracle for a pair
const oracle = await eulerRouter.read.getConfiguredOracle([
  wethAddress,
  usdAddress
]);
```

**Correct (fallback configuration):**

```solidity
// Set fallback oracle for pairs without direct config
// Called when no direct oracle AND base is not a resolved vault
eulerRouter.govSetFallbackOracle(fallbackOracleAddress);

// To remove fallback:
eulerRouter.govSetFallbackOracle(address(0));

// Resolution order:
// 1. base == quote → return inAmount
// 2. Direct config for base/quote → use configured oracle
// 3. Base is resolved vault → convertToAssets, recurse with asset
// 4. Fallback oracle exists → use fallback
// 5. No fallback → revert PriceOracle_NotSupported(base, quote)
```

**Correct (querying existing configuration):**

```solidity
// Get configured oracle for a pair
// Returns address(0) if not configured
address oracle = eulerRouter.getConfiguredOracle(base, quote);

// Check if vault is configured for resolved pricing
address asset = eulerRouter.resolvedVaults(vaultAddress);
bool isResolved = asset != address(0);

// Get current fallback oracle
address fallback = eulerRouter.fallbackOracle();

// Simulate full resolution path
(uint256 resolvedAmount, address resolvedBase, address resolvedQuote, address resolvedOracle) = 
    eulerRouter.resolveOracle(inAmount, base, quote);
```

**Important considerations:**

```solidity
// Gov functions have onlyEVCAccountOwner and onlyGovernor modifiers
// Must be called by governor, typically via EVC context

// Finalize router to make immutable (optional)
eulerRouter.transferGovernance(address(0));
// WARNING: No more configuration changes possible after this!

// For upgradeable setups, use a timelock or multisig as governor
// This allows fixing oracle issues without vault redeployment

// Assets are lexicographically sorted internally in the mapping
// govSetConfig(A, B, oracle) and govSetConfig(B, A, oracle) 
// configure the same pair - order doesn't matter for callers
```

Reference: [EulerRouter Source](https://github.com/euler-xyz/euler-price-oracle/blob/master/src/EulerRouter.sol)
