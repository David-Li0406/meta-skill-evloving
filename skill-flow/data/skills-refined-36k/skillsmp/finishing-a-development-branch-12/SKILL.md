---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
license: MIT
compatibility: opencode
metadata:
  workflow: git
  phase: completion
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

## The Process

### Step 1: Verify Tests

**Before presenting options, verify tests pass:**

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

Stop. Don't proceed to Step 2.

**If tests pass:** Continue to Step 2.

### Step 2: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

### Step 3: Present Options

Use the `question` tool to present the user with exactly these 4 options.

**Tool Call Example:**
```typescript
question({
  "header": "Branch Complete",
  "question": "Implementation complete. What would you like to do?",
  "options": [
    { "label": "Merge to <base-branch>", "description": "Merge this branch locally into <base-branch> and delete it." },
    { "label": "Create Pull Request", "description": "Push the branch and open a new pull request." },
    { "label": "Keep As-Is", "description": "Do nothing and leave the branch as is." },
    { "label": "Discard Work", "description": "Delete the branch and all its changes permanently." }
  ]
})
```

**Note:** Before showing the options, determine the `<base-branch>` as described in Step 2 and substitute it in the option label.

### Step 4: Execute Choice

Before executing the user's choice, you must resolve these placeholders:

-   **`<feature-branch>`**: Get this from the current branch name (`git branch --show-current`).
-   **`<base-branch>`**: Use the branch name you determined in Step 2.
-   **`<test command>`**: Use the project's primary test command that you verified in Step 1.
-   **`<title>`**: For a PR, create a concise, one-line title summarizing the work.
-   **`<worktree-path>`**: If using git worktrees, get the path from the `git worktree list` command.

---

#### Option 1: Merge Locally

```bash
# Switch to base branch
git checkout <base-branch>

# Pull latest
git pull

# Merge feature branch
git merge <feature-branch>

# Verify tests on merged result
<test command>

# If tests pass
git branch -d <feature-branch>
```

Then: Cleanup worktree (Step 5)

---

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

Then: Cleanup worktree (Step 5)

---

#### Option 3: Keep As-Is

Report: "Keeping branch `<feature-branch>`. Worktree preserved at `<worktree-path>`."

**Don't cleanup worktree.**

---

#### Option 4: Discard

**Confirm first** using the `question` tool. Present the consequences clearly.

**Tool Call Example:**
```typescript
question({
  "header": "Confirm Discard",
  "question": "This will permanently delete the branch and all of its commits. This action cannot be undone. Are you sure?",
  "options": [
    { "label": "Yes, Discard Branch", "description": "Permanently delete the <feature-branch> branch." },
    { "label": "No, Cancel", "description": "Do not delete the branch." }
  ]
})
```

If the user confirms, proceed with deletion:
```bash
# Determine base branch to switch to
BASE_BRANCH=$(git merge-base HEAD main 2>/dev/null || git merge-base HEAD master)

# Checkout base branch
git checkout $BASE_BRANCH

# Delete feature branch
git branch -D <feature-branch>
```

Then: Cleanup worktree (Step 5)

### Step 5: Cleanup Worktree

**For Options 1, 2, 4:**

Check if in worktree:
```bash
git worktree list | grep $(git branch --show-current)
```

If yes:
```bash
git worktree remove <worktree-path>
```

**For Option 3:** Keep worktree.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | ✓ | - | - | ✓ |
| 2. Create PR | - | ✓ | ✓ | - |
| 3. Keep as-is | - | - | ✓ | - |
| 4. Discard | - | - | - | ✓ (force) |

## Common Mistakes

**Skipping test verification**
- **Problem:** Merge broken code, create failing PR
- **Fix:** Always verify tests before offering options

**Open-ended questions**
- **Problem:** "What should I do next?" → ambiguous
- **Fix:** Present exactly 4 structured options

**Automatic worktree cleanup**
- **Problem:** Remove worktree when might need it (Option 2, 3)
- **Fix:** Only cleanup for Options 1 and 4

**No confirmation for discard**
- **Problem:** Accidentally delete work
- **Fix:** Require typed "discard" confirmation

## Red Flags

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request

**Always:**
- Verify tests before offering options
- Present exactly 4 options
- Get typed confirmation for Option 4
- Clean up worktree for Options 1 & 4 only

## Integration

**Called by:**
- **subagent-driven-development** (Step 7) - After all tasks complete
- **executing-plans** (Step 5) - After all batches complete

**Pairs with:**
- **using-git-worktrees** - Cleans up worktree created by that skill
