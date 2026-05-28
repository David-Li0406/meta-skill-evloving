---
name: cat:merge-subagent
description: Use this skill to merge a completed subagent branch into the main task branch, resolving any conflicts and cleaning up afterward.
---

# Skill body

## Purpose

Integrate a completed subagent's work back into the parent task branch. This skill handles the merge process, resolves conflicts if necessary, cleans up the subagent branch and worktree, and updates tracking state.

## When to Use

- After `collect-results` confirms subagent work is ready.
- When the subagent has completed its task successfully.
- To preserve partial results from an interrupted subagent.
- When ready to consolidate subagent work into the main task flow.

## Concurrent Execution Safety

This skill operates under the task lock held by `/cat:work`. Refresh the lock heartbeat for long-running merge operations:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/task-lock.sh" heartbeat "$TASK_ID" "${CLAUDE_SESSION_ID}"
```

The task lock is released by the `work` cleanup step after all subagent work is merged.

## Workflow

### 1. Verify Prerequisites

```bash
SUBAGENT_ID="a1b2c3d4"
TASK="1.2-implement-parser"
SUBAGENT_BRANCH="${TASK}-sub-${SUBAGENT_ID}"
TASK_BRANCH="${TASK}"
WORKTREE=".worktrees/${SUBAGENT_BRANCH}"

# Verify subagent results collected
# Check parent STATE.md for ready_for_merge: true

# Verify task branch exists
git branch --list "${TASK_BRANCH}"

# Verify subagent branch exists
git branch --list "${SUBAGENT_BRANCH}"
```

### 2. Checkout Task Branch

```bash
# Return to main workspace (not worktree)
cd /workspace

# Ensure clean working state
git status --porcelain
# Should be empty or only untracked files

# Checkout task branch
git checkout "${TASK_BRANCH}"

# Ensure up to date
git pull origin "${TASK_BRANCH}" 2>/dev/null || true
```

### 3. Merge Subagent Branch

```bash
# Attempt merge
git merge "${SUBAGENT_BRANCH}" --no-edit -m "Merge subagent ${SUBAGENT_ID}: ${TASK}"
```

### 4. Handle Conflicts (If Any)

If the merge fails with conflicts:

```bash
# List conflicted files
git diff --name-only --diff-filter=U

# For each conflict, resolve:
# Option A: Accept subagent version (theirs)
git checkout --theirs path/to/file.java

# Option B: Accept task branch version (ours)
git checkout --ours path/to/file.java

# Option C: Manual resolution
# Edit file to resolve conflicts, then:
git add path/to/file.java

# Complete merge
git commit -m "Merge subagent ${SUBAGENT_ID} with conflict resolution"
```

**Conflict Resolution Strategy:**
1. **Code files**: Prefer subagent version (they have fresher context).
2. **Config files**: Manual resolution may be necessary.