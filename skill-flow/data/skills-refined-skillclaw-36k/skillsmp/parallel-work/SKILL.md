---
name: parallel-work
description: Spawn parallel agents to work on all ready issues from bd
---

# Parallel Work Command

Orchestrates parallel execution of multiple ready issues from the beads (bd) issue tracker using git worktrees for isolation.

## When Invoked

When the user runs `/parallel-work`, determine the current phase:

### Phase 1: Initial Setup (if needed)

**Check**: Run `[ -d .beads ] && echo "initialized" || echo "not initialized"`

**If not initialized**:
1. Use Task tool to spawn a general-purpose agent with this prompt:
   ```
   Read ~/.claude/guides/beads-setup-guide.md and follow the "Project Initialization" section to set up beads in this project.

   CRITICAL: You must complete ALL steps including:
   - Ensure git repository exists (run 'git init' if needed) - MUST be done before bd init
   - bd init (with sanitized prefix if needed)
   - bd hooks install
   - bd setup claude
   - Copy CLAUDE.md template (only if CLAUDE.md doesn't already exist)
   - git add . && git commit -m "Initial beads setup with CLAUDE.md"

   After setup is complete, inform the user they must restart Claude Code for hooks to take effect.
   ```
2. **STOP HERE** - User must restart Claude Code before proceeding

### Phase 2: Create Test Issues (if database empty)

**Check**: Run `bd list --status=open` to see if any issues exist

**If beads initialized AND issue database is empty** (brand new setup):
1. Create test issues for parallel work validation:
   ```bash
   bd create --title "Create README.md with project description (if missing)" --type task --priority 2
   bd create --title "Create .gitignore with common patterns (if missing)" --type task --priority 2 --description="Include .worktrees/ directory used by parallel-work skill"
   bd create --title "Add MIT LICENSE file (if missing)" --type task --priority 2
   bd sync
   ```
2. Inform user: "Created 3 test issues. Run /parallel-work again to execute them in parallel."
3. **STOP HERE**

**If beads initialized AND issues exist BUT none ready**:
- Run `bd blocked` to show blocked issues
- Inform user: "No ready issues to work on. Review blocked issues or create new ones with `bd create`."
- **STOP HERE**

### Phase 3: Execute Parallel Work

**Check**: Run `bd ready` to see ready issues

**If ready issues exist**: Continue to "Parallel Work Execution" section below

### Parallel Work Execution (Phase 3)

When ready issues exist:

1. **Fetch available work** - Run `bd ready` to get all issues with no blockers
2. **Parse issue list** - Extract issue IDs and titles from the output
3. **Store project root** - Save the current directory for later cleanup:
   ```bash
   PROJECT_ROOT="$(pwd)"
   ```
4. **Ensure initial commit exists** - Worktrees require at least one commit:
   ```bash
   # Check if any commits exist
   git log -1 >/dev/null 2>&1 || {
     echo "No commits found. Creating initial commit..."
     git add .
     git commit -m "Initial beads setup with CLAUDE.md"
   }
   ```
5. **Setup worktrees** - For each issue, create a git worktree:
   ```bash
   export BEADS_NO_DAEMON=1  # Worktrees share database; daemon may commit to wrong branch
   mkdir -p .worktrees
   git worktree add ".worktrees/<issue-id>" -b "work/<issue-id>" HEAD
   ```
6. **Spawn parallel agents** - Create one Task (general-purpose agent) per issue with these constraints:
   - Agent works ONLY in their assigned worktree directory: `$PROJECT_ROOT/.worktrees/<issue-id>`
   - Agent can commit to their branch but must NOT push
   - Agent can ONLY update their assigned issue status (`bd update <their-id> --status in_progress`)
   - Agent must NOT run `bd sync` or `git push/pull`
   - Agent should report any cross-issue changes needed (new issues, dependencies, etc.)
7. **Aggregate results** - Wait for all agents, collect their outputs and cross-issue requests
8. **Verify agent work** - For each agent, review their output to confirm:
   - Task was actually completed (not just attempted)
   - No errors or unresolved blockers reported
   - Commits were made as expected

   **If verification fails**: Spawn a new subagent to address the issue, providing:
   - The original task context
   - What the previous agent attempted
   - Why verification failed (error messages, incomplete work, etc.)
   - The same worktree (already has partial progress)

   Repeat until verification succeeds or user intervention is required to make forward progress.

9. **Merge worktrees** - For each verified worktree:
   ```bash
   git merge --no-ff "work/<issue-id>" -m "Merge work/<issue-id>: <issue-title>"
   ```
   Handle merge conflicts if they occur (may need to resolve manually or sequentially)
10. **Process cross-issue changes** - Create any new issues, add dependencies as requested by agents
11. **Cleanup worktrees** - Remove all worktrees (using stored PROJECT_ROOT to ensure correct location):
   ```bash
   # Ensure we're in the project root before cleanup
   cd "$PROJECT_ROOT"
   git worktree remove .worktrees/<issue-id>
   git branch -D "work/<issue-id>"  # Force delete (branches may not be fully merged if errors occurred)
   ```
