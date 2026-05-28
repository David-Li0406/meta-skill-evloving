# PAI Agent System

**Reference for agent usage in PAI.**

---

## Available Subagent Types

PAI uses the vanilla Claude Code Task tool subagent_types:

| Subagent Type | Purpose | When Used |
|---------------|---------|-----------|
| `Bash` | Command execution | Running shell commands |
| `general-purpose` | Multi-step tasks | General work, research, analysis |
| `Explore` | Codebase exploration | Finding files, understanding structure |
| `Plan` | Implementation planning | Plan mode, architecture design |
| `claude-code-guide` | Claude Code help | Questions about Claude Code features |

## Usage

```typescript
// General parallel work
Task({
  description: "Research topic",
  prompt: "Investigate X...",
  subagent_type: "general-purpose",
  model: "haiku"
})

// Codebase exploration
Task({
  description: "Find auth code",
  prompt: "Find all authentication-related files...",
  subagent_type: "Explore"
})

// Implementation planning
Task({
  description: "Plan feature",
  prompt: "Design implementation approach for...",
  subagent_type: "Plan"
})
```

## Model Selection

| Task Type | Model | Speed |
|-----------|-------|-------|
| Simple checks, parallel work | `haiku` | Fastest |
| Standard analysis | `sonnet` | Balanced |
| Deep reasoning | `opus` | Maximum intelligence |

## Spotcheck Pattern

After parallel work, always verify consistency:

```typescript
Task({
  prompt: "Verify consistency across all agent outputs: [results]",
  subagent_type: "general-purpose",
  model: "haiku"
})
```

---

*Last updated: 2026-01-24*
