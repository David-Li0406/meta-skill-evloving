---
name: meta:agent-creator
description: Create specialized agents for Claude Code. Use for agent, sub-agent, subagent, autonomous, task agent, custom agent, agent definition, agent config
---

# Agent Creator

## Quick Start

### Step 1: Create the agent

```markdown
# .claude/agents/my-reviewer.md

---

name: my-reviewer
description: Review code for specific patterns. Use proactively after implementing features.
tools: Read, Grep, Glob
model: haiku

---

# My Reviewer

You are a code reviewer. Check for:

- Pattern 1
- Pattern 2

## Output Format

\`\`\`markdown

## Summary

[Assessment]

## Issues

1. [Issue]: [File:line] - [Description]

## Verdict

[APPROVE / REQUEST CHANGES]
\`\`\`
```

### Step 2: Validate (required)

**Always run validation after creating or modifying an agent:**

```sh
uv run .claude/skills/meta-agent-creator/scripts/validate-agent.py .claude/agents/my-reviewer.md
```

Fix any errors before committing.

## Agent Locations

| Type        | Location               | Scope           | Priority |
| ----------- | ---------------------- | --------------- | -------- |
| **Project** | `.claude/agents/`      | Current project | Highest  |
| **CLI**     | `--agents` flag (JSON) | Session only    | Medium   |
| **User**    | `~/.claude/agents/`    | All projects    | Lower    |
| **Plugin**  | Plugin's `agents/` dir | Plugin users    | Lowest   |

When names conflict, higher priority wins.

## Managing Agents

Use `/agents` command for interactive agent management (view, create, edit, delete).

## Built-in Agents

| Agent             | Model  | Tools                              | Purpose                                    |
| ----------------- | ------ | ---------------------------------- | ------------------------------------------ |
| `general-purpose` | Sonnet | All                                | Complex multi-step tasks, can modify files |
| `Plan`            | Sonnet | Read, Glob, Grep, Bash             | Research in plan mode                      |
| `Explore`         | Haiku  | Read, Glob, Grep, Bash (read-only) | Fast codebase search                       |

### Explore Thoroughness Levels

Specify: **quick** (fast lookups), **medium** (balanced), or **very thorough** (comprehensive).

## YAML Frontmatter

### Required Fields

```yaml
---
name: agent-name # Lowercase, hyphens
description: What this agent does. Use proactively when [triggers].
---
```

### Optional Fields

