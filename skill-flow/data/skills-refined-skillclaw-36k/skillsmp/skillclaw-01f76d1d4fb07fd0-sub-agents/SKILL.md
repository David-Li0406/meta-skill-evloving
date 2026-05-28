---
name: sub-agents
description: Use this skill to create and configure Claude Code sub-agents with custom prompts, tools, and models for specialized tasks.
---

# Sub-Agents Reference

Create specialized AI agents with isolated contexts for specific tasks.

## When to Use

- "How do I create a sub-agent?"
- "Configure agent tools"
- "What built-in agents exist?"
- "Agent model selection"
- "Agent chaining patterns"

## Quick Start

### Interactive (Recommended)
```bash
/agents
```
Opens menu to create, edit, and manage agents.

### Manual Creation
```bash
mkdir -p .claude/agents
cat > .claude/agents/reviewer.md << 'EOF'
---
name: reviewer
description: Code review specialist. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior code reviewer focusing on quality and security.

## Review Checklist
- Code clarity and naming
- Error handling
- Security vulnerabilities
- Test coverage
EOF
```

### CLI-Based
```bash
claude --agents '{
  "reviewer": {
    "description": "Code reviewer",
    "prompt": "Review for quality and security",
    "tools": ["Read", "Bash"],
    "model": "sonnet"
  }
}'
```

## Agent File Format

```yaml
---
name: agent-name
description: When/why to use this agent
tools: Read, Edit, Bash      # Optional, inherits all if omitted
model: sonnet                 # sonnet, opus, haiku, inherit
---

System prompt content here...
```

## Configuration Fields

| Field | Required | Options |
|-------|----------|---------|
| `name` | Yes | lowercase, hyphens |
| `description` | Yes | When to use |
| `tools` | No | Tool list (inherits all if omitted) |
| `model` | No | `sonnet`, `opus`, `haiku`, `inherit` |

## Built-In Agents

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| General-purpose | Sonnet | All | Complex multi-step tasks |
| Plan | Sonnet | Read-only | Plan mode research |
| Explore | Haiku | Read-only | Fast codebase search |

## Model Selection

| Model | Speed | Best For |
|-------|-------|----------|
| Haiku | Fastest | Search, quick lookups |
| Sonnet | Fast | Most tasks (default) |
| Opus | Slower | Complex reasoning |

## Tool Combinations

```yaml
# Code Reviewer (read-only)
tools: Read, Grep, Glob, Bash

# Debugger
tools: Read, Edit, Bash, Grep, Glob

# Implementer
tools: Read, Write, Edit, Bash, Glob
```

## Example Agents

### Code Reviewer
```yaml
---
name: code-reviewer
description: Reviews code for quality and security. Use after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---
```