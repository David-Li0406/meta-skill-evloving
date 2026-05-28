# Euler IRM & Oracles Agent Skill

**Version 1.0.0**  
Euler Labs  
January 2026

> **Note:**  
> This document is for agents and LLMs to follow when working with  
> Euler Finance price oracles and Interest Rate Models. It covers deploying  
> adapters, configuring EulerRouter, querying prices, and understanding IRM types.

---

## Abstract

Oracle and Interest Rate Model guide for Euler Finance V2 protocol. Covers deploying oracle adapters (Chainlink, Pyth, Chronicle, RedStone, Pendle), configuring EulerRouter for price resolution, querying asset prices, and understanding IRM types (Linear Kink, Linear Kinky, Adaptive Curve, Fixed Cyclical Binary).

---

## Table of Contents

1. [Oracle Integration](#1-oracle-integration) — **HIGH**
   - 1.1 [Configure EulerRouter for Price Resolution](#11-configure-eulerrouter-for-price-resolution)
   - 1.2 [Deploy an Oracle Adapter](#12-deploy-an-oracle-adapter)
   - 1.3 [Get Asset Prices from Oracles](#13-get-asset-prices-from-oracles)
2. [Interest Rate Models](#2-interest-rate-models) — **HIGH**
   - 2.1 [Interest Rate Model Types and Configuration](#21-interest-rate-model-types-and-configuration)

---

## 1. Oracle Integration

**Impact: HIGH**

Oracle integration guide for Euler Finance V2 protocol. Covers deploying oracle adapters (Chainlink, Pyth, Chronicle, RedStone, Cross, Fixed Rate), configuring EulerRouter for price resolution, and querying asset prices. Essential for vault creation and price feed management.

### 1.1 Configure EulerRouter for Price Resolution

**Impact: HIGH (Central oracle routing for vault pricing)**

EulerRouter is the central price resolution contract that routes price queries to appropriate oracle adapters. It supports direct pricing and ERC-4626 vault share pricing via `convertToAssets`.

**Incorrect: hardcoding oracle in vault**

```solidity
// Don't hardcode individual oracles in vaults
// This makes upgrades and fixes impossible
IEVault(vault).setOracle(specificOracleAdapter);
// If oracle has issues, vault is stuck
```

**Correct: deploy and configure EulerRouter**

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

**Correct: understanding resolution - NO automatic cross-pricing**

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

**Correct: ERC-4626 vault share pricing**

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

**Example: Pricing sUSDS (ERC4626 vault for USDS) as collateral**

For yield-bearing tokens like sUSDS used as collateral in an Euler vault, you need to configure the full pricing chain:

**Correct: TypeScript router configuration**

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

**Correct: fallback configuration**

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

**Correct: querying existing configuration**

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

Reference: [https://github.com/euler-xyz/euler-price-oracle/blob/master/src/EulerRouter.sol](https://github.com/euler-xyz/euler-price-oracle/blob/master/src/EulerRouter.sol)

### 1.2 Deploy an Oracle Adapter

**Impact: HIGH (Required for vault pricing and risk management)**

Oracle adapters translate external price feeds into Euler's `IPriceOracle` interface. Each adapter is immutable and connects to a single price source.

**Incorrect: using Chainlink directly without adapter**

```solidity
// Chainlink returns (roundId, answer, startedAt, updatedAt, answeredInRound)
// This raw interface is incompatible with Euler's IPriceOracle
(, int256 answer,,,) = AggregatorV3Interface(feed).latestRoundData();
// Also missing staleness checks, decimal handling, etc.
```

**Correct: deploy ChainlinkOracle adapter**

```solidity
import {ChainlinkOracle} from "euler-price-oracle/adapter/chainlink/ChainlinkOracle.sol";

// Deploy adapter with configuration
ChainlinkOracle oracle = new ChainlinkOracle(
    base,           // Base token address (e.g., WETH)
    quote,          // Quote token address (e.g., USD reference)
    feed,           // Chainlink feed address
    maxStaleness    // Max age in seconds (e.g., 3600 for 1 hour)
);

// Adapter now implements IPriceOracle
// getQuote(inAmount, base, quote) returns outAmount
uint256 ethValueInUsd = oracle.getQuote(1e18, weth, usd);
```

**Correct: deploy PythOracle adapter**

```typescript
// TypeScript: Fetching Pyth price updates
async function getPythUpdateData(feedIds: string[]): Promise<string[]> {
  const response = await fetch(
    `https://hermes.pyth.network/api/latest_vaas?ids[]=${feedIds.join('&ids[]=')}`
  );
  const data = await response.json();
  return data.map((vaa: string) => `0x${vaa}`);
}

// Include price update in your transaction
const updateData = await getPythUpdateData([priceFeedId]);
const updateFee = await pythContract.read.getUpdateFee([updateData]);

// Option 1: Separate transaction
await pythContract.write.updatePriceFeeds(updateData, { value: updateFee });
await vault.write.deposit([amount, receiver]);

// Option 2: Batch via EVC (recommended)
const batchItems = [
  {
    targetContract: pythAddress,
    onBehalfOfAccount: zeroAddress,
    value: updateFee,
    data: encodeFunctionData({
      abi: pythABI,
      functionName: 'updatePriceFeeds',
      args: [updateData]
    })
  },
  {
    targetContract: vaultAddress,
    onBehalfOfAccount: account,
    value: 0n,
    data: encodeFunctionData({
      abi: evaultABI,
      functionName: 'borrow',
      args: [amount, receiver]
    })
  }
];
await evc.write.batch(batchItems, { value: updateFee });
```

**CRITICAL: Pyth Price Updates Required**

Pyth oracles are pull-based and **will revert if prices are stale**. You must update prices before any Euler operation that requires health checks (withdrawals, borrows, liquidations, etc.):

**Correct: deploy rate provider oracle for LSTs**

```solidity
import {LidoOracle} from "euler-price-oracle/adapter/lido/LidoOracle.sol";
import {RateProviderOracle} from "euler-price-oracle/adapter/rate/RateProviderOracle.sol";

// For wstETH/stETH - LidoOracle has no constructor (uses hardcoded addresses)
// Only works on mainnet with canonical STETH/WSTETH addresses
LidoOracle wstethOracle = new LidoOracle();
// Supports: STETH -> WSTETH and WSTETH -> STETH

// For other rate providers (e.g., Balancer)
RateProviderOracle rateOracle = new RateProviderOracle(
    base,              // e.g., rETH
    quote,             // e.g., ETH
    rateProvider       // Balancer rate provider address
);
```

**Correct: deploy ChronicleOracle adapter**

```solidity
import {ChronicleOracle} from "euler-price-oracle/adapter/chronicle/ChronicleOracle.sol";

// Chronicle is MakerDAO's oracle system
ChronicleOracle oracle = new ChronicleOracle(
    base,           // Base token address
    quote,          // Quote token address
    feed,           // Chronicle feed address (IChronicle)
    maxStaleness    // Max age in seconds
);

// Note: Chronicle feeds require whitelisting (kiss)
// The adapter address must be whitelisted on the Chronicle feed
// Contact Chronicle team for production whitelisting
```

**Correct: deploy FixedRateOracle for stablecoins**

```solidity
import {FixedRateOracle} from "euler-price-oracle/adapter/fixed/FixedRateOracle.sol";

// For stablecoins pegged 1:1 (e.g., USDC/USD, DAI/USD)
FixedRateOracle oracle = new FixedRateOracle(
    base,       // Base token (e.g., USDC)
    quote,      // Quote token (e.g., USD reference)
    rate        // Fixed rate in 18 decimals (1e18 for 1:1)
);

// Use for:
// - Stablecoin pairs (USDC/USDT at 1:1)
// - Wrapped tokens (WETH/ETH at 1:1)
// - Testing and development
```

**Correct: deploy CrossAdapter for chained pricing**

```solidity
import {CrossAdapter} from "euler-price-oracle/adapter/CrossAdapter.sol";

// CrossAdapter chains two oracles through an intermediate asset
// Constructor: (base, cross, quote, oracleBaseCross, oracleCrossQuote)
// Note: Both cross oracles MUST be bidirectional. Does not support bid/ask pricing.

// Example: LINK/USD via LINK/ETH and ETH/USD
CrossAdapter linkUsdOracle = new CrossAdapter(
    link,                      // base: the asset to price
    weth,                      // cross: intermediate asset
    usd,                       // quote: unit of account
    linkEthChainlinkOracle,    // oracleBaseCross: LINK/ETH (must be bidirectional)
    ethUsdChainlinkOracle      // oracleCrossQuote: ETH/USD (must be bidirectional)
);

// Price flow: LINK -> ETH (via oracleBaseCross) -> USD (via oracleCrossQuote)
// Useful for tokens that only have ETH pairs but vault needs USD pricing
```

**Correct: deploy PendleOracle for yield-bearing tokens**

```solidity
import {PendleOracle} from "euler-price-oracle/adapter/pendle/PendleOracle.sol";

// For Pendle PT (principal tokens) as collateral
// Constructor: (pendleOracle, pendleMarket, base, quote, twapWindow)
PendleOracle oracle = new PendleOracle(
    pendlePYOracle,    // Pendle PY oracle address (IPPYLpOracle)
    pendleMarket,      // Pendle market address
    ptToken,           // base: PT token address
    underlyingToken,   // quote: underlying asset
    twapWindow         // TWAP window: 900-1800 seconds recommended (uint32)
);

// IMPORTANT: Pendle market must be initialized before deployment
// The constructor verifies observations buffer is ready
// Uses PendlePYOracleLib for TWAP pricing
```

**Verification after deployment:**

```solidity
// Verify adapter works correctly
uint256 quoteAmount = oracle.getQuote(1e18, base, quote);
console.log("1 base =", quoteAmount, "quote");

// Check both directions work
uint256 reverseQuote = oracle.getQuote(quoteAmount, quote, base);
// Should be approximately 1e18 (within precision)

// For bid/ask oracles
(uint256 bidOut, uint256 askOut) = oracle.getQuotes(1e18, base, quote);
console.log("Bid:", bidOut, "Ask:", askOut);
```

Reference: [https://github.com/euler-xyz/euler-price-oracle#oracle-adapters](https://github.com/euler-xyz/euler-price-oracle#oracle-adapters)

### 1.3 Get Asset Prices from Oracles

**Impact: HIGH (Essential for value calculations and risk assessment)**

Querying prices is fundamental for calculating position values, health factors, and making trading decisions. Euler oracles use a quote-based interface that returns amounts rather than unit prices.

**Incorrect: assuming unit price response**

```solidity
// Wrong: Oracles don't return "price per token"
uint256 price = oracle.getPrice(token);
uint256 value = tokenAmount * price;
// getPrice() doesn't exist in IPriceOracle!
```

**Correct: using getQuote for amount conversion**

```solidity
import {IPriceOracle} from "euler-price-oracle/interfaces/IPriceOracle.sol";

// IPriceOracle.getQuote: "How much quote do I get for inAmount of base?"
// This is like asking "How much USD is 1 ETH worth?"

// Get value of 1 ETH in USD
uint256 ethInUsd = IPriceOracle(oracle).getQuote(
    1e18,      // inAmount: 1 ETH (18 decimals)
    weth,      // base: the token you have
    usd        // quote: the token you want value in
);
// Returns: 2000e18 (if ETH = $2000)

// Get value of 0.5 BTC in ETH
uint256 btcInEth = IPriceOracle(oracle).getQuote(
    0.5e8,     // inAmount: 0.5 BTC (8 decimals)  
    wbtc,      // base: BTC
    weth       // quote: ETH
);
// Returns: 15e18 (if 0.5 BTC = 15 ETH)
```

**Correct: using OracleLens for comprehensive data**

```typescript
import { OracleLens } from '@eulerxyz/evk-periphery';

// OracleLens provides rich oracle information
const oracleInfo = await oracleLens.getOracleInfo(
  oracleAddress,
  [weth, wbtc, link],  // base tokens
  [usd, usd, usd]       // quote tokens
);

// Access individual prices
oracleInfo.prices.forEach((priceInfo, i) => {
  console.log(`${bases[i]}: ${priceInfo.quote} ${quotes[i]}`);
  console.log(`  Oracle: ${priceInfo.oracle}`);
  console.log(`  Success: ${priceInfo.success}`);
});
```

**Correct: bid/ask pricing for spreads**

```solidity
// getQuotes returns both bid and ask prices
// Useful for more accurate risk calculations
(uint256 bidOut, uint256 askOut) = IPriceOracle(oracle).getQuotes(
    1e18,
    weth,
    usd
);

// bidOut: What you'd get if SELLING 1 ETH (lower)
// askOut: What you'd pay to BUY 1 ETH (higher)
// Spread = askOut - bidOut

// For lending, use bid (selling collateral)
// For borrowing, use ask (buying debt)
uint256 collateralValue = (collateralAmount * bidOut) / 1e18;
uint256 debtValue = (debtAmount * askOut) / 1e18;
```

Key points:

- `getQuote` converts amounts, not returns unit prices

- Decimals are handled internally by adapters

- **Pyth oracles require price updates before any operation that uses them**

Reference: [https://github.com/euler-xyz/euler-price-oracle#iprice oracle](https://github.com/euler-xyz/euler-price-oracle#iprice oracle)

---

## 2. Interest Rate Models

**Impact: HIGH**

Available Interest Rate Models and their configuration. Euler supports multiple IRM types (Linear Kink, Kinky, Adaptive Curve, Fixed Cyclical Binary) each suited for different use cases and risk profiles.

### 2.1 Interest Rate Model Types and Configuration

**Impact: HIGH (Critical for selecting and configuring appropriate interest rates)**

Euler V2 supports multiple Interest Rate Model (IRM) types, each suited for different market dynamics and risk profiles. Governors can also bring their own custom IRM as long as it conforms to the `IIRM` interface, though custom IRMs may not be supported by the Euler UI.

**Incorrect: misconfigured IRM parameters**

```solidity
// WRONG: Poorly configured IRM parameters
// This can lead to suboptimal utilization and poor lender returns
address irm = kinkIRMFactory.deploy(
    0,           // baseRate
    4e27,        // slope1: way too high - discourages borrowing
    300e27,      // slope2: extreme spike after kink
    3865470566   // kink: 90%
);
// Result: rates too high → low utilization → poor capital efficiency
```

**Correct: choosing appropriate IRM type**

```solidity
import {EulerFixedCyclicalBinaryIRMFactory} from "evk-periphery/IRMFactory/EulerFixedCyclicalBinaryIRMFactory.sol";

// Useful for synthetic assets or special vault types
address cyclicalIRM = EulerFixedCyclicalBinaryIRMFactory(factory).deploy(
    1e27,         // primaryRate: 100% SPY during primary phase
    0,            // secondaryRate: 0% during secondary phase
    7 days,       // primaryDuration: 1 week at primary rate
    7 days,       // secondaryDuration: 1 week at secondary rate
    block.timestamp  // startTimestamp: when first cycle begins
);
```

Traditional two-slope model. Rate increases linearly up to kink, then accelerates.

Use the helper script to calculate parameters from human-readable APY values:

See: [calculate-irm-linear-kink.js](https://github.com/euler-xyz/evk-periphery/blob/development/script/utils/calculate-irm-linear-kink.js)

Self-adjusting model that targets specific utilization. Rate at target adjusts based on time spent above/below target.

Use the helper script to calculate parameters from human-readable APY values:

See: [calculate-irm-adaptive-curve.js](https://github.com/euler-xyz/evk-periphery/blob/development/script/utils/calculate-irm-adaptive-curve.js)

Similar to kink IRM but with non-linear acceleration after kink using shape parameter.

Alternates between two fixed rates on a schedule. Useful for special mechanisms.

Reference: [https://github.com/euler-xyz/evk-periphery/tree/master/src/IRM](https://github.com/euler-xyz/evk-periphery/tree/master/src/IRM)

---

## References

1. [https://docs.euler.finance](https://docs.euler.finance)
2. [https://github.com/euler-xyz/euler-price-oracle](https://github.com/euler-xyz/euler-price-oracle)
3. [https://github.com/euler-xyz/evk-periphery](https://github.com/euler-xyz/evk-periphery)