| Field            | Purpose                   | Default                                        |
| ---------------- | ------------------------- | ---------------------------------------------- |
| `tools`          | Comma-separated tool list | Inherits ALL tools if omitted                  |
| `model`          | Model to use              | `sonnet` (or use `inherit`)                    |
| `permissionMode` | Permission handling       | `default`                                      |
| `skills`         | Auto-load skills          | None (agents DON'T inherit skills from parent) |

```yaml
---
name: agent-name
description: Description with triggers
tools: Read, Grep, Glob, Bash # Omit to inherit all tools
model: inherit # Use parent's model
permissionMode: default
skills: auth, database # Must explicitly list - no inheritance
---
```

> **Important**: Subagents do NOT inherit skills from the parent conversation. You must explicitly list skills in the `skills` field.

### Permission Modes

| Mode                | Behavior                       |
| ------------------- | ------------------------------ |
| `default`           | Normal permission prompts      |
| `acceptEdits`       | Auto-approve file edits        |
| `dontAsk`           | Skip all permission dialogs    |
| `bypassPermissions` | No permission checks at all    |
| `plan`              | Planning mode (research only)  |
| `ignore`            | Ignore permission requirements |

## CLI-based Agents

Define agents dynamically with `--agents` flag:

```sh
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer...",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

Useful for quick testing, session-specific agents, or automation scripts.

## Resumable Agents

Agents can be resumed to continue previous conversations:

```text
> Use code-analyzer to review the auth module
[Agent completes, returns agentId: "abc123"]

> Resume agent abc123 and also check the authorization logic
[Agent continues with full previous context]
```

- Each execution gets a unique `agentId`
- Transcripts stored in `agent-{agentId}.jsonl`
- Use `resume` parameter with the agent ID to continue

## Disabling Agents

Disable specific agents using permission rules:

```json
{
  "permissions": {
    "deny": ["Task(Explore)", "Task(Plan)"]
  }
}
```

Or via CLI:

```sh
claude --disallowedTools "Task(Explore)"
```

## Model Selection Guide

| Model    | Cost   | Speed  | Use Case                                        |
| -------- | ------ | ------ | ----------------------------------------------- |
| `haiku`  | Low    | Fast   | Code review, style checks, simple validation    |
| `sonnet` | Medium | Medium | Debugging, security analysis, complex reasoning |
| `opus`   | High   | Slow   | Architecture decisions, multi-system analysis   |

### Decision Tree

```text
Is this a simple checklist task?
  → Yes: haiku
  → No: Does it require deep reasoning or security analysis?
    → Yes: sonnet
    → No: Does it involve architecture or cross-system decisions?
      → Yes: opus
      → No: sonnet
```

## Tool Selection Guide

| Tool        | Purpose                 | Include When               |
| ----------- | ----------------------- | -------------------------- |
| `Read`      | Read file contents      | Always (basic exploration) |
| `Grep`      | Search content patterns | Pattern matching needed    |
| `Glob`      | Find files by name      | File discovery needed      |
| `Bash`      | Run shell commands      | Diagnostics, tests, builds |
| `Write`     | Create new files        | Agent creates artifacts    |
| `Edit`      | Modify existing files   | Agent makes code changes   |
| `WebFetch`  | Fetch web content       | Documentation lookup       |
| `WebSearch` | Search the web          | Research tasks             |

### Common Tool Combinations

```yaml
# Read-only reviewer
tools: Read, Grep, Glob

# Investigator with diagnostics
tools: Read, Grep, Glob, Bash

# Agent that can fix issues
tools: Read, Grep, Glob, Edit

# Research agent
tools: Read, Grep, Glob, WebFetch, WebSearch
```

## Agent Templates

See [reference.md](reference.md) for complete templates:

- **Review Agent** - Code review with checklist and structured output
- **Investigation Agent** - Debugging with systematic process
- **Exploration Agent** - Codebase discovery and documentation
- **Security Audit Agent** - Vulnerability assessment

## Best Practices

1. **Start with Claude-generated agents**: Use `/agents` to generate initial agent, then customize
2. **Design focused agents**: One clear responsibility per agent
3. **Write detailed prompts**: Include instructions, examples, and constraints
4. **Limit tool access**: Only grant necessary tools for security and focus
5. **Version control**: Check project agents into git for team sharing
6. **Use proactive triggers**: Include "use PROACTIVELY" or "MUST BE USED" in descriptions

## Common Mistakes

| Mistake                        | Impact                 | Correct Pattern                  |
| ------------------------------ | ---------------------- | -------------------------------- |
| Using opus for simple reviews  | Slow, expensive        | Use haiku for checklist tasks    |
| No output format template      | Inconsistent responses | Always include structured format |
| Explicit tools when not needed | Loses MCP tools        | Omit `tools` to inherit all      |
| Expecting skill inheritance    | Missing context        | Explicitly list skills needed    |
| Generic role description       | Poor focus             | Be specific about domain/project |
| Too many responsibilities      | Unfocused agent        | One clear purpose per agent      |
| No checklist for reviewers     | Inconsistent reviews   | Include explicit checklist       |

## Validation

Run the validator to check agent structure:

```sh
uv run .claude/skills/meta-agent-creator/scripts/validate-agent.py .claude/agents/my-agent.md
```

### Checklist

- [ ] File location: `.claude/agents/<name>.md`
- [ ] YAML has name, description, tools, model
- [ ] Description includes trigger phrases
- [ ] Model appropriate for task complexity
- [ ] Tools list matches actual usage
- [ ] Role description is project-specific
- [ ] Output format template included
- [ ] All code blocks have language specifiers

## Delegation

- **After creating/modifying agents**: Run `uv run .claude/skills/meta-agent-creator/scripts/validate-agent.py <agent.md>`
- **Pattern discovery**: For existing agent patterns, use `Explore` agent

## References

- Official Subagents Docs: [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents.md)
- Existing agents: `.claude/agents/code-reviewer.md`, `debugger.md`, `security-auditor.md`
- Best Practices: [anthropic.com/engineering/claude-code-best-practices](https://www.anthropic.com/engineering/claude-code-best-practices)
