---
title: Manage EulerEarn Strategies
impact: MEDIUM
impactDescription: Optimize yield through strategy allocation
tags: earn, strategies, allocation, reallocate, queue, publicallocator
---

## Manage EulerEarn Strategies

Strategy management involves adjusting allocations across ERC-4626 vaults to optimize yield while maintaining risk parameters. This is done by curators and allocators.

**Incorrect (wrong function signature and no liquidity check):**

```solidity
// ERROR: Wrong signature! reallocate takes MarketAllocation[] struct array
// Also doesn't check if strategy has enough liquidity
earn.reallocate(
    [strategyA, strategyB],
    [type(uint256).max, 0]  // Wrong! This is not valid syntax
);
// The actual function takes: reallocate(MarketAllocation[] memory allocations)
// where MarketAllocation has { IERC4626 id; uint256 assets; }
```

**Correct (check liquidity before reallocating):**

```solidity
// Check available liquidity in each strategy
function getStrategyLiquidity(address strategy) 
    public view returns (uint256) 
{
    // For EVK vaults, check cash available
    try IEVault(strategy).cash() returns (uint256 cash) {
        return cash;
    } catch {
        // For generic ERC-4626, estimate via maxWithdraw
        return IERC4626(strategy).maxWithdraw(address(earn));
    }
}

// Reallocate respecting liquidity
uint256 availableLiquidity = getStrategyLiquidity(fromStrategy);
uint256 toWithdraw = min(desiredAmount, availableLiquidity);

// reallocate takes MarketAllocation[] struct array
// struct MarketAllocation { IERC4626 id; uint256 assets; }
// 
// CRITICAL: The assets field specifies the TARGET allocation, not the delta!
// - assets = 0: Withdraw everything from this strategy
// - assets = N: Leave exactly N assets in this strategy  
// - assets = type(uint256).max: Deposit all available cash into this strategy
//
// Order matters: withdrawals should come before deposits

MarketAllocation[] memory allocations = new MarketAllocation[](2);
allocations[0] = MarketAllocation({
    id: IERC4626(fromStrategy),
    assets: 0  // Target: leave 0 assets (withdraws everything)
});
allocations[1] = MarketAllocation({
    id: IERC4626(toStrategy),
    assets: type(uint256).max  // Target: deposit all available cash
});

earn.reallocate(allocations);
```

**Correct (updating supply queue priority):**

```typescript
// Supply queue determines deposit order
// First strategy gets filled first, then second, etc.

// Current queue: [vaultA, vaultB, vaultC]
// Want to prioritize vaultB for higher yield

const newSupplyQueue = [vaultB, vaultA, vaultC];

await earn.write.setSupplyQueue([newSupplyQueue]);

// Now deposits flow: vaultB (until cap) -> vaultA -> vaultC
```

**Correct (updating withdraw queue for liquidity):**

```solidity
// Withdraw queue determines withdrawal order
// Put most liquid strategies first for user experience

// Get current allocations
uint256[] memory allocations = new uint256[](strategies.length);
for (uint256 i = 0; i < strategies.length; i++) {
    allocations[i] = IERC4626(strategies[i]).balanceOf(address(earn));
}

// updateWithdrawQueue takes uint256[] indexes, NOT addresses
// The indexes represent the new order of the current withdraw queue
// Example: To swap positions 0 and 1 in a 3-element queue: [1, 0, 2]
uint256[] memory newOrder = sortByLiquidityIndexes(strategies);
earn.updateWithdrawQueue(newOrder);
```

**Correct (reducing strategy cap safely):**

```solidity
// To reduce exposure to a strategy:

// Step 1: Reduce cap (instant for curator/owner)
earn.submitCap(IERC4626(riskyStrategy), newLowerCap);
// No timelock for cap reduction!

// Step 2: If over cap, reallocate excess
uint256 currentAllocation = earn.expectedSupplyAssets(IERC4626(riskyStrategy));
if (currentAllocation > newLowerCap) {
    // reallocate takes MarketAllocation[] struct array
    // Set target allocation for risky strategy to the new cap
    MarketAllocation[] memory allocations = new MarketAllocation[](2);
    allocations[0] = MarketAllocation({
        id: IERC4626(riskyStrategy),
        assets: newLowerCap  // Target: reduce to new cap
    });
    allocations[1] = MarketAllocation({
        id: IERC4626(safeStrategy),
        assets: type(uint256).max  // Target: deposit all freed assets
    });
    
    earn.reallocate(allocations);
}
```

