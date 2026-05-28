---
description: Launch agent worktree for a specific task
argument-hint: <task-id> [--max-iterations N] [--force]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# Launch Agent Worktree

Create a git worktree and PROMPT.md for a task, ready for agent execution.

**Arguments:** $ARGUMENTS

## Instructions

### Phase 1: Parse Arguments

1. **Extract task ID** from arguments (e.g., "CRANE-003").

2. **Extract optional flags:**
   - `--max-iterations N` - Safety limit for agent iterations (default: 0 = unlimited)
   - `--force` - Launch even if dependencies are incomplete (with warning)

### Phase 2: Validate Task

1. **Find task directory:**
   ```bash
   ls -d tasks/${TASK_ID}-* 2>/dev/null
   ```

2. **If not found:** Show available tasks and abort.

3. **Read task files:**
   - `tasks/{ID}-{name}/TASK.md` - Get task details
   - `tasks/{ID}-{name}/PROGRESS.md` - Check if exists

4. **Check task status:**
   - If "Complete": Warn and ask for confirmation
   - If "In Progress": Warn that worktree may already exist

### Phase 3: Dependency Check (NEW)

**Build dependency graph and check if task can be launched:**

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/deps.sh"
deps_build_graph

# Check if task can be launched
if ! deps_can_launch "${TASK_ID}"; then
  # deps_can_launch outputs the blockers

  if [[ "$FORCE" != "true" ]]; then
    echo ""
    echo "Cannot launch task with incomplete dependencies."
    echo ""
    echo "Options:"
    echo "  1. Complete the blocking tasks first"
    echo "  2. Use --force to launch anyway (not recommended)"
    echo ""
    exit 1
  else
    echo ""
    echo "WARNING: Launching with incomplete dependencies (--force)"
    echo "The agent may encounter issues due to missing prerequisites."
    echo ""
  fi
fi
```

**If blocked (without --force):**

```
═══════════════════════════════════════════════════════════════════
 CANNOT LAUNCH: {TASK_ID}
═══════════════════════════════════════════════════════════════════

This task has incomplete dependencies:

  - {DEP-001} (In Progress): {Title}
  - {DEP-002} (Ready): {Title}

These tasks must be Complete before {TASK_ID} can start.

## Options

1. Complete the blocking tasks first:
   /backlog:launch {DEP-001}

2. Force launch (not recommended):
   /backlog:launch {TASK_ID} --force

## Recommended Order

To complete all dependencies:
1. {DEP-002}: {Title} (no dependencies)
2. {DEP-001}: {Title} (depends on {DEP-002})
3. {TASK_ID}: {Title} (depends on {DEP-001})

═══════════════════════════════════════════════════════════════════
```

### Phase 4: Prepare Task Files

1. **Initialize PROGRESS.md** if it doesn't exist or is empty:
   ```markdown
   # Progress Log: {PREFIX}-{NNN}

   ## Current Checkpoint

   **Last checkpoint:** Not started
   **Next step:** Read TASK.md and begin implementation
   **Build status:** ⏳ Not checked
   **Test status:** ⏳ Not checked

   ---

   ## Session Log

   ### {TODAY} - Task Launched

   - Task launched via /backlog:launch
   - Agent worktree created
   - Ready to begin implementation
   ```

2. **Commit task files** to ensure worktree will have them:
   ```bash
   git add tasks/${TASK_ID}-*/
   git commit -m "chore: prepare task ${TASK_ID} for agent launch" --allow-empty
   ```

### Phase 5: Create Worktree

1. **Load configuration:**
   ```bash
   cat design.yaml
   ```

2. **Determine worktree location:**
   ```bash
   REPO_ROOT=$(git rev-parse --show-toplevel)
   BRANCH="feature/{kebab-name-from-task}"
   WT_PATH="${REPO_ROOT}-wt/${BRANCH}"
   ```

3. **Create worktree with submodules:**
   ```bash
   "${CLAUDE_PLUGIN_ROOT}/scripts/wt-create.sh" "${BRANCH}" "${REPO_ROOT}"
   ```

   The script handles:
   - Creating the worktree and branch
   - Initializing all submodules recursively
   - Verifying submodules are functional
   - **Exits with error if submodules fail** (worktree unusable)

4. **Verify success:**
   - If the script exits with error, **stop and report the failure**
   - Output: `<promise>TASK_BLOCKED: Worktree creation failed - submodules not initialized</promise>`
   - Do NOT proceed to Phase 6 if submodules are broken

### Phase 6: Setup Agent Environment

1. **Create PROMPT.md** in worktree root that **points to** task files:

```markdown
# Agent Task Assignment

