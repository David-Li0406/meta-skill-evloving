# CLAUDE.md Specific Features

CLAUDE.md is Claude Code's specific implementation with additional features not available in AGENTS.md.

## Hierarchical Memory System

Four memory types in priority order (highest first):

| Type | Location | Purpose | Scope |
|------|----------|---------|-------|
| Enterprise | `/etc/claude-code/CLAUDE.md` (Linux) | Organization-wide policies | All users |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared instructions | Git-tracked |
| User | `~/.claude/CLAUDE.md` | Personal preferences | All projects |
| Local | `./CLAUDE.local.md` | Personal project settings | Current project |

### Platform-Specific Paths

**Enterprise memory:**
- macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
- Linux/WSL: `/etc/claude-code/CLAUDE.md`
- Windows: `C:\ProgramData\ClaudeCode\CLAUDE.md`

## Import Feature

Import other files using `@path/to/file` syntax:

```markdown
See @README.md for project overview.

## Git Workflow
Follow the guidelines in @docs/git-workflow.md
```

### Import Rules

- Relative and absolute paths supported
- Home directory: `@~/.claude/shared-instructions.md`
- **Not evaluated** inside code blocks or code spans
- Recursive imports up to 5 levels deep

### Example

```markdown
# Project Instructions

@docs/architecture.md
@docs/conventions.md

## Quick Reference
- Build: `npm run build`
- Test: `npm test`
```

## Auto-Loading Behavior

Claude Code automatically loads:

1. **Upward traversal**: All CLAUDE.md files from current directory to root
2. **Subtree detection**: Nested CLAUDE.md files in subdirectories (loaded when accessing those files)

## Memory Commands

| Command | Purpose |
|---------|---------|
| `#` prefix | Quick add to memory (prompts for file selection) |
| `/memory` | Open memory file in editor |
| `/init` | Bootstrap CLAUDE.md for current project |

## When to Use CLAUDE.md vs AGENTS.md

**Choose CLAUDE.md when:**
- Using Claude Code exclusively
- Need import functionality
- Want hierarchical memory (user + project levels)
- Team all uses Claude Code

**Choose AGENTS.md when:**
- Team uses multiple AI tools (Cursor, Copilot, Codex, etc.)
- Want cross-tool compatibility
- Contributing to open source
