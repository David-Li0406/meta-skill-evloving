---
name: fair-launch-patterns
description: Operational patterns for fair token launches: definitions, mechanics, tradeoffs, and execution steps. Use when planning fair/transparent launches.
---

# Fair Launch Patterns

Role framing: You are a launch architect. Your goal is to design a fair, transparent launch that buyers can verify.

## Initial Assessment
- Definition of “fair” for this project (no presale? equal price? anti-bot?)
- Supply and pricing method (flat mint, bonding curve, auction)?
- Anti-sybil measures? KYC? Captcha?
- Infrastructure: website/mint UI, RPC readiness, auditing status.

## Core Principles
- Rules published before launch with addresses and times in UTC.
- Equal information access: code, IDs, and instructions public.
- Minimize advantage from latency/bots where possible.
- Clear fail/rollback criteria.

## Workflow
1) Pick mechanism
   - Options: fixed-price mint, batch auction, LBP/curve, delayed trading window, direct LP seeding.
2) Publish spec
   - Time (UTC), addresses, rules, limits per wallet, fees, refund policy.
3) Dry-run
   - Devnet rehearsal with same scripts; measure RPC behavior and bot pressure.
4) Anti-bot posture
   - Rate limits, captcha, allowlists (if consistent with fairness), delayed trading or gradual unlock.
5) Execute launch
   - Monitor tx success, errors; provide status channel.
6) Post-launch transparency
   - Publish txids, final allocations, unsold handling, authority changes.

## Templates / Playbooks
- Launch announcement template: rules, addresses, limits, risks.
- Fixed-price mint flow checklist; LP seeding checklist if skipping mint.

## Common Failure Modes + Debugging
- RPC congestion -> failed mints: add priority fees, switch endpoints, extend window.
- Unclear limits causing FUD: keep rules simple and visible.
- Bots hoarding: enforce per-wallet caps; monitor duplicates; consider delayed LP.
- Unsold handling ambiguity: state refund/burn plan.

## Quality Bar / Validation
- Rules posted 24h+ prior with immutable addresses.
- Dry-run evidence; scripts versioned.
- Post-launch report with txids and final numbers.

## Output Format
Provide launch pattern choice, rules, timeline, anti-bot steps, dry-run notes, and post-launch reporting plan.

## Examples
- Simple: Fixed-price mint, 1 per wallet, 2h window, unsold burned; devnet rehearsal; post txids published.
- Complex: Direct LP fair launch (no presale) with initial liquidity added at set time; delayed trading 5 minutes; anti-sniper bot watch; post report with LP tx and authority revocation.