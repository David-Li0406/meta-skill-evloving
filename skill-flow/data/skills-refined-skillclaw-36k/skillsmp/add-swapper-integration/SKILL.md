---
name: add-swapper-integration
description: Guide for adding new DEX/swapper integrations to the ShapeShift Revenue Dashboard. Covers research, API investigation, implementation patterns, and frontend integration.
---

# Add Swapper Integration Skill

This skill guides you through adding a new swapper/DEX integration to the ShapeShift Revenue Dashboard.

## Overview

The revenue dashboard tracks affiliate fees from various DEX providers. Each integration collects fee data for a specific swapper and returns it in a standardized format. The main app charges a flat **55 BPS** (0.55%) fee on all swaps.

## Phase 1: Research & Discovery

**Your first task is to understand how ShapeShift integrates with this swapper, then research available data sources.**

### Research Checklist

#### Step 0: Investigate ShapeShift Implementation (REQUIRED FIRST!)

**Before researching APIs, you MUST understand how ShapeShift tracks affiliates for this swapper.**

**Location:** `/home/sean/Repos/shapeshift/packages/swapper/src/swappers/[SwapperName]Swapper/`

**Files to investigate:**
1. **Main swapper file:** `[SwapperName]Swapper.ts`
2. **Quote generation:** `getTradeQuote/get[SwapperName]TradeQuote.ts`
3. **Endpoints:** `endpoints.ts`
4. **Utils:** `utils/*.ts`

**What to find:**
- ✅ **Affiliate identifier** - What does ShapeShift use to identify itself?
  - Affiliate code/ID (e.g., "shapeshift", "ss-partner-123")
  - Referrer parameter (e.g., `referrer=`, `source=`, `affiliate=`)
  - Treasury/fee collection address (e.g., `0x123...`)
  - Broker ID (e.g., Chainflip uses broker ID)
- ✅ **How it's configured** - Look for:
  - Hardcoded values in code
  - Environment variables
  - Constants in `utils/constants.ts` or `endpoints.ts`
- ✅ **Fee structure** - Understand:
  - Does the swapper collect fees for us?
  - Do we specify a fee recipient address?
  - Is there a fee BPS we configure?

**Search patterns to use:**
```typescript
// In /home/sean/Repos/shapeshift/packages/swapper/src/swappers/[SwapperName]Swapper/
grep -r "affiliate" .
grep -r "referrer" .
grep -r "treasury" .
grep -r "fee.*recipient" .
grep -r "source" . | grep -i param
grep -r "SHAPESHIFT" .
```

**Example findings from existing integrations:**

<details>
<summary>THORChain/Maya - Treasury Address</summary>

Location: `swappers/ThorchainSwapper/utils/constants.ts`
```typescript
export const DEFAULT_AFFILIATE_FEE_BPS = '55'
export const DAO_TREASURY_THORCHAIN = 'thor1xmaggkcln5m5fnha2780xrdrulmplvfrz6wj3l'
```
→ **Conclusion:** THORChain swaps specify a treasury address to receive fees
</details>

<details>
<summary>ZRX (0x) - API Key</summary>

Location: `swappers/ZrxSwapper/endpoints.ts`
```typescript
'0x-api-key': getConfig().VITE_ZRX_API_KEY
```
→ **Conclusion:** 0x uses an API key that identifies ShapeShift as the integrator
</details>

<details>
<summary>Relay - Referrer Parameter</summary>

Location: `swappers/RelaySwapper/getTradeQuote.ts`
```typescript
referrer: '0xSHAPESHIFT_ADDRESS'
```
→ **Conclusion:** Relay uses a referrer address parameter
</details>

<details>
<summary>Chainflip - Broker ID</summary>

Location: `swappers/ChainflipSwapper/utils/constants.ts`
```typescript
export const CHAINFLIP_BROKER_ID = 'shapeshift'
```
→ **Conclusion:** Chainflip uses a broker ID string
</details>

**Output from Step 0:**

Document your findings before proceeding:

```markdown
## ShapeShift Integration Analysis for [Swapper Name]

**Affiliate Identifier Type:** [Treasury Address / API Key / Referrer Param / Broker ID / Other]

**Identifier Value:** [The actual value used, e.g., "thor1x..." or "shapeshift"]

**Location in Code:** [File path and line number]

**How It's Used:** [Brief description of how the identifier is passed to the swapper]

**Fee Configuration:** [Any fee BPS or parameters configured]

**Key Code Snippet:**
```typescript
// Paste relevant code here
```

**Conclusion:** [How this affects our revenue tracking approach]
```

