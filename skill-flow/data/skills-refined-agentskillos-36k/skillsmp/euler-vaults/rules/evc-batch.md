---
title: Batch Multiple Operations Atomically
impact: CRITICAL
impactDescription: Gas savings and atomic execution of complex DeFi operations
tags: evc, batch, atomic, multicall, gas
---

## Batch Multiple Operations Atomically

The EVC's batch function allows executing multiple operations in a single transaction. This provides atomicity (all succeed or all fail), gas savings, and deferred liquidity checks.

**Incorrect (separate transactions for each operation):**

```solidity
// Multiple transactions = higher gas, not atomic, potential for partial failure
IEVC(evc).enableCollateral(account, collateralVault);  // Tx 1
IEVault(collateralVault).deposit(amount, account);      // Tx 2
IEVC(evc).enableController(account, borrowVault);       // Tx 3
IEVault(borrowVault).borrow(borrowAmount, account);     // Tx 4
// If Tx 4 fails, Tx 1-3 already executed!
```

**Correct (batch all operations atomically):**

```solidity
IEVC.BatchItem[] memory items = new IEVC.BatchItem[](4);

// Item 1: Enable collateral
// NOTE: When target is EVC itself, onBehalfOfAccount MUST be address(0)
items[0] = IEVC.BatchItem({
    onBehalfOfAccount: address(0),
    targetContract: address(evc),
    value: 0,
    data: abi.encodeCall(IEVC.enableCollateral, (account, collateralVault))
});

// Item 2: Deposit collateral (vault call - use account)
items[1] = IEVC.BatchItem({
    onBehalfOfAccount: account,
    targetContract: collateralVault,
    value: 0,
    data: abi.encodeCall(IEVault.deposit, (amount, account))
});

// Item 3: Enable controller (EVC call - use address(0))
items[2] = IEVC.BatchItem({
    onBehalfOfAccount: address(0),
    targetContract: address(evc),
    value: 0,
    data: abi.encodeCall(IEVC.enableController, (account, borrowVault))
});

// Item 4: Borrow (vault call - use account)
items[3] = IEVC.BatchItem({
    onBehalfOfAccount: account,
    targetContract: borrowVault,
    value: 0,
    data: abi.encodeCall(IEVault.borrow, (borrowAmount, account))
});

// Execute all atomically - liquidity check deferred to end
IEVC(evc).batch(items);
```

**Correct (TypeScript with viem):**

```typescript
import { encodeFunctionData } from 'viem';

const batchItems = [
  // EVC calls: onBehalfOfAccount must be address(0)
  {
    onBehalfOfAccount: '0x0000000000000000000000000000000000000000',
    targetContract: evcAddress,
    value: 0n,
    data: encodeFunctionData({
      abi: evcABI,
      functionName: 'enableCollateral',
      args: [account, collateralVault],
    }),
  },
  // Vault calls: use the actual account
  {
    onBehalfOfAccount: account,
    targetContract: collateralVault,
    value: 0n,
    data: encodeFunctionData({
      abi: eVaultABI,
      functionName: 'deposit',
      args: [depositAmount, account],
    }),
  },
  // ... more items
];

const tx = await evc.write.batch([batchItems]);
```

**Correct (flash loan style - borrow before collateral):**

```solidity
// Deferred checks allow temporarily invalid states!
// Borrow first, deposit collateral second - works in batch
IEVC.BatchItem[] memory items = new IEVC.BatchItem[](4);

items[0] = IEVC.BatchItem({
    onBehalfOfAccount: address(0),  // EVC call - must be address(0)
    targetContract: address(evc),
    value: 0,
    data: abi.encodeCall(IEVC.enableController, (account, borrowVault))
});

items[1] = IEVC.BatchItem({
    onBehalfOfAccount: account,
    targetContract: borrowVault,
    value: 0,
    data: abi.encodeCall(IEVault.borrow, (borrowAmount, account))
});

// Use borrowed funds to get collateral (e.g., swap)
items[2] = IEVC.BatchItem({
    onBehalfOfAccount: account,
    targetContract: swapRouter,
    value: 0,
    data: abi.encodeCall(ISwapRouter.swap, (/* params */))
});

// Deposit collateral - now account is healthy
items[3] = IEVC.BatchItem({
    onBehalfOfAccount: account,
    targetContract: collateralVault,
    value: 0,
    data: abi.encodeCall(IEVault.deposit, (collateralAmount, account))
});

// Liquidity check happens AFTER all operations
IEVC(evc).batch(items);
```

Key benefits:
- Atomic execution - all or nothing
- Gas savings - single transaction overhead
- Deferred liquidity checks - temporary violations allowed
- Can interact with any contract, not just vaults

Reference: [EVC Whitepaper - Batch](https://github.com/euler-xyz/ethereum-vault-connector/blob/master/docs/whitepaper.md#batch)
