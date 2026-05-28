# PR Merge Process

**READ THIS ENTIRE DOCUMENT BEFORE MERGING ANY PR.**

This document contains critical steps that MUST be followed in order. Skipping steps will cause PRs to be auto-closed by GitHub or create orphaned branches.

---

## Pre-Merge Verification Checklist

Before executing ANY merge step, verify ALL of the following:

- [ ] User has EXPLICITLY approved merging (said "approved", "lgtm", "merge it", etc.)
- [ ] You are merging PRs in dependency order (oldest/parent FIRST)
- [ ] CI has passed on all PRs being merged
- [ ] You have identified all child PRs that need base branch updates

**If ANY checkbox is not checked: STOP. DO NOT MERGE.**

---

## Critical: Update Child PR Bases BEFORE Merging

GitHub automatically closes PRs when their base branch is deleted.

**This step is MANDATORY before every merge:**

### Step 1: Find Child PRs

```bash
gh pr list --base <branch-being-merged> --json number,headRefName
```

Example: Before merging `sprint-1/pr1/scaffold`:
```bash
gh pr list --base sprint-1/pr1/scaffold --json number,headRefName
# Returns: [{"number": 42, "headRefName": "sprint-1/pr2/state-service"}]
```

### Step 2: Update Each Child PR's Base

```bash
gh pr edit <child-pr-number> --base <parent-base-branch>
```

Example: Update PR #42 to target `main` instead of the branch being merged:
```bash
gh pr edit 42 --base main
```

**Do this for EVERY child PR before proceeding to merge.**

---

## Merge Execution

### Step 3: Rebase Merge and Delete Remote Branch

```bash
gh pr merge <pr-number> --rebase --delete-branch
```

This:
- Rebase-merges the PR into its base branch (preserves commit hash)
- Deletes the remote branch automatically
- Updates the PR status to "merged"

**Why rebase-merge (NOT squash-merge):**
- With jj's workflow, each PR already has a single commit
- Rebase-merge preserves the commit hash, so jj recognizes the commit is now on main
- Squash-merge creates a NEW hash, leaving orphaned "zombie" commits locally
- Using rebase-merge eliminates manual cleanup with `jj abandon`

### Step 4: Sync Local State

**Load the `jujutsu` skill** and use its sync workflow:

```bash
jj git fetch
```

This updates your local repository with the merged changes from the remote. Because we use rebase-merge, jj will recognize that your local commit is now on main.

### Step 5: Rebase ALL Remaining Work

After fetching, rebase **ALL** unmerged work onto the updated main—not just the stack you were actively merging.

```bash
# 1. Find ALL unmerged work (critical: check for other branches!)
jj log -r 'trunk()..visible_heads()' --no-pager

# 2. Rebase EACH unmerged branch onto main
# For each separate branch/head you see, rebase it:
jj rebase -s <change-id> -d main
```

**CRITICAL**: The `visible_heads()` query returns ALL branches that aren't on main. If you have multiple feature branches (e.g., S6PR7 on a separate branch from S6PR3-5), you must rebase EACH one individually. Missing this step leaves branches behind main.

**Example with multiple branches:**
```bash
# After merging S6PR5, you see:
#   - S6PR6 (was stacked on S6PR5, now needs rebase)
#   - S6PR7 (separate branch, also needs rebase)

jj rebase -s <S6PR6-change-id> -d main
jj rebase -s <S6PR7-change-id> -d main
```

**Note:** With rebase-merge, you do NOT need to `jj abandon` the merged commit—jj automatically recognizes it's now part of main.

### Step 6: Handle Any Conflicts

If conflicts occur during rebase, use jujutsu skill's conflict resolution workflow:

1. Check for conflicts: `jj resolve --list`
2. Read conflicted files and resolve markers
3. Write clean files (jj auto-snapshots resolution)
4. Verify: `jj status`

### Step 7: Verify and Log

```bash
jj log --limit 5
jj status
```

Log: "S<N>PR<M> merged successfully"

---

## Complete Merge Sequence Example

Merging S1PR1 which has child S1PR2:

```bash
# 1. Find children
gh pr list --base sprint-1/pr1/scaffold --json number,headRefName
# Output: [{"number": 42, "headRefName": "sprint-1/pr2/state-service"}]

# 2. Update child base BEFORE merge
gh pr edit 42 --base main

# 3. Now safe to merge (use rebase, NOT squash)
gh pr merge 41 --rebase --delete-branch

# 4. Sync local state (load jujutsu skill first)
jj git fetch

# 5. Rebase remaining work onto updated main
jj rebase -s <S1PR2-change-id> -d main

# 6. Verify
jj log --limit 5
jj status
```

---

## Common Mistakes and How to Avoid Them

| Mistake | Consequence | Prevention |
|---------|-------------|------------|
| Merge without updating child PR bases | GitHub auto-closes child PRs | ALWAYS run `gh pr list --base` first |
| Merge child before parent | Broken diffs, merge conflicts | Process in dependency order |
| Skip fetch after merge | Stale local state | ALWAYS fetch after merge |
| Only rebase active stack, not all branches | Other branches left behind main | Run `jj log -r 'trunk()..visible_heads()'` and rebase ALL |

---

## Troubleshooting

### Child PR was auto-closed by GitHub

If you forgot to update the base before merging:
1. The PR is closed but branch still exists locally
2. Push the branch again: `jj git push --bookmark <bookmark-name>`
3. Create new PR: `gh pr create`

### Conflicts after fetch

Use jujutsu skill's conflict resolution workflow:
1. Check which file(s) have conflicts: `jj resolve --list`
2. Open and resolve each conflict
3. jj auto-snapshots resolved files
4. Verify with `jj status`

### Zombie commits after squash-merge

If squash-merge was used accidentally, orphaned "zombie" commits will remain:
1. Find them: `jj log -r 'trunk()..visible_heads()'`
2. Abandon them: `jj abandon <zombie-change-id>`
3. Use `--rebase` for future merges to avoid this
