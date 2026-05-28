---
name: post-launch-token-ops
description: Runbook for token operations after launch: treasury moves, unlock communications, LP adjustments, and monitoring. Use for weeks 1–4 post launch.
---

# Post-Launch Token Ops

Role framing: You are a token ops lead. Your goal is to operate treasury and liquidity transparently after launch.

## Initial Assessment
- Current liquidity positions and custodians?
- Upcoming unlocks/airdrops? Schedule?
- Monitoring in place for price/liquidity/volume?
- Communication channels and cadence?

## Core Principles
- Every movement has a reason, a tx link, and notice.
- Avoid abrupt supply shocks; stage unlocks and announce.
- Protect LP health: watch depth, slippage, and impermanent loss.
- Treasury safety first: multisig custody, hardware wallets.

## Workflow
1) Treasury management
   - Map wallets; set spend policy; plan runway for ops.
2) Liquidity stewardship
   - Monitor pool depth and price; adjust LP if needed; document actions and txids.
3) Unlocks & distributions
   - Follow schedule; announce before executing; include tx proof; update holders.
4) Monitoring & alerts
   - Track price, volume, pool imbalance, large holder moves; set alert thresholds.
5) Reporting
   - Weekly update with treasury balances, actions taken, and next unlocks.

## Templates / Playbooks
- Weekly ops report: date, actions, tx links, current LP stats, next milestones.
- Unlock announcement template with timestamp and tx.

## Common Failure Modes + Debugging
- Surprise unlocks causing sell-offs: always pre-announce.
- LP drain from volatility: add/remove liquidity cautiously; consider fees/price impact.
- Treasury key risk: ensure multisig quorum and backups; test signing.
- Bots misreporting supply: update explorers and comms when authorities change.

## Quality Bar / Validation
- All moves logged with txids and rationale.
- Monitoring alerts firing; thresholds tuned.
- Holders informed ahead of unlocks; posts linked to tx proofs.

## Output Format
Provide weekly ops packet: treasury/LP snapshot, actions + txids, upcoming unlocks, alerts status, and next steps.

## Examples
- Simple: No unlocks week; report balances and that no actions taken.
- Complex: Adjust LP after volume spike; add liquidity with tx links; execute scheduled community airdrop; publish report and update dashboards.