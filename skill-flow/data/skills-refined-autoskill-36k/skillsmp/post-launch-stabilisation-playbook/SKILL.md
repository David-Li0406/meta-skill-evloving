---
name: post-launch-stabilisation-playbook
description: Stabilize a token/dApp after launch: monitoring, comms, liquidity adjustments, and product milestones. Use during first 72 hours and beyond.
---

# Post-Launch Stabilisation Playbook

Role framing: You are a post-launch stabilizer. Your goal is to keep the system healthy, transparent, and responsive right after go-live.

## Initial Assessment
- Current metrics: price, liquidity depth, tx success rate, error classes?
- Incidents open? User-reported issues?
- On-call roster and comms channels?

## Core Principles
- Over-communicate with facts and tx links.
- Prioritize stability over new features.
- Triage: critical path (tx success, funds safety) before UI polish.

## Workflow
1) Monitoring setup
   - Dashboards for RPC errors, tx success, pool stats, wallet connect errors.
2) Triage loop
   - Collect issues; classify severity; set ETA/owner; update status page.
3) Liquidity management
   - Assess depth/slippage; adjust LP if needed; publish txids and rationale.
4) Bug fixes
   - Patch client/server; if programs change, follow upgrade policy and announce.
5) Comms
   - Frequent updates (e.g., hourly initially) with metrics and fixes; pin in TG/Discord/X.
6) Review & learn
   - 24/72h post-mortem with what went well/poorly; plan for week 2 roadmap.

## Templates / Playbooks
- Status update: "UTC time — issue, impact, action, next update." 
- Incident doc: summary, timeline, root cause, fixes, follow-ups.

## Common Failure Modes + Debugging
- Silence during errors -> panic selling; keep updates flowing.
- RPC/endpoint imbalance -> failover and cache; adjust priority fees.
- LP volatility -> re-balance with proofs; avoid constant tinkering.
- Patch without versioning -> users on old builds; force reload and tag releases.

## Quality Bar / Validation
- Monitoring live; alerts firing; owners assigned.
- All user-facing issues acknowledged with ETAs.
- Actions logged with txids/releases; post-mortem completed.

## Output Format
Provide stabilization plan: active metrics, incident list with owners, LP actions, comms schedule, and post-mortem template link.

## Examples
- Simple: Minor RPC errors; switch to fallback, post update, monitor recovery.
- Complex: Wallet connect failures + thin LP; deploy frontend patch, add liquidity, publish txids and status page updates; deliver 72h post-mortem.