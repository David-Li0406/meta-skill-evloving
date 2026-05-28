---
name: update-after-merge
description: Clean up after PR merge - switch to default branch, delete feature branch, pull latest
allowed-tools: Bash
---

# Update After Merge Skill

Clean up local repository after a PR is merged.

## Usage

```bash
/update-after-merge              # Clean up current feature branch
/update-after-merge branch-name  # Clean up specific branch
```

## What It Does

1. Checks for uncommitted changes (stash if needed)
2. Switches to default branch (main/master)
3. Pulls latest changes
4. Deletes the merged feature branch (local)
5. Deletes remote branch if still exists
6. Prunes stale remote references

## Safety

Uses `git branch -d` (safe delete) - won't delete unmerged branches.

## Runbook

Full procedure: `runbook/update-after-merge.md` in your knowledge base.
