---
name: git-safe-operations
description: Safe git operations wrapper using Git MCP server. Validates operations before execution, provides rollback support, and enforces agentic development workflow. Use for branch creation, commits, merges, and pushes with built-in safety checks. Always uses Git MCP server for reliable, auditable git operations.
---

# Git Safe Operations

Wrapper for common git operations with safety checks, validation, and rollback support via Git MCP server.

## Quick Start

**Create branch safely:**
```
"Create feature branch feature-1.10-infrastructure from epic-1-progressive-coherence"
```

**Commit with validation:**
```
"Commit changes for wave 1.10.1 with message 'Implement catalog change monitor'"
```

**Merge with checks:**
```
"Merge feature-1.10-infrastructure into epic-1-progressive-coherence"
```

## Core Operations

### Operation 1: Create Branch

**Purpose**: Create new branch with validation

**Pre-Checks**:
- ✅ Source branch exists
- ✅ Target branch name doesn't already exist
- ✅ Source branch is appropriate (development, epic, or feature)
- ✅ Branch name follows conventions

**MCP Operation**:
```
mcp__git__create_branch(
  branch_name: "feature-1.10-infrastructure",
  from_branch: "epic-1-progressive-coherence"
)
```

**Post-Validation**:
- Branch created successfully
- Branch pushed to remote
- Branch tracks remote

**Rollback**: Delete branch if creation fails partially

---

### Operation 2: Commit Changes

**Purpose**: Commit staged changes with validation

**Pre-Checks**:
- ✅ On correct branch (not main)
- ✅ Changes are staged
- ✅ Commit message follows conventions
- ✅ No merge conflicts

**MCP Operation**:
```
mcp__git__commit(
  message: "feat(wave-1.10.1): Implement catalog change monitor",
  files: ["src/catalog/monitor.ts", "tests/monitor.test.ts"]
)
```

**Post-Validation**:
- Commit created successfully
- Commit has expected files
- Commit author correct

**Rollback**: Soft reset to HEAD~1 if commit has issues

---

### Operation 3: Push Changes

**Purpose**: Push commits to remote with validation

**Pre-Checks**:
- ✅ Branch has commits to push
- ✅ Branch tracks remote
- ✅ Not pushing to main directly
- ✅ No conflicts with remote

**MCP Operation**:
```
mcp__git__push(
  branch: "feature-1.10-infrastructure",
  force: false,
  set_upstream: true
)
```

**Post-Validation**:
- Push succeeded
- Remote branch updated
- No errors

**Rollback**: Force push previous state if needed (with confirmation)

---

### Operation 4: Merge Branches

**Purpose**: Merge branches with conflict detection

**Pre-Checks**:
- ✅ Source branch has commits
- ✅ Target branch exists
- ✅ No uncommitted changes
- ✅ Branches can be merged (no conflicts)

**MCP Operation**:
```
mcp__git__merge(
  source_branch: "feature-1.10-infrastructure",
  target_branch: "epic-1-progressive-coherence",
  strategy: "squash"  # or "merge", "rebase"
)
```

**Conflict Handling**:
- If conflicts detected, abort merge
- Return conflict details to user
- Suggest resolution steps

**Post-Validation**:
- Merge completed successfully
- No conflicts remain
- All tests pass (if applicable)

**Rollback**: Abort merge if conflicts occur

---

### Operation 5: Create Pull Request

**Purpose**: Create PR with validation

**Pre-Checks**:
- ✅ Source branch exists and pushed
- ✅ Target branch exists
- ✅ PR doesn't already exist
- ✅ Branch relationship valid (per branching strategy)

**Operation** (via gh CLI or GitHub API):
```bash
gh pr create \
  --base epic-1-progressive-coherence \
  --head feature-1.10-infrastructure \
  --title "Feature 1.10: Infrastructure Complete" \
  --body "Completed waves 1.10.1, 1.10.2, 1.10.3"
```

**Validation**:
- PR follows branching strategy
- No PR from feature → main (must go through development)
- PR has description

**Post-Validation**:
- PR created successfully
- PR checks triggered
- PR URL returned

---

### Operation 6: Switch Branch

**Purpose**: Switch branches safely

**Pre-Checks**:
- ✅ Target branch exists
- ✅ No uncommitted changes (or stash option)
- ✅ Not currently on target branch

**MCP Operation**:
```
mcp__git__checkout(
  branch: "development"
)
```

**Post-Validation**:
- Switched to target branch
- Working directory clean
- Branch up-to-date with remote

---

### Operation 7: Delete Branch

**Purpose**: Delete branch safely

**Pre-Checks**:
- ✅ Branch is merged (or force flag provided)
- ✅ Not currently on branch to delete
- ✅ Not deleting main or development
- ✅ Confirmation provided

**MCP Operation**:
```
mcp__git__delete_branch(
  branch: "feature-1.10-infrastructure",
  force: false,
  remote: true
)
```

**Post-Validation**:
- Branch deleted locally
- Branch deleted from remote
- No orphaned branches

---

## Safety Checks

### Pre-Operation Validation

