# State Mismatch Handling

When the codebase doesn't match what handoff/checkpoint expected.

## Common Mismatch Types

### 1. Files Modified Externally

**Symptom**: Git shows changes not in handoff

**Causes**:
- User made manual changes
- Another session worked on the code
- Linter/formatter ran

**Resolution**:
1. Review changes: `git diff`
2. Ask user: "I see changes not in the handoff. Were these intentional?"
3. Update mental model accordingly

### 2. Files Missing

**Symptom**: Files listed in handoff don't exist

**Causes**:
- Deleted manually or by cleanup
- Never committed in previous session
- Wrong branch

**Resolution**:
1. Check git history: `git log --oneline -- [file]`
2. Check other branches: `git branch -a | grep [feature]`
3. May need to recreate or skip

### 3. Database State Changed

**Symptom**: Expected data not present

**Causes**:
- Another session modified data
- Database was reset (check for this!)
- Migration ran

**Resolution**:
1. Query current state: `docker exec -i supabase_db_enhancedhr psql -U postgres -d postgres -c "..."`
2. Compare to expected state
3. May need to recreate test data

### 4. Branch Mismatch

**Symptom**: On different branch than handoff expected

**Causes**:
- User switched branches
- PR was merged

**Resolution**:
1. Check current branch: `git branch --show-current`
2. Check if work was merged: `git log --oneline main | head -10`
3. Either switch branches or adapt to merged state

## Resolution Protocol

```
STATE MISMATCH DETECTED

Expected: [from handoff]
Actual: [current state]

Options:
1. Continue with current state (changes are valid)
2. Investigate differences
3. Restore expected state (if possible)

Which approach? [1/2/3]
```

## Prevention

### At Session End
- Commit all changes
- Push to remote
- Clear handoff of uncommitted expectations

### At Session Start
- Always check git status first
- Note any unexpected changes
- Clarify with user before proceeding

## Severity Levels

| Mismatch | Severity | Action |
|----------|----------|--------|
| Formatting changes | Low | Ignore, continue |
| New files added | Medium | Ask user |
| Files deleted | Medium | Ask user |
| Core logic changed | High | Full investigation |
| Database reset | Critical | Stop, assess damage |
