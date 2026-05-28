# backlog - Task Management Plugin

Manage your tasks/ directory backlog and git worktrees for autonomous agent execution with **memory-enabled agents** that survive context compaction.

## Installation

```bash
/plugin marketplace add cyotee/cyotee-claude-plugins
/plugin install backlog@cyotee
```

## Commands

### `/backlog`

Display a summary table of all tasks from the tasks/ directory.

**Aliases:** `/backlog:status`

**What it does:**
1. Scans for tasks/ directories in the repository
2. Reads tasks/INDEX.md or scans task directories
3. Generates a status table of all tasks
4. Shows summary counts (completed, ready, blocked)
5. Recommends the next task to work on

**Example output:**
```
# Backlog Status - [Layer Name]

| # | Title | Status | Worktree | Dependencies | Created |
|---|-------|--------|----------|--------------|---------|
| [P]-1 | Feature One | ✅ complete | - | - | 2026-01-05 |
| [P]-2 | Feature Two | 🚀 in_progress | `feature/two` | [P]-1 | 2026-01-08 |
| [P]-3 | Feature Three | 🆕 pending | - | [P]-2 | 2026-01-10 |

Summary:
- ✅ Complete: 1
- 🚀 In Progress: 1
- 🆕 Pending: 1

Recommended next: [P]-3 (after [P]-2 completes)
```

---

### `/backlog:read <task-id>`

Display the full content of a specific task.

**What it does:**
1. Parses task ID (e.g., `P-5` or just `5`)
2. Detects layer from prefix or current directory
3. Reads PRD.md, PROGRESS.md, and REVIEW.md
4. Displays formatted task summary

**Example usage:**
```
/backlog:read P-5
```

---

### `/backlog:launch <task-id>`

Create a git worktree and launch a **memory-enabled agent** for a task.

**What it does:**
1. Reads the task from tasks/[ID]/PRD.md
2. Checks worktree state (new, existing clean, existing dirty, behind main)
3. Creates worktree using `./scripts/wt-create.sh` if needed
4. Generates **PROMPT.md** in worktree root with:
   - Memory protocol instructions
   - Task summary and key requirements
   - Context management (`/compact` and reload instructions)
   - Completion criteria
5. Creates or preserves **PROGRESS.md** in tasks/[ID]/ with:
   - Checkpoints section for resumable state
   - Work log for tracking actions
6. Updates task status to `in_progress`
7. Updates tasks/INDEX.md
8. Outputs launch instructions for the human

**Worktree States:**
| State | Action |
|-------|--------|
| Doesn't exist | Create new worktree, fresh PROMPT.md and PROGRESS.md |
| Exists, clean | Ask about PROMPT.md (review/regenerate/keep), preserve PROGRESS.md |
| Exists, dirty | Warn about uncommitted changes, ask how to proceed |
| Behind local main | Suggest `git merge main` before continuing |

**Example usage:**
```
/backlog:launch I-5
```

**Example output:**
```
================================================================================
# Task I-5: Protocol DETF System
================================================================================

**Status:** in_progress
**Worktree:** /path/to/repo-wt/feature/protocol-detf
**Dependencies:** None

## Launch Commands

Run these commands to start the agent:

    cd /path/to/repo-wt/feature/protocol-detf
    claude --dangerously-skip-permissions

## Start the Agent

Once Claude Code is running, enter this command:

    /ralph-loop:ralph-loop "Read PROMPT.md and follow its instructions. This file tells you which other files to read and how to track your progress." --completion-promise "TASK_COMPLETE" --max-iterations 15

## Files Created/Updated

- PROMPT.md (worktree root) - Agent instructions with memory protocol
- tasks/I-5/PROGRESS.md - Work log and resumable state

## When Complete

The agent will output `<promise>TASK_COMPLETE</promise>` when done.

Then return to this session and run:

    /backlog:complete I-5

================================================================================
```

**Memory Protocol:**