**Branch Protection Check**:
```python
def validate_branch_protection(branch_name):
    """Prevent operations on protected branches."""
    if branch_name == "main":
        return {
            "allowed": False,
            "reason": "Cannot perform direct operations on main branch"
        }
    return {"allowed": True}
```

**Branch Naming Check**:
```python
def validate_branch_name(branch_name, branch_type):
    """Validate branch name follows conventions."""
    patterns = {
        "epic": r"^epic-\d+-[a-z0-9-]+$",
        "feature": r"^feature-\d+\.\d+-[a-z0-9-]+$",
        "wave": r"^wave-\d+\.\d+\.\d+-[a-z0-9-]+$",
        "hotfix": r"^hotfix-[a-z0-9-]+$"
    }
    if not re.match(patterns[branch_type], branch_name):
        return {
            "valid": False,
            "reason": f"Branch name doesn't match {branch_type} pattern",
            "expected_pattern": patterns[branch_type]
        }
    return {"valid": True}
```

**Commit Message Check**:
```python
def validate_commit_message(message):
    """Validate commit message follows conventional commits."""
    pattern = r"^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+"
    if not re.match(pattern, message):
        return {
            "valid": False,
            "reason": "Commit message doesn't follow conventional commits format",
            "expected_format": "type(scope): description"
        }
    return {"valid": True}
```

---

### Post-Operation Validation

**Verify Operation Success**:
```python
def verify_branch_created(branch_name):
    """Verify branch was created successfully."""
    result = mcp__git__list_branches()
    if branch_name not in result["branches"]:
        return {
            "success": False,
            "reason": "Branch not found after creation"
        }
    return {"success": True}
```

**Verify Remote Sync**:
```python
def verify_remote_sync(branch_name):
    """Verify branch is synchronized with remote."""
    local_sha = mcp__git__get_branch_sha(branch=branch_name)
    remote_sha = mcp__git__get_branch_sha(branch=f"origin/{branch_name}")

    if local_sha != remote_sha:
        return {
            "synchronized": False,
            "local_sha": local_sha,
            "remote_sha": remote_sha
        }
    return {"synchronized": True}
```

---

## Rollback Support

### Rollback Scenarios

**1. Branch Creation Failed**
```python
def rollback_branch_creation(branch_name):
    """Delete branch if creation failed partially."""
    try:
        mcp__git__delete_branch(branch=branch_name, force=True)
        return {"rollback": "success", "message": "Branch deleted"}
    except Exception as e:
        return {"rollback": "failed", "error": str(e)}
```

**2. Commit Has Issues**
```python
def rollback_commit():
    """Undo last commit if it has issues."""
    mcp__git__reset(mode="soft", target="HEAD~1")
    return {"rollback": "success", "message": "Commit undone, changes staged"}
```

**3. Push Failed**
```python
def rollback_push(branch_name, previous_sha):
    """Reset branch to previous state before push."""
    mcp__git__reset(mode="hard", target=previous_sha)
    mcp__git__push(branch=branch_name, force=True)
    return {"rollback": "success", "message": f"Branch reset to {previous_sha}"}
```

**4. Merge Has Conflicts**
```python
def rollback_merge():
    """Abort merge if conflicts occur."""
    mcp__git__merge_abort()
    return {"rollback": "success", "message": "Merge aborted, working directory restored"}
```

---

## Operation Examples

### Example 1: Create Epic Branch

**Scenario**: Start new epic from development

**Operation**:
```markdown
## Create Epic Branch: epic-1-progressive-coherence

**Pre-Checks**:
- ✅ Currently on development branch
- ✅ Development branch is clean (no uncommitted changes)
- ✅ Development branch up-to-date with remote
- ✅ Epic branch name follows convention: `epic-\d+-[a-z0-9-]+`

**MCP Operations**:
1. Create branch from development
   ```
   mcp__git__create_branch(
     branch_name: "epic-1-progressive-coherence",
     from_branch: "development"
   )
   ```

2. Push branch to remote
   ```
   mcp__git__push(
     branch: "epic-1-progressive-coherence",
     set_upstream: true
   )
   ```

**Post-Validation**:
- ✅ Branch created locally
- ✅ Branch pushed to remote
- ✅ Branch tracks origin/epic-1-progressive-coherence
- ✅ Currently on epic-1-progressive-coherence branch

**Result**: SUCCESS - Epic branch created and ready for features
```

---

### Example 2: Commit Wave Implementation

**Scenario**: Commit completed wave to feature branch

**Operation**:
```markdown
## Commit Wave 1.10.1 Implementation

**Pre-Checks**:
- ✅ Currently on feature-1.10-infrastructure branch
- ✅ Changes staged (2 files modified)
- ✅ No merge conflicts
- ✅ Commit message follows convention: `feat(wave-1.10.1): ...`

**MCP Operations**:
1. Verify staged changes
   ```
   mcp__git__status()
   # Output: 2 files staged
   ```

2. Create commit
   ```
   mcp__git__commit(
     message: "feat(wave-1.10.1): Implement catalog change monitor",
     files: ["src/catalog/monitor.ts", "tests/monitor.test.ts"]
   )
   ```

3. Push commit
   ```
   mcp__git__push(branch: "feature-1.10-infrastructure")
   ```

**Post-Validation**:
- ✅ Commit created with correct message
- ✅ Commit contains expected files
- ✅ Commit pushed to remote
- ✅ Remote branch updated

**Result**: SUCCESS - Wave 1.10.1 committed and pushed
```

