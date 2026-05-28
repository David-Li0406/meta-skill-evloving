---
name: agent-orchestration
description: Use this skill when you need to coordinate multiple agents for task execution, ensuring efficient context management and workflow delegation.
---

# Agent Orchestration Skill

## Overview

This skill provides a framework for orchestrating multiple agents to perform tasks efficiently while managing context and workflow. It includes guidelines for when to use agents, how to launch them, and how to handle outputs.

## Core Principles

1. **Agent-Only Execution**: Always use agents for task execution; they handle specific domains exclusively.
2. **Context Preservation**: Avoid context bloat by letting agents manage their own tasks and outputs.
3. **Workflow Mapping**: Each request should map to a defined workflow, ensuring clarity and structure.
4. **Failure Handling**: Stop on failures, report clearly, and return control to the main process.

## When to Use Agents

| Task Type                     | Use Agent? | Reason                                      |
|-------------------------------|------------|---------------------------------------------|
| Multi-file implementation      | Yes        | Agents handle complexity internally          |
| Following a plan phase        | Yes        | Agents read the plan and implement          |
| New feature with tests        | Yes        | Agents can run tests                        |
| Single-line fix               | No         | Faster to do directly                       |
| Quick config change           | No         | Overhead not worth it                       |

## Launching Agents

To launch multiple agents in parallel, use the following pattern:

```typescript
// Launch all in a single message block (parallel)
Task({
  description: "Task 1",
  prompt: "...",
  subagent_type: "general-purpose",
  run_in_background: true
})
Task({
  description: "Task 2",
  prompt: "...",
  subagent_type: "general-purpose",
  run_in_background: true
})
// ... up to 15 parallel agents
```

## Output Management

### Simple Confirmation

For tasks where agents just need to confirm completion, use:

```bash
# Agent writes to shared status file
echo "COMPLETE: <task-name> - $(date)" >> .claude/cache/<batch-name>-status.txt
```

### Detailed Output

For tasks requiring detailed findings, structure outputs as follows:

```
.claude/cache/agents/<task-type>/<agent-id>/
├── output.md      # Main findings
├── artifacts/     # Any generated files
└── status.txt     # Completion confirmation
```

## Monitoring Agent Status

To check the completion status of agents, use:

```bash
# Check completion status
cat .claude/cache/<batch>-status.txt

# Count completions
wc -l .claude/cache/<batch>-status.txt

# Watch for updates
tail -f .claude/cache/<batch>-status.txt
```

## Best Practices

- Always use `run_in_background: true` for agents.
- Have agents write to status files and append (`>>`) rather than overwrite (`>`).
- Trust agents to handle their phases and return control after completion.

This skill integrates the best practices from various orchestration methods, ensuring efficient and effective multi-agent coordination.