**Correct (emergency strategy removal):**

```solidity
// If a strategy is reverting/compromised:

// Step 1: Set cap to 0
earn.submitCap(IERC4626(brokenStrategy), 0);

// Step 2: Submit forced removal (starts timelock)
// Note: Takes IERC4626, not address
earn.submitMarketRemoval(IERC4626(brokenStrategy));

// Step 3: Wait for timelock

// Step 4: After timelock, update withdraw queue with new indexes
// updateWithdrawQueue takes uint256[] indexes to reorder/remove
// To remove an entry, omit its index from the array
// WARNING: Funds in removed strategy are considered lost!
uint256[] memory newIndexes = getQueueWithoutBrokenStrategy();
earn.updateWithdrawQueue(newIndexes);
```

**Correct (monitoring and rebalancing):**

```typescript
interface StrategyMetrics {
  address: Address;
  allocation: bigint;
  apy: number;
  utilization: number;
  liquidity: bigint;
}

async function getStrategyMetrics(
  earn: Address,
  strategy: Address
): Promise<StrategyMetrics> {
  const allocation = await IERC4626(strategy).balanceOf(earn);
  const vaultInfo = await vaultLens.getVaultInfoDynamic(strategy);
  
  return {
    address: strategy,
    allocation,
    apy: vaultInfo.irmInfo.interestRateInfo[0].supplyAPY / 1e25,
    utilization: vaultInfo.totalBorrowed / vaultInfo.totalAssets,
    liquidity: vaultInfo.totalCash,
  };
}

async function optimizeAllocation(earn: Address) {
  const strategies = await earn.withdrawQueue();
  const metrics = await Promise.all(
    strategies.map(s => getStrategyMetrics(earn, s))
  );
  
  // Sort by APY descending
  const byApy = [...metrics].sort((a, b) => b.apy - a.apy);
  
  // Reallocate to higher-yield strategies (respecting caps and liquidity)
  for (const highYield of byApy.slice(0, 3)) {
    // config() returns { balance, cap, enabled, removableAt }
    const strategyConfig = await earn.read.config([highYield.address]);
    const headroom = strategyConfig.cap - highYield.allocation;
    
    if (headroom > MIN_REALLOCATION) {
      // Find lower-yield strategy to pull from
      const lowYield = byApy[byApy.length - 1];
      const moveAmount = min(headroom, lowYield.liquidity);
      
      if (moveAmount > MIN_REALLOCATION) {
        // Reallocate: reduce low yield, increase high yield
        // type(uint256).max in TypeScript = 2n ** 256n - 1n
        const MAX_UINT256 = 2n ** 256n - 1n;
        const allocations = [
          { id: lowYield.address, assets: lowYield.allocation - moveAmount },
          { id: highYield.address, assets: MAX_UINT256 },
        ];
        await earn.write.reallocate([allocations]);
      }
    }
  }
}
```

Key considerations:
- Only allocators/curators/owner can reallocate
- Respect strategy liquidity when withdrawing
- Cap increases are timelocked; decreases are instant
- Monitor strategy APYs and adjust allocations
- Keep some allocation in liquid/idle vault for withdrawals

---

## PublicAllocator: Permissionless Reallocation

PublicAllocator enables anyone to trigger reallocations on EulerEarn vaults within admin-configured flow caps. This allows third parties (bots, keepers, MEV searchers) to optimize allocations without requiring allocator permissions.

**Correct (admin configuring PublicAllocator):**

```solidity
import {IPublicAllocator, FlowCapsConfig, FlowCaps} from "euler-earn/interfaces/IPublicAllocator.sol";

IPublicAllocator publicAllocator = IPublicAllocator(publicAllocatorAddress);

// Only vault owner or PublicAllocator admin can configure
// Set admin for this vault (optional - owner can always configure)
publicAllocator.setAdmin(earnVault, adminAddress);

// Set fee for public reallocations (in wei, paid by caller)
publicAllocator.setFee(earnVault, 0.001 ether);

// Configure flow caps per strategy
// maxIn: max assets that can flow INTO this strategy via public reallocation
// maxOut: max assets that can flow OUT OF this strategy via public reallocation
FlowCapsConfig[] memory configs = new FlowCapsConfig[](2);

configs[0] = FlowCapsConfig({
    id: IERC4626(strategyA),
    caps: FlowCaps({
        maxIn: 100_000e6,   // Allow up to 100k USDC to flow in
        maxOut: 50_000e6    // Allow up to 50k USDC to flow out
    })
});

configs[1] = FlowCapsConfig({
    id: IERC4626(strategyB),
    caps: FlowCaps({
        maxIn: 200_000e6,
        maxOut: 100_000e6
    })
});

publicAllocator.setFlowCaps(earnVault, configs);
```

