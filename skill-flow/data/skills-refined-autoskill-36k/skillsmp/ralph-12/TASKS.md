# Ralph + Claude Code Tasks Integration

Ralph now integrates with Claude Code's native Tasks feature for improved cross-session coordination.

## What Are Claude Code Tasks?

Claude Code Tasks (announced Jan 2026) are a native primitive for:
- **Dependencies**: Tasks can block each other
- **Persistence**: Stored in `~/.claude/tasks`
- **Broadcasting**: Changes sync across sessions
- **Multi-session**: Share via `CLAUDE_CODE_TASK_LIST_ID`

## How Ralph Uses Tasks

### Hybrid Approach

Ralph uses **both** its custom `task.md` format AND Claude Code Tasks:

| System | Purpose |
|--------|---------|
| `.ralph/task.md` | Ralph's validation-based tasks (passes: true/false) |
| Claude Code Tasks | Native coordination, dependencies, progress tracking |

### Task List ID

Each Ralph project gets a deterministic Task List ID:

```bash
TASK_LIST_ID="ralph-${PROJECT_NAME}"
```

This allows:
- Multiple Ralph iterations to share task state
- Parallel workers to coordinate
- External tools to query progress via `~/.claude/tasks`

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `CLAUDE_CODE_TASK_LIST_ID` | Shared task list identifier | `ralph-my-project` |

Both `ralph-docker.sh` and `ralph-loop-host.sh` automatically set this.

## Allowed Tools

Ralph now includes Task tools in `--allowedTools`:

```bash
--allowedTools "Read,Write,Edit,Bash,Grep,Glob,TaskCreate,TaskUpdate,TaskList,TaskGet"
```

## Prompt.md Updates

The `prompt.md` template now instructs Claude to:

1. Check `.ralph/task.md` for validation-based tasks
2. Use `TaskCreate`/`TaskUpdate` for sub-tasks and coordination
3. Mark dependencies in Task metadata

## Benefits

### Before (Ralph alone)
- Tasks defined in markdown
- No dependency tracking
- Completion via grep `passes: true`

### After (Ralph + Tasks)
- Native task primitive with dependencies
- Real-time broadcast across sessions
- Works with Claude Code's built-in task management
- Still uses `.ralph/task.md` for validation commands

## Example Workflow

```
Iteration 1:
  - Reads .ralph/task.md, finds first task
  - Creates Task via TaskCreate for sub-work
  - Completes task, marks passes: true
  - Task state persists in ~/.claude/tasks

Iteration 2 (fresh context):
  - Same Task List ID loads previous Tasks
  - Sees iteration 1's progress
  - Picks up where it left off
  - No context pollution from iteration 1
```

## Parallel Mode

When using `ralph-parallel.sh`, multiple workers share the same Task List:

```bash
# Worker 1, 2, 3 all use:
CLAUDE_CODE_TASK_LIST_ID="ralph-my-project"
```

Tasks automatically coordinate which worker handles what via native blocking/dependencies.

## Monitoring Tasks

View Ralph's task state:

```bash
# Ralph's custom format
grep "passes:" .ralph/task.md

# Claude Code's native Tasks
ls ~/.claude/tasks/ralph-*/
```

## Backward Compatibility

- Old Ralph setups continue to work (task.md is still primary)
- Tasks integration is additive, not required
- If Tasks aren't used, Ralph falls back to pure file-based coordination
