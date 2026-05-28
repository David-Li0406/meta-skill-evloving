---
name: multi-agent-scan
description: This skill should be used when the user asks to "scan the codebase", "analyze multiple patterns", "parallel agent workflow", or "multi-agent research". Spawns multiple agents in parallel for comprehensive codebase analysis.
version: 1.0.0
---

# Multi-Agent Parallel Scan

Orchestrates multiple agents in parallel to perform comprehensive codebase analysis across different dimensions simultaneously.

## When to Use

Invoke this skill when the user requests:
- "Scan my codebase"
- "Analyze multiple patterns"
- "Multi-agent workflow"
- "Parallel analysis"
- "Comprehensive code review"

## Workflow Pattern

### Phase 1: Parallel Exploration (Independent Tasks)

Fire multiple agents simultaneously to explore different aspects. All agents start in parallel when launched in a single message:

```
# Scan for different code patterns in parallel
Task(subagent_type="tutorial-workflow:file-scanner", model="haiku", prompt="Find all TypeScript files with TODO comments")
Task(subagent_type="tutorial-workflow:file-scanner", model="haiku", prompt="Find all files using deprecated APIs")
Task(subagent_type="tutorial-workflow:file-scanner", model="haiku", prompt="Find all large files (>500 lines)")
```

### Phase 2: Deep Analysis (Sequential)

After results arrive, perform deeper analysis:

```
Task(
  subagent_type="tutorial-workflow:code-analyzer",
  model="opus",
  prompt=f"""Analyze these findings and provide recommendations:

  TODOs: {todo_results}
  Deprecated APIs: {deprecated_results}
  Large files: {large_files}

  Provide refactoring recommendations prioritized by impact."""
)
```

### Phase 3: External Research (Parallel)

Run parallel research while analysis happens:

```
Task(subagent_type="tutorial-workflow:web-researcher", model="sonnet", prompt="Search for TypeScript best practices for code organization")
Task(subagent_type="tutorial-workflow:web-researcher", model="sonnet", prompt="Find latest recommendations for handling deprecated APIs")
```

## Best Practices

1. **Always use single message for parallel calls** - Multiple Task calls in one message execute concurrently
2. **Match model to task complexity** - Use Haiku for simple searches, Sonnet for research, Opus for analysis
3. **Background long-running tasks** - Use `run_in_background: true` for builds, installs, tests
4. **Limit concurrency** - Maximum 5 concurrent background tasks to prevent resource exhaustion

## Concurrency Limits

- **Max 5 concurrent background tasks** - Claude Code's default limit
- **No limit on parallel foreground tasks** - As many as your message can fit
- **Batch dependent work** - Run independent batches in parallel, wait, then next batch

## Example Session

```
User: "Scan my codebase using the multi-agent workflow"

Claude:
1. Spawns 3 file-scanner agents in parallel (TODOs, deprecated APIs, large files)
2. Collects results from all agents
3. Spawns code-analyzer for deep analysis
4. Spawns web-researcher agents for best practices research
5. Provides comprehensive report with prioritized recommendations
```