---

#### Step 1: Explore Available APIs
   - Search for official API documentation
   - Look for affiliate/partner APIs
   - Check for transaction/trade history APIs
   - Look for analytics or reporting APIs
   - Check if there's a GraphQL endpoint
   - **Use the affiliate identifier from Step 0 to test filtering!**

   **⚠️ CRITICAL - API Cost Requirements:**
   - ✅ **MUST be completely FREE** with no time limits
   - ❌ **NO paid APIs**
   - ❌ **NO time-limited free trials** (e.g., "14-day free trial then $99/month")
   - ✅ Free tier with reasonable rate limits is acceptable
   - ✅ Free tier that requires API key but no payment is acceptable
   - If no free API exists, proceed to on-chain analysis (Step 3)

#### Step 2: Identify Data Availability
   For each API you find, determine:
   - ✅ Can filter by affiliate/referrer ID? **Use the identifier from Step 0!**
   - ✅ Can filter by time range (start/end timestamps or dates)?
   - ✅ What fee data is available?
     - Direct fee amounts in crypto?
     - Fee amounts in USD?
     - Volume data we can calculate fees from?
   - ✅ What format is the data in?
     - **Decimal format** (e.g., "2.5" USDC, "0.001" ETH)?
     - **Base units** (e.g., "2500000" wei USDC, "1000000000000000" wei ETH)?
   - ✅ Pagination support?
   - ✅ Rate limits?
   - ✅ Requires API key?

   **⚠️ CRITICAL - Performance Requirements:**
   - ✅ **Must retrieve 30 days of data in under 15 seconds**
   - ✅ **Batch queries preferred** (get all fees for date range in one/few calls)
   - ❌ **Avoid per-transaction queries** (if 100 txs = 100 API calls, too slow!)
   - ✅ Pagination is acceptable if page size is reasonable (e.g., 100-1000 items per page)
   - ✅ GraphQL batch queries are good
   - ❌ REST endpoints requiring one call per tx/day are problematic

   **Performance Estimation:**
   - You don't need to fetch full 30 days - estimate based on test queries
   - Assume 50-200 transactions over 30 days (typical volume)
   - Test a small query and calculate: `estimated_time = (api_response_time × number_of_calls_needed)`
   - Examples:
     - ✅ Single API call for date range = 1 second → **GOOD**
     - ✅ Paginated (5 pages @ 200ms each) = 1 second → **GOOD**
     - ❌ Per-transaction API (150 txs @ 100ms each) = 15 seconds → **BORDERLINE/BAD**
     - ❌ Per-day + per-transaction lookups (30 days × 5 txs × 200ms) = 30 seconds → **TOO SLOW**
   - Mark slow approaches as a major drawback in your research summary

#### Step 3: On-Chain Analysis (if no suitable API)
   If no good API exists, investigate on-chain options:
   - Use the **treasury address from Step 0** (if applicable)
   - What contracts send fees to this address?
   - Are there events/logs we can filter?
   - Can we use block explorers (Etherscan, Blockscout)?
   - What transaction data is available?

   **RPC Providers:**
   - ✅ **Check `/home/sean/Repos/shapeshift/.env` for RPC proxies**
   - ShapeShift has private RPC endpoints configured for most chains
   - These are **faster and more reliable** than public RPCs
   - Look for env vars like `VITE_ETHEREUM_NODE_URL`, `VITE_POLYGON_NODE_URL`, etc.
   - If available for your target chain, prefer these over public RPCs

#### Step 4: Test Your Findings
   - Make sample API requests **using the affiliate identifier from Step 0**
   - Verify data structure matches documentation
   - Test filtering by date range
   - Confirm fee data accuracy
   - Check if crypto amounts AND/OR USD values are provided
   - **CRITICAL: Test if amounts are in decimal or base units!**

### Integration Approaches (Ranked by Preference)

After research, you should determine which approach fits best:

#### **Approach 1: Direct Revenue/Fee API** ⭐⭐⭐⭐⭐
**Examples:** THORChain, Maya Protocol

**Characteristics:**
- Dedicated affiliate fee endpoint
- Returns raw crypto amounts (usually in base units)
- Clean, purpose-built API
- Easy time filtering

**Strengths:**
- Most accurate
- Easiest to implement
- **Best performance** - single/few API calls for entire date range
- Direct fee data

**Performance:** ⚡⚡⚡ Excellent (typically <2 seconds for 30 days)

