# Agent Skills

Universal skill manager for AI coding assistants (Codex CLI, Claude Code, Cursor, Gemini CLI).

Includes reference documentation from upstream specs to help AI agents discover and create skills.

## Installation

```bash
pip install -e /path/to/agent_skills
```

## Quick Start

```bash
# Scan for skills in your projects
skills scan ~/scripts/modules

# Auto-register any found skills
skills auto ~/scripts/modules --sync

# List what's registered
skills list

# Sync to all CLIs
skills sync
```

## How It Works

1. **Central directory**: Skills registered at `~/.local/share/agent-skills/`
2. **Symlinks**: Each skill is a symlink to the actual project
3. **CLI sync**: Creates symlinks in each CLI's skill directory
4. **SKILL.md**: Standard format all CLIs understand

## CLI Reference

| Command | Description |
|---------|-------------|
| `skills list` | List registered skills |
| `skills add <path>` | Add skill from directory with SKILL.md |
| `skills remove <name>` | Remove a skill |
| `skills sync [cli]` | Sync to CLI directories |
| `skills scan <path>` | Find SKILL.md files |
| `skills auto <path>` | Auto-register found skills |
| `skills info <name>` | Show skill details |

## Supported CLIs

- **Codex CLI**: `~/.codex/skills/`
- **Claude Code**: `~/.claude/skills/`
- **Cursor**: `~/.cursor/skills/`

## What Makes a Good Skill?

When scanning a codebase, look for modules that:

| Criteria | Why It Matters |
|----------|----------------|
| Has a CLI interface | AI can invoke it directly |
| Solves a specific problem | Focused purpose = better skill |
| Works standalone | No complex dependencies |
| Fills a gap | Does something AI can't do natively |

### Good Candidates
- CLI tools with `argparse`/`click` entry points
- Wrappers around external tools (ffmpeg, yt-dlp)
- API clients for services AI can't access
- Local/network tools (accessing LAN URLs)

### Weak Candidates
- Pure libraries with no CLI
- UI-only code
- Simple utility functions

## Creating Skills

Any project can become a skill by adding `SKILL.md`:

```markdown
---
name: my-tool
description: Short description
metadata:
  version: 1.0.0
compatibility:
  - codex-cli
  - claude-code
---

# My Tool

Instructions for AI assistants...

## Commands

\`\`\`bash
my-tool --help
my-tool do-something --flag value
\`\`\`

## When to Use

- Use when: <scenarios>
- Do not use when: <anti-patterns>
```

## SKILL.md vs AGENTS.md

| | SKILL.md | AGENTS.md |
|---|----------|-----------|
| **Purpose** | Define a capability | Define agent behavior |
| **Scope** | Per-module/tool | Per-repo or global |
| **Loading** | On-demand | Always in context |

## Reference Documentation

This module includes upstream specs as git submodules:

- `refs/agentskills/` - [Anthropic Agent Skills spec](https://agentskills.io)
- `refs/openai-skills/` - [OpenAI Codex skill catalog](https://github.com/openai/skills)

## Directory Structure

```
agent_skills/
├── agent_skills/       # Python module (CLI + discovery)
├── refs/
│   ├── agentskills/    # Anthropic spec (submodule)
│   └── openai-skills/  # OpenAI catalog (submodule)
├── docs/               # Usage guides
├── tests/              # Pytest tests
├── AGENTS.md           # Instructions for AI agents
├── SKILL.md            # This module as a skill
└── README.md           # This file
```

## License

MIT