The generated PROMPT.md instructs the agent to:
1. Read CLAUDE.md, PRD.md, and PROGRESS.md on every iteration
2. Update PROGRESS.md after each significant action
3. When context gets long: update PROGRESS.md, run `/compact`, then re-read all files
4. Use the Checkpoints section in PROGRESS.md for resumable state

This allows agents to survive context compaction and resume work across sessions.

---

### `/backlog:complete [task-id] [--push]`

Finalize a completed task using a **two-phase workflow** for smooth completion.

**Two-Phase Workflow:**

#### Phase 1: Prepare from Task Worktree
Run from the task's worktree (NOT main):
1. Commits all final changes (EXCEPT PROMPT.md which is auto-excluded)
2. Rebases the worktree branch onto local main
3. Marks task as "Pending Merge" in INDEX.md
4. Displays instructions to run Phase 2 from main

#### Phase 2: Finalize from Main Worktree
Run from the main worktree:
1. Verifies task is "Pending Merge" and fast-forward is possible
2. Fast-forward merges main to include the task's commits
3. Marks task as "Complete" in INDEX.md
4. Updates dependent tasks (unblocks blocked tasks)
5. Archives task files to tasks/archive/
6. Removes the worktree and branch automatically
7. Displays completion summary with unblocked tasks

**Key Benefits:**
- ✓ PROMPT.md automatically excluded from commits
- ✓ Clean linear history (fast-forward only)
- ✓ Automatic worktree cleanup
- ✓ Automatic task archival
- ✓ Dependency cascade updates
- ✓ Safe rollback between phases

**Arguments:**
| Argument | Description |
|----------|-------------|
| `<task-id>` | Task ID (e.g., CRANE-003) - optional, prompts if not provided |
| `--push` | Push main to origin after merge (Phase 2 only) |

**Example:**
```bash
# Phase 1: In task worktree
$ /backlog:complete CRANE-003
# → Commits changes, rebases, marks "Pending Merge"

# Phase 2: In main worktree
$ /backlog:complete CRANE-003 --push
# → Merges, archives, cleans up, unblocks dependents
```

---

### `/backlog:prune [task-id] [--all]`

Archive completed and reviewed tasks.

**What it does:**
1. Identifies tasks with `status: complete` and passing review
2. Moves task directories to `tasks/archive/`
3. Updates tasks/INDEX.md
4. Outputs cleanup instructions for worktrees

**Arguments:**
| Argument | Description |
|----------|-------------|
| `<task-id>` | Specific task to archive (e.g., P-5) |
| `--all` | Archive all completed tasks |

---

### `/backlog:list [--worktrees-only]`

List all unarchived tasks with their status, dependencies, and worktrees.

**Aliases:** `/backlog:worktrees` (with --worktrees-only)

**What it does:**
1. Reads tasks/INDEX.md and builds dependency graph
2. Computes effective status for each task (blocked if deps incomplete)
3. Cross-references with git worktrees
4. Displays unified task list with status icons

**Example output:**
```
═══════════════════════════════════════════════════════════════════
 TASK LIST: IndexedEx

| ID | Title | Status | Dependencies | Worktree |
|----|-------|--------|--------------|----------|
| IDXEX-001 | Core infrastructure | ✅ Complete | - | - |
| IDXEX-002 | Registry system | 🚀 In Progress | - | feature/registry |
| IDXEX-003 | Fee collector | ❌ Blocked | IDXEX-002 | - |
| IDXEX-004 | Vault types | 🆕 Ready | IDXEX-001 | - |

## Summary

Total: 4 tasks
✅ Complete: 1 | 🚀 In Progress: 1 | 🆕 Ready: 1 | ❌ Blocked: 1

## Next Actions

Ready to start:
- /backlog:launch IDXEX-004

Currently blocked:
- IDXEX-003: Waiting on IDXEX-002
═══════════════════════════════════════════════════════════════════
```

