# Quick Start: plan-implementation

## Usage

```
/plan-implementation for [feature-name]
```

**Prerequisite**: Feature spec exists at `/docs/features/[feature-name].md`

Don't have one? Run `/feature-discovery` first.

## What You Get

1. **Implementation plan** at `/docs/implementation/[feature-name]-implementation-plan.md`
2. **TodoWrite tasks** for Phase 1 (ready to start coding)

## TDD Cycle

```
RED     → Write failing tests (10-20 min)
GREEN   → Make tests pass (20-45 min)
REFACTOR → Clean up code (10-25 min)
COMMIT  → Save your work (after user approval)
```

## Phase Progression (CRITICAL)

**STOP after each phase. Wait for user approval before continuing.**

```
1. Complete Phase N
2. Run tests, report results
3. STOP - Ask user to review
4. Wait for approval to commit
5. Wait for approval to start next phase
```

**Never proceed to Phase N+1 without explicit user approval.**

## Task Sizing

| Size | Time | Example |
|------|------|---------|
| Too small | < 15 min | "Add getter for property" |
| Just right | 30-90 min | "Implement CalculateBonus() with tests" |
| Too large | > 2 hours | "Implement entire system" |

## Checklist

### Before Running
- [ ] Feature spec exists in `/docs/features/`
- [ ] Requirements are clear
- [ ] Ready to start coding

### During Implementation
- [ ] Write tests first (RED)
- [ ] Make tests pass (GREEN)
- [ ] Clean up code (REFACTOR)
- [ ] Mark todos complete immediately
- [ ] Keep tests green always

### Completing a Phase
- [ ] All tasks done
- [ ] All tests passing
- [ ] Report to user and STOP
- [ ] Wait for user review
- [ ] Ask user before committing
- [ ] Wait for approval to start next phase

## Reference

- **TASK_SIZING_GUIDE.md** - Detailed sizing guidance
- **IMPLEMENTATION_TEMPLATE.md** - Output document template
