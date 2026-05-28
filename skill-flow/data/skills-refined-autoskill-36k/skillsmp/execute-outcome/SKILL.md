---
name: execute-outcome
description: Execute all Work Units for an Outcome with dependency-aware ordering
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task, mcp__linear-server__get_issue, mcp__linear-server__list_issues, mcp__linear-server__update_issue
---

# Execute Outcome

Execute all Work Units (sub-issues) for an Outcome, handling dependencies intelligently.

## Usage
```
/execute-outcome <outcome-issue-id>
```

Example: `/execute-outcome BHU-139`

## Important: Using Linear MCP

Use Linear MCP tools as direct function calls, NOT bash commands.

## Git Worktree Strategy

Parallel execution requires isolation. Each parallel Work Unit runs in its own git worktree.

```
main-repo/
├── .git/
├── src/
├── ...
└── .worktrees/              # Created during execution
    ├── wu-BHU-141/          # Worktree for WU 1
    │   ├── src/
    │   └── ...
    └── wu-BHU-142/          # Worktree for WU 2
        ├── src/
        └── ...
```

**Why worktrees?**
- Each agent modifies files independently
- Tests run in isolation (no interference)
- Git state stays clean (one branch per WU)
- Merge conflicts detected at integration, not during work

**Setup requirements:**
1. Add `.worktrees/` to `.gitignore` (one-time setup)
2. Worktrees share the same `.git` directory — no duplicate clones
3. Dependencies (node_modules, .venv) must exist in worktree or be symlinked

### Worktree Environment Setup

Before running `/work` in a worktree, ensure dependencies are available:

**Python (uv/pip):**
```bash
# Option A: Install in worktree (isolated, slower)
cd .worktrees/wu-BHU-141 && uv sync

# Option B: Symlink from main (shared, faster)
ln -s $(pwd)/.venv .worktrees/wu-BHU-141/.venv
```

**Node (npm/pnpm):**
```bash
# Option A: Install in worktree
cd .worktrees/wu-BHU-141 && npm install

# Option B: Symlink node_modules (careful with native deps)
ln -s $(pwd)/node_modules .worktrees/wu-BHU-141/node_modules
```

**Recommendation:** Use symlinks for speed. If a WU modifies dependencies, install fresh.

## Workflow

### Step 1: Fetch Outcome and Work Units

1. Fetch Outcome issue via `mcp__linear-server__get_issue`
2. List child issues (Work Units) via `mcp__linear-server__list_issues` with `parentId`
3. Display:
   ```
   Outcome: [title]

   Work Units found: N
   1. [WU-1 title] (proof: X, budget: Y)
   2. [WU-2 title] (proof: X, budget: Y)
   ...
   ```

### Step 2: Determine Dependencies

Ask human:
```
Do any Work Units depend on others?

1. WU-1: [title]
2. WU-2: [title]
3. WU-3: [title]

Enter dependencies (e.g., "2→1" means WU-2 depends on WU-1):
Or type "none" if all are independent.
```

Build dependency graph from response.

### Step 3: Plan Execution Order

Based on dependencies:
1. Topological sort to find valid order
2. Identify parallelizable groups (no interdependencies)
3. Present plan:
   ```
   Execution Plan:

   Batch 1 (parallel, 2 worktrees):
   - BHU-141: [title]
   - BHU-143: [title]

   Batch 2 (after batch 1):
   - BHU-142: [title] (depends on BHU-141)

   Proceed? [y/n]
   ```

### Step 4: Execute Batches

For each batch:

**If batch has 1 Work Unit:**
- Execute inline using `/work` logic (no worktree needed)
- Commit directly to current branch

**If batch has multiple Work Units (parallel):**

1. **Setup worktrees:**
   ```bash
   # Get current branch name
   CURRENT_BRANCH=$(git branch --show-current)

   # Create worktree directory
   mkdir -p .worktrees

   # For each WU in batch, create worktree with feature branch
   git worktree add .worktrees/wu-BHU-141 -b wu/BHU-141 $CURRENT_BRANCH
   git worktree add .worktrees/wu-BHU-143 -b wu/BHU-143 $CURRENT_BRANCH
   ```

2. **Launch parallel agents:**

   For each Work Unit in the batch, invoke the Task tool:

   ```
   Task(
     subagent_type: "general-purpose"
     description: "Execute WU BHU-141"
     prompt: |
       Execute Work Unit BHU-141 in isolated worktree.

       ## Context
       - Issue ID: BHU-141
       - Worktree path: /absolute/path/to/.worktrees/wu-BHU-141
       - Base branch: wu/BHU-141

       ## Instructions
       1. cd to worktree: cd /absolute/path/to/.worktrees/wu-BHU-141
       2. Run /work BHU-141 workflow (fetch issue, TDD, implement, review)
       3. All file operations MUST happen in the worktree path
       4. All git commands MUST use: git -C /absolute/path/to/.worktrees/wu-BHU-141
       5. Commit format: [BHU-141] <type>: <description>

       ## Critical
       - NEVER modify files outside the worktree
       - Return verdict: APPROVED / NEEDS_CHANGES / BLOCKED_FOR_HUMAN
   )
   ```

   Launch all batch agents in parallel (single message with multiple Task calls).

