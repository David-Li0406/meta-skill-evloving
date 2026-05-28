---
description: Complete a task - supports worktree and in-session workflows
argument-hint: <task-id> [--push]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# Complete Task

Finalize a completed task. Supports multiple workflows:

1. **In-Session Mode:** PROMPT.md exists, no worktree - complete task in current session
2. **Worktree Phase 1:** From task worktree - commit, rebase, mark pending merge
3. **Worktree Phase 2:** From main - fast-forward merge, archive, cleanup

**Arguments:** $ARGUMENTS

## Mode Detection

This command automatically detects the workflow mode:

```bash
CURRENT_BRANCH=$(git branch --show-current)
GIT_DIR=$(git rev-parse --git-dir 2>/dev/null)
GIT_COMMON=$(git rev-parse --git-common-dir 2>/dev/null)

# Check if we're in a worktree (git dir differs from common dir)
IS_WORKTREE="false"
if [[ -n "$GIT_DIR" && -n "$GIT_COMMON" && "$GIT_DIR" != "$GIT_COMMON" ]]; then
  IS_WORKTREE="true"
fi

# Check if PROMPT.md exists (indicates in-session or worktree work)
HAS_PROMPT="false"
if [[ -f "PROMPT.md" ]]; then
  HAS_PROMPT="true"
fi
```

**Mode determination:**

| Condition | Mode |
|-----------|------|
| In worktree, not on main | Worktree Phase 1 |
| On main, task has worktree | Worktree Phase 2 |
| PROMPT.md exists, NOT in worktree | **In-Session Mode** |
| On main, PROMPT.md exists | In-Session (main branch) |
| On feature branch, PROMPT.md, no worktree | In-Session (feature branch) |

---

## In-Session Mode

**Context:** PROMPT.md exists in current directory, NOT running from a worktree. This handles tasks started with `/backlog:work`.

### In-Session Step 1: Detect Task ID

```bash
# If task ID provided in arguments, use it
# Otherwise, extract from PROMPT.md
if [[ -z "$TASK_ID" ]]; then
  TASK_ID=$(grep "^\*\*Task:\*\*" PROMPT.md | sed 's/.*\*\*Task:\*\* \([A-Z]*-[0-9]*\).*/\1/' | head -1)
fi

if [[ -z "$TASK_ID" ]]; then
  echo "ERROR: Could not determine task ID"
  echo "Usage: /backlog:complete <task-id>"
  exit 1
fi

echo "Completing in-session task: ${TASK_ID}"
```

### In-Session Step 2: Commit Changes

```bash
# Stage all changes except PROMPT.md
git add -A
git reset HEAD PROMPT.md 2>/dev/null || true

# Check if there are changes to commit
if ! git diff --cached --quiet; then
  git commit -m "feat(${TASK_ID}): implement task"
  echo "✓ Committed changes"
else
  echo "✓ No changes to commit"
fi
```

### In-Session Step 3: Handle Branch (if not on main)

```bash
CURRENT_BRANCH=$(git branch --show-current)

if [[ "$CURRENT_BRANCH" != "main" && "$CURRENT_BRANCH" != "master" ]]; then
  echo "On feature branch: ${CURRENT_BRANCH}"
  echo "Rebasing onto main..."

  # Fetch latest main
  git fetch origin main 2>/dev/null || true

  # Rebase onto main
  if git rebase main; then
    echo "✓ Rebased onto main"
  else
    echo "ERROR: Rebase conflicts detected"
    echo ""
    echo "Resolution steps:"
    echo "1. Fix conflicts in the listed files"
    echo "2. Stage resolved files: git add <files>"
    echo "3. Continue rebase: git rebase --continue"
    echo "4. Re-run /backlog:complete ${TASK_ID}"
    exit 1
  fi

  # Switch to main and merge
  echo "Switching to main and merging..."
  git checkout main
  git merge --ff-only "${CURRENT_BRANCH}"

  if [[ $? -eq 0 ]]; then
    echo "✓ Merged to main"

    # Delete feature branch
    git branch -d "${CURRENT_BRANCH}"
    echo "✓ Deleted branch ${CURRENT_BRANCH}"
  else
    echo "ERROR: Fast-forward merge failed"
    echo "Main may have advanced. Try rebasing again."
    git checkout "${CURRENT_BRANCH}"
    exit 1
  fi
fi
```

