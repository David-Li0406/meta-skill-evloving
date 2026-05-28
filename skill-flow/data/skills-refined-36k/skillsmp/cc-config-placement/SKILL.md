---
name: cc-config-placement
description: Use when adding rules, commands, or skills to dotfiles - decides global vs project-local placement
---

# CC Config Placement

Decide whether Claude Code config belongs in global (`claude/`) or project-local (`.claude/`).

## The Two Levels

| Path | Symlinked To | Scope |
|------|--------------|-------|
| `claude/` | `~/.claude/` | All projects |
| `.claude/` | (not symlinked) | Dotfiles repo only |

## Decision Guide

**Global (`claude/`):**
- Communication preferences, work style
- Commit format, API rules
- Skills/commands useful across all projects

**Project-local (`.claude/`):**
- Dotfiles-specific conventions
- Commands like `/audit`
- Rules scoped to specific dotfiles

## When Ambiguous

Ask: "Should this apply globally (all projects) or just to dotfiles?"

Ambiguous examples:
- "Add a rule about X" → which level?
- "Create a command for Y" → global or local?
- "Remember that I prefer Z" → sounds global, confirm

## File Structure

```
dotfiles/
├── claude/           → ~/.claude/ (GLOBAL)
│   ├── CLAUDE.md
│   ├── skills/
│   └── rules/
│
└── .claude/          PROJECT-LOCAL
    ├── CLAUDE.md
    ├── skills/
    ├── commands/
    └── rules/
```
