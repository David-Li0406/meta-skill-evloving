---
name: setup
description: Configure Claude Code with symlinks to knowledge base agents and skills
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Setup Skill

Set up and maintain your Claude Code configuration from the team knowledge base.

## Usage

```bash
/setup             # First-time setup or status check
/setup update      # Update CLAUDE.md and sync new skills
```

## Overview

- **First run**: Detects knowledge base, symlinks agents, copies skills, generates CLAUDE.md
- **Status check**: Shows current config status and available updates
- **Update**: Syncs shared sections of CLAUDE.md, offers to copy new skills

## Quick Reference

Runbook: `runbook/setup-claude-code.md` in your knowledge base.

## What Gets Configured

| Item | Method | Why |
|------|--------|-----|
| Agents | Symlink | Auto-updates on git pull |
| Skills | Copy | Allows personal additions |
| CLAUDE.md | Generate | Paths differ per user |

## Adding Personal Skills

After setup, add skills directly to `~/.claude/skills/`:

```bash
mkdir ~/.claude/skills/my-skill
# Add SKILL.md with your definition
```

To share with the team, copy to the knowledge base and commit.
