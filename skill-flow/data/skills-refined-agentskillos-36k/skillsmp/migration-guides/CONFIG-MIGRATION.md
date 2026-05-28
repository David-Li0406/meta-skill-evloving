# Configuration Migration Guide

Detailed guide for migrating configurations, settings, rules, and customizations to Claude Code.

## Configuration Overview

### Claude Code Configuration Files

| File | Scope | Purpose |
|------|-------|---------|
| `~/.claude/settings.json` | User global | Personal settings across all projects |
| `.claude/settings.json` | Project | Shared team settings (committed) |
| `.claude/settings.local.json` | Local project | Personal overrides (gitignored) |
| `CLAUDE.md` | Project | Context and instructions |
| `~/.claude/CLAUDE.md` | User global | Personal context for all projects |
| `.claude/commands/*.md` | Project | Custom slash commands |
| `.claude/hooks/*` | Project | Hook scripts |

### Configuration Precedence

```
Enterprise Policy (highest)
    |
    v
~/.claude/settings.json (user global)
    |
    v
.claude/settings.json (project shared)
    |
    v
.claude/settings.local.json (local overrides)
    |
    v
CLI flags (lowest, but immediate override)
```

## Migrating from Other Tools

### From .cursorrules

Cursor's `.cursorrules` maps to Claude Code's `CLAUDE.md`.

**Source** `.cursorrules`:
```
You are an expert TypeScript developer.

Project Structure:
- src/ contains all source code
- tests/ contains test files
- Use Vitest for testing

Code Style:
- Use functional components
- Prefer const over let
- Always add JSDoc comments
- Use TypeScript strict mode

Naming:
- camelCase for variables
- PascalCase for components
- kebab-case for files
```

**Target** `CLAUDE.md`:
```markdown
# Project Configuration

## Tech Stack
- TypeScript (strict mode)
- React with functional components
- Vitest for testing

## Project Structure
- `src/` - Source code
- `tests/` - Test files

## Code Conventions

### Style
- Use functional components exclusively
- Prefer `const` over `let`
- Always add JSDoc comments
- TypeScript strict mode enabled

### Naming Conventions
- Variables: camelCase
- Components: PascalCase
- Files: kebab-case

## Key Commands
```bash
bun test        # Run tests
bun run build   # Build project
bun run lint    # Lint code
```
```

### From .github/copilot-instructions.md

GitHub Copilot instructions migrate directly to `CLAUDE.md`.

**Source** `.github/copilot-instructions.md`:
```markdown
## Context
This is a Next.js 14 application using the App Router.

## Guidelines
- Use Server Components by default
- Client Components only when needed
- Use Tailwind CSS for styling
- Follow the Next.js file conventions

## Testing
- Use Playwright for E2E tests
- Use Jest for unit tests
```

**Target** `CLAUDE.md`:
```markdown
# Next.js Application

## Framework
- Next.js 14 with App Router
- Server Components by default
- Client Components when interactivity needed

## Styling
- Tailwind CSS for all styling
- Follow utility-first approach

## Testing
- E2E: Playwright (`tests/e2e/`)
- Unit: Jest (`tests/unit/`)

## File Conventions
Follow Next.js App Router conventions:
- `app/` - Routes and layouts
- `components/` - Reusable components
- `lib/` - Utilities and helpers
```

### From .sourcegraph/cody.json

Cody configuration migrates to settings.json and CLAUDE.md.

**Source** `.sourcegraph/cody.json`:
```json
{
  "chat": {
    "preInstruction": "Always respond in TypeScript examples",
    "contextFiles": ["README.md", "docs/architecture.md"]
  },
  "autocomplete": {
    "enabled": true
  },
  "commands": {
    "explain": {
      "prompt": "Explain this code in detail"
    },
    "test": {
      "prompt": "Generate unit tests for this code"
    }
  }
}
```

**Target** `CLAUDE.md`:
```markdown
# Project Context

When providing examples, use TypeScript.

## Key Documentation
- README.md - Project overview
- docs/architecture.md - System architecture

## Available Commands
- `/explain` - Explain code in detail
- `/test` - Generate unit tests
```

