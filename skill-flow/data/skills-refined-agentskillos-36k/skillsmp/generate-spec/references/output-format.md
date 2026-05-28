# Output Format Reference

## Completion Report

```
✅ Specification Complete: [Feature Name]

Created Files:
- specs/N-short-name/spec.md       (Requirements, acceptance criteria)
- specs/N-short-name/plan.md       (Technical approach, DDD mapping)
- specs/N-short-name/checklist.md  (Domain-specific checklist) [if enabled]
- specs/N-short-name/tasks.md      (Actionable work items)

GitHub Issues: [if created]
- #145: Repository Layer implementation
- #146: API Client implementation
- #147: Hooks implementation
- ... (15 issues total)

Branch: N-short-name
Location: specs/N-short-name/

Next Steps:
- Review spec.md for completeness
- Ready to implement: skill:implement
```

## Dependencies

### Foundation Commands (Layer 1)

- `/speckit.specify` - Create spec.md
- `/speckit.plan` - Create plan.md
- `/speckit.tasks` - Create tasks.md
- `/speckit.clarify` - Clarify underspecified areas
- `/speckit.checklist` - Generate custom checklist

### Skills (Layer 2)

- `skill:create-issues` - Convert tasks to GitHub Issues (optional)

## Error Handling

If any phase fails:

1. Report specific error to agent
2. Suggest remediation (e.g., clarify requirements, check branch)
3. Do not proceed to next phase
4. Agent decides next action

## Success Criteria

This skill succeeds when:

- ✅ spec.md exists with all required sections
- ✅ No [NEEDS CLARIFICATION] markers remain
- ✅ plan.md maps to DDD 4-layer architecture
- ✅ tasks.md has actionable, dependency-ordered items
- ✅ User has approved all optional phases
- ✅ All files are in correct location (specs/N-short-name/)
