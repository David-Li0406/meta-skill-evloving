# AGENTS.md

Instructions for AI coding assistants working in this repository.

## Purpose

This is a **knowledge base** for understanding Agent Skills. Use it to:
1. Learn how to identify good skill candidates in codebases
2. Create proper SKILL.md files for new skills
3. Register skills using the `skills` CLI

## Your Task: Finding Skills

When asked to scan a codebase for potential skills, look for:

### Strong Candidates ✓
- **CLI tools** with clear commands (has `argparse`, `click`, entry points)
- **Automation scripts** that solve specific problems
- **Wrappers** around external tools (ffmpeg, yt-dlp, etc.)
- **API clients** for services AI can't access directly
- **Local/network tools** that bridge gaps in AI capabilities

### Weak Candidates ✗
- Pure libraries with no CLI
- UI-only code (no programmatic interface)
- Internal business logic (not reusable)
- Simple utility functions (too granular)

## Scanning Workflow

```bash
# 1. Scan directory for existing SKILL.md files
skills scan ~/path/to/code

# 2. For modules WITHOUT SKILL.md, evaluate them:
#    - Does it have a CLI? Check pyproject.toml [project.scripts]
#    - Is it standalone? Minimal external deps
#    - Does it fill an AI capability gap?

# 3. Create SKILL.md for good candidates

# 4. Register and sync
skills add /path/to/module --sync
```

## SKILL.md Template

```markdown
---
name: <short-name>
description: <one-line description for AI discovery>
metadata:
  version: <semver>
  author: <username>
compatibility:
  - codex-cli
  - claude-code
  - cursor
---

# <Skill Name>

<What this skill does and when to use it>

## Commands

\`\`\`bash
<command> --help
<command> <subcommand> [options]
\`\`\`

## Examples

<Concrete usage examples>

## When to Use

- Use when: <scenarios>
- Do not use when: <anti-patterns>
```

## Key Paths

| Path | Purpose |
|------|---------|
| `~/scripts/modules/` | Source modules (scan here) |
| `~/.local/share/agent-skills/` | Central skills registry |
| `~/.codex/skills/` | Codex symlinks |
| `~/.claude/skills/` | Claude symlinks |

## Reference Material

- `agentskills/` - Anthropic spec (format details)
- `skills/` - OpenAI catalog (real examples)
- `USING_LOCAL_WEB_SKILL.md` - Usage guide example

## Do Not

- Modify `agentskills/` or `skills/` (upstream references)
- Create skills for trivial utilities
- Skip the compatibility field in SKILL.md
