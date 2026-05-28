---
title: Data Querying with Subgraphs
impact: MEDIUM
impactDescription: Track active accounts and vault factories
tags: subgraph, graphql, data, indexing, tracking
---

## Data Querying with Subgraphs

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

**Correct (querying vault factory origin):**

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

**Correct (querying active accounts by address prefix):**

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

**Correct (querying account vault balances - amounts are updated at the time of last interaction):**

```graphql
# Get all vault positions for an address prefix
query GetPositionsByPrefix($prefix: Bytes!) {
  trackingVaultBalances(where: { addressPrefix: $prefix }) {
    id
    vault
    account
    balance
    debt
    blockTimestamp
  }
}

# Get positions with non-zero balances
query GetActivePositions($prefix: Bytes!) {
  trackingVaultBalances(
    where: { addressPrefix: $prefix, balance_gt: "0" }
  ) {
    vault
    account
    balance
    debt
  }
}

# Get positions with active borrows
query GetBorrowPositions($prefix: Bytes!) {
  trackingVaultBalances(
    where: { addressPrefix: $prefix, debt_gt: "0" }
  ) {
    vault
    account
    balance
    debt
  }
}
```

**TypeScript: Computing address prefix:**

```typescript
// The subgraph indexes by address prefix (first 19 bytes)
// This groups a main account with all its 256 EVC sub-accounts
function getAddressPrefix(account: string): string {
  // Address is 20 bytes, prefix is first 19 bytes
  // Remove '0x', take first 38 hex chars (19 bytes), add '0x' back
  return '0x' + account.slice(2, 40); // first 19 bytes
}

// Example: All these accounts share the same prefix
const mainAccount = '0x1234567890abcdef1234567890abcdef12345678';
const subAccount1 = '0x1234567890abcdef1234567890abcdef12345601'; // sub-account 1
const subAccount2 = '0x1234567890abcdef1234567890abcdef12345602'; // sub-account 2

const prefix = getAddressPrefix(mainAccount);
// prefix = '0x1234567890abcdef1234567890abcdef123456'
// Same prefix for all sub-accounts!
```

**TypeScript: Complete subgraph integration:**

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

Reference: [Euler Subgraph Repository](https://github.com/euler-xyz/euler-subgraph)
