# Euler Lens & Data Agent Skill

**Version 1.0.0**  
Euler Labs  
January 2026

> **Note:**  
> This document is for agents and LLMs to follow when querying Euler data  
> or using developer tools. It covers Lens contracts, subgraphs, contract  
> interfaces, and no-code vault deployment.

---

## Abstract

Developer tools and data access guide for Euler Finance V2. Covers Lens contracts for querying vault data, subgraph queries for historical data, contract interfaces and ABIs, and no-code vault deployment via Euler Creator.

---

## Table of Contents

1. [Developer Tools](#1-developer-tools) — **MEDIUM**
   - 1.1 [Contract Addresses and ABIs](#11-contract-addresses-and-abis)
   - 1.2 [Data Querying with Subgraphs](#12-data-querying-with-subgraphs)
   - 1.3 [Lens Contracts for Data Queries](#13-lens-contracts-for-data-queries)

---

## 1. Developer Tools

**Impact: MEDIUM**

Tools and resources for developers including Lens contracts for querying vault and account data, subgraph for tracking active accounts, and contract addresses and ABIs. Essential for efficient Euler development and integration.

### 1.1 Contract Addresses and ABIs

**Impact: MEDIUM (Essential reference for Euler contract integration)**

The `euler-interfaces` repository provides verified contract addresses and ABIs for all supported chains. Always use this package rather than hardcoding addresses.

**Incorrect: hardcoding addresses**

```typescript
// WRONG: Addresses may differ between chains and change over time
const EVC = "0x0C9a3dd6b8F28529d72d7f9cE918D493519EE383";
const FACTORY = "0x29a56a1b8214D9Cf7c5561811750D5cBDb45CC8e";
// What about Arbitrum? Base? Other chains?
// What if addresses are updated?
```

**Correct: using euler-interfaces package**

```typescript
// Install: npm install @eulerxyz/euler-interfaces

// Import chain-specific addresses
import coreMainnet from '@eulerxyz/euler-interfaces/addresses/1/CoreAddresses.json';
import peripheryMainnet from '@eulerxyz/euler-interfaces/addresses/1/PeripheryAddresses.json';
import lensMainnet from '@eulerxyz/euler-interfaces/addresses/1/LensAddresses.json';

// For other chains, use their chain ID
import coreArbitrum from '@eulerxyz/euler-interfaces/addresses/42161/CoreAddresses.json';
import coreBase from '@eulerxyz/euler-interfaces/addresses/8453/CoreAddresses.json';

// Access addresses
console.log('EVC:', coreMainnet.evc);
console.log('Factory:', coreMainnet.eVaultFactory);
console.log('VaultLens:', lensMainnet.vaultLens);
```

**Correct: dynamic chain-based loading**

```typescript
// Dynamic address loading for multi-chain apps
async function getEulerAddresses(chainId: number) {
  const core = await import(
    `@eulerxyz/euler-interfaces/addresses/${chainId}/CoreAddresses.json`
  );
  const periphery = await import(
    `@eulerxyz/euler-interfaces/addresses/${chainId}/PeripheryAddresses.json`
  );
  const lens = await import(
    `@eulerxyz/euler-interfaces/addresses/${chainId}/LensAddresses.json`
  );
  
  return { core, periphery, lens };
}

// Usage
const { core, periphery, lens } = await getEulerAddresses(1); // Mainnet
const { core: arbCore } = await getEulerAddresses(42161);     // Arbitrum
```

**Address file structure in euler-interfaces:**

```typescript
@eulerxyz/euler-interfaces/
├── addresses/
│   ├── 1/                        # Ethereum Mainnet
│   │   ├── CoreAddresses.json    # EVC, factory, protocol config
│   │   ├── PeripheryAddresses.json # IRMs, perspectives, fee flow
│   │   ├── LensAddresses.json    # Lens contracts
│   │   ├── OracleAdaptersAddresses.csv # Deployed oracles
│   │   └── ...
│   ├── 42161/                    # Arbitrum
│   ├── 8453/                     # Base
│   ├── 10/                       # Optimism
│   └── ...
└── abis/
    ├── EVault.json
    ├── EthereumVaultConnector.json
    └── ...
```

**Correct: using with viem**

```typescript
import { createPublicClient, http, getContract } from 'viem';
import { mainnet } from 'viem/chains';
import core from '@eulerxyz/euler-interfaces/addresses/1/CoreAddresses.json';
import evcABI from '@eulerxyz/euler-interfaces/abis/EthereumVaultConnector.json';
import evaultABI from '@eulerxyz/euler-interfaces/abis/EVault.json';

const client = createPublicClient({
  chain: mainnet,
  transport: http()
});

// Create contract instances using imported addresses
const evc = getContract({
  address: core.evc as `0x${string}`,
  abi: evcABI,
  client
});

// Check collaterals for an account
const collaterals = await evc.read.getCollaterals([accountAddress]);
```

**Correct: Solidity remapping**

```solidity
// In remappings.txt for Foundry
euler-interfaces/=node_modules/@eulerxyz/euler-interfaces/

// In Solidity
import {IEVault} from "euler-interfaces/interfaces/IEVault.sol";
import {IEVC} from "euler-interfaces/interfaces/IEVC.sol";
```

Always refer to the euler-interfaces package for the most up-to-date addresses. The package is maintained by Euler Labs and updated when new contracts are deployed.

Reference: [https://github.com/euler-xyz/euler-interfaces](https://github.com/euler-xyz/euler-interfaces)

### 1.2 Data Querying with Subgraphs

**Impact: MEDIUM (Track active accounts and vault factories)**

Euler provides a minimal subgraph deployed via Goldsky for tracking active accounts and vault factory origins. The subgraph is intentionally limited in scope - **use Lens contracts for real-time vault data, positions, and configuration**.

**Subgraph Schema:**

```graphql
# Vault entity - tracks which factory created each vault
type Vault @entity(immutable: true) {
  id: Bytes!      # vault address
  factory: Bytes! # factory that created this vault
}

# Active account tracking - indexed by address prefix (first 19 bytes)
# Groups main account with all 256 sub-accounts under the same prefix
type TrackingActiveAccount @entity {
  id: Bytes!            # addressPrefix (first 19 bytes)
  addressPrefix: Bytes! # first 19 bytes shared by main address and sub-accounts
  deposits: [Bytes!]!   # list of account+vault IDs with deposits
  borrows: [Bytes!]!    # list of account+vault IDs with borrows
  blockNumber: BigInt!
  blockTimestamp: BigInt!
  transactionHash: Bytes!
}

# Per-account vault balance tracking
type TrackingVaultBalance @entity {
  id: Bytes!            # account + vault (concatenated)
  vault: Bytes!
  addressPrefix: Bytes! # links to TrackingActiveAccount
  account: Bytes!
  balance: BigInt!      # vault shares
  debt: BigInt!         # borrowed amount
  blockNumber: BigInt!
  blockTimestamp: BigInt!
  transactionHash: Bytes!
}
```

**When to Use Subgraph vs Lens:**

| Use Case | Tool |

|----------|------|

| Find all active accounts | Subgraph: `TrackingActiveAccount` |

| Check which factory created a vault to know the vault type | Subgraph: `Vault.factory` |

| Get vault configuration (caps, LTVs, oracle) | Lens: `VaultLens.getVaultInfoFull()` |

| Get account position details | Lens: `AccountLens.getAccountInfo()` |

| Get real-time balances and health | Lens: `AccountLens.getAccountLiquidityInfo()` |

| Get interest rates and APYs | Lens: `UtilsLens.getAPYs()` |

**Correct: querying vault factory origin**

```graphql
# Find which factory deployed a vault
query GetVaultFactory($vault: Bytes!) {
  vault(id: $vault) {
    id
    factory
  }
}

# Get all vaults from a specific factory
query GetVaultsFromFactory($factory: Bytes!) {
  vaults(where: { factory: $factory }) {
    id
    factory
  }
}
```

**Correct: querying active accounts by address prefix**

```graphql
# Get all active accounts (accounts with deposits or borrows)
# Note: Indexed by address prefix (first 19 bytes)
# This groups main account + all 256 sub-accounts together
query GetActiveAccounts($first: Int = 100) {
  trackingActiveAccounts(first: $first, where: { deposits_not: [], borrows_not: [] }) {
    id
    addressPrefix
    deposits
    borrows
    blockTimestamp
  }
}

# Find active accounts by address prefix
query GetAccountByPrefix($prefix: Bytes!) {
  trackingActiveAccount(id: $prefix) {
    addressPrefix
    deposits
    borrows
    blockTimestamp
  }
}
```

**Correct: querying account vault balances - amounts are updated at the time of last interaction**

```typescript
import { request, gql } from 'graphql-request';

// Get current endpoint from docs.euler.finance
// Deployed via Goldsky
const SUBGRAPH_URL = 'https://api.goldsky.com/...';

// Get address prefix (first 19 bytes)
function getAddressPrefix(account: string): string {
  return ('0x' + account.slice(2, 40)).toLowerCase();
}

// Check which factory created a vault
async function getVaultFactory(vaultAddress: string): Promise<string | null> {
  const query = gql`
    query GetVaultFactory($id: Bytes!) {
      vault(id: $id) {
        factory
      }
    }
  `;
  
  const result = await request(SUBGRAPH_URL, query, { 
    id: vaultAddress.toLowerCase() 
  });
  
  return result.vault?.factory ?? null;
}

// Get all active positions for an account (including sub-accounts)
async function getAccountPositions(account: string) {
  const prefix = getAddressPrefix(account);
  
  const query = gql`
    query GetPositions($prefix: Bytes!) {
      trackingVaultBalances(where: { addressPrefix: $prefix }) {
        vault
        account
        balance
        debt
        blockTimestamp
      }
    }
  `;
  
  return request(SUBGRAPH_URL, query, { prefix });
}

// Check if an account has any active positions
async function isAccountActive(account: string): Promise<boolean> {
  const prefix = getAddressPrefix(account);
  
  const query = gql`
    query CheckActive($prefix: Bytes!) {
      trackingActiveAccount(id: $prefix) {
        deposits
        borrows
      }
    }
  `;
  
  const result = await request(SUBGRAPH_URL, query, { prefix });
  const active = result.trackingActiveAccount;
  
  return active && (active.deposits.length > 0 || active.borrows.length > 0);
}
```

**TypeScript: Computing address prefix:**

**TypeScript: Complete subgraph integration:**

**Combining Subgraph with Lens Contracts:**

```typescript
import { getContract } from 'viem';
import { request, gql } from 'graphql-request';
import lens from '@eulerxyz/euler-interfaces/addresses/1/LensAddresses.json';
import accountLensABI from '@eulerxyz/euler-interfaces/abis/AccountLens.json';

// Best practice: 
// 1. Use subgraph to discover active accounts
// 2. Use Lens contracts for detailed, real-time position data

// Step 1: Find active accounts from subgraph
const activeAccountsQuery = gql`
  query {
    trackingActiveAccounts(first: 100, where: { borrows_not: [] }) {
      addressPrefix
      borrows
    }
  }
`;
const activeAccounts = await request(SUBGRAPH_URL, activeAccountsQuery);

// Step 2: Use AccountLens for detailed position data
const accountLens = getContract({
  address: lens.accountLens as Address,
  abi: accountLensABI,
  client: publicClient
});

for (const tracking of activeAccounts.trackingActiveAccounts) {
  // Get detailed liquidity info for each borrowing position
  for (const positionId of tracking.borrows) {
    // positionId is account + vault concatenated
    const account = '0x' + positionId.slice(2, 42);
    const vault = '0x' + positionId.slice(42);
    
    // Real-time health check via Lens
    const liquidityInfo = await accountLens.read.getAccountLiquidityInfo([
      account,
      vault
    ]);
    
    console.log(`Account ${account} in vault ${vault}:`);
    console.log(`  Health: ${liquidityInfo.collateralValueLiquidation / liquidityInfo.liabilityValueLiquidation}`);
    console.log(`  TTL: ${liquidityInfo.timeToLiquidation}`);
  }
}
```

**Important Notes:**

1. **Minimal by design**: The subgraph only tracks account activity and vault factories. Use Lens contracts for vault configuration, LTVs, caps, oracles, IRM info, etc.

2. **Address prefix indexing**: Accounts are indexed by their first 19 bytes. This means a main account and all its 256 EVC sub-accounts share the same `TrackingActiveAccount` entity.

3. **Balance tracking**: `TrackingVaultBalance` stores raw balances and debt at the time of the last interactions. For accurate health factor and liquidation status, use `AccountLens.getAccountLiquidityInfo()`.

4. **Factory verification**: Use `Vault.factory` to verify a vault was deployed from an official Euler factory.

Reference: [https://github.com/euler-xyz/euler-subgraph](https://github.com/euler-xyz/euler-subgraph)

### 1.3 Lens Contracts for Data Queries

**Impact: MEDIUM (Essential for reading comprehensive vault and account data)**

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

**Incorrect: making many individual calls**

```typescript
// WRONG: Multiple calls easy to miss data
const totalAssets = await vault.read.totalAssets();
const totalBorrows = await vault.read.totalBorrows();
const cash = await vault.read.cash();
const governor = await vault.read.governorAdmin();
const irm = await vault.read.interestRateModel();
// ... many more calls needed
```

**Correct: using VaultLens for comprehensive vault data**

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

**Correct: using AccountLens for position data**

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

**Correct: using AccountLens for liquidity info only**

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

**Correct: using AccountLens for all EVC-enabled vaults**

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

**Correct: using AccountLens with no-validation mode**

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

**Correct: using AccountLens for on-chain reward info**

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

> **Note:** The balance tracking and reward-streams mechanism (`TrackingRewardStreams`) is embedded in the EVK but has seen limited adoption. Most Euler rewards are distributed via **off-chain mechanisms like [Merkl](https://merkl.xyz/)**. The on-chain reward-streams may not be supported in all UIs. Check the specific vault's reward distribution method before relying on this data.

**Correct: using VaultLens for IRM curve data**

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

**Correct: using OracleLens for oracle validation**

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

**Correct: using UtilsLens for calculations**

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

**Correct: using IRMLens for interest rate model details**

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

**Correct: using EulerEarnVaultLens for yield strategies**

```solidity
// DON'T use Lens on-chain - it's not gas efficient
// IAccountLens(lens).getAccountLiquidityInfo(account, vault); // Expensive!

// DO call vault methods directly for on-chain checks
(uint256 collateralValue, uint256 liabilityValue) = IEVault(vault).accountLiquidity(account, true);
bool isHealthy = collateralValue >= liabilityValue;
```

**Important: Lens contracts are for off-chain queries only**

Lens contracts are optimized for convenience, not gas efficiency. They aggregate multiple calls and return large structs, which is expensive on-chain. For on-chain integrations, call vault methods directly:

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

Reference: [https://github.com/euler-xyz/evk-periphery/tree/master/src/Lens](https://github.com/euler-xyz/evk-periphery/tree/master/src/Lens)

---

## References

1. [https://docs.euler.finance](https://docs.euler.finance)
2. [https://github.com/euler-xyz/evk-periphery](https://github.com/euler-xyz/evk-periphery)
3. [https://github.com/euler-xyz/euler-vault-kit](https://github.com/euler-xyz/euler-vault-kit)
