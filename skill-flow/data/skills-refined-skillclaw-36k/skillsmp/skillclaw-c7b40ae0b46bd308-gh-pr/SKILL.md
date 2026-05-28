---
name: gh-pr
description: Use this skill when you need to create or update GitHub Pull Requests with the gh CLI, ensuring proper handling of existing PRs and branch management.
---

# GH PR

## Overview

Create or update GitHub Pull Requests with the gh CLI using a detailed body template and strict same-branch rules.

## Decision rules (must follow)

1. **Do not create or switch branches.** Always use the current branch as the PR head.
2. **Check for an existing PR for the current head branch.**
   - `gh pr list --head <head> --state all --json number,state,mergedAt,updatedAt,url,title,mergeCommit`
3. **If no PR exists** → create a new PR.
4. **If any PR exists and is NOT merged** (`mergedAt` is null) → push only and finish (do **not** create a new PR).
   - This applies to OPEN or CLOSED (unmerged) PRs.
   - Only update title/body/labels if the user explicitly requests changes.
5. **If all PRs for the head are merged** → check for post-merge commits (see below).
6. **If multiple PRs exist for the head** → use the most recently updated PR for reporting, but the create vs push decision is based on `mergedAt`.

## Post-merge commit check (critical)

When all PRs for the head branch are merged, you **must** check whether there are new commits after the merge:

1. **Get the merge commit SHA** of the most recent merged PR.
2. **Count commits after the merge**: `git rev-list --count <merge_commit>..HEAD`
3. **Decision**:
   - If new commits exist → create a new PR (these changes are not in the base branch).
   - If no new commits → report "No changes since last merge" and finish (do **not** create an empty PR).

### Why this matters

- **Scenario A**: PR merged → user makes local changes → pushes → changes are NOT in the merged PR.
  - Without this check, the changes would be lost or require manual intervention.
- **Scenario B**: PR merged → user says "create PR" without new changes → would create empty/duplicate PR.
  - This check prevents unnecessary PR creation.

## Workflow (recommended)

1. **Confirm repo + branches**
   - Repo root: `git rev-parse --show-toplevel`
   - Current branch (head): `git rev-parse --abbrev-ref HEAD`
   - Base branch defaults to `develop` unless user specifies.

2. **Fetch latest remote state**
   - `git fetch origin` to ensure accurate state.