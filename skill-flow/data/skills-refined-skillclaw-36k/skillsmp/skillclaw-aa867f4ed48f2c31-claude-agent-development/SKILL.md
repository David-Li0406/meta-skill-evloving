---
name: claude-agent-development
description: Use this skill when creating agents, writing agent frontmatter, configuring subagents, or when "create agent", "agent.md", "subagent", or "Task tool" are mentioned.
---

# Claude Agent Development

Create and validate specialized subagents that extend Claude Code with focused expertise.

## Agents vs Skills

**Critical distinction**:

| Aspect         | Agents (This Skill)                         | Skills                                 |
| -------------- | ------------------------------------------- | -------------------------------------- |
| **Purpose**    | Specialized subagents with focused expertise | Capability packages with instructions  |
| **Invocation** | Task tool (`subagent_type` parameter)       | Automatic (model-triggered by context) |
| **Location**   | `agents/` directory                         | `skills/` directory                    |
| **Structure**  | Single `.md` file with frontmatter          | Directory with `SKILL.md` + resources  |

See [agent-vs-skill.md](references/agent-vs-skill.md) for details.

## Quick Start

### Using Templates

Copy a template from `templates/`:

| Template          | Use When                                     |
| ----------------- | -------------------------------------------- |
| `basic.md`        | Simple agents with focused expertise         |
| `advanced.md`     | Full-featured agents with all config options |

### Scaffolding

```bash
./scripts/scaffold-agent.sh security-reviewer -t reviewer
```

## Workflow Overview

1. **Discovery** - Define purpose, scope, and triggers
2. **Design** - Choose archetype and configuration
3. **Implementation** - Write frontmatter and instructions
4. **Validation** - Verify against quality standards

---

## Phase 1: Discovery

Before writing code, clarify:

- **Purpose**: What specialized expertise does this agent provide?
- **Triggers**: What keywords/phrases should invoke it?
- **Scope**: What does it do? What does it NOT do?
- **Location**: Personal (`~/.claude/agents/`), project (`agents/`), or plugin?

**Key questions**:
- Is this a specialized role or a general capability? (Role = agent, Capability = skill)
- What user phrases should trigger this agent?
- What tools does it need access to?

---

## Phase 2: Design

### Agent Archetypes

| Type | Purpose | Typical Tools |
|------|---------|---------------|
| ...  | ...     | ...           |