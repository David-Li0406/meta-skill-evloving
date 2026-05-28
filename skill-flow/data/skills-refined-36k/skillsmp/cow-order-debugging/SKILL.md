---
name: cow-order-debugging
description: Load when debugging CoW Protocol limit orders that aren't filling, investigating flash loan settlement failures, or troubleshooting EIP-1271 signature issues
---

# CoW Order Debugging

This skill covers how to debug Kapan's CoW Protocol limit orders, from order creation through settlement.

## Architecture Overview

```
User → MultiplyEvmModal → useCowOrder → KapanOrderManager → ComposableCoW
                                              ↓
                              KapanOrderHandler (generates GPv2 orders)
                                              ↓
                              CoW Watchtower (monitors & submits)
                                              ↓
                              FlashLoanRouter → KapanCowAdapter → Settlement
```

## Key Contracts (Base)

| Contract | Address | Purpose |
|----------|---------|---------|
| KapanOrderManager | `0x12F80f5Fff3C0CCC283c7b2A2cC9742ddf8c093A` | Stores order context, executes hooks |
| KapanOrderHandler | `0x9a503a4489ebeb2e6f13adcd28f315e972b63371` | IConditionalOrder - generates GPv2 orders |
| KapanCowAdapter | `0xF6342053a12AdBc92C03831BF88029608dB4C0B6` | Flash loan borrower, funds OrderManager |
| KapanRouter | `0xFA3B0Efb7E26CDd22F8b467B153626Ce5d34D64F` | Executes lending operations |

## Orders Not Reaching Solvers (Autopilot Filtering)

**Symptom**: Order shows as "open" on CoW Explorer but never fills, even for liquid pairs.

### The Two Receiver Concepts

CoW Protocol has TWO different "receiver" fields that serve different purposes:

1. **`appData.metadata.flashloan.receiver`** - Used by CoW API for balance override validation during order submission
2. **`GPv2Order.receiver`** - Used by autopilot to decide whether to skip balance filtering before sending to solvers

### The Autopilot Balance Filtering Gap

CoW Protocol's autopilot has a gap in flash loan handling:

- **API validation** (`orderbook` crate): Correctly uses `flashloan.receiver` from appData for balance override
- **Autopilot** (`solvable_orders.rs`): Ignores flashloan metadata entirely, only skips balance filtering when `GPv2Order.receiver == Settlement`

```rust
// CoW autopilot hack - only skips balance check if receiver is Settlement
if order.data.receiver.as_ref() == Some(&settlement_contract) {
    return true;  // Skip balance filtering - TODO: replace with proper detection
}
```

### What This Means for Kapan

- Our `GPv2Order.receiver = OrderManager` (set by KapanOrderHandler) - THIS IS CORRECT
- Autopilot runs balance check on OrderManager
- OrderManager doesn't have tokens pre-flash-loan
- Orders may get filtered out before reaching solvers (not always)

### CRITICAL: Do NOT Change GPv2Order.receiver

**NEVER set `GPv2Order.receiver = Settlement`** for flash loan orders. This was tried and it BREAKS the flow:

1. With `receiver = Settlement`, buyToken goes to Settlement after swap
2. But `_executePostHook()` checks `balanceOf(address(this))` at OrderManager
3. OrderManager has 0 buyToken because it went to Settlement
4. Post-hook fails!

The `appData.metadata.flashloan.receiver` is different - that's for CoW API balance validation, NOT for the GPv2Order.

### Autopilot Filtering Reality

In practice, autopilot filtering is not as aggressive as feared. Orders with flash loan metadata usually get through because:
1. The appData.flashloan tells solvers to use flash loans
2. Solvers that support flash loans will pick up the order
3. The order may take longer to fill but will eventually fill for liquid pairs

If orders aren't filling, check other causes first (token liquidity, solver routing, etc.).

## Exotic Token Routing (GHO, PT Tokens)

**Symptom**: Orders for GHO, Pendle PT tokens, or other exotic assets never fill.

### Why This Happens

