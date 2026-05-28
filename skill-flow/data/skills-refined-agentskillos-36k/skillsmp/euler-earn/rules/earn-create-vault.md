---
title: Create an EulerEarn Vault
impact: MEDIUM
impactDescription: Deploy yield aggregation vaults
tags: earn, vault, yield, factory, aggregation
---

## Create an EulerEarn Vault

EulerEarn vaults are yield aggregation meta-vaults that allocate deposited assets across multiple ERC-4626 strategy vaults. They provide passive yield optimization with role-based governance.

**Incorrect (deploying without proper initialization):**

```solidity
// Don't deploy EulerEarn directly - use factory
EulerEarn vault = new EulerEarn();
// Missing proper initialization, not tracked by factory
```

**Correct (deploy via EulerEarnFactory):**

```solidity
import {EulerEarnFactory} from "euler-earn/EulerEarnFactory.sol";
import {IEulerEarn} from "euler-earn/interfaces/IEulerEarn.sol";

// Deploy EulerEarn vault via factory
// Parameters: initialOwner, initialTimelock, asset, name, symbol, salt
address earnVault = EulerEarnFactory(factory).createEulerEarn(
    initialOwner,       // Address that becomes vault owner
    0,                  // Initial timelock (can be 0)
    asset,              // Underlying asset (e.g., USDC)
    name,               // Vault name (e.g., "Euler USDC Earn")
    symbol,             // Vault symbol (e.g., "eUSDC")
    bytes32(0)          // Salt for CREATE2 (0 for default)
);

IEulerEarn earn = IEulerEarn(earnVault);
```

**Correct (configure vault after deployment):**

```solidity
// Set fee (max 50%)
earn.setFeeRecipient(treasuryAddress);
earn.setFee(0.1e18); // 10% of yield (setFee, not setPerformanceFee)

// Set timelock for governance actions (two-step process)
// Initial timelock can be 0, but subsequent changes are timelocked
// Step 1: Submit new timelock value
earn.submitTimelock(24 hours);
// Step 2: After current timelock elapses, accept the new value
earn.acceptTimelock();

// Set guardian for emergency actions (also two-step if timelock > 0)
earn.submitGuardian(guardianAddress);

// Set curator for strategy management
earn.setCurator(curatorAddress);

// Add allocators who can rebalance
earn.setIsAllocator(allocatorAddress, true);
```

**Correct (add strategy vaults):**

```solidity
// Strategy vaults must be ERC-4626 compliant
// EVK vaults are preferred due to built-in protections

// Submit cap for a strategy (timelocked if timelock > 0)
// Note: submitCap takes IERC4626, not address
earn.submitCap(
    IERC4626(strategyVault),  // IERC4626 strategy vault
    100_000e6                  // Supply cap (e.g., 100k USDC)
);

// After timelock, accept the cap
earn.acceptCap(IERC4626(strategyVault));

// Add strategy to supply queue (order matters)
// Note: setSupplyQueue takes IERC4626[] not address[]
IERC4626[] memory newSupplyQueue = new IERC4626[](2);
newSupplyQueue[0] = IERC4626(strategyVault1);  // First priority
newSupplyQueue[1] = IERC4626(strategyVault2);  // Second priority
earn.setSupplyQueue(newSupplyQueue);

// Withdraw queue contains all strategies with allocation
// Updated automatically, but can be reordered
```

**Correct (TypeScript vault creation):**

```typescript
import { encodeFunctionData } from 'viem';

// Deploy earn vault via factory
const earnVaultAddress = await eulerEarnFactory.write.createEulerEarn([
  ownerAddress,          // initialOwner
  0n,                    // initialTimelock
  usdcAddress,           // asset
  'Euler USDC Earn',     // name
  'eUSDC',               // symbol
  '0x0000000000000000000000000000000000000000000000000000000000000000', // salt
]);

// Configure in batch
const setupCalls = [
  encodeFunctionData({
    abi: eulerEarnABI,
    functionName: 'setFeeRecipient',
    args: [treasuryAddress],
  }),
  encodeFunctionData({
    abi: eulerEarnABI,
    functionName: 'setFee',
    args: [0.1e18], // 10%
  }),
  encodeFunctionData({
    abi: eulerEarnABI,
    functionName: 'setCurator',
    args: [curatorAddress],
  }),
  encodeFunctionData({
    abi: eulerEarnABI,
    functionName: 'submitGuardian',
    args: [guardianAddress],
  }),
];

// Execute setup
for (const call of setupCalls) {
  await ownerWallet.sendTransaction({
    to: earnVaultAddress,
    data: call,
  });
}
```

**Role permissions overview:**

| Role | Capabilities |
|------|-------------|
| Owner | All actions, set other roles, set fee |
| Curator | Manage caps, submit removals, do allocator actions |
| Guardian | Revoke pending changes, emergency stops |
| Allocator | Set queues, reallocate funds |

**Non-borrowable idle vault setup:**

```solidity
// For guaranteed liquidity, add a non-borrowable "idle" strategy
// This ensures some funds are always withdrawable

// Create or use an Escrow Vault (non-borrowable EVK)
address escrowVault = createEscrowVault(asset);

// Add to EulerEarn with infinite cap
earn.submitCap(IERC4626(escrowVault), type(uint184).max);
// Wait for timelock...
earn.acceptCap(IERC4626(escrowVault));

// Put at end of supply queue (last priority)
// Funds only go here if other strategies are full
```

---

## EulerEarnFactory Query Functions

The factory provides useful functions for discovering and validating EulerEarn vaults:

```solidity
import {EulerEarnFactory} from "euler-earn/EulerEarnFactory.sol";

EulerEarnFactory factory = EulerEarnFactory(factoryAddress);

// Check if an address is an EulerEarn vault deployed by this factory
bool isEarnVault = factory.isVault(vaultAddress);

// Check if a strategy is allowed (verified by perspective OR is an EulerEarn vault)
// Strategies must pass this check to be added to an EulerEarn vault
bool allowed = factory.isStrategyAllowed(strategyAddress);

// Get the perspective used for strategy verification
address perspective = factory.supportedPerspective();

// Get total number of deployed vaults
uint256 count = factory.getVaultListLength();

// Get a slice of deployed vaults (for pagination)
// Use type(uint256).max for end to get all remaining
address[] memory vaults = factory.getVaultListSlice(0, 10);  // First 10
address[] memory allVaults = factory.getVaultListSlice(0, type(uint256).max);  // All
```

```typescript
// TypeScript: Query factory for deployed vaults
const vaultCount = await factory.read.getVaultListLength();
console.log(`Total EulerEarn vaults: ${vaultCount}`);

// Check if strategy can be used
const canUseStrategy = await factory.read.isStrategyAllowed([strategyAddress]);
if (!canUseStrategy) {
  console.error('Strategy not verified by perspective');
}

// Get all deployed vaults (pass type(uint256).max for end)
const MAX_UINT256 = 2n ** 256n - 1n;
const allVaults = await factory.read.getVaultListSlice([0n, MAX_UINT256]);
```

Reference: [EulerEarn README](https://github.com/euler-xyz/euler-earn#readme), [EulerEarnFactory.sol](https://github.com/euler-xyz/euler-earn/blob/master/src/EulerEarnFactory.sol)
