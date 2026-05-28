# Protocol Example Patterns

Use these as inspiration when mapping invariants.

## Ethereum Vault Connector (EVC)
- Share price monotonicity with bad‑debt exception.
- Exchange‑rate spike bounds (±5%).
- Vault balance ≥ internal cash accounting.
- Asset transfers accounted by Withdraw/Borrow/Deposit events.
- Account health must not degrade after EVC calls (batch/call/controlCollateral).
- Note: decode nested batch/call payloads to extract real targets and accounts.
- Use `getAllCallInputs` for delegatecall batches; dedupe accounts/vaults.

## Lagoon v0
- Sync vs async deposit mode exclusivity.
- NAV validity lifecycle: expiration, lifespan, manual expire.
- Epoch isolation: syncDeposit does not affect epoch counters.
- Uses unstructured storage offsets for packed NAV metadata.
- Epoch parity, settlement ordering, and epoch increment bounds.
- Silo balance consistency via event‑based deltas.

## Myx v2
- Order fill bounds: filledSize ≤ size.
- Pool reserve solvency: reserved ≤ total.
- Transaction‑level collateral accounting (net deltas).
- Debt‑collateral coupling: debt implies collateral.
- Use `staticcall` to read getters missing from interfaces.

## Malda Lending
- Outflow limiter: cumulative USD outflows within a window.
- Oracle config bounds: staleness, max deltas, per‑symbol limits.
- Rebalancer allowlists + transfer size limits + rate limits.
- Oracle price sanity and cross‑feed deviation on borrow.
- Uses downstream call verification for bridge sends.
- Borrow index monotonicity gated by accrual timestamps.
- Time‑window reset invariants for cumulative limits.
- Liquidity preconditions via `before*` guard hooks.

## Etherex
- Timelock min delay.
- Emissions multiplier bounds by epoch.
- Authorized minting only by Minter.
- Proxy admin ownership and upgrade authorization.
- Constant product k non‑decrease for AMMs.
- Gauge reward solvency against liabilities.
- Backing ratio constraints (xREX).

## Lending Protocols (Generic)
- Interest-bearing token supply deltas match per‑call mint/burn deltas (no full user enumeration).
- Underlying balance covers net liability (deposit token supply - debt token supply).
- Virtual accounting <= actual; index identities use scaled supply and normalized income.
- Reserve config gating: active/frozen/paused/borrowable + supply/borrow caps.
- Health factor classification: only specific actions can decrease HF; safe→unsafe transitions are restricted.
- Actor isolation: user HF changes do not affect unrelated users.
- Liquidation: grace period, close factor, and dust/min‑leftover bounds.
- Deficit rules: only created when collateral is zero; deficit equals burned debt; only on active reserves.
- Category modes (e.g., e‑mode): assets must be borrowable in category; HF >= 1 after switching.
- Oracle: price consistency within tx and bounded deviation across tx.
