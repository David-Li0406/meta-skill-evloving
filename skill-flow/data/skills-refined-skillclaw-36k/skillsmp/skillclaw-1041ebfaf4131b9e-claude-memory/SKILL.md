---
name: claude-memory
description: Use this skill when creating and optimizing CLAUDE.md memory files or .claude/rules/ modular rules for Claude Code projects, ensuring effective context awareness and project organization.
---

# Skill body

## Objective
Master the creation of effective Claude Code memory systems using either CLAUDE.md files or the modular `.claude/rules/` directory. This skill covers file hierarchy, content structure, path-scoped rules, formatting, emphasis techniques, and common anti-patterns to avoid.

Memory files are automatically loaded at session startup, consuming tokens from your 200k context window. Every instruction competes with Claude Code's ~50 built-in instructions, leaving ~100-150 effective instruction slots for your customizations.

**Two approaches available:**

- **CLAUDE.md** - Single file, simpler, best for small projects.
- **.claude/rules/** - Modular files with optional path-scoping, best for large projects.

## Quick Start

### Bootstrap New Project
Run `/init` in Claude Code to auto-generate a CLAUDE.md with project structure.

Or create manually at project root:

```markdown
# Project Name

## Tech Stack

- [Primary language/framework]
- [Key libraries]

## Commands

- `npm run dev` - Start development
- `npm test` - Run tests
- `npm run build` - Build for production

## Code Conventions

- [2-3 critical conventions]

## Important Context

- [1-2 architectural decisions worth knowing]
```

### Quick Add Memory
Press `#` during a Claude Code session to quickly add new memory items without editing the file directly.

### Edit Memory
Use the `/memory` command to open CLAUDE.md in your system editor.

## File Hierarchy
Claude Code loads CLAUDE.md files in a specific order. Higher priority files are loaded first and take precedence.

### Loading Order
| Priority | Location | Purpose | Scope |
|----------|----------|---------|-------|
| 1 (Highest) | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | Enterprise policy (managed by IT) | All org users |
| 2 | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Project memory (git-tracked) | Team via git |
| 2 | `./.claude/rules/*.md` | Modular rules (git-tracked) | Team via git |
| 3 | `~/.claude/CLAUDE.md` | User-specific memory |