**USD Enrichment:** ✅ **Use `enrichFeesWithUsdPrices()`**
- Integration returns crypto `amount` only
- Enrichment calculates USD value using **CURRENT** prices
- Most accurate revenue tracking

**Amount Format:** Usually base units (no conversion needed)

**Example Structure:**
```typescript
// API returns: { fees: [{ amount: "123456789", txId: "...", timestamp: 1234567890 }] }
const fees = data.fees.map(fee => ({
  chainId: 'cosmos:thorchain-1',
  assetId: 'cosmos:thorchain-1/slip44:931',
  service: 'swappername',
  txHash: fee.txId,
  timestamp: fee.timestamp,
  amount: fee.amount, // Already in base units (smallest denomination)
  // No amountUsd - let enrichment handle it
}))
return enrichFeesWithUsdPrices(fees)
```

---

#### **Approach 2: Transaction API with Fee Calculation** ⭐⭐⭐⭐
**Examples:** Bebop, 0x (ZRX)

**Characteristics:**
- Trade/transaction history API
- May include fee BPS or calculated fees
- Sometimes provides historical USD values
- Can filter by affiliate/source
- **Often returns amounts in DECIMAL format** (needs conversion)

**Strengths:**
- Good data availability
- Usually has volume data
- Can verify fee calculations
- **Good performance** - batch queries with pagination

**Drawbacks:**
- May need to calculate fees ourselves (volume * BPS)
- Historical USD values (if provided) are less accurate
- **Requires decimal-to-base-unit conversion**

**Performance:** ⚡⚡⚡ Excellent (typically <3 seconds for 30 days with pagination)

**USD Enrichment:** ✅ **Use `enrichFeesWithUsdPrices()`**
- Integration returns crypto `amount` (primary)
- May optionally include `amountUsd` (historical) as backup
- Enrichment recalculates using **CURRENT** prices
- If enrichment fails, falls back to historical `amountUsd`

**Amount Format:** ⚠️ **Usually DECIMAL - requires conversion**

**Example Structure:**
```typescript
// API returns: { trades: [{ volume: 1000, partnerFeeBps: 55, partnerFeeNative: "2.5", token: "0x...", ... }] }

for (const trade of data.trades) {
  const chainId = `eip155:${trade.chainId}`
  const assetId = `${chainId}/erc20:${trade.token}`

  // ⚠️ CRITICAL: API returns DECIMAL amount ("2.5" USDC)
  // Must convert to base units (wei): "2.5" → "2500000" (for 6 decimals)
  const decimals = await assetDataService.getAssetDecimals(assetId)
  const amountInWei = decimalToBaseUnit(trade.partnerFeeNative, decimals)

  fees.push({
    chainId,
    assetId,
    service: 'swappername',
    txHash: trade.txHash,
    timestamp: trade.timestamp,
    amount: amountInWei, // Now in base units (wei)
    amountUsd: trade.volumeUsd ? String(trade.volumeUsd * (trade.partnerFeeBps / 10000)) : undefined,
  })
}

return enrichFeesWithUsdPrices(fees)
```

---

#### **Approach 3: API with Current USD Pricing** ⭐⭐⭐⭐
**Examples:** Relay

**Characteristics:**
- API already calculates USD using current/live prices
- Returns `amountUsdCurrent` (not historical)
- Also includes crypto amounts (may be decimal or base units)

**Strengths:**
- USD values already accurate
- No need for price enrichment
- Reduces API calls
- **Good performance** - batch queries

**Drawbacks:**
- Must verify API actually uses current prices (not historical)
- Less common pattern
- May still need decimal conversion for amounts

**Performance:** ⚡⚡⚡ Excellent (typically <3 seconds for 30 days)

**USD Enrichment:** ❌ **Do NOT use `enrichFeesWithUsdPrices()`**
- Integration returns both `amount` AND `amountUsd`
- The `amountUsd` is already using **CURRENT** prices from their API
- Return fees as-is without enrichment

**Amount Format:** Check API - may need conversion

**Example Structure:**
```typescript
// API returns: { fees: [{ amount: "123456789", amountUsdCurrent: "100.50", ... }] }
const fees = data.fees.map(fee => ({
  chainId: config.chainId,
  assetId: buildAssetId(...),
  service: 'swappername',
  txHash: fee.txHash,
  timestamp: fee.timestamp,
  amount: fee.amount, // Check if in base units or decimal!
  amountUsd: fee.amountUsdCurrent, // Already using current prices
}))
return fees // No enrichment!
```

**⚠️ CRITICAL:** You must **TEST** the API to confirm:
1. It provides current USD values (not historical)
2. The amount format (decimal vs base units)

