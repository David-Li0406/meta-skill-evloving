# Lending Protocol Invariant Checklist

Use this checklist to map invariants for pool/lending protocols without anchoring to a single implementation.

## Reserve and Config Gating
- Reserve active/not paused/not frozen for supply/withdraw/borrow/repay.
- Borrowable/supplyable flags enforced.
- Supply cap and borrow cap respected.
- Grace period bounded by protocol max and updated after unpause/config changes.

## Accounting and Indexing
- Deposit token and debt token supply deltas match per‑call mint/burn deltas.
- Underlying balance covers net liability (deposit supply - debt supply).
- Virtual accounting <= actual balances.
- Index identities hold (scaled supply * index + accrued to treasury).
- Indexes are monotonic when time advances.

## Health Factor and Risk
- Health factor safe/unsafe transitions restricted to expected actions.
- Only specific actions can decrease HF (borrow/withdraw/price/interest).
- Actor isolation: unrelated users’ HF should not change.

## Borrow/Repay Liveness
- Full repay should always succeed when reserve is active.
- Full withdraw should succeed when user has no debt.
- Borrow requires sufficient collateral and liquidity.
- Identify any sentinel amounts (max uint) that represent "full balance."

## Liquidation Rules
- Liquidation only if HF < threshold.
- Respect grace period, close factor, and min‑leftover dust bounds.
- Post‑liquidation HF improves and remains >= threshold when required.

## Deficit Management
- Deficit only created when collateral is zero.
- Deficit equals burned debt and only on active reserves.
- Deficit reduction only via authorized burn/repay paths.

## Mode/Category Restrictions
- Category (e.g., risk mode) borrowable assets enforced.
- Switching category keeps HF >= 1.
- Exposure cannot increase if asset becomes unborrowable in the category.

## Oracle Requirements
- Price non‑zero, consistent within a tx, and within deviation bounds across tx.
- Staleness bounds enforced where supported.

## Flashloan Safety
- Pool balance after >= pre + fee; fail if not repaid.
- Flashloan only allowed when reserve active/not paused.

## Token Transfer Safety
- Transfer/transferFrom of deposit tokens must not make sender unhealthy.
- Exclude zero-amount transfers and self-transfers from HF checks.

## Timelock and Governance Queue
- Timelocked config changes require a prior submit and are not executable before `executableAt`.
- Timelock executions clear `executableAt` (no reuse).
- Revokes clear pending actions; submit rejects duplicate pending data.

## Vault Caps and Allowances
- Cap setters are monotonic (increase-only or decrease-only) and bounded by protocol max (e.g., relative cap <= 1e18).
- Allowance deltas match token flows (withdraw/redeem/transferFrom reduce allowance unless unlimited).
- Permit increments nonce by 1 and sets allowance to signed value.
