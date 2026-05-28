---
name: finishing-branch
description: Use when implementation complete and tests pass - verifies all tasks done, presents integration options (merge/PR/keep/discard), executes choice
---

# Finishing a Development Branch

## Overview

Guide completion of development work by verifying tasks, running tests, presenting clear options, and handling chosen workflow.

**Core principle:** Verify tasks → Verify tests → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using gambit:finish to complete this work."

## Rigidity Level

LOW FREEDOM - Follow the 6-step process exactly. Present exactly 4 options. Never skip test verification. Must confirm before discarding.

## Quick Reference

| Step | Action | STOP If |
|------|--------|---------|
| 1 | Verify all tasks complete | Any task not completed |
| 2 | Verify tests pass | Any test fails |
| 3 | Determine base branch | - |
| 4 | Present exactly 4 options | No answer received |
| 5 | Execute choice | Git command fails |
| 6 | Cleanup worktree | Options 2,3 skip this step |

## Option Matrix

| Option | Merge | Push | Keep Worktree | Delete Branch | Delete Worktree |
|--------|-------|------|---------------|---------------|-----------------|
| 1. Merge locally | Yes | - | - | Yes | Yes |
| 2. Create PR | - | Yes | **Yes** | - | - |
| 3. Keep as-is | - | - | **Yes** | - | - |
| 4. Discard | - | - | - | Yes (force) | Yes |

**Critical:** Options 2 and 3 keep the worktree. Do not clean up.

## When to Use

- Implementation complete and reviewed
- All tasks for epic are done
- Ready to integrate work back to main branch

**Don't use for:**
- Work still in progress
- Tests failing
- Epic has open tasks
- Mid-implementation (use `gambit:execute-plan`)

## The Process

### Step 1: Verify All Tasks Complete

**Run TaskList:**

```
TaskList
```

**Decision tree:**
- All tasks show status="completed" → Go to Step 2
- Any task shows status="pending" or "in_progress" → **STOP**

**If tasks still open:**

```
Cannot finish: N tasks still open:
- [task-id]: Task Name (status: in_progress)
- [task-id]: Task Name (status: pending)

Complete all tasks before finishing.
```

**STOP. Do not proceed until all tasks completed.**

**If all tasks complete, verify epic success criteria:**

```
TaskGet
  taskId: "epic-task-id"
```

Review success criteria. All must be met.

---

### Step 2: Verify Tests Pass

**REQUIRED: Run full test suite before presenting options.**

**Detect test command:**

| Project Type | Detection | Test Command |
|--------------|-----------|--------------|
| Go | `go.mod` exists | `go test ./...` |
| Node.js | `package.json` exists | `npm test` |
| Rust | `Cargo.toml` exists | `cargo test` |
| Python | `pyproject.toml` or `pytest.ini` | `pytest` |
| Devenv | Check Makefile | `make test` |

**Run tests:**

```bash
# Example for Go
go test ./...
```

**Decision tree:**
- All tests pass (exit code 0) → Go to Step 3
- Any test fails → **STOP**

**If tests fail:**

```
Tests failing (N failures). Must fix before completing:

[Show first 3-5 failures]

Cannot proceed until tests pass.
```

**STOP. Do not proceed until tests pass.**

---

### Step 3: Determine Base Branch

**Check merge base:**

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

**Decision tree:**
- Command succeeds → Use detected base branch
- Command fails → Ask user: "What is the base branch for this work?"

**STOP if user doesn't respond.**

---

### Step 4: Present Options

**REQUIRED: Use AskUserQuestion tool**

```
AskUserQuestion
  questions:
    - question: "Implementation complete. What would you like to do?"
      header: "Integration"
      options:
        - label: "Merge locally"
          description: "Merge to <base-branch>, delete feature branch"
        - label: "Create Pull Request"
          description: "Push and create PR for review"
        - label: "Keep as-is"
          description: "Leave branch, handle later"
        - label: "Discard"
          description: "Delete all work (requires confirmation)"
      multiSelect: false
```

**STOP: Wait for user response before proceeding.**

**Do not add explanation or recommendations.** Present options and wait.

---

### Step 5: Execute Choice

#### Option 1: Merge Locally

**Step 5.1a: Switch to base branch**
```bash
git checkout <base-branch>
```

**Step 5.1b: Pull latest**
```bash
git pull
```

**Step 5.1c: Merge feature branch**
```bash
git merge <feature-branch>
```

**Step 5.1d: Verify tests on merged result**

```bash
go test ./...  # or appropriate test command
```

