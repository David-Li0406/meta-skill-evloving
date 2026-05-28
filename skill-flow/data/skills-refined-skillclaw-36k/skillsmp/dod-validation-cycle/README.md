# generated: 2025-12-25
# System Auto: last updated on: 2025-12-25T18:25:06
# DoD Validation Cycle

**Validation Skill** (bridge) for Definition of Done validation before work item closure.

## Purpose

Validates that work items meet ADR-033 DoD criteria before the close-work-cycle proceeds. Acts as a MUST gate ensuring quality before closure.

## Workflow

```
CHECK --> VALIDATE --> APPROVE
```

1. **CHECK:** Verify DoD prerequisites exist (plans, memory_refs)
2. **VALIDATE:** Check each DoD criterion (tests, WHY, docs, plans)
3. **APPROVE:** Confirm ready for closure or report blockers

## Invocation

```
Skill(skill="dod-validation-cycle")
```

## DoD Criteria (ADR-033)

| Criterion | Verification |
|-----------|--------------|
| Tests pass | User confirms or test output |
| WHY captured | memory_refs populated |
| Docs current | CLAUDE.md/READMEs updated |
| Traced files | Associated plans complete |

## Integration

This skill is invoked as a **MUST gate** by close-work-cycle before its VALIDATE phase.

## Related Skills

- `plan-validation-cycle` - Pre-DO validation
- `design-review-validation` - During-DO validation
- `close-work-cycle` - Invokes this skill

## Files

- `SKILL.md` - Full skill definition with phases