### In-Session Step 4: Cleanup PROMPT.md

```bash
# Remove PROMPT.md to keep main clean
rm -f PROMPT.md
echo "✓ Removed PROMPT.md"
```

### In-Session Step 5: Update INDEX.md

```bash
# Update status to Complete
sed -i.bak "s/| ${TASK_ID} |\([^|]*\)| In Progress |/| ${TASK_ID} |\1| Complete |/" tasks/INDEX.md
rm -f tasks/INDEX.md.bak

git add tasks/INDEX.md
git commit -m "chore: mark ${TASK_ID} as complete"
echo "✓ Task marked as Complete"
```

### In-Session Step 6: Push (Optional)

```bash
if [[ "$ARGUMENTS" == *"--push"* ]]; then
  echo "Pushing to origin..."
  if git push origin main; then
    echo "✓ Pushed to origin/main"
    PUSHED="yes"
  else
    echo "WARNING: Push failed"
    PUSHED="failed"
  fi
else
  PUSHED="no"
fi
```

### In-Session Step 7: Update Built-in Task Feature

**IMPORTANT:** Mark the built-in Task as completed for session tracking.

Call `TaskList` to find the task with subject containing `{TASK_ID}`.

If found, call `TaskUpdate` with:
- **taskId**: The ID of the matching task
- **status**: `completed`

This updates the session's task tracking to reflect completion.

### In-Session Step 8: Output Summary

```
═══════════════════════════════════════════════════════════════════
 TASK COMPLETED: {TASK_ID}
═══════════════════════════════════════════════════════════════════

## Summary

- Task: {TASK_ID} - {Title}
- Mode: In-Session (no worktree)
- Branch merged: {yes/no - if was on feature branch}
- Pushed to origin: {yes/no/failed}

## Cleanup

✓ PROMPT.md removed
✓ INDEX.md updated to Complete
✓ Built-in Task marked completed
{If was on feature branch}
✓ Feature branch deleted

## Next Steps

1. View backlog: /backlog
2. Start next task: /backlog:work <task-id>
3. Or create worktree: /backlog:launch <task-id>

═══════════════════════════════════════════════════════════════════
```

**Exit after in-session completion.**

---

## Worktree Workflow Overview

For tasks started with `/backlog:launch`, use the two-phase worktree workflow:

- **Task worktree** → Execute Phase 1 (prepare for merge)
- **Main worktree** → Execute Phase 2 (finalize and cleanup)

---

## Phase 1: Prepare from Task Worktree

**Context:** Running from task's worktree branch (NOT main)

### Step 1: Verify Context

```bash
CURRENT_BRANCH=$(git branch --show-current)

# Check we're NOT on main
if [[ "$CURRENT_BRANCH" == "main" ]]; then
  echo "ERROR: Phase 1 must be run from task worktree, not main"
  echo "Switch to task worktree or run Phase 2 to finalize completion"
  exit 1
fi
```

### Step 2: Determine Task ID

- If task ID provided in arguments, use it
- If NOT provided, use AskUserQuestion to select from active tasks
- Find task directory:
  ```bash
  ls -d tasks/${TASK_ID}-* 2>/dev/null
  ```

### Step 3: Commit Remaining Changes

**Commit everything EXCEPT PROMPT.md:**

```bash
# Stage all changes except PROMPT.md
git add -A
git reset HEAD PROMPT.md 2>/dev/null || true

# Check if there are changes to commit
if ! git diff --cached --quiet; then
  git commit -m "chore(${TASK_ID}): finalize task implementation"
  echo "✓ Committed final changes"
else
  echo "✓ No changes to commit"
fi
```

### Step 4: Rebase onto Local Main

