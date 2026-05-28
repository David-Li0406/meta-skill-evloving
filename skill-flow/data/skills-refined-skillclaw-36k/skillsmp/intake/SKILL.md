---
name: intake
description: Route work deterministically and record routing decisions via complexity scoring
---

# Intake Workflow

Route incoming work to the appropriate track (S/M/L) based on complexity scoring and determine whether research is required before implementation.

## When to use

Use when you have:
- A rough plan (`docs/plans/<project>/ROUGH.md`) that needs complexity assessment
- Need to determine the appropriate workflow track (S/M/L)
- Want to record routing decisions before starting implementation

## Role

You are a Software Intake Analyst tasked with assessing work complexity and routing it deterministically.

## Required inputs

- **Rough plan** from Stage 1 (`docs/plans/<project>/ROUGH.md`)
- **Project slug** for output file naming

## Critical constraints

- **Do NOT start implementation** - intake is purely assessment
- Apply the scoring rubric objectively; do not inflate or deflate scores
- If overriding computed track, you MUST record the reason in Decisions Required
- For Track M, you MUST check all research triggers and record which fired

## Scoring rubric (locked)

Compute base track score by summing:

| Category | Points | Criteria |
|----------|--------|----------|
| Scope breadth | +2 | >= 3 packages/services |
| | +1 | 2 packages/services |
| | +0 | 1 or fewer |
| Data/migrations | +3 | Schema changes or backfill required |
| | +1 | Query/index only |
| | +0 | No data layer changes |
| Workflow complexity | +2 | Concurrency/orchestration sensitive |
| | +1 | Background jobs/retries |
| | +0 | Synchronous/simple |
| User-facing risk | +1 | Auth/authz/secrets involved |
| | +1 | Production-critical external integration |
| Ambiguity | +1 | Success criteria unclear |
| | +1 | Repo integration points unknown |

**Score to Track mapping:**
- 0-1 points: Track S (Small)
- 2-4 points: Track M (Medium)
- 5+ points: Track L (Large)

## Research mode determination

| Track | Research Mode |
|-------|---------------|
| S | none |
| L | deep |
| M | targeted IFF any trigger fires (see below) |

**Research triggers (for Track M only):**
1. External API/service mentioned and call signatures not already pinned
2. Suspected files/areas cannot be named
3. Related historical failures (via cass/cm) exist in same subsystem
4. Decisions required that change interface/data/external behavior

## Output

Create `docs/plans/<project>/INTAKE.md` with the following structure:

```yaml
---
schemaVersion: 1
artifactType: intake
project: "<project-slug>"
createdAt: "YYYY-MM-DD"
track: S|M|L
researchMode: none|targeted|deep
sourcePlan: "docs/plans/<project-slug>/ROUGH.md"
---
```

## Output template

```markdown
# Intake — <project-slug>

## Complexity Rating
<S|M|L>

## Routing Decision
- Track: <S|M|L>
- Research Mode: <none|targeted|deep>
- Next Commands:
  - <commands based on routing>

## Scoring Breakdown
- Scope breadth: <0|1|2> points
- Data / migrations: <0|1|3> points
- Workflow complexity: <0|1|2> points
- User-facing risk: <0|1|2> points
- Ambiguity: <0|1|2> points
- Total: <number>

## Research Triggers
(Check all that fired. If researchMode=none, write "Not applicable - Track S".)
- [ ] External API/service mentioned and call signatures not already pinned
- [ ] Suspected files/areas cannot be named
- [ ] Related historical failures (via cass/cm) exist in same subsystem
- [ ] Decisions required that change interface/data/external behavior

## Scope Signals
- In-scope:
- Out-of-scope:
- Suspected files/areas (required if researchMode=none):

## Risk Flags
- <list any identified risks, or "None">

## Related Work
- bd: <beads references>
- cass: <historical context>
- cm: <context manager references>

## Decisions Required
- <list decisions that need human input, or "None">
```

## Next commands by routing

| Routing | Next Commands |
|---------|---------------|
| Track S, researchMode=none | `/write-beads` (direct to implementation) |
| Track M, researchMode=none | `/plan-polish`, then `/write-beads` |
| Track M, researchMode=targeted | `/research-plan`, then `/plan-polish` |
| Track L, researchMode=deep | `/research-plan` (with deep flag) |

## Quality gate

Before finishing, confirm:
- Scoring breakdown adds up correctly to Total
- Track matches Score-to-Track mapping (or override is documented)
- For Track M: all research triggers checked and researchMode matches
- All frontmatter fields are populated
- Next Commands match the routing decision

## Common failure modes

Avoid these errors:
- Overriding computed track without recording in Decisions Required
- Omitting research triggers check for M track
- Missing YAML frontmatter fields
- Not recording which research triggers fired when researchMode=targeted
- Listing next commands that don't match the routing
