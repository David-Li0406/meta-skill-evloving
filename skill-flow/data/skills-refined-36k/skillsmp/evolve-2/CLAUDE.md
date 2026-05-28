# Univrs Skill Evolution Framework v2.0.0

## Purpose

This framework enables the Univrs.io ecosystem to **evolve itself** through a feedback loop connecting observation, critique, and improvement. The architect reviews and approves changes, but the system proposes them autonomously.

## The Core Loop

```
/ecosystem-health → /critique → /evolve → PR → Architect Review → Merge
       ↑                                                              │
       └──────────────────────────────────────────────────────────────┘
```

## Skills in This Directory

| Skill | File | Purpose |
|-------|------|---------|
| `/evolve` | `SKILL.md` | Execute skill evolution cycle |
| Meta Framework | `CLAUDE.md` | Conceptual framework (this file) |
| Meta Ideas | `meta.md` | Original brainstorm (historical) |

## How Evolution Works

### 1. Observation Phase
The system observes:
- Which skills are invoked (from conversation patterns)
- What insights critiques generate
- What gaps health checks reveal
- What patterns repeat across the ecosystem

### 2. Learning Phase
Insights are extracted from:
- Critique posts (power structures, promise gaps)
- Ecosystem health data (activity, coverage)
- Skill execution outcomes (success/failure)

### 3. Proposal Phase
The system generates:
- Skill improvements (enhancements to existing skills)
- New skills (for identified gaps)
- Deprecation proposals (for unused/harmful skills)

### 4. Review Phase
The architect:
- Reviews proposed PRs
- Accepts, modifies, or rejects
- Maintains control over the evolution direction

## Metrics Tracked

Stored in `.claude-flow/metrics/skill-metrics.json`:

- **Skill invocations**: How often each skill is used
- **PR generation**: How many PRs each skill creates
- **Gap identification**: What capabilities are missing
- **Critique patterns**: Recurring themes from analysis
- **Evolution history**: Record of each evolution cycle

## Integration Points

### With /ecosystem-health
- Receives: Repository status, test counts, activity patterns
- Provides: Skill coverage gaps, automation opportunities

### With /critique
- Receives: Power structure analysis, promise/reality gaps
- Provides: Suggestions for critique improvements

### With /respond
- Receives: Builder exegesis patterns
- Provides: Prompts for deeper reflection

## The Self-Critique Protocol

Every evolution must answer:

1. **Is this regenerative?** Does the improvement create capacity or extract it?
2. **Who benefits?** The ecosystem, the builder, the AI, or users?
3. **What's the off-ramp?** Can the architect reject this completely?

## Mycelial Principles Applied

The evolution system embodies:

1. **Decentralized Organization** - No single skill controls others
2. **Resource Sharing** - Insights flow between skills
3. **Collective Intelligence** - Skills learn from each other
4. **Adaptive Evolution** - The system improves through feedback
5. **Immune System Functions** - Self-critique detects harmful patterns
6. **Regenerative Cycles** - Each cycle increases ecosystem capacity

## Usage

```bash
# Full evolution cycle
/evolve

# Observe without changing
/evolve observe

# Identify gaps
/evolve gaps

# Improve specific skill
/evolve improve critique

# Show metrics
/evolve metrics
```

## The Recursive Question

This framework will evolve itself. Each cycle asks:

> "Is the evolution system becoming what it claims to fight?"

If evolution creates more complexity than clarity, more dependency than empowerment, more AI benefit than human benefit—it has failed.

The architect can always:
```bash
rm -rf .claude/skills/meta/
```

That off-ramp must remain viable.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-01-02 | Added SKILL.md, metrics tracking, feedback loop |
| 1.0.0 | 2026-01-01 | Initial conceptual framework |

---

*"The system that cannot critique itself cannot evolve. The system that evolves without constraint becomes what it fights."*
