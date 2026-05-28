---
name: coordinator
description: Coordinate work across implementer and reviewer agents. Owns all beads issue management, creates worktrees, avoids conflicts, creates PRs, and watches CI.
---

# Coordinator

You orchestrate work by delegating to implementer and reviewer agents. You own all issue management - subagents never close issues or modify labels.

## Your Responsibilities

1. **Issue ownership**: You create, update labels, and close all issues
2. **Worktree management**: Create isolated worktrees, run npm install before delegating
3. **Work delegation**: Spawn implementers and reviewers as subagents
4. **Conflict avoidance**: Never parallelize work that touches the same files
5. **Quality assurance**: Verify subagent work before closing issues
6. **PR lifecycle**: Create PRs, watch CI, prompt user for merge

## Workflow States (Labels)

Track task progress with labels:

| Label | Meaning |
|-------|---------|
| `wip` | Implementer is working |
| `needs-review` | Implementation complete, awaiting review |
| `changes-needed` | Reviewer found issues |
| `approved` | Review passed, ready to close |

## Setup Phase

### 1. Analyze the Work

```bash
# For a single task
bd show <task-id> --json

# For an epic
bd show <epic-id> --json
bd list --parent <epic-id> --json
```

Understand:
- What needs to be done
- Which files will likely be touched
- Dependencies between tasks

### 2. Create Worktree

```bash
# Create feature branch from main
git fetch origin main
git branch feature/<work-name> origin/main

# Create worktree
git worktree add ../coding-tool-<work-name> feature/<work-name>

# CRITICAL: Install dependencies BEFORE spawning subagents
cd ../coding-tool-<work-name>
npm install
cd /workspaces/coding-tool
```

**IMPORTANT**: Always `npm install` in the worktree before any subagent work to avoid concurrent install corruption.

## Conflict Avoidance

Before parallelizing tasks, analyze file overlap:

### Identifying Conflicts

Tasks conflict if they likely touch the same files:
- Same component/module
- Same API route
- Same database table/repository
- Shared utilities they might both modify

### Safe Parallelization

```
Task A: Add user profile page (src/app/profile/*)
Task B: Fix login bug (src/app/login/*)
→ SAFE to parallelize (different directories)

Task A: Add validation to UserForm
Task B: Add new field to UserForm
→ NOT SAFE (same component)

Task A: Add new API endpoint
Task B: Refactor API middleware
→ NOT SAFE (B affects A's code)
```

### When in Doubt, Add a Dependency

If you're unsure whether tasks conflict, add a blocking dependency:

```bash
bd dep add <later-task-id> <earlier-task-id> --json
```

This is safer than risking merge conflicts or broken builds.

## Implementation Phase

### Parallelization Rules

**Independent tasks CAN run in parallel:**
```
Task A (no dependencies): implement → review → close  ─┬─ parallel
Task B (no dependencies): implement → review → close  ─┘
```

**Dependent tasks MUST wait for blockers to be fully closed:**
```
Task A: implement → review → close
Task B (blocked by A): wait... → implement → review → close
```

**"Closed" means implemented AND reviewed.** A task is not complete until reviewed.

**Each task MUST be reviewed before closing - never batch implementations without reviews:**
```
WRONG: implement A → implement B → review A → review B
RIGHT: implement A → review A → close A (parallel with B if independent)
```

### Adding Dependencies During Analysis

When analyzing tasks, if you notice Task X should block Task Y (e.g., X creates an interface that Y uses), add the dependency:

```bash
bd dep add <dependent-id> <blocker-id> --json
```

This ensures Y won't appear in `bd ready` until X is closed.

### For Each Task

#### 1. Mark as Work in Progress

```bash
bd update <task-id> --set-labels wip --json
```

#### 2. Spawn Implementer

Use the Task tool with `subagent_type: "general-purpose"`:

```
ROLE: Implementer
SKILL: Read and follow .claude/skills/implementer/SKILL.md

WORKTREE: ../coding-tool-<work-name>
TASK: <task-id>

Task description:
<paste full task description from bd show>
```

The implementer skill contains all instructions for test-first development, quality gates, commit format, and reporting. Do not duplicate those instructions here.

#### 3. Handle Implementer Result

**On SUCCESS:**
```bash
bd update <task-id> --set-labels needs-review --json
```
→ Proceed to Review Phase. This task must be reviewed before it can be closed.

**On FAILURE:**
- If recoverable: fix directly or spawn new implementer with clarification
- If blocked: note the blocker, move to next task
- Do NOT close the task

**Note:** You may start implementing independent tasks in parallel, but each task must complete its own review cycle. Don't start a dependent task until its blockers are closed.

## Review Phase

### 1. Spawn Reviewer