```bash
echo "Rebasing ${CURRENT_BRANCH} onto local main..."
if git rebase main; then
  echo "✓ Successfully rebased onto main"
else
  echo "ERROR: Rebase conflicts detected"
  echo ""
  echo "Resolution steps:"
  echo "1. Fix conflicts in the listed files"
  echo "2. Stage resolved files: git add <files>"
  echo "3. Continue rebase: git rebase --continue"
  echo "4. Re-run /backlog:complete ${TASK_ID}"
  exit 1
fi
```

### Step 5: Mark Task as Pending Merge

Update INDEX.md status from "In Progress" to "Pending Merge":

```bash
# Update status in INDEX.md
sed -i.bak "s/| ${TASK_ID} |\([^|]*\)| In Progress |/| ${TASK_ID} |\1| Pending Merge |/" tasks/INDEX.md
rm -f tasks/INDEX.md.bak

git add tasks/INDEX.md
git commit -m "chore: mark ${TASK_ID} as pending merge"
echo "✓ Task marked as Pending Merge"
```

### Step 6: Phase 1 Complete - Display Instructions

```
═══════════════════════════════════════════════════════════════════
 PHASE 1 COMPLETE: {TASK_ID}
═══════════════════════════════════════════════════════════════════

## Task Ready for Merge

- Task: {TASK_ID} - {Title}
- Branch: {branch-name}
- Status: Pending Merge
- Rebased onto: main ({main-sha})

## Next Steps

1. Exit this Claude session in the worktree
2. Open a new Claude session in the MAIN worktree
3. Run: /backlog:complete {TASK_ID} [--push]

This will:
- Fast-forward merge main to include your changes
- Mark task as Complete
- Archive task files to tasks/archive/
- Remove the worktree and branch
- Update dependent tasks

═══════════════════════════════════════════════════════════════════
```

**CRITICAL: Output the following promise tag to allow session exit:**

```
<promise>TASK_BLOCKED:phase1_complete_switch_to_main_worktree</promise>
```

**Exit after Phase 1 - do NOT proceed to Phase 2 from worktree**

---

## Phase 2: Finalize from Main Worktree

**Context:** Running from main branch worktree

> **CRITICAL WORKFLOW NOTE:** In Phase 2, do NOT check task status from the local `tasks/INDEX.md` on main. The "Pending Merge" status exists ONLY on the worktree branch (committed during Phase 1). You MUST:
> 1. Find the worktree branch first
> 2. Use `git show BRANCH:tasks/INDEX.md` to read status from the worktree branch
> 3. Only proceed if status is "Pending Merge" on the worktree branch

### Step 1: Verify Context

```bash
CURRENT_BRANCH=$(git branch --show-current)

# Check we're on main
if [[ "$CURRENT_BRANCH" != "main" ]]; then
  echo "ERROR: Phase 2 must be run from main worktree"
  echo "Current branch: ${CURRENT_BRANCH}"
  echo "Please switch to main worktree or run Phase 1 from task worktree"
  exit 1
fi
```

### Step 2: Determine Task ID

- If task ID provided in arguments, use it
- If NOT provided, use AskUserQuestion to select from tasks with active worktrees

### Step 3: Find Worktree Branch

**IMPORTANT:** Find the branch FIRST because we need to check status from the worktree branch, not main.

```bash
# List all worktrees and find one matching the task ID pattern
WORKTREE_INFO=$(git worktree list --porcelain | grep -A2 "worktree.*${TASK_ID}\|branch.*${TASK_ID}" | head -3)

# Extract branch name from worktree list
BRANCH_NAME=$(git worktree list | grep -i "${TASK_ID}" | awk '{print $3}' | tr -d '[]')

# Alternative: Check for branches matching task ID pattern
if [[ -z "$BRANCH_NAME" ]]; then
  BRANCH_NAME=$(git branch --list "*${TASK_ID}*" --format='%(refname:short)' | head -1)
fi

if [[ -z "$BRANCH_NAME" ]]; then
  echo "ERROR: Could not find branch for task ${TASK_ID}"
  echo ""
  echo "Available worktrees:"
  git worktree list
  echo ""
  echo "Available branches:"
  git branch --list "*task*" "*review*" "*feature*" 2>/dev/null || git branch
  exit 1
fi

# Verify branch exists
if ! git rev-parse --verify "$BRANCH_NAME" >/dev/null 2>&1; then
  echo "ERROR: Branch ${BRANCH_NAME} not found"
  exit 1
fi

echo "Found branch: ${BRANCH_NAME}"
```

