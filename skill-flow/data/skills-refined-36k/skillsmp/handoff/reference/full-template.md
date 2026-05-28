# Full Handoff Template

Use this template for comprehensive session handoffs.

```markdown
# Session Handoff

**Date**: [YYYY-MM-DD HH:MM]
**Duration**: [approximate session length]
**Original Request**: [what user asked for]

---

## Summary

[2-3 sentence summary of what was accomplished]

## Work Completed

### Features/Fixes
- [Feature/fix 1]: [brief description]
- [Feature/fix 2]: [brief description]

### Files Changed
| File | Change Type | Description |
|------|-------------|-------------|
| [path] | [created/modified/deleted] | [what changed] |

### Database Changes
- [ ] Migrations created: [list or "none"]
- [ ] Production SQL needed: [yes/no]
- [ ] RLS changes: [yes/no]

## Agent Activity

### Agents Spawned
| Agent | Purpose | Status | Key Output |
|-------|---------|--------|------------|
| [type] | [why spawned] | [completed/active] | [what it produced] |

### Agent Notes
[Observations about agent interactions or patterns]

## Documentation

### Docs Updated
- [x] [doc path]: [sections changed]

### Docs Need Updating
- [ ] [doc path]: [what needs to change]

### Drift Status
- Last drift-check: [timestamp or "not run"]
- Known drift: [list or "none"]

## Verification

### Commands
```bash
[verification commands]
```

### UI Steps
1. Navigate to [route]
2. Perform [action]
3. Expect [outcome]

### Data Checks
```sql
SELECT ... FROM ...;
```

### Tests Run
- [ ] Static analysis: [pass/fail]
- [ ] Feature checklist: [pass/fail]

## Remaining Work

### Not Yet Complete
- [ ] [Task 1]: [why incomplete]
- [ ] [Task 2]: [what's needed]

### Known Issues
- **[Issue]**: [description]
  - Severity: [blocking/non-blocking]
  - Workaround: [if any]

### Deferred Decisions
- **[Decision]**: [options considered]

## Next Session Prep

### Start With
```
/session-start
```

### Docs to Load
- `docs/features/[primary].md`
- `docs/features/[related].md`

### Files to Review
- `[critical file 1]`
- `[critical file 2]`

### First Actions
1. [What to do first]
2. [What to do second]

---

## Session Metadata

### Context Usage
- Recommendation: [compact recommended / ok for continuation]

### Optimization Opportunities
- Topics: [brief list or "none"]

### User Preferences Noted
[Preferences that should persist]
```
