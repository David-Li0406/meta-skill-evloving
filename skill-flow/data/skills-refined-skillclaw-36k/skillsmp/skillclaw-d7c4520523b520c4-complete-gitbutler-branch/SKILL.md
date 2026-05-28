---
name: complete-gitbutler-branch
description: Use this skill when you need to complete a virtual branch, merge changes into the main branch, or create a pull request using GitButler.
---

# Skill body

## When to Use

- Virtual branch work is complete and ready to ship.
- Tests pass and code is reviewed (if required).
- Ready to merge changes into the main branch.
- Need to clean up completed branches.

**NOT for:** ongoing work, branches needing more development, stacks (complete bottom-to-top).

## Prerequisites

**Before completing any branch:**
- [ ] GitButler initialized (`but --version` succeeds).
- [ ] Virtual branch exists with committed changes.
- [ ] Main branch tracked as base.
- [ ] No uncommitted changes (or changes assigned to branches).
- [ ] Tests passing.

## Quick Start

### Preferred Method: Using `but publish`

```bash
# 1. Verify branch state
but status
but log

# 2. Create safety snapshot
but snapshot --message "Before publishing feature-auth"

# 3. Publish branch (pushes and creates PR)
but publish -b feature-auth

# 4. Review and merge PR on GitHub

# 5. Update local and clean up
but base update
but branch rm feature-auth
```

### Direct Merge to Main

```bash
# 1. Verify branch state
but status
but log

# 2. Create snapshot
but snapshot --message "Before integrating feature-auth"

# 3. Switch to main
git checkout main

# 4. Update main from remote
git pull origin main

# 5. Merge virtual branch
git merge --no-ff refs/gitbutler/feature-auth -m "feat: add user authentication"

# 6. Push to remote
git push origin main

# 7. Clean up and return
but branch rm feature-auth
git checkout gitbutler/workspace
```

### Manual PR Workflow

```bash
# 1. Push branch to remote
git push origin refs/gitbutler/feature-auth:refs/heads/feature-auth

# 2. Create PR
gh pr create

# 3. Merge PR on GitHub

# 4. Clean up
but branch rm feature-auth
```

## Pre-Integration Checklist

Run through before any integration:

| Check | Command | Expected |
|-------|---------|----------|
| GitButler running | `but --version` | Version output |
| Work committed | `but status` | Committed changes, no unassigned files |
| Tests passing | `bun test` (or project equivalent) | All green |
| Base updated | `but base update` | Up to date with main |
| Snapshot created | `but snapshot -m "Before integrating..."` | Snapshot ID returned |