**Arguments:**
| Argument | Description |
|----------|-------------|
| `--worktrees-only` | Show only active worktrees (legacy behavior) |

**Status Icons:**
| Icon | Status | Description |
|------|--------|-------------|
| ✅ | Complete | Task finished and merged |
| 🚀 | In Progress | Agent actively working |
| 📋 | In Review | Work complete, code review |
| 🆕 | Ready | All dependencies met, can start |
| ❌ | Blocked | Waiting on dependencies |

---

## Layer Detection

Layers are detected dynamically:

```bash
# Find all tasks/ directories
find . -type d -name "tasks" -not -path "*/node_modules/*" 2>/dev/null
```

For each discovered tasks/ directory:
1. Read `tasks/INDEX.md` for layer name and prefix
2. If not found, auto-detect from directory/repo name
3. Prefix is first letter of layer name (uppercase)

## Task States

| State | Icon | Description |
|-------|------|-------------|
| pending | 🆕 | Ready to start, dependencies met |
| in_progress | 🚀 | Agent actively working |
| review | 📋 | Work complete, awaiting review |
| complete | ✅ | Reviewed and approved |
| blocked | ❌ | Waiting on dependencies |

---

## Scripts

The plugin includes submodule-aware worktree management scripts in `scripts/`:

### `wt-create.sh`

Creates a worktree with proper submodule initialization:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/wt-create.sh" <branch-name> [repo-root]
```

### `wt-remove.sh`

Removes a worktree safely (handles submodules):

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/wt-remove.sh" <branch-name> [repo-root]
```

**Why scripts instead of `git wt -d`?**
1. Worktrees with submodules can't be removed without `--force`
2. Submodule pointers can become corrupt
3. Lock files cause "Another git process" errors
4. Nested submodules need fallback copying when git init fails

## Requirements

- **git-wt** or **wt-create.sh**: Git worktree helper
- **tasks/**: Task directory (created by `/design:init`)

## Workflow Integration

```
1. /design <feature>      # Create task in tasks/
2. /backlog               # View all tasks
3. /backlog:read I-5      # Read task details
4. /backlog:launch I-5    # Create worktree + PROMPT.md + PROGRESS.md
5. cd <worktree>          # Human switches to worktree
6. claude --skip-perms    # Human starts Claude Code
7. /ralph-loop "..."      # Human starts agent loop
8. (agent works)          # Agent executes, updates PROGRESS.md
9. /backlog:complete I-5  # Prepare for review
10. /backlog:prune I-5    # Archive after review
```

## Memory Protocol Files

### PROMPT.md (worktree root)

Generated by `/backlog:launch`. Contains:
- Memory protocol instructions for the agent
- Task summary extracted from PRD.md
- Key requirements as bullet list
- Context management instructions (`/compact` handling)
- Completion criteria

### PROGRESS.md (tasks/[ID]/)

Maintained by the agent. Contains:
- **Checkpoints section**: Resumable state after `/compact`
  - Current phase
  - Files modified
  - Test status
  - Next action
- **Work Log**: Reverse-chronological record of actions

**Example PROGRESS.md structure:**
```markdown
# Progress: I-5 - Protocol DETF System

**Started:** 2026-01-11 14:30
**Status:** in_progress

## Checkpoints

**Current phase:** Implementing CHIR token
**Files modified:** contracts/tokens/CHIR.sol, test/CHIR.t.sol
**Tests passing:** 3/5 passing
**Next action:** Fix failing rebasing tests

---

## Work Log

### 2026-01-11 15:45 - Implemented base token

- Completed: CHIR ERC20 with mint/burn
- Files modified: contracts/tokens/CHIR.sol
- Next: Add rebasing logic
- Blockers: None

---
```

## Requirements

- **ralph-loop plugin**: For autonomous agent loops
- **git-wt** or **wt-create.sh**: Git worktree helper
- **tasks/**: Task directory (created by `/design:init`)

## License

MIT