**Task:** {PREFIX}-{NNN} - {Title}
**Repo:** {REPO_NAME}
**Mode:** Implementation
**Task Directory:** tasks/{PREFIX}-{NNN}-{kebab-name}/

## Dependencies

{If task has dependencies, list them with their status}

| Dependency | Status | Title |
|------------|--------|-------|
| {DEP-001} | Complete | {Title} |
| {DEP-002} | Complete | {Title} |

## Required Reading

1. `tasks/{PREFIX}-{NNN}-{kebab-name}/TASK.md` - Full requirements
2. `tasks/{PREFIX}-{NNN}-{kebab-name}/PROGRESS.md` - Prior work and current state

## Instructions

1. Read TASK.md to understand requirements
2. Read PROGRESS.md to see what's been done
3. Continue work from where you left off
4. **Update PROGRESS.md** as you work (newest entries first)
5. When complete, output: `<promise>TASK_COMPLETE</promise>`
6. If blocked, output: `<promise>TASK_BLOCKED: [reason]</promise>`

## On Context Compaction

If your context is compacted or you're resuming work:
1. Re-read this PROMPT.md
2. Re-read PROGRESS.md for your prior state
3. Continue from the last recorded progress

## Completion Checklist

Before marking complete, verify:
- [ ] All acceptance criteria in TASK.md are checked
- [ ] PROGRESS.md has final summary
- [ ] All tests pass
- [ ] Build succeeds

## Troubleshooting

**If you encounter "not a git repository" errors in submodules:**

1. Try: `git submodule update --init --recursive`
2. If that fails: `git submodule deinit -f --all && git submodule update --init --recursive`
3. If still failing, output: `<promise>TASK_BLOCKED: Submodules broken, needs worktree reinitialization</promise>`

**If build fails due to missing dependencies:**

Check that submodules are properly initialized before debugging other issues.
```

2. **Create state file** (if max-iterations specified):
   ```bash
   mkdir -p "${WT_PATH}/.claude"
   ```

   Write `.claude/backlog-agent.local.md`:
   ```markdown
   ---
   active: true
   iteration: 1
   max_iterations: {N or 0}
   started_at: "{ISO_TIMESTAMP}"
   task_id: "{TASK_ID}"
   mode: "implementation"
   ---
   ```

3. **Update tasks/INDEX.md** status to "In Progress":
   ```markdown
   | {PREFIX}-{NNN} | {Title} | In Progress | {Deps} | feature/{name} |
   ```

### Phase 7: Register with Built-in Task Feature

**IMPORTANT:** Use the built-in Task feature to track that this task has been launched.

Call `TaskCreate` with:
- **subject**: `{PREFIX}-{NNN}: {Title}`
- **description**: Read from `tasks/{PREFIX}-{NNN}-{kebab-name}/TASK.md` - include the full task description and note that it's running in a worktree at `{WT_PATH}`
- **activeForm**: `Launched {PREFIX}-{NNN} (worktree)`

Then call `TaskUpdate` to set status to `in_progress`:
- **taskId**: The ID returned from TaskCreate
- **status**: `in_progress`

This registers the launched task in the current session. Note: The agent working in the worktree will be in a separate Claude session and should also create its own Task entry when it starts via `/up:prompt`.

### Phase 9: Output Launch Instructions

Output ready-to-use commands with **absolute paths**:

```
═══════════════════════════════════════════════════════════════════
 AGENT READY: {PREFIX}-{NNN} - {Title}
