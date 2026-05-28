---
name: parallel-agent-workflow
description: "Coordinate multiple agents working in parallel using git worktrees to avoid file conflicts. Use when needing concurrent agents to modify different files/components with worktree isolation, or when asked to use worktrees for parallel agent work."
---

# Parallel Agent Workflow

Execute multi-agent refactoring, feature development, or parallel work using git worktrees to prevent conflicts.

## How It Works

1. **Split work** across N agents, each in isolated git worktree
2. **Agents work independently** on different components/files
3. **Merge in stages** - combine related work into logical groups
4. **Final merge** - all work combined into single branch

## Instructions

### Phase 1: Planning

1. **Identify the work units** - What needs to be done?
2. **Determine agent count**:
   - If user specifies: Use that count
   - If not specified: Auto-determine based on independent work units
3. **Ask for missing requirements** if not in environment:
   - Setup script (if `dev-setup` doesn't exist): "What command sets up dependencies?"
   - Test command (if unknown): "What command verifies the build?"
4. **Create merge strategy**:
   - Group related work units logically
   - Plan merge stages (N agents → M groups → 1 final)
   - Example: 6 agents → 2 groups → 1 final

### Phase 2: Execute Agent Work

For each agent:

1. **Create worktree**:
   ```bash
   # Pattern: {project}@{branch-name}
   git worktree add ../{project}@{work-unit-name} -b {branch-name}
   ```
   - **CRITICAL**: If worktree creation fails → STOP IMMEDIATELY, report error

2. **Agent instructions must include**:
   - cd into worktree
   - Run setup script (or `dev-setup` if exists)
   - Run test command BEFORE changes
   - Do the work
   - Run test command AFTER changes
   - Commit changes
   - Remove worktree

3. **Launch agents concurrently** using Task tool with multiple invocations in single message

4. **Monitor results**:
   - Agent fails: Surface reason in conversation
   - Agent succeeds: Note commit hash

### Phase 3: Staged Merges

Merge in stages based on logical grouping:

1. **Stage 1**: Merge related work into group branches
   - Create worktree for each group
   - Merge related branches
   - **Merge conflicts**: Agent resolves automatically, surfaces resolution in output
   - Run test command to verify merge
   - Remove worktree

2. **Stage N**: Final merge
   - Create final worktree
   - Merge all group branches
   - Run test command
   - Remove worktree

### Phase 4: Completion

Report to user:
- Final branch name
- Final commit hash
- Summary of all changes merged
- Any conflicts that were resolved
- Any failures that occurred

**DO NOT** create PR - just report the branch.

## Worktree Naming Convention

```
{project-dir}@{descriptive-name}
```

Examples:
- `iac-lockin@headscale-refactor`
- `myapp@feature-auth`
- `webapp@fix-api-bug`

## Merge Strategy Examples

### Example 1: Component Refactoring (6 → 2 → 1)
```
Stage 1: 6 agents work independently
  - Agent 1: Refactor ComponentA → branch: refactor/component-a
  - Agent 2: Refactor ComponentB → branch: refactor/component-b
  - Agent 3: Refactor ComponentC → branch: refactor/component-c
  - Agent 4: Refactor ComponentD → branch: refactor/component-d
  - Agent 5: Refactor ComponentE → branch: refactor/component-e
  - Agent 6: Refactor ComponentF → branch: refactor/component-f

Stage 2: 2 merge agents (logical grouping)
  - Merge Agent 1: Combine A+B+C → branch: refactor/merge-group-1
  - Merge Agent 2: Combine D+E+F → branch: refactor/merge-group-2

Stage 3: 1 final merge agent
  - Final Merge: Combine group-1 + group-2 → branch: refactor/final
```

### Example 2: Feature Development (4 → 1)
```
Stage 1: 4 agents work independently
  - Agent 1: Backend API → branch: feature/backend-api
  - Agent 2: Frontend UI → branch: feature/frontend-ui
  - Agent 3: Database migrations → branch: feature/db-migrations
  - Agent 4: Tests → branch: feature/tests

Stage 2: 1 final merge agent
  - Final Merge: All branches → branch: feature/complete
```

## Error Handling

### Critical Failures (STOP)
- Worktree creation fails
- Setup script not found and user doesn't provide one
- Test command not found and user doesn't provide one

### Recoverable Issues (Agent handles)
- Merge conflicts → Agent resolves, surfaces in output
- Test failures → Agent reports, surfaces reason
- Code errors → Agent fixes or reports

## Template Agent Prompt

```markdown
You are working on {WORK_DESCRIPTION}.

## Setup Instructions

1. **Create git worktree**:
   - Worktree path: `../{PROJECT}@{WORK_NAME}`
   - Branch: `{BRANCH_NAME}`
   - Command: `git worktree add ../{PROJECT}@{WORK_NAME} -b {BRANCH_NAME}`

2. **Setup worktree**:
   - cd into worktree
   - Run: `{SETUP_COMMAND}`
   - Run: `{TEST_COMMAND}` to verify initial state

3. **Do the work**:
   {SPECIFIC_WORK_INSTRUCTIONS}

4. **Verify**:
   - Run: `{TEST_COMMAND}` to verify changes
   - If tests fail: Fix issues before committing

5. **Finalize**:
   - Commit: "{COMMIT_MESSAGE}"
   - Remove worktree: `git worktree remove ../{PROJECT}@{WORK_NAME}`

## Important
- If worktree creation fails: STOP and report error
- If merge conflicts: Resolve them and document resolution
- If tests fail: Report failure reason with details

Return: Summary, files modified, commit hash, any issues.
```

## Best Practices

1. **Work isolation**: Each agent should modify different files/components
2. **Logical grouping**: Merge related work together in stages
3. **Test coverage**: Always verify before and after changes
4. **Clear naming**: Use descriptive worktree and branch names
5. **Conflict resolution**: Let agents resolve conflicts automatically when possible
6. **Status reporting**: Surface all issues in conversation for user visibility

## Version History

- v1.0.0 (2025-11-09): Initial version based on component refactoring workflow