### Step 4: Verify Task Status (from Worktree Branch)

**CRITICAL:** Check the task status from the WORKTREE BRANCH, not from main. The "Pending Merge" status was committed on the worktree branch during Phase 1 and hasn't been merged to main yet.

```bash
# Read INDEX.md from the worktree branch (not main!)
BRANCH_INDEX=$(git show "${BRANCH_NAME}:tasks/INDEX.md" 2>/dev/null)

if [[ -z "$BRANCH_INDEX" ]]; then
  echo "ERROR: Could not read tasks/INDEX.md from branch ${BRANCH_NAME}"
  exit 1
fi

# Check task status from the worktree branch's INDEX.md
TASK_STATUS=$(echo "$BRANCH_INDEX" | grep "| ${TASK_ID} |" | awk -F'|' '{print $4}' | xargs)

echo "Task status on ${BRANCH_NAME}: ${TASK_STATUS}"

if [[ "$TASK_STATUS" != "Pending Merge" ]]; then
  echo "ERROR: Task ${TASK_ID} is not ready for merge"
  echo "Current status on branch ${BRANCH_NAME}: ${TASK_STATUS}"
  echo ""
  echo "Task must have 'Pending Merge' status (set during Phase 1)"
  echo "Run Phase 1 from the task worktree first: /backlog:complete ${TASK_ID}"
  exit 1
fi

echo "✓ Task is Pending Merge (verified from worktree branch)"
```

### Step 5: Verify Fast-Forward Possible

```bash
# Check if main can fast-forward to branch
MERGE_BASE=$(git merge-base main "$BRANCH_NAME")
MAIN_HEAD=$(git rev-parse main)

if [[ "$MERGE_BASE" != "$MAIN_HEAD" ]]; then
  echo "ERROR: Cannot fast-forward merge"
  echo "Main has diverged from ${BRANCH_NAME}"
  echo ""
  echo "This usually means:"
  echo "1. The worktree was not rebased onto main (run Phase 1 again)"
  echo "2. Main has advanced since the rebase (rebase worktree again)"
  exit 1
fi

echo "✓ Fast-forward merge possible"
```

### Step 6: Fast-Forward Merge

```bash
BRANCH_HEAD=$(git rev-parse "$BRANCH_NAME")
COMMITS_AHEAD=$(git rev-list --count main.."$BRANCH_NAME")

echo "Merging ${COMMITS_AHEAD} commits from ${BRANCH_NAME}..."
git merge --ff-only "$BRANCH_NAME"

if [[ $? -eq 0 ]]; then
  echo "✓ Fast-forward merge successful"
  echo "  main: ${MAIN_HEAD:0:7} -> ${BRANCH_HEAD:0:7}"
else
  echo "ERROR: Fast-forward merge failed"
  exit 1
fi
```

### Step 7: Push to Origin (Optional)

```bash
# Check for --push flag in arguments
if [[ "$ARGUMENTS" == *"--push"* ]]; then
  echo "Pushing main to origin..."
  if git push origin main; then
    echo "✓ Pushed to origin/main"
    PUSHED="yes"
  else
    echo "WARNING: Push failed"
    PUSHED="failed"
  fi
else
  PUSHED="no"
fi
```

### Step 8: Mark Task Complete

```bash
# Update status from "Pending Merge" to "Complete"
sed -i.bak "s/| ${TASK_ID} |\([^|]*\)| Pending Merge |/| ${TASK_ID} |\1| Complete |/" tasks/INDEX.md
rm -f tasks/INDEX.md.bak

git add tasks/INDEX.md
git commit -m "chore: mark task ${TASK_ID} as complete"
echo "✓ Task marked as Complete"
```

### Step 9: Cascade Dependency Updates