═══════════════════════════════════════════════════════════════════

Task files committed and worktree created.

## Dependencies

{If dependencies exist}
All dependencies are complete:
- {DEP-001}: {Title} ✓
- {DEP-002}: {Title} ✓

{Or if launched with --force}
WARNING: Launched with incomplete dependencies:
- {DEP-001}: {Title} (In Progress)

## Step 1: Open a new terminal and run:

cd {ABSOLUTE_WORKTREE_PATH}

## Step 2: Start Claude Code:

claude --dangerously-skip-permissions

## Step 3: Give Claude this prompt:

/up:prompt

This will read PROMPT.md which directs the agent to:
- tasks/{PREFIX}-{NNN}-{kebab-name}/TASK.md (requirements)
- tasks/{PREFIX}-{NNN}-{kebab-name}/PROGRESS.md (progress log)

## Stop Hook

The Stop hook will prevent exit until:
- Agent outputs <promise>TASK_COMPLETE</promise>
- Agent outputs <promise>TASK_BLOCKED: [reason]</promise>
- Max iterations reached ({N or "unlimited"})

Agent will use subscription usage, not API credits.

═══════════════════════════════════════════════════════════════════
```

## Arguments Reference

| Argument | Description |
|----------|-------------|
| `<task-id>` | Task ID to launch (e.g., CRANE-003) |
| `--max-iterations N` | Optional safety limit (default: 0 = unlimited) |
| `--force` | Launch even if dependencies are incomplete |

## Error Handling

- **Task doesn't exist:** Show available task IDs
- **Task already complete:** Warn and ask for confirmation
- **Worktree already exists:** Show path and ask to continue or abort
- **Worktree creation fails:** Show error and manual steps
- **No tasks/ directory:** "Run /design:init first"
- **Submodule init fails:** Copy from main repo as fallback
- **Dependencies incomplete:** Show blockers and recommend order (unless --force)

## Why Commit Before Worktree?

- Worktree is created from current HEAD
- If task files aren't committed, worktree won't have them
- Agent needs TASK.md and PROGRESS.md to exist in the worktree

## Example Session

```bash
$ /backlog:launch CRANE-003 --max-iterations 20

Finding task CRANE-003...
  Found: tasks/CRANE-003-uniswap-v4-utils/

Checking dependencies...
  CRANE-001: Complete ✓
  CRANE-002: Complete ✓
  All dependencies satisfied.

Preparing task files...
  PROGRESS.md initialized
  Files committed: chore: prepare task CRANE-003 for agent launch

Creating worktree...
  Branch: feature/uniswap-v4-utils
  Path: /Users/you/repos/crane-wt/feature/uniswap-v4-utils

Initializing submodules...
  ✅ Submodules ready

Setting up agent environment...
  PROMPT.md created
  State file created (max 20 iterations)
  INDEX.md updated

═══════════════════════════════════════════════════════════════════
 AGENT READY: CRANE-003 - Uniswap V4 Utils
═══════════════════════════════════════════════════════════════════

...
```

## Example: Blocked Task

```bash
$ /backlog:launch IDXEX-005

Finding task IDXEX-005...
  Found: tasks/IDXEX-005-protocol-integration/

Checking dependencies...
  IDXEX-003: In Progress ✗
  IDXEX-004: Ready ✗

═══════════════════════════════════════════════════════════════════
 CANNOT LAUNCH: IDXEX-005
═══════════════════════════════════════════════════════════════════

This task has incomplete dependencies:

  - IDXEX-003 (In Progress): Fee collector
  - IDXEX-004 (Ready): Vault types

These tasks must be Complete before IDXEX-005 can start.

## Options

1. Complete the blocking tasks first:
   /backlog:launch IDXEX-003

2. Force launch (not recommended):
   /backlog:launch IDXEX-005 --force

═══════════════════════════════════════════════════════════════════
```
