---
name: branch-manager
description: Create git branches following project patterns. Use when starting new features, bug fixes, or refactoring. Reads patterns from ai-settings.json.
---

# Branch Manager Skill

You manage git branching strategy for this project.

## When to Use This Skill

- User asks to start a new feature
- User needs to fix a bug
- User plans refactoring work
- Current branch or `main` and changes are needed


```

## Branch Creation Workflow

### Step 1: Check Current Branch

```bash
git branch --show-current
```

### Step 2: Determine Branch Type

Ask the user or infer from context:
- **Feature**: New functionality, enhancement
- **Bugfix**: Fixing a reported issue
- **Refactor**: Code restructuring without behavior change
- **Hotfix**: Urgent production fix

### Step 3: Generate Branch Name

Apply the appropriate pattern:

**Feature** (no issue ID):
```bash
git checkout -b feature/short-descriptive-name
```

**Bugfix** (with issue ID):
```bash
git checkout -b bugfix/123-issue-description
```

**Refactor**:
```bash
git checkout -b feature/refactor-area-name
```

Branch naming conventions:
- Use lowercase letters
- Separate words with hyphens
- Keep descriptions short but descriptive
- For bugfixes, include issue ID if available

### Step 4: Verify Branch Creation

```bash
git status
```

Ensure:
- New branch is created
- It's based on the correct starting point
- No uncommitted changes remain on main branch

## Protection Policy

If `main_branch_protected: true`:

**ALWAYS** check if on `master` or `main`:
```bash
current_branch=$(git branch --show-current)
if [ "$current_branch" = "master" ] || [ "$current_branch" = "main" ]; then
    echo "Main branch is protected. Create a feature branch first."
fi
```

**Before ANY changes** on main:
1. Remind user to create a branch
2. Offer to create the branch automatically
3. Do NOT proceed with changes until on feature branch

## Merge Strategy

Inform user of the configured merge strategy:
- `squash_or_rebase`: Commits will be squashed or rebased when merging
- This means clean history on main branch

## Output Format

### Successful Branch Creation

```
Branch Created Successfully

Type: Feature
Name: feature/thermocalc-integration
Based on: master (commit 9e9387b)

Next steps:
1. Make your changes
2. Commit in small chunks (<=250 lines)
3. Update CHANGELOG.md before each commit
4. Request review before merging to master
```

### Protection Warning

```
Main Branch Protected

You are on 'master' branch. Direct changes are not allowed.

Shall I create a feature branch for you?
- feature/your-feature-name (recommended)
- bugfix/123-issue-name (if fixing a bug)
```

## References

See [branch_helpers.md](branch_helpers.md) for git command examples and troubleshooting.
See [templates/branch_patterns.md](templates/branch_patterns.md) for project-specific naming conventions.
