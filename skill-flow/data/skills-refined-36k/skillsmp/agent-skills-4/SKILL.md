---
name: agent-skills
description: Manage and discover skills for AI coding assistants. Register skills, sync to CLIs, scan for candidates.
metadata:
  version: 0.1.0
  author: mcarls
  category: meta
compatibility:
  - codex-cli
  - claude-code
  - cursor
  - gemini-cli
---

# Agent Skills Manager

Universal skill management for AI coding assistants. Includes reference specs from Anthropic and OpenAI.

## Commands

```bash
# List registered skills
skills list
skills list --json

# Add a skill (directory must contain SKILL.md)
skills add /path/to/skill
skills add /path/to/skill --name custom-name
skills add /path/to/skill --sync  # Also sync to CLIs

# Remove a skill
skills remove skill-name

# Sync skills to CLI directories
skills sync            # All CLIs
skills sync codex      # Just Codex
skills sync claude     # Just Claude
skills sync cursor     # Just Cursor

# Scan for skills
skills scan ~/projects
skills scan ~/projects --json

# Auto-register all found skills
skills auto ~/projects
skills auto ~/projects --sync

# Show skill details
skills info skill-name
skills info skill-name --json
```

## Finding Skill Candidates

When scanning a codebase, look for:

### Strong Candidates ✓
- CLI tools with `argparse`, `click`, entry points
- Wrappers around external tools (ffmpeg, yt-dlp)
- API clients for services AI can't access
- Local/network tools that bridge AI capability gaps

### Weak Candidates ✗
- Pure libraries with no CLI
- UI-only code
- Simple utility functions

## Reference Documentation

This module includes upstream specs:

- `refs/agentskills/` - Anthropic Agent Skills specification
- `refs/openai-skills/` - OpenAI Codex skill catalog

Use these to understand the SKILL.md format and see real examples.

## Directories

| Path | Purpose |
|------|---------|
| `~/.local/share/agent-skills/` | Central skills registry |
| `~/.codex/skills/` | Codex skill symlinks |
| `~/.claude/skills/` | Claude skill symlinks |
| `~/.cursor/skills/` | Cursor skill symlinks |

## Creating a Skill

Add a `SKILL.md` file to any project:

```markdown
---
name: my-skill
description: What this skill does
metadata:
  version: 1.0.0
compatibility:
  - codex-cli
  - claude-code
---

# My Skill

Documentation for the AI to read...
```

Then register it:

```bash
skills add /path/to/my-project --sync
```