---

#### **Approach 4: USD-Only Data** ⭐⭐⭐
**Examples:** Chainflip

**Characteristics:**
- API only provides USD values
- No crypto amount available
- Must reverse-engineer crypto amount (for stablecoins, use 1:1 ratio)

**Strengths:**
- Simple USD tracking
- Works when crypto amounts unavailable
- **Good performance** - batch queries

**Drawbacks:**
- Less accurate (historical USD values)
- Can't verify with on-chain data
- Loses native token information

**Performance:** ⚡⚡⚡ Excellent (typically <3 seconds for 30 days)

**USD Enrichment:** ❌ **Do NOT use `enrichFeesWithUsdPrices()`**
- Integration returns synthesized `amount` (calculated from USD) AND `amountUsd`
- The `amountUsd` is historical (from when swap occurred)
- No enrichment possible - we don't have real crypto amounts

**Amount Format:** Synthesized in base units

**Example Structure:**
```typescript
// API returns: { swaps: [{ affiliateFeeValueUsd: "10.50", ... }] }
// Chainflip only provides USD - must synthesize crypto amount

const fees = data.swaps.map(swap => {
  // Synthesize USDC amount from USD value (1:1 ratio for stablecoins)
  // $10.50 USD = 10.50 USDC = 10,500,000 wei (6 decimals)
  const usdValue = swap.affiliateFeeValueUsd
  const usdcDecimals = 6
  const usdcWei = decimalToBaseUnit(usdValue, usdcDecimals)

  return {
    chainId: 'eip155:1',
    assetId: 'eip155:1/erc20:0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', // USDC
    service: 'swappername',
    txHash: '',
    timestamp: swap.timestamp,
    amount: usdcWei, // Synthesized from USD
    amountUsd: usdValue, // Historical USD value
  }
})

return fees // No enrichment - we don't have real amounts
```

---

#### **Approach 5: On-Chain Analysis** ⭐⭐
**Examples:** Portals

**Characteristics:**
- No suitable API available
- Scrape blockchain explorers for events/logs
- Filter transfers to treasury address
- Complex event decoding

**Strengths:**
- Works when no API exists
- Most trustless/verifiable
- Direct on-chain data

**Drawbacks:**
- Most complex implementation
- **Slower performance** - multiple API calls per transaction
- Requires block number lookups
- Explorer API rate limits
- Fallback fee calculations needed

**Performance:** ⚡⚡ Moderate (typically 5-10 seconds for 30 days, can be slower)
- **WARNING:** If approach requires looking up individual tx details, it can be too slow
- Per-tx lookups: 150 txs × 100ms = 15 seconds (borderline)
- Must implement carefully with batching/caching to stay under 15s limit
- **TIP:** Use ShapeShift's private RPC proxies (see `/home/sean/Repos/shapeshift/.env`) for better performance than public RPCs

**USD Enrichment:** ✅ **Use `enrichFeesWithUsdPrices()`**
- Integration returns crypto `amount` from on-chain transfers
- Enrichment calculates USD value using **CURRENT** prices

**Amount Format:** On-chain data is always in base units (wei)

**Example Structure:**
```typescript
// Scrape explorer for Portal events
const events = await getPortalEventsFromExplorer(config, startTimestamp, endTimestamp)

// For each event, look up the actual token transfer to treasury
const fees = await Promise.all(events.map(async event => {
  const transfer = await getFeeTransferFromExplorer(config, event.txHash)

  if (transfer) {
    return {
      chainId: config.chainId,
      assetId: buildAssetId(config.chainId, transfer.token),
      service: 'swappername',
      txHash: event.txHash,
      timestamp: event.timestamp,
      amount: transfer.amount, // Already in base units (from blockchain)
    }
  } else {
    // Fallback: calculate from input amount
    return {
      chainId: config.chainId,
      assetId: buildAssetId(config.chainId, event.inputToken),
      service: 'swappername',
      txHash: event.txHash,
      timestamp: event.timestamp,
      amount: calculateFallbackFee(event.inputAmount), // 55 BPS of input
    }
  }
}))

return enrichFeesWithUsdPrices(fees)
```

---

### Output Phase 1: Research Summary

After completing your research, provide a summary report:

```markdown
## Research Summary for [Swapper Name]

### ShapeShift Integration (Step 0)

**Affiliate Identifier:** [Type and value]

**Found in ShapeShift code:** [File path]

**How fees are tracked:** [Treasury address / API key / Referrer param / etc.]

**Key insight:** [Brief explanation of how this affects our revenue tracking]

---

### Available Options

1. **Option 1: [Name]**
   - **Type:** [Direct Revenue API / Transaction API / etc.]
   - **Endpoint:** [URL]
   - **Filtering:** [Time range support, affiliate ID, etc.]
   - **Data Provided:** [Fee amounts, volumes, USD values]
   - **Amount Format:** [Decimal / Base Units / Unknown - needs testing]
   - **Cost:** [Free / Paid / Free trial only] ⚠️ Must be FREE!
   - **API Key Required:** [Yes/No]
   - **Performance Estimate:** [e.g., "1 call for 30 days ≈ 1s", "5 pages × 200ms ≈ 1s", "150 txs × 100ms ≈ 15s"]
   - **Strengths:** [List]
   - **Drawbacks:** [List - include performance issues if slow]

2. **Option 2: [Name]**
   - [Same structure...]

### Recommendation

**Recommended Approach:** Option X - [Approach Name]

**Reasoning:**
- [Why this is best for our use case]
- [Alignment with our requirements]
- [Accuracy considerations]

**Performance:** [Estimated time to fetch 30 days] ⚡⚡⚡ / ⚡⚡ / ⚡
- [Brief justification - batch queries, pagination, per-tx, etc.]
- ✅ Meets 15-second requirement / ⚠️ Borderline / ❌ Too slow

**Amount Format:** [Decimal/Base Units] - [Conversion needed: Yes/No]

**USD Enrichment Strategy:**
- ✅ Use enrichFeesWithUsdPrices() / ❌ Return as-is
- **Rationale:** [Explain based on data available]

**Implementation Complexity:** [Low/Medium/High]

**Proceed?** [Wait for user confirmation before implementing]
```

---

## Phase 2: Implementation

Once the user approves your recommended approach, proceed with implementation.

### Step 1: Create Integration Directory

**Location:** `apps/revenue-api/src/affiliateRevenue/[swappername]/`

**Required Files:**
- `index.ts` - Export `getFees` function
- `[swappername].ts` - Main implementation
- `types.ts` - TypeScript types for API responses
- `constants.ts` - **API URLs, keys, and affiliate identifier from Step 0**
- `utils.ts` - Helper functions (if needed)

**In `constants.ts`, define the affiliate identifier you found in Step 0:**
```typescript
// Example: Treasury address (THORChain/Maya)
export const DAO_TREASURY = '0x...' // or 'thor1x...'

// Example: Broker ID (Chainflip)
export const SHAPESHIFT_BROKER_ID = 'shapeshift'

// Example: Referrer address (Relay)
export const SHAPESHIFT_REFERRER = '0x...'

// Example: API key (0x)
export const SWAPPERNAME_API_KEY = process.env.SWAPPERNAME_API_KEY ?? ''
```

### Step 2: Implement Core Integration

**Standard `getFees` Pattern:**

Every integration MUST follow this pattern:

```typescript
export const getFees = async (startTimestamp: number, endTimestamp: number): Promise<Fees[]> => {
  const startTime = Date.now()
  const threshold = getCacheableThreshold()
  const { cacheableDates, recentStart } = splitDateRange(startTimestamp, endTimestamp, threshold)

  // === CACHE LOOKUP ===
  const cachedFees: Fees[] = []
  const datesToFetch: string[] = []
  let cacheHits = 0
  let cacheMisses = 0

  for (const date of cacheableDates) {
    const cached = tryGetCachedFees('swappername', chainId, date)
    if (cached) {
      cachedFees.push(...cached)
      cacheHits++
    } else {
      datesToFetch.push(date)
      cacheMisses++
    }
  }

  // === FETCH MISSING DATES ===
  const newFees: Fees[] = []
  if (datesToFetch.length > 0) {
    const fetchStart = getDateStartTimestamp(datesToFetch[0])
    const fetchEnd = getDateEndTimestamp(datesToFetch[datesToFetch.length - 1])
    const fetched = await fetchFeesFromAPI(fetchStart, fetchEnd)

    const feesByDate = groupFeesByDate(fetched)
    for (const date of datesToFetch) {
      saveCachedFees('swappername', chainId, date, feesByDate[date] || [])
    }
    newFees.push(...fetched)
  }

  // === FETCH RECENT (UNCACHEABLE) DATA ===
  const recentFees: Fees[] = []
  if (recentStart !== null) {
    recentFees.push(...(await fetchFeesFromAPI(recentStart, endTimestamp)))
  }

  // === LOGGING ===
  const totalFees = cachedFees.length + newFees.length + recentFees.length
  const duration = Date.now() - startTime
  console.log(`[swappername] Total: ${totalFees} fees in ${duration}ms | Cache: ${cacheHits} hits, ${cacheMisses} misses`)

  // === USD ENRICHMENT (conditional) ===
  const allFees = [...cachedFees, ...newFees, ...recentFees]

  // ✅ If using Approach 1, 2, or 5:
  return enrichFeesWithUsdPrices(allFees)

  // ❌ If using Approach 3 or 4:
  return allFees
}
```

