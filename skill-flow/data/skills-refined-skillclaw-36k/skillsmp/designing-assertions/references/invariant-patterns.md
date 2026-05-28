# Invariant Patterns

Use these as starting points. Pick the smallest invariant that blocks the exploit path.

## Monotonicity / Ratio Bounds
- Example: share price must not decrease unless a specific event occurs.
- Observation: pre/post `totalAssets`, `totalSupply` or reserves.
- Triggers: call triggers on vault operations or controller entrypoints.

## Reserve Configuration Gating
- Example: supply/borrow only when reserve is active, not paused, not frozen.
- Observation: read config bits (active/frozen/paused/borrowable).
- Triggers: call triggers on supply/borrow/withdraw/repay.

## Caps and Limits
- Example: total supply <= supply cap; total borrow <= borrow cap.
- Observation: pre/post totalSupply and cap values from config.
- Triggers: call triggers on supply/borrow; storage triggers on cap slots.

## Accounting Conservation
- Example: `totalAssets` moves exactly by settled amounts; transfers out are accounted by events.
- Observation: parse events with `getLogs` and compare to post-state.
- Triggers: settlement functions or storage slot changes.
- Notes: if no settlement event fired, expect no change; use `>=` when airdrops/donations are possible.
- If internal accounting increases, actual balances should not decrease in the same transaction.

## Supply vs User Balances
- Example: totalSupply equals sum of user balances (aToken/debt token).
- Observation: compare totalSupply delta to sum of per-call deltas (avoid enumerating accounts).
- Triggers: call triggers on actions that mint/burn the token.

## Rate Limits and Time Windows
- Example: cumulative outflow within a window must not exceed a limit.
- Observation: pre/post cumulative counters + timestamp reset logic.
- Triggers: outflow entrypoints (borrow, redeem, rebalancer).
- Check reset semantics: if window expired, counter resets and timestamp advances; otherwise monotonic.

## Upgradeability and Initialization
- Example: implementation slot changes only by admin; initializers called once.
- Observation: pre/post `ph.load` on EIP-1967 slots; call input checks for upgrade selectors.
- Triggers: storage change on implementation/admin slots or call triggers on upgrade functions.

## Authorization on Sensitive Changes
- Example: implementation slot changes only via ProxyAdmin; mint only by Minter.
- Observation: pre/post `ph.load` on EIP-1967 slots + `getCallInputs` for upgrade or mint selectors.
- Triggers: storage change on the slot or call trigger on upgrade/mint.

## Change-Only-On-Allowed-Actions
- Example: interest rate, virtual balance, or liquidity index only update on specific actions.
- Observation: detect change and whitelist permitted selectors or call paths.
- Triggers: storage trigger on the slot + allowlist check, or call triggers on all modifying actions.

## Solvency / Reserve Coverage
- Example: reserved <= total in pools; vault balance >= cash; gauge rewards balance >= liabilities.
- Observation: post-state view functions; sometimes need loops over reward tokens.
- Triggers: reserve updates, position execution, or storage change on reserve slots.
- Backing ratio: protocol-held backing >= minimum exit coverage (xToken backing).
- Net liability coverage: underlying >= (deposit supply - debt supply).

## Index and Scaled Supply Identities
- Example: `virtualBalance + currentDebt == (scaledATokenSupply + accruedToTreasury) * liquidityIndex`.
- Observation: scaled supply, accruedToTreasury, and normalized income.
- Triggers: reserve updates (supply/borrow/repay/withdraw).

## Index Monotonicity
- Example: interest indexes only increase when time advances.
- Observation: pre/post index with timestamp delta.
- Triggers: reserve‑updating entrypoints.

## Coupling Invariants
- Example: if `totalDebt > 0`, then `baseCollateral > 0`.
- Observation: post-state struct read.
- Triggers: functions that mutate either side of the coupling.

## Cross-Contract Health
- Example: account health must remain healthy across controller vaults.
- Observation: extract affected accounts from call inputs, then check each controller.
- Triggers: call triggers on protocol entrypoints that touch accounts.

## Health-Factor Classification
- Example: only specific actions can decrease HF; healthy → unhealthy transitions only via borrow/withdraw or price/interest.
- Observation: pre/post HF via account data; classify actions as nonIncreasing/nonDecreasing.
- Triggers: action-specific call triggers + price update hooks.
- Allow exceptions for price updates or interest accrual if they are external to user actions.

## Collateral Token Transfer Safety
- Example: transferring collateral tokens should not make the sender unhealthy.
- Observation: pre/post HF of sender; exclude zero-amount and self-transfers.
- Triggers: `transfer`/`transferFrom` on collateral tokens.

## Actor Isolation
- Example: HF changes for actor A do not change HF for unrelated actors.
- Observation: sample non-targeted accounts before/after.
- Triggers: action triggers that touch user balances.

## Position Flags Consistency
- Example: if a user has debt, borrowing flag is true; if no collateral, collateral flag is false.
- Observation: compare user config flags vs balances.
- Triggers: borrow/repay/supply/withdraw.

## Oracle Sanity and Cross-Feed Deviation
- Example: prices must be non-zero, fresh, and within per-symbol deltas.
- Observation: read price + staleness; compare two feeds with a bounded delta.
- Triggers: risk-critical entrypoints (borrow, liquidate, execute).

## Token Integration Safety
- Example: fee-on-transfer, rebasing, missing return values, or low/high decimals.
- Observation: prefer balance deltas over return values; validate decimal assumptions.
- Triggers: transfer/mint/burn entrypoints and accounting updates.