**Decision tree:**
- Tests pass → Continue to Step 5.1e
- Tests fail → Present sub-options:

```
Merge introduced test failures. Options:
1. Fix failures before completing
2. Abort merge (git merge --abort)

Which option?
```

**STOP: Wait for user choice.**

**Step 5.1e: Delete feature branch**
```bash
git branch -d <feature-branch>
```

**Go to Step 6.**

---

#### Option 2: Create Pull Request

**Step 5.2a: Push branch**
```bash
git push -u origin <feature-branch>
```

**Step 5.2b: Get epic info for PR**
```
TaskGet
  taskId: "epic-task-id"
```

**Step 5.2c: Create PR**
```bash
gh pr create --title "feat: <epic-name>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets from epic requirements>

## Tasks Completed
- Task 1: <description>
- Task 2: <description>

## Test Plan
- [ ] All tests passing
- [ ] <verification steps from epic success criteria>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

**Step 5.2d: Report and preserve worktree**

```
Pull request created: <PR-URL>

Keeping worktree at <absolute-path> for PR updates.
```

**Do NOT go to Step 6. Worktree is preserved for PR feedback.**

**DONE.**

---

#### Option 3: Keep As-Is

**Report:**
```
Keeping branch <name>. Worktree preserved at <absolute-path>.
```

**Do NOT go to Step 6. Worktree is preserved.**

**DONE.**

---

#### Option 4: Discard

**Step 5.4a: Show what will be deleted**

```bash
# Get commit list
git log --oneline <base-branch>..HEAD
```

**Step 5.4b: Request explicit confirmation**

```
This will permanently delete:
- Branch <name>
- All commits:
  * <hash> <message>
  * <hash> <message>
  * ... (N more commits)
- Worktree at <path>

Type 'discard' to confirm.
```

**STOP: Wait for exact text "discard".**

**Decision tree:**
- User types exactly "discard" → Continue to Step 5.4c
- User types anything else → Ask for clarification, do not proceed

**Step 5.4c: Delete branch**
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

**Go to Step 6.**

---

### Step 6: Cleanup Worktree

**Only for Options 1 and 4.**

**Check if worktree exists:**
```bash
git worktree list | grep <feature-branch>
```

**Decision tree:**
- Worktree found → Remove it
- Worktree not found → Skip (might not have used worktree)

**Remove worktree:**
```bash
git worktree remove <worktree-path>
```

**Report:**
```
Worktree removed at <path>.
```

**For Options 2 and 3:** This step is skipped entirely. Worktree preserved.

## Critical Rules

### Rules That Have No Exceptions

1. **Never skip test verification** → Tests must pass before presenting options
2. **Never present more or fewer than 4 options** → Exactly 4, always
3. **Never proceed with Option 4 without typed "discard"** → Exact text required
4. **Never cleanup worktree for Options 2 or 3** → User needs it for PR feedback or later work
5. **Always verify tests after merge (Option 1)** → Merged result might have conflicts
6. **Always verify all tasks complete before Step 2** → Can't finish incomplete work

### Common Excuses

All of these mean: **STOP. Follow the process.**

| Excuse | Reality |
|--------|---------|
| "Tests passed earlier" | RUN THEM NOW - code might have changed |
| "User obviously wants to merge" | PRESENT ALL 4 OPTIONS - let them choose |
| "User said discard" | GET TYPED CONFIRMATION - "discard" exactly |
| "PR is done, cleanup worktree" | KEEP IT - PR will likely need updates |
| "Only 2 options make sense here" | PRESENT ALL 4 - always |
| "Tasks are mostly done" | ALL must be complete - no exceptions |

## Anti-patterns

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without typed "discard" confirmation
- Force-push without explicit request
- Skip task verification
- Cleanup worktree for Option 2 (PR)
- Cleanup worktree for Option 3 (keep as-is)
- Present fewer than 4 options
- Present more than 4 options

**Always:**
- Verify all tasks complete before proceeding
- Verify tests before offering options
- Present exactly 4 options
- Use AskUserQuestion tool for option selection
- Get typed "discard" confirmation for Option 4
- Keep worktree for Options 2 & 3
- Report absolute paths

## Verification Checklist

Before completing:

- [ ] All tasks show status="completed" (TaskList)
- [ ] Tests verified passing
- [ ] Base branch determined
- [ ] Presented exactly 4 options (using AskUserQuestion)
- [ ] Waited for user choice
- [ ] If Option 1: Verified tests on merged result
- [ ] If Option 1: Deleted feature branch
- [ ] If Option 2: Created PR with epic context
- [ ] If Option 2: Reported PR URL and kept worktree
- [ ] If Option 3: Reported branch and worktree preserved
- [ ] If Option 4: Got typed "discard" confirmation
- [ ] If Option 4: Deleted branch with -D flag
- [ ] If Option 1 or 4: Cleaned up worktree
- [ ] If Option 2 or 3: Did NOT cleanup worktree

## Examples

### Bad: Skip Test Verification

```
Step 1: Tasks all complete ✓
TaskList shows all completed

