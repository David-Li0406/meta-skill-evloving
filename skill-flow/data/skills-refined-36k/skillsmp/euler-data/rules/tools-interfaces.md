---
title: Contract Addresses and ABIs
impact: MEDIUM
impactDescription: Essential reference for Euler contract integration
tags: addresses, abi, interfaces, contracts, chains
---

## Contract Addresses and ABIs

The `euler-interfaces` repository provides verified contract addresses and ABIs for all supported chains. Always use this package rather than hardcoding addresses.

**Incorrect (hardcoding addresses):**

```typescript
// WRONG: Addresses may differ between chains and change over time
const EVC = "0x0C9a3dd6b8F28529d72d7f9cE918D493519EE383";
const FACTORY = "0x29a56a1b8214D9Cf7c5561811750D5cBDb45CC8e";
// What about Arbitrum? Base? Other chains?
// What if addresses are updated?
```

**Correct (using euler-interfaces package):**

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

**Correct (dynamic chain-based loading):**

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

```
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

**Correct (using with viem):**

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

**Correct (Solidity remapping):**

```solidity
// In remappings.txt for Foundry
euler-interfaces/=node_modules/@eulerxyz/euler-interfaces/

// In Solidity
import {IEVault} from "euler-interfaces/interfaces/IEVault.sol";
import {IEVC} from "euler-interfaces/interfaces/IEVC.sol";
```

Always refer to the euler-interfaces package for the most up-to-date addresses. The package is maintained by Euler Labs and updated when new contracts are deployed.

Reference: [euler-interfaces](https://github.com/euler-xyz/euler-interfaces)
