---
name: memory-reference
description: Claude Code memory (CLAUDE.md) configuration reference. Use when setting up project memory, understanding memory hierarchy, or configuring persistent instructions.
---

# Claude Code Memory Reference

Memory files (CLAUDE.md) provide persistent instructions that Claude loads every session.

## Memory Hierarchy (Priority Order)

| Priority | Location | Purpose | Shared With |
|----------|----------|---------|-------------|
| 1 (highest) | Enterprise policy | Organization rules | All users |
| 2 | `./CLAUDE.md` | Project instructions | Team via git |
| 3 | `./.claude/CLAUDE.md` | Alternative project location | Team via git |
| 4 | `./.claude/rules/*.md` | Modular project rules | Team via git |
| 5 | `~/.claude/CLAUDE.md` | Personal preferences | Just you |
| 6 | `./CLAUDE.local.md` | Personal project prefs | Just you (gitignored) |

## File Locations

```
/Library/Application Support/ClaudeCode/CLAUDE.md  # Enterprise (macOS)
./CLAUDE.md                                         # Project root
./.claude/CLAUDE.md                                 # Alternative project
./.claude/rules/*.md                                # Modular rules
~/.claude/CLAUDE.md                                 # User global
~/.claude/rules/*.md                                # User modular rules
./CLAUDE.local.md                                   # Project personal
```

## Basic CLAUDE.md

```markdown
# Project Instructions

## Code Style
- Use TypeScript for all new files
- Prefer functional components in React
- Use ESLint and Prettier for formatting

## Commands
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`

## Architecture
- Components in `src/components/`
- API routes in `src/api/`
- Types in `src/types/`
```

## Importing Files

Use `@path/to/file` to import other files:

```markdown
# Project Memory

See @README.md for project overview.
See @package.json for available commands.

## Team Guidelines
@docs/guidelines.md

## Personal Preferences
@~/.claude/my-prefs.md
```

Import rules:
- Relative and absolute paths allowed
- Max depth: 5 hops
- Not evaluated in code blocks

## Modular Rules (.claude/rules/)

Organize rules by topic:

```
.claude/rules/
├── code-style.md
├── testing.md
├── security.md
└── api-design.md
```

### Path-Specific Rules

Use frontmatter to scope rules:

```markdown
---
paths: src/api/**/*.ts
---

# API Development Rules

- All endpoints must validate input
- Use consistent error response format
- Document with OpenAPI comments
```

### Glob Patterns

| Pattern | Matches |
|---------|---------|
| `**/*.ts` | All TypeScript files |
| `src/**/*` | All files under src/ |
| `*.md` | Markdown in root |
| `src/components/*.tsx` | React components |
| `src/**/*.{ts,tsx}` | TS and TSX in src/ |

## Memory Commands

| Command | Description |
|---------|-------------|
| `/memory` | View/edit memory files |
| `/init` | Bootstrap CLAUDE.md |
| `/memory user` | Edit user memory |
| `/memory project` | Edit project memory |

## Best Practices

### Be Specific
```markdown
# Good
- Use 2-space indentation
- Name React components with PascalCase

# Bad
- Format code properly
- Use good naming
```

### Use Structure
```markdown
# Build Commands
- `npm run build` - Production build
- `npm run dev` - Development server

# Test Commands
- `npm test` - Run all tests
- `npm test:watch` - Watch mode
```

### Keep Updated
Review and update memory as project evolves.

## Example: Full Project Memory

```markdown
# MyApp Project

## Overview
React + TypeScript web application with Express backend.

## Quick Commands
- Dev: `npm run dev`
- Test: `npm test`
- Build: `npm run build`
- Deploy: `npm run deploy`

## Code Style
- TypeScript strict mode
- Functional React components
- CSS Modules for styling
- Jest for testing

## Architecture
- `src/client/` - React frontend
- `src/server/` - Express backend
- `src/shared/` - Shared types

## Common Patterns
- Use `useQuery` for API calls
- Validate props with Zod schemas
- Log errors to Sentry

## Git Workflow
- Feature branches from `main`
- Squash merge PRs
- Conventional commit messages
```

## Symlinks

Share rules across projects:

```bash
# Symlink shared rules
ln -s ~/shared-rules .claude/rules/shared

# Symlink specific file
ln -s ~/company-security.md .claude/rules/security.md
```

Symlinks are followed during loading.

## Debugging

```bash
# View loaded memory
/memory

# Check what files are loaded
# Memory command shows all active files
```

---

For complete documentation, see:
- [memory-full.md](memory-full.md) - Complete memory reference