Standard CoW solvers focus on high-volume pairs (WETH/USDC/USDT/DAI). They may not have routes for:
- **GHO**: Aave's stablecoin, limited DEX liquidity (Balancer, some Curve)
- **PT tokens**: Pendle principal tokens, very niche (Pendle AMM only)
- Other low-liquidity or specialized tokens

### Diagnosis

If orders for common pairs (WETH → USDC) fill but exotic pairs don't, it's a solver routing issue, not balance filtering.

### Options

1. **Wait for liquidity** - As tokens get more DEX depth, solvers add routes
2. **Custom solver** - Run a solver with 1inch/Paraswap integration for better routing
3. **Different token** - Use more liquid alternatives if available

## Common Failure Points

### 1. OrderHandler Not Set

**Symptom**: `createOrder` reverts with `InvalidHandler()`

**Check**:
```bash
cast call <OrderManager> "orderHandler()" --rpc-url <RPC>
# Should NOT be 0x0000...0000
```

**Fix**: Run `npx hardhat deploy --tags KapanOrderHandler --network <chain>`

### 2. Order Not Registered on ComposableCoW

**Symptom**: Order created but watchtower ignores it

**Check**:
```bash
# Get order hash from OrderManager logs
cast logs --from-block <block> --address <OrderManager> --rpc-url <RPC>

# Verify on ComposableCoW
cast call 0xfdaFc9d1902f4e0b84f65F49f244b32b31013b74 \
  "singleOrders(address,bytes32)(bool)" <OrderManager> <cowOrderHash> --rpc-url <RPC>
```

### 3. EIP-1271 Signature Invalid

**Symptom**: `GPv2: invalid eip1271 signature`

**Cause**: Order parameters in signature don't match what handler returns

**Debug**:
1. Get the order from handler:
```typescript
const [order, sig] = await composableCoW.getTradeableOrderWithSignature(
  orderManagerAddr, cowParams, "0x", []
);
```
2. Compare with what you're passing to `settle()`
3. `receiver` must ALWAYS be OrderManager (for both flash loan and non-flash-loan orders)
4. If receiver is anything else, post-hook will fail

### 4. Missing Token Approval (PullToken fails)

**Symptom**: `ErrorNotEnoughAllowance()` (selector: `0xc2139725`)

**Check**:
```bash
cast call <token> "allowance(address,address)(uint256)" <user> <router> --rpc-url <RPC>
```

**Cause**: Frontend didn't execute approval transaction before/during order creation

**Debug flow**:
1. Check `authorizeInstructions` returns approval call:
```typescript
const [targets, data] = await router.authorizeInstructions([pullInstruction], userAddress);
```
2. Verify approval is in the transaction batch
3. Check if approval was actually executed on-chain

### 5. Flash Loan Lender Not Configured

**Symptom**: Adapter reverts on flash loan callback

**Check**:
```bash
cast call <Adapter> "allowedLenders(address)(bool)" <lenderAddress> --rpc-url <RPC>
cast call <Adapter> "getLenderType(address)(uint8)" <lenderAddress> --rpc-url <RPC>
# Type: 1=Aave, 2=Morpho
```

## Known Issues / TODOs

### `isFlashLoanOrder` Flag Purpose

The `KapanOrderParams` struct has an `isFlashLoanOrder` boolean. This flag is used for:
1. **Frontend logic** - Determines instruction building flow
2. **OrderManager state** - Tracks that this is a flash loan order

**IMPORTANT**: The `isFlashLoanOrder` flag does NOT change `GPv2Order.receiver`. Receiver is ALWAYS OrderManager because:
- OrderManager._executePostHook() needs the bought tokens at `address(this)`
- Setting receiver to Settlement would break this flow

```solidity
// KapanOrderHandler.sol - CORRECT, DO NOT CHANGE
address receiver = address(orderManager);  // ALWAYS OrderManager
```

**Status**: Working as intended. Do not change receiver logic.

## Decoding Order Instructions

Use `scripts/decode-order.ts` to inspect stored order:

```bash
FORK_CHAIN=base MAINNET_FORKING_ENABLED=true npx hardhat run scripts/decode-order.ts --network hardhat
```