**Key Implementation Notes:**

1. **Amount Normalization (CRITICAL!):**
   ```typescript
   // ⚠️ ALWAYS store amounts in smallest unit (wei, satoshis, etc.)

   // If API returns BASE UNITS (e.g., "2500000" for 2.5 USDC with 6 decimals):
   const amount = fee.amount // Use directly

   // If API returns DECIMAL format (e.g., "2.5" for 2.5 USDC):
   const decimals = await assetDataService.getAssetDecimals(assetId)
   const amount = decimalToBaseUnit(fee.amount, decimals) // Convert to wei

   // Example conversions:
   // - "2.5" USDC (6 decimals) → "2500000" wei
   // - "0.001" ETH (18 decimals) → "1000000000000000" wei
   // - "1.0" BTC (8 decimals) → "100000000" satoshis
   ```

   **How to test if API returns decimal or base units:**
   ```typescript
   // Make a test API call and check the amount
   // If you see small numbers like "0.5", "2.5" → DECIMAL format
   // If you see large numbers like "500000", "2500000" → BASE UNITS
   // Compare with actual token decimals to verify
   ```

2. **Cache Strategy:**
   - Cache by date for historical data (never changes)
   - Don't cache "today" (prices update)
   - Use `splitDateRange` to separate cacheable vs. recent
   - Cache key: `swappername:chainId:YYYY-MM-DD`

3. **Timestamps:**
   - API params use Unix timestamps (seconds)
   - Internal storage uses Unix timestamps
   - Cache keys use ISO date strings (YYYY-MM-DD)

4. **Asset IDs:**
   - Follow CAIP format: `chainId/tokenType:tokenAddress`
   - Native tokens: `eip155:1/slip44:60` (ETH)
   - ERC20 tokens: `eip155:1/erc20:0x...`
   - Cosmos chains: `cosmos:thorchain-1/slip44:931`
   - Use existing `getSlip44ForChain()` utility

5. **Affiliate Identifier (from Step 0):**
   - **ALWAYS use the affiliate identifier you found in Step 0**
   - Add it to `constants.ts` (see example above)
   - Use it in your API calls to filter for ShapeShift's fees
   ```typescript
   // Example: Filtering by referrer
   const { data } = await axios.get(API_URL, {
     params: {
       referrer: SHAPESHIFT_REFERRER, // From Step 0
       startTimestamp,
       endTimestamp,
     }
   })

   // Example: Filtering by broker ID
   const { data } = await axios.post(API_URL, {
     query: GET_SWAPS_QUERY,
     variables: {
       brokerId: SHAPESHIFT_BROKER_ID, // From Step 0
       startDate,
       endDate,
     }
   })

   // Example: API key identifies us
   const { data } = await axios.get(API_URL, {
     headers: {
       'api-key': SWAPPERNAME_API_KEY, // From Step 0
     }
   })
   ```

6. **Error Handling:**
   - Use `withRetry()` wrapper for API calls
   - Log errors with `console.error`
   - Return empty array on complete failure
   - Partial failures should be logged but not throw

### Step 3: Environment Variables

If API key required:

1. **Add to `apps/revenue-api/.env.example`:**
   ```bash
   SWAPPERNAME_API_KEY=your_key_here
   ```

2. **Add to server setup:**
   ```typescript
   // In constants.ts
   export const SWAPPERNAME_API_KEY = process.env.SWAPPERNAME_API_KEY ?? ''
   ```

3. **Document in README** under Environment Variables section

### Step 4: Register Integration

**File: `apps/revenue-api/src/affiliateRevenue/index.ts`**

1. Import your module:
   ```typescript
   import * as swappername from './swappername'
   ```

2. Add to provider names array:
   ```typescript
   const providerNames: Service[] = [
     'bebop',
     'butterswap',
     // ... existing providers
     'swappername', // Add here (alphabetical order preferred)
   ]
   ```

