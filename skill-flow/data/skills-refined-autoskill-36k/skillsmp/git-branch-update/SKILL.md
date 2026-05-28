---
name: git-branch-update
description: Update branch with main safely. Handles rebase vs merge decision, conflict detection, and recovery.
license: MIT
metadata:
  author: shipitsmarter
  version: "1.0"
---

# Git Branch Update Skill

Safely update a feature branch with the latest changes from main. Handles the rebase vs merge decision intelligently.

---

## Trigger

Use when:
- Branch is behind main before PR review
- Need to incorporate main changes into feature branch
- Merge conflicts need to be resolved

---

## Quick Reference

```bash
# Check if behind main
git fetch origin main
git rev-list --left-right --count origin/main...HEAD
# Output: "X Y" where X = behind, Y = ahead. If X > 0, needs update.

# Via GitHub
gh pr view --json mergeable,mergeStateStatus
```

---

## Process

### Step 1: Check Current State

```bash
git fetch origin main
git status --porcelain  # Must be empty
git rev-list --left-right --count origin/main...HEAD
```

| State | Meaning | Action |
|-------|---------|--------|
| `0 Y` | Up to date | No action needed |
| `X Y` where X > 0 | Behind main | Proceed to Step 2 |
| Dirty working directory | Uncommitted changes | Ask user to commit/stash first |

### Step 2: Ask User for Strategy

**Always ask before modifying the branch:**

```markdown
Branch is **X commits behind** main.

**Options:**
1. **Rebase** (recommended) - Cleaner history, replays your commits on top of main
2. **Merge** - Creates merge commit, preserves branch history

Which approach? [1/2]
```

**When to recommend each:**

| Situation | Recommendation |
|-----------|----------------|
| Solo work, clean history | Rebase |
| Shared branch, others have pulled | Merge |
| Many commits, complex changes | Merge (safer) |
| Simple feature, few commits | Rebase |

### Step 3: Execute Update

#### Option A: Rebase

```bash
git rebase origin/main
```

**If successful:**
```bash
git push --force-with-lease
```

**If conflicts:**
```markdown
Rebase paused due to conflicts in:
- `src/components/Example.vue`
- `src/utils/helpers.ts`

**To resolve:**
1. Edit files to resolve conflicts
2. `git add <resolved-files>`
3. `git rebase --continue`
4. Repeat until complete
5. `git push --force-with-lease`

**To abort:** `git rebase --abort`
```

#### Option B: Merge

```bash
git merge origin/main -m "Merge main into $(git branch --show-current)"
```

**If successful:**
```bash
git push
```

**If conflicts:**
```markdown
Merge paused due to conflicts in:
- `src/components/Example.vue`

**To resolve:**
1. Edit files to resolve conflicts
2. `git add <resolved-files>`
3. `git commit` (merge commit message is pre-filled)
4. `git push`

**To abort:** `git merge --abort`
```

---

## Conflict Resolution Tips

### Common Conflict Patterns

| Pattern | Resolution |
|---------|------------|
| Both modified same line | Manually choose correct version |
| File deleted vs modified | Decide: keep changes or accept deletion |
| Import conflicts | Usually keep both, remove duplicates |

### After Resolving

Always verify:
```bash
npm run lint
npm run type-check
```

---

## Recovery Commands

| Situation | Command |
|-----------|---------|
| Rebase going wrong | `git rebase --abort` |
| Merge going wrong | `git merge --abort` |
| Already pushed bad rebase | `git reflog` to find previous state, then `git reset --hard <hash>` |
| Force push rejected | Someone else pushed; fetch and try again |

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| **pr-review** | Full PR review workflow |
| **github-workflow** | Commit messages, PR creation |
