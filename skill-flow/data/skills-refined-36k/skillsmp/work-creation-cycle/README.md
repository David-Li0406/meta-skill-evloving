# generated: 2025-12-25
# System Auto: last updated on: 2025-12-25T10:41:35
# Work Creation Cycle Skill

Guides agents through populating work item fields after scaffolding.

## Files

- `SKILL.md` - Main skill definition with VERIFY->POPULATE->READY workflow

## Invocation

```
Skill(skill="work-creation-cycle")
```

Automatically invoked by `/new-work` command after scaffolding.

## Phases

1. **VERIFY** - Confirm work file was created and is valid
2. **POPULATE** - Fill in Context and Deliverables sections
3. **READY** - Validate work item is actionable

## Related

- ADR-039: Work Item as File Architecture
- INV-033: Skill as Node Entry Gate Formalization