12. **Land the plane** - Execute the session close protocol:
    - Run quality gates if code changed (tests, linters, builds)
    - Only close issues that were verified successful: `bd close <id1> <id2> ...`
    - Serialize git operations: `git pull --rebase && bd sync && git push`
    - Verify push succeeded: `git status`

## Parallel Agent Instructions

Each spawned agent receives:

```
Work on issue <ISSUE_ID>: <ISSUE_TITLE>

WORKING DIRECTORY: <WORKTREE_PATH>
You are working in a dedicated git worktree. All file operations must use this path.

IMPORTANT CONSTRAINTS:
- Work ONLY in your worktree: <WORKTREE_PATH>
- You may commit changes to your branch (work/<ISSUE_ID>) but DO NOT push
- You may ONLY update your assigned issue: <ISSUE_ID>
- DO NOT run: bd sync, git push, git pull, or update ANY other issues
- DO NOT create new issues directly
- Start by running: bd show <ISSUE_ID> to understand the full requirements
- Update status: bd update <ISSUE_ID> --status in_progress (when starting)
- When done, commit your changes: git add -A && git commit -m "<descriptive message>"
- DO NOT close your issue - the orchestrator will verify and close after merge

If you need to:
- Create new issues (follow-up work, blockers discovered, etc.)
- Add/remove dependencies
- Update other issues

Report these in your final output using this format:

CROSS_ISSUE_REQUESTS:
- create: {title: "...", type: "task|bug|feature", priority: 0-4, description: "..."}
- dependency: {from: "<issue-id>", dependsOn: "<issue-id>"}
- update: {issue: "<issue-id>", status: "...", reason: "..."}

Your work summary should include:
- What was accomplished
- Any blockers encountered
- Files changed (committed to your branch)
- Any cross-issue requests
```

## Example Execution

```
User: /parallel-work

Claude:
Let me check what work is ready...

[Runs bd ready, finds 3 issues: da-app-123, da-app-456, da-app-789]

Setting up git worktrees for parallel work...
[Creates worktrees at .worktrees/da-app-{123,456,789}]

Spawning 3 parallel agents to work on these issues:
1. da-app-123: Install dependencies (worktree: .worktrees/da-app-123)
2. da-app-456: Configure Redis (worktree: .worktrees/da-app-456)
3. da-app-789: Update documentation (worktree: .worktrees/da-app-789)

[Spawns 3 Task tools in parallel, waits for completion]

All agents completed. Merging worktree branches...
- Merged work/da-app-123 (3 files changed)
- Merged work/da-app-456 (2 files changed)
- Merged work/da-app-789 (1 file changed)

Processing cross-issue requests:
- Agent 2 requested new issue: "Test Redis connection"
[Runs bd create for new issues]

Cleaning up worktrees...
[Removes worktrees and deletes branches]

Landing the plane...
[Runs tests, bd close, git pull --rebase && bd sync && git push]

Done! All 3 issues completed and pushed to remote.
```

## Key Rules

1. **Worktree isolation** - Each agent works in its own git worktree with its own branch
2. **All agents spawn in parallel** - Use a single message with multiple Task tool invocations
3. **Commit but don't push** - Agents commit locally; orchestrator merges and pushes
4. **Controlled issue updates** - Each agent only updates their assigned issue (status only, not close)
5. **Orchestrator closes issues** - Subagents DO NOT close their issues; orchestrator verifies work completed successfully after merge, then closes
6. **Retry on failure** - If verification fails, spawn a new subagent with failure context; repeat until success or user intervention needed
7. **Single merge point** - All branches merged serially at the end to handle conflicts
8. **Single sync point** - All git/beads operations happen serially at the end
9. **Follow session close protocol** - Always verify `git push` succeeded before declaring done

## Merge Conflict Handling

If merge conflicts occur:
1. Attempt automatic merge first
2. If conflict, try merging branches one at a time with conflict resolution
3. If still unresolvable, report conflict and ask user for guidance
4. Track conflicting changes in issue updates

## Error Handling

If any agent fails or gets blocked:
- Continue with other agents while retrying the failed one
- Spawn a new subagent with:
  - Original task context
  - Previous attempt details and failure reason
  - Same worktree (preserves partial progress)
- Retry until success or user intervention required
- Don't let one failure stop the entire workflow
- Only skip merging if retries exhausted and user confirms to proceed without

## Cleanup on Failure

Always clean up worktrees, even on failure (ensure you're in project root first):
```bash
cd "$PROJECT_ROOT"  # Return to project root (stored at beginning)
git worktree list | grep "/.worktrees/" | awk '{print $1}' | xargs -I{} git worktree remove --force {}
git branch --list 'work/*' | xargs -I{} git branch -D {}
```
