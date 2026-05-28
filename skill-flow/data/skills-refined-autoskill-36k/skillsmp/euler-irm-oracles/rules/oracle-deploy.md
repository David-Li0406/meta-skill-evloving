---
title: Deploy an Oracle Adapter
impact: HIGH
impactDescription: Required for vault pricing and risk management
tags: oracle, deploy, chainlink, pyth, chronicle, redstone, adapter
---

## Deploy an Oracle Adapter

Oracle adapters translate external price feeds into Euler's `IPriceOracle` interface. Each adapter is immutable and connects to a single price source.

**Incorrect (using Chainlink directly without adapter):**

```solidity
// Chainlink returns (roundId, answer, startedAt, updatedAt, answeredInRound)
// This raw interface is incompatible with Euler's IPriceOracle
(, int256 answer,,,) = AggregatorV3Interface(feed).latestRoundData();
// Also missing staleness checks, decimal handling, etc.
```

**Correct (deploy ChainlinkOracle adapter):**

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

**Correct (deploy PythOracle adapter):**

```solidity
import {PythOracle} from "euler-price-oracle/adapter/pyth/PythOracle.sol";

// Pyth is a pull-based oracle - requires price updates
PythOracle oracle = new PythOracle(
    pythContract,         // Pyth contract address
    base,                 // Base token
    quote,                // Quote token
    feedId,               // Pyth price feed ID (bytes32)
    maxStaleness,         // Max staleness in seconds
    maxConfidenceInterval // Max confidence width (e.g., 0.01e18 for 1%)
);
```

**CRITICAL: Pyth Price Updates Required**

Pyth oracles are pull-based and **will revert if prices are stale**. You must update prices before any Euler operation that requires health checks (withdrawals, borrows, liquidations, etc.):

```solidity
import {IPyth} from "@pythnetwork/pyth-sdk-solidity/IPyth.sol";

// Step 1: Get update data off-chain (from Pyth Hermes API)
// https://hermes.pyth.network/docs/

// Step 2: Update price on-chain before your operation
bytes[] memory updateData = getUpdateDataFromHermes(feedId);
uint256 updateFee = pyth.getUpdateFee(updateData);
pyth.updatePriceFeeds{value: updateFee}(updateData);

// Step 3: Now Euler operations that need oracle will work
// Note: deposits don't require oracle, but withdrawals/borrows do
vault.withdraw(amount, receiver, owner); // Oracle query succeeds
```

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

**Correct (deploy rate provider oracle for LSTs):**

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

**Correct (deploy ChronicleOracle adapter):**

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

**Correct (deploy FixedRateOracle for stablecoins):**

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

**Correct (deploy CrossAdapter for chained pricing):**

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

**Correct (deploy PendleOracle for yield-bearing tokens):**

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

Reference: [Euler Price Oracle Adapters](https://github.com/euler-xyz/euler-price-oracle#oracle-adapters)
