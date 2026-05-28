# Built-in Subagent Patterns

Claude Code provides built-in subagents for efficient exploration without bloating main context.

## Available Subagents

| Subagent | Model size | Best For |
|----------|------------|----------|
| **Explore** | small (haiku) | File discovery, pattern search, codebase questions |
| **general-purpose** | medium (sonnet) | Complex multi-step research, code analysis |
| **Plan** | medium (sonnet) | Architecture design, implementation planning |

Model sizes map to Claude tiers: small = haiku, medium = sonnet, large = opus.

## Explore Agent Thoroughness Levels

| Level | Use Case | Example |
|-------|----------|---------|
| `quick` | Known location, simple search | Find a specific file |
| `medium` | Moderate exploration | Find related implementations |
| `very thorough` | Comprehensive analysis | Understand entire subsystem |

## Pre-Implementation Exploration

Before implementing a task, gather context efficiently:

```
Use the Explore agent (medium thoroughness) to find:
- Existing implementations of similar patterns
- Test files for the target module
- Related documentation that may need updates
- Import/export patterns in the target directory
```

## Pattern: Find Related Code

```
Use the Explore agent (quick thoroughness) to find:
- All files importing {module-name}
- Test coverage for {function-name}
- Configuration files affecting {feature}
```

## Pattern: Understand Architecture

```
Use the Explore agent (very thorough) to understand:
- How {subsystem} is structured
- Data flow through {component}
- Integration points with {external-system}
```

## When NOT to Use Subagents

- Single file already in context
- Task specifies exact file paths
- Near context limit (80%+)
- Simple, isolated changes
