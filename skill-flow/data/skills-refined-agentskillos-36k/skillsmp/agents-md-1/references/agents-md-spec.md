# AGENTS.md Specification

AGENTS.md is a standardized file format for AI coding agents, adopted by 60,000+ open source projects.

## Purpose

- "README for AI agents" - structured instructions for AI tools
- Cross-tool compatibility (20+ tools support it)
- Keeps README.md concise for humans

## Supported Tools

- OpenAI Codex
- Google Jules
- Cursor
- Aider
- VS Code (with extensions)
- GitHub Copilot
- And more...

## File Format

Plain Markdown with no special syntax. No required fields - flexibility is a core principle.

## Recommended Sections

```markdown
# AGENTS.md

## Project Overview
[Brief description]

## Setup Commands
[Dependency installation, dev server startup]

## Testing
[How to run tests]

## Code Style
[Coding conventions - though prefer linters]

## PR/Commit Conventions
[Branch naming, commit message format]

## Security Considerations
[Sensitive files, forbidden operations]
```

## Hierarchical Priority

In monorepos, the nearest AGENTS.md takes priority:

```
monorepo/
├── AGENTS.md              ← Root level (lowest priority)
├── packages/
│   ├── frontend/
│   │   └── AGENTS.md      ← Package level (higher priority)
│   └── backend/
│       └── AGENTS.md      ← Package level (higher priority)
```

## Key Differences from CLAUDE.md

| Feature | AGENTS.md | CLAUDE.md |
|---------|-----------|-----------|
| Import syntax | ❌ | ✅ (`@file`) |
| Hierarchical memory | ❌ | ✅ (4 levels) |
| Memory commands | ❌ | ✅ (`#`, `/memory`) |
| Tool compatibility | 20+ tools | Claude Code only |
| Adoption | 60,000+ projects | Claude Code users |

## When to Use AGENTS.md

- Open source projects (broadest compatibility)
- Teams using multiple AI tools
- Projects where contributors may use different AI assistants
- When simplicity is preferred over Claude-specific features

## Migration

### From CLAUDE.md to AGENTS.md

1. Remove `@import` syntax - inline or link to files instead
2. Rename file to `AGENTS.md`
3. Content structure can remain the same

### From AGENTS.md to CLAUDE.md

1. Rename file to `CLAUDE.md`
2. Optionally add `@imports` for referenced docs
3. Consider using hierarchical memory for personal preferences