**Target** `.claude/commands/explain.md`:
```markdown
---
description: Explain selected code in detail
---
Explain this code thoroughly, including:
- Purpose and functionality
- Key algorithms or patterns used
- Dependencies and side effects
- Potential improvements
```

**Target** `.claude/commands/test.md`:
```markdown
---
description: Generate unit tests for code
---
Generate comprehensive unit tests for this code:
- Test happy path
- Test edge cases
- Test error handling
- Use the project's testing framework
```

### From .continue/config.json

Continue.dev configuration migrates to multiple Claude Code files.

**Source** `.continue/config.json`:
```json
{
  "models": [...],
  "slashCommands": [
    {
      "name": "review",
      "description": "Review code for issues",
      "prompt": "Review this code for bugs, security issues, and improvements"
    }
  ],
  "contextProviders": [
    {
      "name": "docs",
      "params": {
        "sites": ["https://docs.example.com"]
      }
    }
  ],
  "customCommands": [
    {
      "name": "deploy-check",
      "prompt": "Check if this code is ready for deployment"
    }
  ]
}
```

**Target** `.claude/commands/review.md`:
```markdown
---
description: Review code for issues
---
Review this code for:
- Potential bugs
- Security vulnerabilities
- Performance issues
- Code style violations
- Improvement suggestions
```

**Target** `.claude/commands/deploy-check.md`:
```markdown
---
description: Check deployment readiness
---
Analyze if this code is ready for deployment:
- All tests passing?
- No console.log statements?
- Error handling complete?
- Documentation updated?
- Breaking changes documented?
```

**Target** `.claude/settings.json` (for docs):
```json
{
  "mcpServers": {
    "docs": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "docs.example.com"
      }
    }
  }
}
```

### From .aider.conf.yml

Aider configuration migrates to settings.json.

**Source** `.aider.conf.yml`:
```yaml
model: claude-3-opus
auto-commits: true
attribute-author: false
attribute-committer: false
gitignore: true
pretty: true
stream: true
edit-format: diff
```

**Target** `.claude/settings.json`:
```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep", "Write", "Edit"],
    "deny": []
  }
}
```

**Target** `CLAUDE.md` (for git behavior):
```markdown
# Git Workflow

## Commit Conventions
- Create commits when explicitly requested
- Use descriptive commit messages
- Follow conventional commits format

## Note
Unlike Aider, Claude Code does not auto-commit.
Request commits explicitly: "commit these changes"
```

## Migrating Settings

### Permission Settings

**Old Format** (pre-2.0):
```json
{
  "allowedTools": ["Read", "Write", "Edit"],
  "blockedTools": ["Bash"]
}
```

**New Format** (2.0+):
```json
{
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Glob",
      "Grep"
    ],
    "deny": [
      "Bash(rm -rf *)"
    ]
  }
}
```

### Hook Configuration

**Old Format** (pre-2.0):
```json
{
  "hooks": {
    "beforeWrite": "npm run format",
    "afterWrite": "npm run lint"
  }
}
```

**New Format** (2.0+):
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'About to write file'"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm run format -- \"$CLAUDE_PROJECT_DIR\""
          }
        ]
      }
    ]
  }
}
```

### MCP Server Configuration

**Basic Configuration**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

## Migrating Custom Commands

### Creating Command Files

Location: `.claude/commands/`

**Basic Command**:
```markdown
---
description: Short description for command list
---
Detailed instructions for what Claude should do when this command is invoked.
```

**Command with Arguments**:
```markdown
---
description: Generate tests for a specific file
---
Generate comprehensive tests for the file: $ARGUMENTS