3. Add to Promise.allSettled:
   ```typescript
   const results = await Promise.allSettled([
     bebop.getFees(startTimestamp, endTimestamp),
     // ... existing providers
     swappername.getFees(startTimestamp, endTimestamp), // Add here
   ])
   ```

**File: `apps/revenue-api/src/types.ts`**

Add to services array:
```typescript
export const services = [
  'bebop',
  // ... existing
  'swappername', // Add in alphabetical order
] as const
```

### Step 5: Frontend Integration

**File: `apps/revenue-dashboard/src/constants/services.ts`**

1. **Add display label:**
   ```typescript
   export const SERVICE_LABELS: Record<string, string> = {
     // ... existing
     swappername: 'Swapper Display Name',
   }
   ```

2. **Add color (use a color not already taken):**
   ```typescript
   export const SERVICE_COLORS: Record<string, string> = {
     // ... existing
     swappername: '#3b82f6', // Choose unique color
   }
   ```

3. **Add to stack order (determines chart order):**
   ```typescript
   export const SERVICE_STACK_ORDER = [
     'thorchain',
     // ... existing
     'swappername', // Add in desired display order
   ]
   ```

**Available Colors (TailwindCSS):**
- `#3b82f6` - blue-500
- `#a855f7` - purple-500
- `#ef4444` - red-500
- `#10b981` - emerald-500
- `#f59e0b` - amber-500
- `#06b6d4` - cyan-500
- `#ec4899` - pink-500
- `#14b8a6` - teal-500
- `#84cc16` - lime-500
- `#f97316` - orange-500
- `#6366f1` - indigo-500
- `#22c55e` - green-500

### Step 6: Testing

1. **Test API calls locally:**
   ```bash
   bun dev:backend
   ```

2. **Test amount conversion (if using decimal format):**
   ```typescript
   // Verify your conversion is correct
   // Example: "2.5" USDC → "2500000" (6 decimals)
   console.log(decimalToBaseUnit("2.5", 6)) // Should output "2500000"
   ```

3. **Test full stack:**
   ```bash
   bun dev
   ```

4. **Verify data:**
   - Check browser network tab for API responses
   - Verify revenue amounts are reasonable
   - Check charts display correctly
   - Confirm caching works (check logs)
   - **Verify amounts are in base units (large numbers like "2500000", not "2.5")**

5. **Test date ranges:**
   - Last 7 days
   - Last 30 days
   - Last 90 days
   - Custom ranges

### Step 7: Audit for Additional UI Updates

**Search for hardcoded service references:**

Run these checks to ensure nothing was missed:

```bash
# Search for service arrays/lists
grep -r "thorchain.*mayachain.*chainflip" apps/revenue-dashboard/src/

# Search for service type definitions
grep -r "Service.*=.*{" apps/revenue-dashboard/src/

# Search for service-specific styling
grep -r "switch.*service" apps/revenue-dashboard/src/
```

**Common locations to check:**
- Type definitions
- Chart components
- Table components
- Color/styling utilities
- Mock data files
- Test files

If you find any hardcoded lists or switch statements, update them to include the new swapper.

### Step 8: Code Quality

Before submitting, ensure:

- ✅ No TypeScript errors: `bun type-check`
- ✅ No linting errors: `bun lint:fix`
- ✅ Follows existing code conventions
- ✅ Proper error handling
- ✅ Logging includes service name prefix
- ✅ Caching implemented correctly
- ✅ **Amount normalization correct (all amounts in base units/wei)**
- ✅ USD enrichment strategy correct for your approach
- ✅ All console.logs use `[swappername]` prefix

---

## Critical Reminders

### Amount Format Decision Tree

```
What format does the API return amounts in?

├─ BASE UNITS (large numbers like "2500000")
│  └─ ✅ Use amount directly: amount = fee.amount
│
├─ DECIMAL (small numbers like "2.5", "0.001")
│  └─ ⚠️ Must convert to base units:
│     1. Get asset decimals: const decimals = await assetDataService.getAssetDecimals(assetId)
│     2. Convert: const amount = decimalToBaseUnit(fee.amount, decimals)
│
└─ UNKNOWN
   └─ ⚠️ Test the API with known amounts and compare!
```

**Example Test:**
```typescript
// If you see: { amount: "2.5", token: "0xUSDC..." }
// And USDC has 6 decimals
// Then 2.5 USDC should be stored as "2500000" (2.5 × 10^6)

const decimals = await assetDataService.getAssetDecimals(assetId)
const baseUnits = decimalToBaseUnit("2.5", decimals)
// baseUnits = "2500000" ✅
```