## Mode Exclusivity
- Example: sync deposit allowed only when NAV valid; async otherwise.
- Observation: post-state `isTotalAssetsValid()` or expiration slot.
- Triggers: call triggers on both sync and async entrypoints.

## Mode and Category Restrictions
- Example: borrowable assets in a risk category; switching category keeps HF >= 1.
- Observation: category config + user positions.
- Triggers: category switch and borrow entrypoints.

## Epoch and Lifecycle State Machines
- Example: epoch parity (deposit odd, redeem even), ordering (lastSettled <= current - 2), increment by 0 or 2.
- Observation: packed epoch fields in storage slots; pre/post comparisons.
- Triggers: epoch-mutating entrypoints (settle, update, sync paths).

## Expiration and Lifespan Rules
- Example: `expiration == block.timestamp + lifespan` after settlement; manual expire sets expiration to 0.
- Observation: packed expiration/lifespan slots + `isValid()` flag.
- Triggers: settlement, expire, and update functions.

## Supply/Cap Bounds
- Example: totalSupply <= cap; emissions multiplier within range.
- Observation: post-state reads and optional pre/post comparison.
- Triggers: storage change or call triggers on mint/update functions.

## Exception-Gated Invariants
- Example: share price cannot decrease unless a specific event (bad debt) occurs.
- Observation: pre/post ratio + event scan in the same transaction.
- Triggers: call triggers on protocol entrypoints, with event-based exceptions.

## Timelocks and Cooling Periods
- Example: upgrade or admin actions only after min delay; no rapid multisig threshold changes.
- Observation: pre/post timelock fields + timestamps; call inputs for execute/upgrade.
- Triggers: call triggers on execute/upgrade or storage triggers on delay/threshold slots.

## Grace Periods and Close Factors
- Example: no liquidation during grace period; liquidation must respect close factor and min leftover dust.
- Observation: pre/post user debt/collateral and grace period timestamp.
- Triggers: liquidation entrypoints.
- Bound grace periods to the protocol-defined max and ensure they update after unpause.

## Deficit Management
- Example: deficits only created when collateral is zero; deficit equals burned debt; only on active reserves.
- Observation: pre/post reserve deficit and user debt.
- Triggers: liquidation or deficit-elimination entrypoints.

## Liveness / Exit Guarantees
- Example: full repay succeeds when debt > 0; full withdraw succeeds when no debt.
- Observation: enforce success or state‑no‑change on failure.
- Triggers: repay/withdraw entrypoints.
- Account for sentinel amounts (max uint) meaning "full balance" in the protocol.

## Emergency Pause Modes
- Example: when paused, only withdrawals allowed; balances cannot increase.
- Observation: pre/post pause flag + balance deltas; call inputs for deposit/mint.
- Triggers: call triggers on entrypoints or storage trigger on pause slot.

## AMM Math and Fee Invariants
- Example: constant product maintained; tick stays within bounds; fee only from whitelist.
- Observation: reserve product, tick state, fee slot changes.
- Triggers: storage change on reserve/tick/fee slots; call triggers on swap/mint/burn.

## ERC4626 Accounting
- Example: assets/shares consistency; preview* matches actual; share value monotonic.
- Observation: pre/post assets + supply + preview outputs; call inputs for deposit/withdraw.
- Triggers: call triggers on ERC4626 entrypoints, optional storage trigger on totalSupply.

## Price Liveness and Deviation
- Example: oracle updates within time window; price deviation within bps; intra-tx deviations.
- Observation: post-state timestamp + per-call price checks via forkPostCall.
- Triggers: call triggers on price update or risk-critical functions (borrow/liquidate).

## Intra-Tx Price Stability
- Example: price must not deviate more than X bps from pre-tx during borrow/liquidate.
- Observation: pre-tx baseline + per-call post snapshots.
- Triggers: risk-critical entrypoints and guard hooks.

## Intra-Tx Price Consistency
- Example: oracle returns the same price on repeated reads within a single tx.
- Observation: pre/post read on the same asset; compare exact equality.
- Triggers: borrow/supply/withdraw/flashloan entrypoints.

## Flashloan Safety
- Example: pool balance after >= pre + fee; fail if amount+fee not returned.
- Observation: pre/post pool balance; fee computation.
- Triggers: flashloan entrypoints.

## Drain and Outflow Limits
- Example: per-tx outflow capped; large transfers only to whitelisted recipients.
- Observation: pre/post balance delta; optional recipient allowlist via call inputs.
- Triggers: balance trigger for ETH; call triggers on transfer/withdraw.

## Rounding and Proportionality
- Example: withdrawals reduce balances proportional to shares burned.
- Observation: per-call pre/post balances with dynamic tolerance (bps + min 1 wei).
- Triggers: call triggers on withdraw/redeem; use forkPreCall/forkPostCall.

## First-Depositor and Exchange-Rate Floors
- Example: minimum supply after market open; deposit must mint >0 shares.
- Observation: pre/post totalSupply, exchange rate, and deposit amount.
- Triggers: call triggers on deposit/mint or storage trigger on totalSupply slot.
- Use protocol-specific conversion formulas (e.g., virtual deposits) to avoid false positives.

## Phantom Collateral and Value Bounds
- Example: reported collateral/AUM cannot exceed actual extractable value.
- Observation: compare view-reported value vs real token balances + oracle rate.
- Triggers: call triggers on valuation-sensitive entrypoints.

## Configuration and Parameter Bounds
- Example: oracle staleness, price delta, emission multipliers, or timelock delays stay within safe ranges.
- Observation: decode config setter inputs and validate post-state matches.
- Triggers: call triggers on config setters; avoid global storage triggers when possible.
