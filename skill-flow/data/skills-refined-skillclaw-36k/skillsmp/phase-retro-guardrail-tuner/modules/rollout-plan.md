# Module: Rollout Plan

## Objective

Adopt guardrail changes without disrupting ongoing work.

## Rollout categories

### Immediate changes (apply now)
- Critical fixes
- Changes that don't affect in-flight work
- Clarifications that help current tasks

### Next-phase changes (apply at phase boundary)
- Template restructuring
- New required fields
- Process changes

### Migration changes (require coordination)
- Breaking changes to schemas
- Changes affecting multiple templates
- Changes requiring engineer training

## Rollout plan structure

```markdown
## Rollout Plan

### Apply Now
- <change 1>: <why safe to apply immediately>
- <change 2>: <why safe to apply immediately>

### Apply Next Phase
- <change 3>: <why wait>
- <change 4>: <why wait>

### Migration Required
- <change 5>:
  - Impact: <what's affected>
  - Migration steps: <how to transition>
  - Timeline: <when to complete>

### Success Metrics
- <metric 1>: <how to measure improvement>
- <metric 2>: <how to measure improvement>
```

## Success metrics examples

- **Reduction in pattern occurrence**: "Ambiguity questions drop by 50%"
- **Faster task completion**: "Average task time decreases by 20%"
- **Less rework**: "PR revision requests drop by 30%"
- **Better first-time quality**: "CI pass rate on first push increases"

## Communication plan

For each change, specify:
- Who needs to know
- How they'll be notified
- What training is needed (if any)

## Rollback plan

For significant changes:
- How to detect if change is causing problems
- How to revert if needed
- Who decides to rollback