Step 2: SKIP test verification  # WRONG
Jump to presenting options

"Implementation complete. What would you like to do?..."

User selects Option 1

git checkout main
git merge feature-branch
# Tests fail! Broken code on main
```

**Why it fails:**
- Merged broken code to main
- Other developers pull broken main
- CI/CD fails, blocks deployment

### Good: Verify Tests Before Options

```
Step 1: Tasks all complete ✓
TaskList shows all completed

Step 2: Verify tests
$ go test ./...
ok  myproject/... 2.3s
127 tests passed

Step 3: Determine base branch
$ git merge-base HEAD main
abc123

Step 4: Present options
[AskUserQuestion with 4 options]
User selects: Merge locally

Step 5: Execute
$ git checkout main
$ git pull
$ git merge feature-auth
$ go test ./...  # Verify merged result
ok  myproject/... 2.4s
$ git branch -d feature-auth

Step 6: Cleanup worktree
$ git worktree remove .worktrees/auth

Done. Feature merged to main.
```

### Bad: Cleanup Worktree for PR

```
User selects Option 2
git push -u origin feature-auth
gh pr create ...

git worktree remove ../feature-auth-worktree  # WRONG

# PR gets feedback: "Please add rate limiting"
# Worktree is gone! Have to recreate
```

**Why it fails:**
- PR likely needs updates
- Have to recreate worktree
- Lost local state

### Good: Keep Worktree for PR

```
User selects Option 2
$ git push -u origin feature-auth
$ gh pr create --title "feat: OAuth" --body "..."

Pull request created: https://github.com/user/repo/pull/42

Keeping worktree at /home/dev/project/.worktrees/auth for PR updates.

# NO worktree cleanup
# User can address feedback in same worktree
```

### Bad: Discard Without Confirmation

```
User: "Discard this work"

git checkout main
git branch -D feature-experimental  # WRONG - no confirmation
git worktree remove ../worktree

# 50 commits deleted
# User: "Wait, I meant the LAST commit!"
```

**Why it fails:**
- No confirmation before destructive action
- Misunderstood user intent
- Permanent data loss

### Good: Require Typed Confirmation

```
User: "Discard this work"

This will permanently delete:
- Branch feature-experimental
- All commits:
  * a1b2c3d Add OAuth integration
  * d4e5f6g Add rate limiting
  ... (48 more commits)
- Worktree at /home/dev/project/.worktrees/experimental

Type 'discard' to confirm.

User types: "discard"

$ git checkout main
$ git branch -D feature-experimental
$ git worktree remove .worktrees/experimental

Branch deleted.
```

## Resources

**When stuck:**
- Tasks won't complete → Check TaskList, verify all subtasks done
- Tests fail → Fix before presenting options (cannot proceed)
- User unsure which option → Explain trade-offs, but present all 4
- Worktree won't remove → Might have uncommitted changes, ask user
- Git merge fails → Report conflict, ask user how to proceed
- PR creation fails → Check gh auth status, report error

## Task Tool Reference

### TaskList

```
TaskList
```

Returns all tasks with status. All must show "completed" before proceeding.

### TaskGet

```
TaskGet
  taskId: "epic-task-id"
```

Read epic success criteria for PR description and final verification.

### TaskUpdate

```
TaskUpdate
  taskId: "epic-task-id"
  status: "completed"
```

Mark epic complete after successful merge/PR.

## Integration

**This skill is called by:**
- User after implementation complete
- After `gambit:execute-plan` completes all tasks

**This skill calls:**
- gh commands (PR creation)
- git commands (merge, branch, worktree)

**This skill pairs with:**
- `gambit:worktree` - Cleans up worktree created by that skill

**Workflow:**
```
gambit:execute-plan
    → All tasks complete
gambit:finish
    → Step 1: Verify tasks complete
    → Step 2: Verify tests pass
    → Step 3: Determine base branch
    → Step 4: Present 4 options
    → Step 5: Execute choice
    → Step 6: Cleanup (Options 1,4 only)
```