**Correct (public reallocation by anyone):**

```solidity
import {IPublicAllocator, Withdrawal} from "euler-earn/interfaces/IPublicAllocator.sol";

// Anyone can call reallocateTo if they pay the fee
// This moves assets FROM withdrawal strategies TO a supply strategy

// Step 1: Get the fee
uint256 fee = publicAllocator.fee(earnVault);

// Step 2: Prepare withdrawals (must be sorted by address, ascending)
// Withdrawal struct: { IERC4626 id; uint128 amount; }
Withdrawal[] memory withdrawals = new Withdrawal[](2);
withdrawals[0] = Withdrawal({
    id: IERC4626(lowYieldStrategy),
    amount: 10_000e6  // Withdraw 10k from this strategy
});
withdrawals[1] = Withdrawal({
    id: IERC4626(anotherLowYieldStrategy),
    amount: 5_000e6   // Withdraw 5k from this strategy
});

// IMPORTANT: Withdrawals must be sorted by address (ascending)
// and the supplyId cannot be in the withdrawals array

// Step 3: Execute reallocation (paying the fee)
publicAllocator.reallocateTo{value: fee}(
    earnVault,
    withdrawals,
    IERC4626(highYieldStrategy)  // Deposit all withdrawn assets here
);

// Flow caps are automatically updated:
// - Withdrawn strategies: maxIn increases, maxOut decreases
// - Supply strategy: maxIn decreases, maxOut increases
```

**Correct (TypeScript public reallocation):**

```typescript
import { encodeFunctionData, parseEther } from 'viem';

// Check flow caps before attempting reallocation
const [maxIn, maxOut] = await publicAllocator.read.flowCaps([
  earnVault,
  strategyAddress,
]);

console.log(`Strategy flow caps: maxIn=${maxIn}, maxOut=${maxOut}`);

// Get fee
const fee = await publicAllocator.read.fee([earnVault]);

// Prepare withdrawals (sorted by address!)
const withdrawals = [
  { id: lowYieldStrategy, amount: 10000n * 10n ** 6n },
].sort((a, b) => a.id.toLowerCase().localeCompare(b.id.toLowerCase()));

// Execute public reallocation
await publicAllocator.write.reallocateTo(
  [earnVault, withdrawals, highYieldStrategy],
  { value: fee }
);
```

**Correct (claiming accrued fees as admin):**

```solidity
// Check accrued fees
uint256 accrued = publicAllocator.accruedFee(earnVault);

// Transfer fees to recipient (only admin or vault owner)
publicAllocator.transferFee(earnVault, payable(feeRecipient));
```

**PublicAllocator Key Points:**

| Aspect | Details |
|--------|---------|
| Who can configure | Vault owner or designated admin |
| Who can reallocate | Anyone (permissionless) |
| Fee | Paid in ETH by caller, set per vault |
| Flow caps | Per-strategy limits on in/out flows |
| Sorting | Withdrawals must be sorted by address (ascending) |
| Restrictions | Cannot include supplyId in withdrawals; strategies must be enabled |

**Common Errors:**

```solidity
// IncorrectFee: msg.value doesn't match configured fee
// EmptyWithdrawals: No withdrawals provided
// MarketNotEnabled: Strategy not in earn vault
// InconsistentWithdrawals: Not sorted by address or duplicates
// DepositMarketInWithdrawals: supplyId appears in withdrawals
// MaxOutflowExceeded: Trying to withdraw more than maxOut
// MaxInflowExceeded: Trying to deposit more than maxIn
// NotEnoughSupply: Strategy doesn't have enough assets
```

See also: [Lens Contracts](tools-lens) - EulerEarnVaultLens provides `getVaultInfoFull()` to query all strategies and their allocations.

Reference: [EulerEarn Roles](https://github.com/euler-xyz/euler-earn#roles), [PublicAllocator.sol](https://github.com/euler-xyz/euler-earn/blob/master/src/PublicAllocator.sol)