3. **Wait and collect:**
   - Wait for all agents to complete
   - Collect results (APPROVE/NEEDS_CHANGES/BLOCKED)

4. **Integrate completed work:**
   ```bash
   # For each successful WU, merge its branch
   git merge wu/BHU-141 --no-edit
   git merge wu/BHU-143 --no-edit
   ```

5. **Cleanup worktrees:**
   ```bash
   git worktree remove .worktrees/wu-BHU-141
   git worktree remove .worktrees/wu-BHU-143
   git branch -d wu/BHU-141
   git branch -d wu/BHU-143
   ```

**Between batches:**
- Report progress
- Ensure all merges from previous batch are complete
- If any Work Unit failed, ask human:
  ```
  BHU-141 failed review. Options:
  1. Retry BHU-141
  2. Skip BHU-141, continue with others (cleanup its worktree)
  3. Stop execution (cleanup all worktrees)
  ```

### Step 5: Handle Merge Conflicts

After parallel batch completion, merges may conflict:

1. **Detect conflict:**
   ```bash
   git merge wu/BHU-141 --no-edit
   # If exit code != 0 and output contains "CONFLICT"
   ```

2. **On conflict, report to human:**
   ```
   Merge conflict integrating BHU-141.

   Conflicting files:
   - src/models/land.py
   - src/services/valuation.py

   Options:
   1. I'll resolve manually (pause execution)
   2. Abort BHU-141, keep other WUs
   3. Stop execution entirely
   ```

3. **If human resolves:**
   - Wait for human to run `git add . && git commit`
   - Verify merge complete: `git status` shows clean state
   - Continue with next merge or batch

4. **Conflict prevention tips:**
   - Work Units touching same files should be sequential, not parallel
   - During dependency mapping (Step 2), ask: "Do any WUs modify the same files?"

### Step 6: Handle Blocked Items

If a Work Unit is BLOCKED_FOR_HUMAN:
1. Pause batch execution
2. Report the blocking issue
3. **Keep worktree intact** (human may need to inspect)
4. Wait for human decision
5. Resume or abort based on decision

### Step 7: Update Outcome

After all Work Units complete:
1. Update Outcome issue status checklist:
   ```markdown
   ## Status
   - [x] Work Units defined
   - [x] Work Units complete
   - [ ] Success metric verified
   ```
2. Report to human:
   ```
   ## Outcome Execution Complete

   Outcome: [title]

   Work Units: N/N complete
   - [x] WU-1: [title] - APPROVED
   - [x] WU-2: [title] - APPROVED
   - [x] WU-3: [title] - APPROVED

   Total lines changed: X
   Total decisions logged: Y

   Next: Verify success metric.
   ```

## Error Handling

| Situation | Action |
|-----------|--------|
| Work Unit fails review (NEEDS_CHANGES) | Retry up to 3x in worktree, then ask human |
| Work Unit blocked for human | Pause, keep worktree for inspection, wait for decision |
| Dependency failed | Skip dependents, cleanup failed worktree, report, ask human |
| Merge conflict | Pause, report conflicting files, wait for human resolution |
| Worktree creation fails | Check disk space, check for existing worktree, report |
| MCP failure | Report error, retry once, then fail |

### Cleanup on Abort

If execution is aborted (by human or error), always cleanup:

```bash
# List all worktrees created for this outcome
git worktree list | grep ".worktrees/wu-"

# Remove each worktree
git worktree remove .worktrees/wu-BHU-141 --force
git worktree remove .worktrees/wu-BHU-143 --force

# Delete orphan branches
git branch -D wu/BHU-141 wu/BHU-143

# Remove worktrees directory if empty
rmdir .worktrees 2>/dev/null || true
```

**Never leave worktrees behind** — they consume disk space and cause confusion.

## Execution Modes

**Sequential (safe):**
```
/execute-outcome BHU-139 --sequential
```
Runs all Work Units one by one, no parallelism.

**Parallel (fast):**
```
/execute-outcome BHU-139 --parallel
```
Maximum parallelism based on dependency graph.

**Default:** Ask about dependencies, then optimize.

## Progress Tracking

During execution, maintain state:
```
Outcome: BHU-139
Started: 2026-01-21 12:30
Base branch: feature/land-valuation

Batch 1/2 (parallel):
  Worktrees: .worktrees/wu-BHU-141, .worktrees/wu-BHU-143
  - [x] BHU-141: APPROVED → merged ✓
  - [x] BHU-143: APPROVED → merged ✓
  Worktrees cleaned up ✓

Batch 2/2 (sequential):
  - [~] BHU-142: IN PROGRESS...

Active worktrees: 0
Elapsed: 7 min
```

### Worktree Status Commands

To inspect state during execution:

```bash
# List all worktrees
git worktree list

# Check branch status in a worktree
git -C .worktrees/wu-BHU-141 status

# View commits made in worktree
git -C .worktrees/wu-BHU-141 log --oneline -5
```