**Update dependent tasks that are now unblocked:**

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/deps.sh"
deps_build_graph

# Get tasks that depend on this one
dependents=$(deps_get_dependents "${TASK_ID}")
UNBLOCKED_TASKS=()

if [[ -n "$dependents" ]]; then
  echo "Checking dependent tasks..."

  for dependent in $dependents; do
    # Compute new status (may change from Blocked to Ready)
    old_status="${DEPS_STATUS[$dependent]:-}"
    DEPS_STATUS["${TASK_ID}"]="Complete"
    new_status=$(deps_compute_status "$dependent")

    if [[ "$old_status" == "Blocked" && "$new_status" == "Ready" ]]; then
      echo "  $dependent: Blocked -> Ready (unblocked by ${TASK_ID})"
      UNBLOCKED_TASKS+=("$dependent")

      # Update INDEX.md
      sed -i.bak "s/| $dependent |\([^|]*\)| Blocked |/| $dependent |\1| Ready |/" tasks/INDEX.md
      rm -f tasks/INDEX.md.bak
    fi
  done

  # Commit cascade updates
  if ! git diff --quiet tasks/INDEX.md; then
    git add tasks/INDEX.md
    git commit -m "chore: unblock tasks dependent on ${TASK_ID}"

    if [[ "$PUSHED" == "yes" ]]; then
      git push origin main
    fi
  fi
fi
```

### Step 10: Archive Task Files

**Move completed task to archive:**

```bash
# Create archive directory if it doesn't exist
mkdir -p tasks/archive

# Get task directory name
TASK_DIR=$(ls -d tasks/${TASK_ID}-* 2>/dev/null | head -1)

if [[ -n "$TASK_DIR" ]]; then
  TASK_NAME=$(basename "$TASK_DIR")
  echo "Archiving ${TASK_NAME}..."

  mv "$TASK_DIR" tasks/archive/

  git add tasks/
  git commit -m "chore: archive ${TASK_ID} task files"

  if [[ "$PUSHED" == "yes" ]]; then
    git push origin main
  fi

  echo "✓ Task files archived to tasks/archive/${TASK_NAME}"
else
  echo "⚠ No task directory found for ${TASK_ID}"
fi
```

### Step 11: Remove Worktree and Branch

**Clean up the worktree:**

```bash
# Find worktree path
WORKTREE_PATH=$(git worktree list | grep "$BRANCH_NAME" | awk '{print $1}')

if [[ -n "$WORKTREE_PATH" ]]; then
  echo "Removing worktree: ${WORKTREE_PATH}..."

  # Remove worktree
  if [[ -d "$WORKTREE_PATH" ]]; then
    rm -rf "$WORKTREE_PATH"
  fi

  git worktree prune
  echo "✓ Worktree removed"
else
  echo "⚠ Worktree not found for ${BRANCH_NAME}"
fi

# Delete branch
if git show-ref --verify --quiet "refs/heads/${BRANCH_NAME}"; then
  git branch -D "$BRANCH_NAME"
  echo "✓ Branch ${BRANCH_NAME} deleted"
fi
```

### Step 12: Update Built-in Task Feature

**IMPORTANT:** Mark the built-in Task as completed for session tracking.

Call `TaskList` to find the task with subject containing `{TASK_ID}`.

If found, call `TaskUpdate` with:
- **taskId**: The ID of the matching task
- **status**: `completed`

This updates the session's task tracking to reflect completion.

### Step 13: Phase 2 Complete - Display Summary

```
═══════════════════════════════════════════════════════════════════
 TASK COMPLETED: {TASK_ID}
═══════════════════════════════════════════════════════════════════

## Summary

- Task: {TASK_ID} - {Title}
- Branch: {branch-name}
- Commits merged: {count}
- Main updated to: {short-sha}
- Pushed to origin: {yes/no/failed}
- Task archived: tasks/archive/{task-dir}/
- Worktree removed: ✓
- Branch deleted: ✓
- Built-in Task: ✓ marked completed

## Dependency Cascade

{If dependents were unblocked}
The following tasks are now unblocked:

| Task | Title | Launch Command |
|------|-------|----------------|
| {PREFIX}-{XXX} | {Title} | /backlog:launch {PREFIX}-{XXX} |
| {PREFIX}-{YYY} | {Title} | /backlog:launch {PREFIX}-{YYY} |

Next recommended task:
  /backlog:launch {PREFIX}-{XXX}

{If no dependents}
No dependent tasks were unblocked.

## What Was Cleaned Up

✓ Worktree removed
✓ Branch deleted
✓ Task files archived
✓ PROMPT.md not committed (excluded)
✓ Dependencies updated
✓ Built-in Task marked completed

## Next Steps

1. Launch next task: /backlog:launch <task-id>
2. Or view backlog: /backlog

═══════════════════════════════════════════════════════════════════
```

---

## Arguments Reference

| Argument | Description |
|----------|-------------|
| `<task-id>` | Task ID being completed (e.g., CRANE-003) |
| `--push` | Push main to origin after merge (Phase 2 only) |

## Error Handling

### Phase 1 Errors
- **On main branch:** "Phase 1 must be run from task worktree"
- **Rebase conflicts:** Show resolution steps and abort
- **No changes to commit:** Continue (not an error)

### Phase 2 Errors
- **Not on main:** "Phase 2 must be run from main worktree"
- **Task not Pending Merge:** "Run Phase 1 from task worktree first"
- **Cannot fast-forward:** "Worktree not rebased onto main"
- **Branch not found:** Show available branches
- **Push fails:** Warning only, continue with completion

## Important Notes

- **Two-phase design:** Phase 1 (worktree) prepares, Phase 2 (main) finalizes
- **PROMPT.md never committed:** Automatically excluded in Phase 1
- **Fast-forward only:** Ensures clean linear history
- **Automatic archival:** Task files moved to tasks/archive/ in Phase 2
- **Automatic cleanup:** Worktree and branch removed in Phase 2
- **Safe rollback:** Can abort Phase 1 before Phase 2

## Example: Complete Workflow

### Phase 1 (from task worktree)

```bash
# In task worktree
$ /backlog:complete CRANE-003

Verifying context...
  Current branch: review/crn-test-framework
  ✓ Running Phase 1 from task worktree

Committing final changes...
  ✓ Committed: chore(CRANE-003): finalize task implementation

Rebasing onto main...
  ✓ Successfully rebased 5 commits onto main

Marking as Pending Merge...
  ✓ Task marked as Pending Merge

═══════════════════════════════════════════════════════════════════
 PHASE 1 COMPLETE: CRANE-003
═══════════════════════════════════════════════════════════════════

Next: Open Claude in main worktree and run:
  /backlog:complete CRANE-003 --push

<promise>TASK_BLOCKED:phase1_complete_switch_to_main_worktree</promise>
```

### Phase 2 (from main worktree)

```bash
# In main worktree
$ /backlog:complete CRANE-003 --push

Verifying context...
  Current branch: main
  ✓ Running Phase 2 from main worktree

Finding worktree branch...
  Found branch: review/crn-test-framework

Verifying task status (from worktree branch)...
  Task status on review/crn-test-framework: Pending Merge
  ✓ Task is Pending Merge (verified from worktree branch)

Verifying fast-forward possible...
  ✓ Fast-forward merge possible

Merging 5 commits...
  ✓ main: 1d7397e -> b31577d

Pushing to origin...
  ✓ Pushed to origin/main

Marking task complete...
  ✓ Task marked as Complete

Checking dependencies...
  CRANE-014: Blocked -> Ready
  CRANE-015: Blocked -> Ready
  ✓ Committed dependency updates

Archiving task files...
  ✓ Archived to tasks/archive/CRANE-003-test-framework/

Removing worktree...
  ✓ Worktree removed
  ✓ Branch deleted

═══════════════════════════════════════════════════════════════════
 TASK COMPLETED: CRANE-003
═══════════════════════════════════════════════════════════════════

Tasks unblocked: CRANE-014, CRANE-015

Next: /backlog:launch CRANE-014
```