Include:
- Unit tests for each function
- Integration tests where appropriate
- Edge case coverage
- Mock external dependencies
```

### Migrating from Other Tools

| Source | Pattern | Claude Code Location |
|--------|---------|---------------------|
| Cursor commands | In-IDE | `.claude/commands/*.md` |
| Cody commands | JSON config | `.claude/commands/*.md` |
| Continue commands | JSON config | `.claude/commands/*.md` |
| VS Code tasks | tasks.json | `.claude/commands/*.md` or hooks |

## Migrating Hooks and Automation

### ESLint/Prettier Integration

**Approach 1: PostToolUse Hook**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx eslint --fix \"$CHANGED_FILE\" && npx prettier --write \"$CHANGED_FILE\""
          }
        ]
      }
    ]
  }
}
```

**Approach 2: Hook Script**

`.claude/hooks/format.sh`:
```bash
#!/bin/bash
# Read input JSON
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [ -n "$FILE" ]; then
  # Run formatters
  npx eslint --fix "$FILE" 2>/dev/null
  npx prettier --write "$FILE" 2>/dev/null
fi

exit 0
```

### Pre-commit Hook Integration

Claude Code hooks are different from git pre-commit hooks. For git integration:

**Option 1: Use existing pre-commit**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "git add \"$CHANGED_FILE\" && npx lint-staged"
          }
        ]
      }
    ]
  }
}
```

**Option 2: Dedicated formatting hook**
Keep pre-commit for git, use Claude hooks for immediate formatting.

### CI/CD Integration

Migrate CI checks to validation hooks:

**GitHub Actions** (keep for CI):
```yaml
name: Lint
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run lint
```

**Claude Hook** (for development):
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint:file -- \"$CHANGED_FILE\""
          }
        ]
      }
    ]
  }
}
```

## Team Configuration Migration

### Shared Settings

Create `.claude/settings.json` for team:
```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep"],
    "deny": []
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bun run format"
          }
        ]
      }
    ]
  }
}
```

### .gitignore Updates

```gitignore
# Claude Code
.claude/settings.local.json
.claude/cache/
```

### Team CLAUDE.md Template

```markdown
# Project Name

## Quick Start
```bash
bun install
bun dev
```

## Tech Stack
- [List technologies]

## Conventions
- [Code style rules]
- [Naming conventions]
- [File organization]

## Key Files
- `src/config.ts` - Configuration
- `src/lib/` - Shared utilities
- `tests/` - Test files

## Commands
```bash
bun test        # Run tests
bun run build   # Build for production
bun run lint    # Lint code
```

## Team Notes
- [Important context for Claude]
```

## Validation After Migration

### Configuration Validation

```bash
# Check settings loaded
claude config list

# Verify hooks
# Start claude and type /hooks

# Test custom commands
# Type /command-name
```

### Functionality Checklist

- [ ] CLAUDE.md context loads correctly
- [ ] Custom commands appear in / menu
- [ ] Hooks execute on file changes
- [ ] Permissions work as expected
- [ ] MCP servers connect (if configured)
- [ ] Team members can use shared config

### Migration Verification Script

```bash
#!/bin/bash
echo "Verifying Claude Code configuration..."

# Check settings files exist
[ -f ".claude/settings.json" ] && echo "Project settings: OK" || echo "Project settings: MISSING"
[ -f "CLAUDE.md" ] && echo "CLAUDE.md: OK" || echo "CLAUDE.md: MISSING"

# Check commands directory
if [ -d ".claude/commands" ]; then
  CMD_COUNT=$(ls .claude/commands/*.md 2>/dev/null | wc -l)
  echo "Custom commands: $CMD_COUNT found"
else
  echo "Custom commands: None"
fi

# Check hooks
if [ -d ".claude/hooks" ]; then
  HOOK_COUNT=$(ls .claude/hooks/* 2>/dev/null | wc -l)
  echo "Hook scripts: $HOOK_COUNT found"
else
  echo "Hook scripts: None"
fi

# Verify Claude Code installation
if command -v claude &> /dev/null; then
  VERSION=$(claude --version)
  echo "Claude Code version: $VERSION"
else
  echo "Claude Code: NOT INSTALLED"
fi

echo "Verification complete."
```

## Troubleshooting Migration

| Issue | Cause | Solution |
|-------|-------|----------|
| Context not loading | CLAUDE.md not found | Check file location and name |
| Commands not showing | Wrong directory | Use `.claude/commands/` |
| Hooks not firing | JSON syntax error | Validate settings.json |
| Settings ignored | Precedence conflict | Check all settings files |
| MCP not connecting | Config error | Verify command and args |

### Debug Configuration

```bash
# Run with debug output
claude --debug

# Check which config is loaded
claude config list

# Verify hook registration
# In claude, type /hooks
```
