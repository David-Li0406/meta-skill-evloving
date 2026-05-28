# Subagent Investigation Patterns

For complex fidelity reviews, leverage Claude Code's built-in subagents to gather context before and investigate findings after the MCP review.

## Built-in Subagents for Fidelity Review

| Subagent | Model size | Use Case |
|----------|------------|----------|
| **Explore** | small (haiku) | Fast file discovery, implementation mapping |
| **general-purpose** | medium (sonnet) | Complex deviation analysis requiring code reading |

## Pre-Review Context Gathering

Before running `mcp__plugin_foundry_foundry-mcp__review action="fidelity"`, gather implementation context:

**Phase review preparation:**
```
Use the Explore agent (medium thoroughness) to find:
- All files matching the phase's task file_path patterns
- Test files corresponding to implementation files
- Configuration or setup files that affect behavior
- Recent git changes in the implementation area
```

**Task review preparation:**
```
Use the Explore agent (quick thoroughness) to find:
- The implementation file and its imports
- Related test file for the task
- Any configuration the implementation depends on
```

## Post-Review Investigation

After receiving fidelity results, investigate deviations:

**For major deviations:**
```
Use the Explore agent (very thorough) to investigate:
- Why the implementation differs from spec
- What constraints led to the deviation
- Whether deviation is documented (comments, commits, journals)
- Impact on dependent files
```

**For missing functionality:**
```
Use the Explore agent (medium thoroughness) to find:
- Whether the feature exists elsewhere (different file/name)
- Related implementations that might explain the gap
- Test coverage for the expected functionality
```

## When to Use Subagents vs Direct Review

**Use Explore subagent when:**
- Phase spans many files you haven't read
- Deviations are unclear and need investigation
- Need to understand implementation context first
- Want to preserve main context for review results

**Skip subagent exploration when:**
- Single task review in familiar code
- Implementation files already in context
- Quick validation of known changes
- Near context limit

## Benefits

| Benefit | Description |
|---------|-------------|
| **Context isolation** | File searches don't bloat main conversation |
| **Faster discovery** | Small model size (haiku) finds files quickly |
| **Focused investigation** | Post-review exploration targets specific deviations |
| **Parallel preparation** | Can explore while formulating review strategy |