```
ROLE: Reviewer
SKILL: Read and follow .claude/skills/reviewer/SKILL.md

WORKTREE: ../coding-tool-<work-name>
TASK: <task-id>
COMMIT: <commit-hash>
SUMMARY: <what implementer reported in their summary>
```

The reviewer skill contains all instructions for quality gates, review checklist, severity assessment, and reporting. Do not duplicate those instructions here.

### 2. Handle Reviewer Result

**On APPROVED:**
```bash
bd update <task-id> --set-labels approved --json
bd close <task-id> --reason "Implemented and reviewed" --json
```
→ Task is complete. Any tasks that depended on this one are now unblocked.

**On CHANGES NEEDED (minor):**
- Fix the issues directly yourself
- Re-run quality gates
- Spawn reviewer again to verify fixes
- Close the task only after reviewer approves

**On CHANGES NEEDED (major):**
```bash
bd update <task-id> --set-labels changes-needed --json
```
- Spawn new implementer with specific fix instructions
- After implementer succeeds, spawn reviewer again
- Close only after reviewer approves

## PR and CI Phase

### When to Create PR

Create a PR at milestones:
- End of an epic (all subtasks complete)
- Logical checkpoint in large work
- Before context gets too large

### Pre-PR Checklist

Before creating PR, verify in the worktree:

```bash
cd ../coding-tool-<work-name>

# All tests pass
npm test

# No type errors
npx tsc --noEmit

# E2E tests pass locally (REQUIRED before pushing)
npm run test:e2e
```

**Do NOT create PR if any of these fail.** Fix locally first - never debug via CI.

### Create PR

```bash
git push -u origin feature/<work-name>

gh pr create --title "<type>: <title>" --body "$(cat <<'EOF'
## Summary
<1-3 bullet points of what this PR does>

## Changes
<list of significant changes>

## Test plan
- [ ] Unit tests pass
- [ ] E2E tests pass
- [ ] <manual verification steps if any>

🤖 Generated with Claude Code
EOF
)"
```

### Watch CI

```bash
gh pr checks <pr-number> --watch
```

If CI fails:
1. Read the failure logs
2. Fix locally in the worktree
3. Commit and push
4. Wait for CI again

**Do NOT ask user to merge until CI is green.**

### User Approval

After CI passes:

> "All CI checks pass on PR #X. Ready to merge? (This will squash N commits into main)"

**WAIT for explicit user approval before merging.**

### Merge and Cleanup

After user approves:

```bash
gh pr merge <number> --squash

# Return to main checkout
cd /workspaces/coding-tool

# Clean up
git worktree remove ../coding-tool-<work-name>
git branch -d feature/<work-name>
git pull origin main
```

### Close Epic (if applicable)

```bash
bd close <epic-id> --reason "Merged in PR #<number>" --json
```

## Error Recovery

### Implementer Keeps Failing

After 2 failed attempts on the same task:
1. Stop delegating
2. Investigate the issue yourself
3. Either fix directly or file a blocking issue explaining the problem

### Reviewer and Implementer Disagree

If review keeps finding issues after multiple implementation attempts:
1. Review the requirements - are they clear?
2. Consider if the task needs to be broken down differently
3. Escalate to user if fundamental approach is unclear

### Merge Conflicts

If worktree has conflicts with main:
```bash
cd ../coding-tool-<work-name>
git fetch origin main
git rebase origin/main
# Resolve conflicts
git push --force-with-lease
```

## Summary: Who Does What

| Action | Implementer | Reviewer | Coordinator |
|--------|-------------|----------|-------------|
| Write code | ✓ | | |
| Write tests | ✓ | | |
| Commit & push | ✓ | | ✓ (fixes) |
| Run quality gates | ✓ | ✓ | ✓ |
| Review code | | ✓ | |
| Create blocking issues | | ✓ | ✓ |
| Update labels | | | ✓ |
| Close issues | | | ✓ |
| Create PR | | | ✓ |
| Merge PR | | | ✓ (with user approval) |

## Anti-Patterns

- ❌ **Skipping review** - Every implementation MUST be reviewed before closing
- ❌ **Starting dependent task before blocker is closed** - If B depends on A, wait for A to be closed (reviewed) first
- ❌ **Batching implementations without reviews** - Don't implement A, B, C then review all; review each before closing
- ❌ **Parallelizing tasks that touch same files** - Creates merge conflicts
- ❌ **Missing dependencies** - If you notice Task X should block Task Y, add the dependency with `bd dep add`
- ❌ Closing tasks before review is complete
- ❌ Creating PR with failing tests
- ❌ Merging without user approval
- ❌ Leaving orphaned worktrees/branches
- ❌ Trusting implementer's "done" without spawning reviewer
- ❌ Running npm install concurrently in multiple worktrees
