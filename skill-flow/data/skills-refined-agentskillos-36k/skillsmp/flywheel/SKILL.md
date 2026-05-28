---
name: flywheel
description: 'Knowledge flywheel health monitoring. Checks velocity, pool depths, staleness. Triggers: "flywheel status", "knowledge health", "is knowledge compounding".'
---

# Skill: Flywheel

> Monitor knowledge compounding. Is the flywheel spinning?

## Triggers

- `/flywheel`
- "knowledge health"
- "flywheel status"
- "is knowledge compounding"
- "check knowledge velocity"

## Synopsis

```bash
/flywheel                # Full health report
/flywheel --velocity     # Just velocity metrics
/flywheel --pools        # Just poao depths
/flywheel --stale        # Just staleness check
```

## What It Does

1. **Measure** - Calculate knowledge velocity
2. **Assess** - Check poao health
3. **Detect** - Find stale or orphaned knowledge
4. **Report** - Provide actionable insights

## The Flywheel Model

```
Sessions → Transcripts → Forge → Poao → Promote → Knowledge
     ↑                                               │
     └───────────────────────────────────────────────┘
                    Future sessions find it
```

**Velocity** = Rate of knowledge flowing through the system
**Friction** = Bottlenecks slowing the flywheel

## Health Report

```markdown
# Knowledge Flywheel Health

## Velocity (Last 7 Days)
| Metric | Value | Trend |
|--------|-------|-------|
| Sessions | 12 | +20% |
| Transcripts forged | 8 | +33% |
| Candidates created | 24 | +15% |
| Promotions (0→1) | 6 | +50% |
| Patterns recognized | 2 | +100% |

**Status:** Healthy - flywheel accelerating

## Poao Depths
| Poao | Count | Oldest | Action |
|------|-------|--------|--------|
| Candidates (Tier 0) | 18 | 5 days | Review 3 ready for promotion |
| Learnings (Tier 1) | 42 | 30 days | 2 candidates for Tier 2 |
| Patterns (Tier 2) | 8 | 60 days | 1 ready for skill creation |

## Friction Points
- 5 candidates older than 7 days without review
- 2 learnings never cited (consider archiving)

## Recommendations
1. Review oldest 5 candidates
2. Archive 2 uncited learnings
3. Consider promoting "wave-execution" to skill
```

## Velocity Metrics

| Metric | Formula | Healthy Range |
|--------|---------|---------------|
| **Extraction rate** | candidates/transcript | 2-5 |
| **Promotion rate** | promotions/week | 3-10 |
| **Citation rate** | citations/learning | 1-3 within 14 days |
| **Staleness** | % artifacts > 30 days without citation | < 20% |

## Friction Detection

| Friction | Signal | Fix |
|----------|--------|-----|
| **Poao backup** | Candidates > 20 | Run review session |
| **Stale knowledge** | Artifacts > 30 days uncited | Archive or refresh |
| **Orphan growth** | Provenance missing | Run `/provenance --orphans` |
| **Low extraction** | < 1 candidate/transcript | Check forge taxonomy |

## Integration with /post-mortem

After `/post-mortem`:

```bash
/flywheel --since-postmortem

# Shows:
# - New candidates from retro
# - Promotion candidates
# - Flywheel impact
```

## See Also

- `/forge` - Feed the flywheel
- `/provenance` - Track lineage
- `/post-mortem` - Standard extraction path
