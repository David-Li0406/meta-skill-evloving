# Pre-Risk Checkpoint Template

Use this template before attempting risky operations.

```markdown
# Pre-Risk Checkpoint: [timestamp]

**Type**: pre-risk
**Operation**: [what we're about to attempt]

## Risk Context

### Operation About to Attempt
[Detailed description of the risky operation]

### Why It's Risky
- [Potential issue 1]
- [Potential issue 2]
- [Potential issue 3]

### Rollback Plan
If this fails:
1. [Rollback step 1]
2. [Rollback step 2]
3. [Recovery step]

### Point of No Return
[What would make rollback impossible]

### Abort Criteria
Stop immediately if:
- [Condition 1]
- [Condition 2]
- [Condition 3]

## Current State (Before Operation)

### Files That Will Change
| File | Current State | Backed Up |
|------|---------------|-----------|
| [path] | [state] | [yes/no] |

### Database State
- [Relevant table]: [current state]
- [Relevant data]: [backed up]

### Environment
- Branch: [current branch]
- Last commit: [hash]
- Uncommitted changes: [list or "none"]

## Post-Operation Verification

### Success Indicators
- [ ] [What indicates success]
- [ ] [What indicates success]

### Failure Indicators
- [ ] [What indicates failure]
- [ ] [What indicates failure]

## Recovery Resources

### Backup Location
[Where backups are stored]

### Help Resources
- [Doc or person who can help]
- [Alternative approach if this fails]
```

## When to Use

- Before database schema changes
- Before bulk data operations
- Before changing auth/RLS policies
- Before any operation that can't be undone easily
- When user says "try this" for something uncertain
