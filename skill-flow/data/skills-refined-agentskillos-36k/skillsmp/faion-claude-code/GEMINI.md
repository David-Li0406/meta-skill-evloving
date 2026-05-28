# faion-claude-code Skill

## Overview

Claude Code configuration skill for creating and managing Claude Code components:
- Skills (SKILL.md files, references, automation)
- Agents (subagents with isolated context)
- Commands (slash commands with arguments)
- Hooks (lifecycle automation scripts)
- MCP servers (Model Context Protocol integrations)

Also covers settings, permissions, IDE integrations, and naming conventions.

---

## Directory Structure

```
faion-claude-code/
├── SKILL.md           # Main skill definition and routing
├── CLAUDE.md          # This navigation file
├── skills.md          # Skill creation guide (~346 lines)
├── agents.md          # Agent creation guide (~361 lines)
├── commands.md        # Command creation guide (~288 lines)
├── hooks.md           # Hook development guide (~484 lines)
├── mcp.md             # MCP server reference (~706 lines)
└── ref-CLAUDE.md      # Extended references
```

---

## Key Files

| File | Purpose | Size |
|------|---------|------|
| **SKILL.md** | Main entry point with routing table, naming conventions, settings reference, quick commands | ~276 lines |
| **skills.md** | SKILL.md creation, frontmatter fields, token economy, locations, troubleshooting | ~346 lines |
| **agents.md** | Agent files, tools whitelist, prompt writing, parallel execution patterns | ~361 lines |
| **commands.md** | Slash commands, argument syntax ($1, $ARGUMENTS), special syntax (!, @) | ~288 lines |
| **hooks.md** | Lifecycle events, input/output schemas, templates (Python/Bash), common patterns | ~484 lines |
| **mcp.md** | MCP server development (TS/Python), catalog of 40+ servers, configuration | ~706 lines |

---

## Routing Logic

The skill routes requests based on keywords:

| Keywords | Reference Loaded |
|----------|-----------------|
| skill, SKILL.md | skills.md |
| agent, subagent | agents.md |
| command, /cmd, slash | commands.md |
| hook, PreToolUse, PostToolUse | hooks.md |
| MCP, server, install mcp | mcp.md |
| settings, config | Handled directly in SKILL.md |

---

## Naming Conventions Summary

### Global (faion-network)

| Component | Pattern | Example |
|-----------|---------|---------|
| Skill (orchestrator) | `faion-net` | `faion-net` |
| Skill (role-based) | `faion-{role}` | `faion-software-developer`, `faion-ux-ui-designer` |
| Skill (process) | `faion-{process}` | `faion-sdd`, `faion-feature-executor` |
| Agent | `faion-{name}-agent` | `faion-task-YOLO-executor-opus-agent` |
| Command | `{verb}` | `commit`, `deploy` |
| Hook | `faion-{event}-{purpose}-hook.{ext}` | `faion-pre-bash-security-hook.py` |

### Project-specific (gitignored)

| Component | Pattern | Example |
|-----------|---------|---------|
| Skill | `{project}-{name}` | `myapp-auth`, `myapp-deploy` |
| Agent | `{project}-{name}-agent` | `myapp-deploy-agent` |
| Command | `{project}-{action}` | `myapp-build` |
| Hook | `{project}-{event}-{purpose}-hook.{ext}` | `myapp-pre-bash-lint-hook.sh` |

---

## Quick Reference

### Create Skill
```bash
mkdir -p ~/.claude/skills/faion-my-skill
# Write SKILL.md with frontmatter
```

### Create Agent
```bash
# Write ~/.claude/agents/faion-my-agent.md
```

### Create Command
```bash
# Write ~/.claude/commands/my-cmd.md
```

### Install MCP Server
```bash
claude mcp add <name> -s user -e KEY=value -- npx -y <package>
```

---

## Documentation

- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [MCP Servers](https://docs.anthropic.com/en/docs/claude-code/mcp)