### USD Enrichment Decision Tree

```
Do you have crypto amounts from the API?
├─ YES
│  └─ Does the API provide USD values?
│     ├─ NO → ✅ Use enrichFeesWithUsdPrices() (Approach 1)
│     └─ YES
│        └─ Are the USD values calculated with CURRENT prices or HISTORICAL prices?
│           ├─ CURRENT → ❌ Return as-is (Approach 3)
│           └─ HISTORICAL → ✅ Use enrichFeesWithUsdPrices() (Approach 2)
└─ NO
   └─ ❌ Return as-is, synthesize crypto amounts from USD 1:1 (Approach 4)
```

### Fee Calculation

If you need to calculate fees from volume:
```typescript
const FEE_BPS = 55
const FEE_BPS_DENOMINATOR = 10000

const feeAmount = volume * (FEE_BPS / FEE_BPS_DENOMINATOR) // = volume * 0.0055
```

### Asset ID Format

Always use CAIP format:
```typescript
// EVM native
`eip155:${chainId}/slip44:${slip44}`

// EVM ERC20
`eip155:${chainId}/erc20:${address.toLowerCase()}`

// Cosmos native
`cosmos:${chainName}/slip44:${slip44}`

// Solana native
`solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp/slip44:501`
```

### Caching Rules

- ✅ Cache complete days (00:00:00 to 23:59:59 UTC)
- ✅ Cache indefinitely (TTL handled by LRU)
- ❌ Don't cache partial days
- ❌ Don't cache "today"
- ✅ Use `splitDateRange()` to separate cacheable vs recent

---

## Success Checklist

Before marking the integration complete:

- [ ] Research phase completed with user approval
- [ ] Integration directory created with all files
- [ ] Core `getFees` function implemented
- [ ] **Amount normalization correct (all amounts in base units/wei)**
- [ ] Correct USD enrichment strategy applied
- [ ] Caching implemented correctly
- [ ] Environment variables added (if needed)
- [ ] Backend type/service registration complete
- [ ] Frontend constants updated (labels, colors, order)
- [ ] No TypeScript errors (`bun type-check`)
- [ ] No linting errors (`bun lint:fix`)
- [ ] Tested with multiple date ranges
- [ ] **Verified amounts are large numbers (wei), not decimal**
- [ ] Logging includes service name prefix
- [ ] Additional UI locations audited and updated
- [ ] README updated with new provider (if needed)

---

## Reference Files

Key files to reference during implementation:

**ShapeShift Swapper Implementations (for Step 0):**
- `/home/sean/Repos/shapeshift/packages/swapper/src/swappers/` - All swapper implementations
- `/home/sean/Repos/shapeshift/packages/swapper/src/swappers/ThorchainSwapper/` - Treasury address example
- `/home/sean/Repos/shapeshift/packages/swapper/src/swappers/ZrxSwapper/` - API key example
- `/home/sean/Repos/shapeshift/packages/swapper/src/swappers/RelaySwapper/` - Referrer parameter example
- `/home/sean/Repos/shapeshift/packages/swapper/src/swappers/ChainflipSwapper/` - Broker ID example
- `/home/sean/Repos/shapeshift/.env` - **RPC proxy endpoints** for on-chain queries

**Backend (Revenue Dashboard):**
- `apps/revenue-api/src/affiliateRevenue/thorchain/thorchain.ts` - Simple API (base units)
- `apps/revenue-api/src/affiliateRevenue/bebop/bebop.ts` - **Decimal conversion example** ⭐
- `apps/revenue-api/src/affiliateRevenue/zrx/zrx.ts` - **Decimal conversion example** ⭐
- `apps/revenue-api/src/affiliateRevenue/relay/relay.ts` - Current USD pricing (base units)
- `apps/revenue-api/src/affiliateRevenue/chainflip/chainflip.ts` - USD-only, synthesized amounts
- `apps/revenue-api/src/affiliateRevenue/portals/portals.ts` - On-chain (always base units)
- `apps/revenue-api/src/affiliateRevenue/cache.ts` - Caching utilities
- `apps/revenue-api/src/affiliateRevenue/enrichment.ts` - USD enrichment logic
- `apps/revenue-api/src/affiliateRevenue/utils.ts` - **`decimalToBaseUnit()` utility** ⭐

**Frontend:**
- `apps/revenue-dashboard/src/constants/services.ts` - Service display configuration
- `apps/revenue-dashboard/src/types/index.ts` - TypeScript types

**Documentation:**
- `README.md` - Environment variables, architecture
