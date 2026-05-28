<parallel_agents>
Run multiple Claude agents on the same JJ repo simultaneously. JJ's immutable commits and stable change IDs make this safe.

<modes>
<shared_mode>
All agents share the same `@` revision, partitioned by file patterns.
- Setup: instant
- Best for: quick parallel tasks, file-based splits
- Risk: agents must respect their file assignments
</shared_mode>

<workspace_mode>
Each agent gets an isolated workspace with its own `@`.
- Setup: creates `.jjtask-workspaces/<agent>/`
- Best for: longer tasks, complete isolation
- Risk: none (physical isolation)
</workspace_mode>
</modes>

<quick_start>
Shared mode:
```bash
# Create parent task
jjtask create @ "Main feature"
jj edit <task-id>

# Start session with assignments
jjtask parallel-start --mode shared \
  --assign "agent-a:src/api/**,agent-b:src/ui/**" \
  <task-id>

# Launch agents with context
jjtask agent-context agent-a  # Shows assignment, files to avoid
```

Workspace mode:
```bash
# Create parent with child tasks
jjtask create @ "Platform work"
jjtask parallel <parent> "API service" "Auth service"
jj edit <parent>

# Start workspace session
jjtask parallel-start --mode workspace <parent>

# Agents work in isolated directories
# .jjtask-workspaces/agent-a/
# .jjtask-workspaces/agent-b/
```
</quick_start>

<commands>
| Command | Purpose |
|---------|---------|
| `jjtask parallel-start [--mode shared\|workspace] [--agents N] <task>` | Start parallel session |
| `jjtask parallel-start --assign "a:pattern,b:pattern" <task>` | Start with file assignments |
| `jjtask agent-context <agent-id>` | Show mode, assignment, files to avoid |
| `jjtask agent-context <id> --format json` | JSON output |
| `jjtask parallel-status [<task>]` | All agents, progress, conflicts |
| `jjtask parallel-stop [--merge] [--force] [<task>]` | Cleanup; --merge squashes to parent |
| `jjtask parallel-recover --workspace <agent>` | Fix single workspace |
| `jjtask parallel-recover --session <task>` | Recover session |
</commands>

<mode_comparison>
| Aspect | Shared | Workspace |
|--------|--------|-----------|
| Setup time | Instant | ~30s |
| Isolation | Logical (file patterns) | Physical (directories) |
| Conflict risk | Possible if patterns overlap | None |
| Best for | Quick splits, 2 agents | Independent tasks, 3+ agents |
| Cleanup | Automatic | Remove workspaces |
</mode_comparison>

<agent_prompts>
Shared mode prompt:
```
You are agent-a in a parallel agent session.

Working directory: /path/to/repo
Mode: shared (you share @ with other agents)

YOUR ASSIGNMENT: src/api/**
Only modify files matching this pattern.

FILES TO AVOID (other agents):
- agent-b: src/ui/**

Run 'jjtask agent-context agent-a' for full context.
```

Workspace mode prompt:
```
You are agent-a in a parallel agent session.

Working directory: /path/to/repo/.jjtask-workspaces/agent-a
Mode: workspace (isolated - you have your own @)

Your task: API service implementation

You are fully isolated. Just implement your task.
When done: jjtask flag @ done
```
</agent_prompts>

<troubleshooting>
Conflict in shared mode - agents edited same file:
1. `jjtask parallel-status` to see conflicts
2. One agent reverts: `jj restore --from @- <file>`
3. Or manually merge changes

Workspace disappeared:
```bash
jjtask parallel-recover --workspace agent-a --recreate
```

Session stuck:
```bash
jjtask parallel-stop --force <task>
```

Manual cleanup:
```bash
jj workspace forget agent-a agent-b
rm -rf .jjtask-workspaces/
```
</troubleshooting>
</parallel_agents>