---

### Example 3: Merge Feature to Epic

**Scenario**: Merge completed feature branch to epic

**Operation**:
```markdown
## Merge feature-1.10-infrastructure → epic-1-progressive-coherence

**Pre-Checks**:
- ✅ Feature branch has all waves committed
- ✅ Feature branch pushed to remote
- ✅ No uncommitted changes
- ✅ Epic branch exists
- ✅ No merge conflicts detected

**MCP Operations**:
1. Switch to epic branch
   ```
   mcp__git__checkout(branch: "epic-1-progressive-coherence")
   ```

2. Pull latest from remote
   ```
   mcp__git__pull(branch: "epic-1-progressive-coherence")
   ```

3. Merge feature branch
   ```
   mcp__git__merge(
     source_branch: "feature-1.10-infrastructure",
     target_branch: "epic-1-progressive-coherence",
     strategy: "merge"
   )
   ```

4. Push merge
   ```
   mcp__git__push(branch: "epic-1-progressive-coherence")
   ```

**Post-Validation**:
- ✅ Merge completed without conflicts
- ✅ All feature commits in epic branch
- ✅ Epic branch pushed to remote
- ✅ Feature branch can be deleted

**Result**: SUCCESS - Feature merged to epic
```

---

### Example 4: Create Pull Request

**Scenario**: Create PR from development to main

**Operation**:
```markdown
## Create PR: development → main

**Pre-Checks**:
- ✅ Development branch pushed to remote
- ✅ Development has commits ahead of main
- ✅ No existing PR from development to main
- ✅ Branch relationship valid (development → main allowed)
- ✅ PR branch check workflow will pass

**Operation**:
```bash
gh pr create \
  --base main \
  --head development \
  --title "Release: Sprint 5.1 Complete" \
  --body "## Summary

Completed waves:
- Wave 1.10.1: Catalog change monitor
- Wave 1.10.2: Template staleness detection
- Wave 1.10.3: Impact analysis

## Testing
All tests passing, ready for release."
```

**Post-Validation**:
- ✅ PR created successfully
- ✅ PR checks triggered (check-source-branch)
- ✅ PR URL: https://github.com/org/repo/pull/123
- ✅ PR ready for review

**Result**: SUCCESS - PR #123 created
```

---

## Integration with Workflow

### Before Every Git Operation

1. Invoke `git-repository-setup-validation` (if not already done)
2. Verify repository properly configured
3. Use `git-safe-operations` for all git commands
4. Validate operation before executing

### During Development

1. Use safe operations for branch creation
2. Use safe operations for commits
3. Use safe operations for merges
4. Get rollback support automatically

### Error Handling

```markdown
If safe operation fails:
1. Check error message from skill
2. Review pre-check failures
3. Fix issues (e.g., uncommitted changes)
4. Retry operation
5. If still failing, use rollback
```

---

## Available Resources

### Scripts

- **scripts/safe_branch_create.py** — Create branch with validation
- **scripts/safe_commit.py** — Commit with validation
- **scripts/safe_merge.py** — Merge with conflict detection
- **scripts/safe_push.py** — Push with validation

### References

- **references/git-operation-patterns.md** — Common operation patterns
- **references/rollback-procedures.md** — How to rollback operations
- **references/error-codes.md** — Error codes and solutions

---

## Success Criteria

- ✅ Operation validated before execution
- ✅ Operation executed via Git MCP server
- ✅ Post-validation confirms success
- ✅ Rollback available if needed
- ✅ Clear error messages on failure
- ✅ Audit trail maintained

---

## Tips for Safe Operations

1. **Always validate first** - Use pre-checks before operations
2. **Use MCP server** - Don't bypass with raw git commands
3. **Commit frequently** - Smaller commits easier to rollback
4. **Push after commits** - Keep remote synchronized
5. **Test merge locally** - Check for conflicts before PR
6. **Follow conventions** - Branch names and commit messages
7. **Use rollback** - Don't be afraid to undo and retry

---

## Common Issues and Solutions

### Issue 1: Branch Already Exists
**Problem**: Trying to create branch that already exists
**Solution**: Use different branch name or delete existing branch first

### Issue 2: Uncommitted Changes
**Problem**: Can't switch branches with uncommitted changes
**Solution**: Commit changes, stash changes, or discard changes

### Issue 3: Merge Conflicts
**Problem**: Merge has conflicts that can't auto-resolve
**Solution**: Abort merge, resolve conflicts manually, retry merge

### Issue 4: Push Rejected
**Problem**: Remote has commits not in local
**Solution**: Pull from remote, merge/rebase, then push

### Issue 5: Invalid Branch Name
**Problem**: Branch name doesn't follow conventions
**Solution**: Rename branch to match convention pattern

---

**Last Updated**: 2025-01-30
