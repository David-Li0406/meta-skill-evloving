# Invariant Mapping Workflow

## Step 1: Protocol Map
- **Assets**: tokens, vault balances, reserves, accounting units.
- **Roles**: owner/admin/timelock, guardians, rebalancer EOAs, oracles.
- **Entrypoints**: external functions that move value or modify critical state.
- **Critical state**: totals, exchange rates, health factors, caps, expirations, epoch/mode flags.
- **Routers**: batch/call hubs and controller contracts that centralize flows.
- **Config setters**: oracle configs, limits, timelock delays, lifespans.

## Step 1.5: Evidence Sources
- Protocol specs, docs, and whitepapers.
- Audit reports and invariant test suites.
- Existing production assertions or incident postmortems.
- Tests that encode invariants as constants or comments (e.g., `tests/invariants/specs`).

## Step 2: Invariant Inventory (by category)
- **Access control**: only authorized upgrades, minting, role changes.
- **Accounting**: balance deltas match events and internal counters.
- **Pricing**: oracle liveness, deviation bounds, cross‑feed sanity.
- **Solvency**: reserves/borrowed/collateral relationships.
- **Limits**: caps, rate limits, timelock delays, emissions bounds.
- **Modes**: pause/upgrade/deposit modes are mutually exclusive.
- **State machines**: epochs, ordering, parity, and lifecycle transitions.
- **Cross‑contract**: routing or controller invariants across modules.
- **Health factor**: classify actions by HF impact; define safe/unsafe transitions.
- **Deficit management**: deficit creation, accounting, and elimination rules.
- **Position flags**: config flags reflect actual debt/collateral positions.

## Step 3: Exceptions
Examples:
- Bad‑debt socialization can allow share‑price decreases.
- Emergency mode allows withdrawals but blocks deposits.
- Initial epochs can permit calibration outside bounds.

## Step 4: Observation Plan
Decide how to observe each invariant:
- **State**: pre/post values, storage slots, mapping entries.
- **Logs**: Transfer/Withdraw/Borrow/Deposit events for accounting.
- **Call inputs**: decode parameters and verify outcomes.
- **Call frames**: per‑call checks with `forkPreCall`/`forkPostCall`.
- **Slots**: unstructured storage and packed fields when no getter exists.
- **Downstream calls**: verify that external calls actually occur.
- **Packed calldata**: decode using protocol‑specific packing logic (assetId, amount, mode).

## Step 5: Trigger Plan
- **Call triggers**: for specific operations (withdraw, liquidate, upgrade).
- **Storage triggers**: for slots that can change via multiple paths.
- **Balance triggers**: for ETH outflows.
- **Before hooks**: trigger on guard/validator functions that pre‑check actions.
- **Router batches**: plan for nested calldata decoding and call dedupe.
- **Global postconditions**: if invariant applies after any action, trigger at the chokepoint.

## Step 6: Coverage Matrix
For each invariant:
- **Where it runs** (selector/slot/balance).
- **What it reads** (state/logs/inputs).
- **Exceptions** (explicit checks).
- **Priority** (P0/P1/P2).
- **Gas risk** (loop sizes, per‑call forking, log scans).
