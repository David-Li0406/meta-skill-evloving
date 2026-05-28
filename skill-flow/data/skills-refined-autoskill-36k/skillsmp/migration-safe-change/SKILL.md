---
name: migration-safe-change
description: Safety checklist for DB/API changes covering compatibility, rollout, backout, and observability
---

# Migration-Safe Change

Use when altering schemas, migrations, or public APIs.

## Steps
1) Understand change
- What breaks if old/new versions coexist? Identify clients and data paths

2) Compatibility plan
- Prefer additive changes; keep old fields/routes until clients updated
- Default values, nullability, indexes, constraints; handle backfill

3) Migration plan
- Idempotent migration script; handles retry
- Data backfill strategy (batching, throttling); measure impact

4) Rollout/backout
- Deploy order: migration → app → cleanup
- Backout: stop new writes, rollback app, rollback/patch data if safe

5) Observability
- Metrics/logs for error rates, latency, bad rows, missing fields
- Add temporary logging/feature flag if needed

6) Testing
- Apply migration on a copy/snapshot if possible
- Minimal regression checks for impacted queries/routes

## Outputs
- Plan summary (compat, rollout, backout)
- Risks and mitigations
- Test/validation steps run (or not possible)
- Follow-ups (remove old paths, drop columns later)

## When to stop and ask
- Unclear client list or data shape
- Non-idempotent migration required
- Irreversible data change without backup
