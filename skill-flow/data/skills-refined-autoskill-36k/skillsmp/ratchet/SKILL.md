---
name: ratchet
description: 'Brownian Ratchet progress gates for RPI workflow. Check, record, verify. Triggers: "check gate", "verify progress", "ratchet status".'
---

# Ratchet Skill

Track progress through the RPI (Research-Plan-Implement) workflow.

## The Brownian Ratchet

```
Progress = Chaos × Filter → Ratchet
```

| Phase | What Happens |
|-------|--------------|
| **Chaos** | Multiple parallel attempts (exploration, polecats) |
| **Filter** | Validation gates (tests, /vibe, review) |
| **Ratchet** | Lock progress permanently (merged, closed, stored) |

**Key insight:** You can always add more chaos, but you can't un-ratchet. Progress is permanent.

## Triggers

- "ratchet status"
- "check gate"
- "record step"
- "validate ratchet"

## Usage

```bash
# Check current ratchet chain status
ao ratchet status

# Check if a step's gate is met
ao ratchet check research
ao ratchet check plan
ao ratchet check implement

# Record step completion
ao ratchet record research --output ".agents/research/auth.md"
ao ratchet record plan --output ".agents/plans/auth-plan.md"
ao ratchet record implement --files "src/auth.ts,src/auth_test.ts"

# Skip a step intentionally
ao ratchet skip pre-mortem --reason "Bug fix, no spec needed"

# Validate step requirements
ao ratchet validate plan --lenient

# Trace provenance backward
ao ratchet trace implement

# Find artifacts
ao ratchet find --epic-id at-1234

# Record tier promotion
ao ratchet promote --tier 2
```

## Workflow Steps

| Step | Gate | Output |
|------|------|--------|
| `research` | Research artifact exists | `.agents/research/*.md` |
| `product` | Product brief exists | `.agents/products/*.md` |
| `pre-mortem` | Pre-mortem complete | `.agents/pre-mortems/*.md` |
| `plan` | Plan artifact exists | `.agents/plans/*.md` |
| `implement` | Code + tests pass | Source files |
| `validate` | /vibe passes | Validation report |
| `post-mortem` | Learnings extracted | `.agents/retros/*.md` |

## Chain Storage

The ratchet chain is stored in `.agents/ao/chain.jsonl`:

```json
{"step":"research","status":"completed","output":".agents/research/auth.md","time":"2026-01-25T10:00:00Z"}
{"step":"plan","status":"completed","output":".agents/plans/auth-plan.md","time":"2026-01-25T11:00:00Z"}
{"step":"implement","status":"in_progress","time":"2026-01-25T12:00:00Z"}
```

## Integration with /crank

The `/crank` skill uses ratchet to:
1. Check which steps are complete
2. Validate gates before proceeding
3. Record progress after each step

## See Also

- `/forge` - Extract knowledge from transcripts
- `/provenance` - Trace knowledge lineage
- [Brownian Ratchet Philosophy](../references/brownian-ratchet.md)