Key things to verify:
- PullToken user matches order creator
- PushToken target is KapanCowAdapter (for flash loan repayment)
- Borrow amount matches flash loan + fee
- DepositCollateral uses correct market context

## Testing Real Orders

The test file `test/v2/CowRealFlow.fork.ts` can simulate settling real orders:

```bash
FORK_CHAIN=base MAINNET_FORKING_ENABLED=true FORK_BLOCK=latest \
  npx hardhat test test/v2/CowRealFlow.fork.ts --grep "<order-id>"
```

### Test Structure

1. **Direct settle** (bypasses flash loan, better errors):
```typescript
await settlement.connect(solver).settle(tokens, prices, [trade], interactions);
```

2. **Full flash loan flow**:
```typescript
await flashLoanRouter.connect(solver).flashLoanAndSettle(loans, settlementCalldata);
```

If direct settle works but flash loan fails, the issue is in the flash loan callback chain.

### Flash Loan Settlement Test

`test/v2/CowFlashLoanSettlement.fork.ts` tests the full flash loan flow:
- Uses `receiver = OrderManager` (the correct production setting)
- Simulates solver behavior with pre-fund and interactions
- Verifies the complete flash loan → swap → post-hook → repay flow

Note: The test manually builds settlement calldata because it's testing what solvers do. Production orders go through Watchtower → Solvers who build the settlement.

## Hook Execution Flow

**Pre-hooks** (executed before swap):
1. `fundOrder(token, recipient, amount)` on Adapter - transfers flash-loaned tokens to OrderManager
2. `executePreHookBySalt(user, salt)` on OrderManager - runs pre-instructions (usually empty for flash loan orders)

**Post-hooks** (executed after swap):
1. `executePostHookBySalt(user, salt)` on OrderManager - runs post-instructions:
   - PullToken (user's margin)
   - Add (combine swap output + margin)
   - Approve (for lending protocol)
   - DepositCollateral (to Morpho/Aave)
   - Borrow (to repay flash loan)
   - PushToken (send borrowed tokens to Adapter for repayment)

## Flash Loan Repayment

For Morpho flash loans, the Adapter must have the borrowed amount + 0 fee (Morpho is free) to repay.

The post-hook borrows from user's position and pushes to Adapter:
```
User's Morpho Position → Borrow WETH → PushToken → KapanCowAdapter → repay Morpho
```

## Debugging Console Logs

The contracts have `console.log` statements. In fork tests:
```
fundOrder: START
fundOrder: amount = 18399910693677945
fundOrder: recipient = 0x12f80f5fff3c0ccc283c7b2a2cc9742ddf8c093a
fundOrder: adapter balance = 18399910693677945
fundOrder: COMPLETE
```

If you see `_executePostHook: router call FAILED with low-level error`, decode the selector:
```bash
cast 4byte <selector>
```

## Key Files

- `packages/hardhat/contracts/v2/cow/KapanOrderManager.sol` - Order storage and hook execution
- `packages/hardhat/contracts/v2/cow/KapanOrderHandler.sol:90` - GPv2 order generation (receiver logic)
- `packages/hardhat/contracts/v2/cow/KapanCowAdapter.sol` - Flash loan handling
- `packages/nextjs/hooks/useCowOrder.tsx` - Frontend order creation
- `packages/nextjs/components/modals/MultiplyEvmModal.tsx` - UI and instruction building
- `packages/nextjs/utils/cow/appData.ts:417` - AppData flashloan.receiver setting
- `packages/hardhat/test/v2/CowRealFlow.fork.ts` - Integration tests
- `packages/hardhat/test/v2/CowFlashLoanSettlement.fork.ts` - Flash loan with receiver=Settlement test

## Quick Diagnosis Checklist

1. [ ] OrderHandler set on OrderManager?
2. [ ] Order registered on ComposableCoW?
3. [ ] AppData registered with CoW API?
4. [ ] User approved Router for margin token?
5. [ ] User has credit delegation for borrow?
6. [ ] Flash loan lender allowed on Adapter?
7. [ ] VaultRelayer approved for sell token?
8. [ ] Is token exotic (GHO, PT)? May need custom solver
9. [ ] Flash loan order? Check autopilot filtering section
