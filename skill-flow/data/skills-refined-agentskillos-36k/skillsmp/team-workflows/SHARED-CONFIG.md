# Sharing Configurations Across Team

Deep dive on sharing Claude Code configurations through version control.

## What to Share

### CLAUDE.md (Required)

The primary configuration file. Should include:

```markdown
# Project Name

Short description of the project.

## Commands

Essential commands every team member needs:

```bash
bun install          # Install dependencies
bun dev              # Start development server
bun test             # Run tests
bun build            # Build for production
bun lint             # Check code style
bun typecheck        # TypeScript check
```

## Tech Stack

- **Runtime:** Bun
- **Framework:** React + Hono
- **Database:** PostgreSQL + Drizzle
- **Testing:** Vitest + Playwright

## Architecture

Brief overview of key directories:

```
src/
  routes/      # API endpoints
  components/  # React components
  services/    # Business logic
  db/          # Database layer
```

## Conventions

- Use absolute imports with `@/` prefix
- Components in PascalCase, files in kebab-case
- Tests colocated with source files
```

### Rules Directory (.claude/rules/)

Share file-specific instructions:

```
.claude/rules/
  code-style.md        # TypeScript/React conventions
  testing.md           # Test writing standards
  api-design.md        # API endpoint patterns
  database.md          # Database query patterns
  security.md          # Security requirements
```

#### Example: testing.md

```yaml
---
globs: ["**/*.test.ts", "**/*.spec.ts", "**/*.test.tsx"]
description: Testing conventions and patterns
alwaysApply: false
---

# Testing Standards

## Unit Tests
- One assertion per test when possible
- Use descriptive test names: `should [action] when [condition]`
- Mock external dependencies

## Integration Tests
- Test full request/response cycle
- Use test database with fixtures
- Clean up after each test

## E2E Tests
- Use data-testid for selectors
- Test critical user flows
- Run in CI before merge

## Coverage Requirements
- Minimum 80% line coverage
- 100% for critical paths (auth, payments)
```

### Settings File (.claude/settings.json)

Share non-sensitive tool settings:

```json
{
  "permissions": {
    "allow": [
      "Bash(bun:*)",
      "Bash(git:*)",
      "Bash(docker:*)",
      "mcp__database__query"
    ],
    "deny": [
      "Bash(rm -rf /)",
      "Bash(*--force*)"
    ]
  }
}
```

**Warning:** Never include API keys or secrets in settings.json. Those belong in personal config or environment variables.

### Team Skills (.claude/skills/)

Share project-specific workflows:

```
.claude/skills/
  deploy/
    SKILL.md           # Deployment procedures
  release/
    SKILL.md           # Release workflow
  migration/
    SKILL.md           # Database migration process
```

## Git Configuration

### .gitignore

Exclude personal configurations:

```gitignore
# Personal Claude configurations (not shared)
.claude/settings.local.json
.claude/.credentials

# Keep these (shared with team)
# !CLAUDE.md
# !.claude/rules/
# !.claude/skills/
# !.claude/settings.json
```

### .gitattributes

Ensure consistent line endings:

```gitattributes
CLAUDE.md text eol=lf
.claude/**/*.md text eol=lf
.claude/**/*.json text eol=lf
```

## Configuration Merging

Claude Code merges configurations in order:

```
~/.claude/CLAUDE.md      (personal - lowest priority)
      |
      v
./CLAUDE.md              (project root)
      |
      v
./.claude/CLAUDE.md      (project .claude dir)
      |
      v
./.claude/rules/*.md     (conditional - highest priority)
```

### Handling Conflicts

When personal and project configs conflict, project wins:

**Personal (~/.claude/CLAUDE.md):**
```markdown
- Use 4-space indentation
- Prefer forEach over for-loops
```

**Project (./CLAUDE.md):**
```markdown
- Use 2-space indentation
- Prefer for-loops over forEach
```

**Result:** Project settings apply (2-space, for-loops).

### Override Pattern

For must-follow team rules, add explicit overrides:

```markdown
## Code Style (REQUIRED - overrides personal preferences)

These settings are mandatory for this project:
- 2-space indentation (no exceptions)
- for-loops over forEach (team standard)
- Single quotes (Prettier enforced)
```

## Multi-Environment Setup

### Development vs Production

Create environment-specific rules:

```
.claude/rules/
  dev-only.md            # Development shortcuts
  prod-safety.md         # Production safeguards
```

**dev-only.md:**
```yaml
---
globs: ["**/*"]
description: Development environment helpers
alwaysApply: false
---

# Development Shortcuts

- Use `bun dev` for hot reload
- Database: localhost:5432
- Skip SSL verification for local
```

**prod-safety.md:**
```yaml
---
globs: ["**/deploy/**", "**/ci/**"]
description: Production safety rules
alwaysApply: true
---

# Production Safety

NEVER:
- Deploy without tests passing
- Run migrations without backup
- Force push to main

ALWAYS:
- Use feature flags for new features
- Have rollback plan ready
- Notify on-call before major changes
```

### Branch-Specific Configs

For different branch conventions:

```markdown
## Branch Conventions

### main
- Protected, no direct pushes
- Requires 2 approvals
- Must pass all CI checks

### develop
- Feature branches merge here
- Requires 1 approval
- Tests must pass

### feature/*
- Branch from develop
- Naming: feature/TICKET-123-description
- Squash merge to develop
```

## Syncing Configurations

### PR Reviews for Config Changes

Treat CLAUDE.md and .claude/ changes like code:

```markdown
## PR Review: Configuration Changes

When reviewing changes to CLAUDE.md or .claude/:

- [ ] Changes align with team discussion
- [ ] No secrets included
- [ ] Glob patterns are correct
- [ ] Instructions are clear and actionable
- [ ] Doesn't conflict with existing rules
```

### Onboarding Sync

New team members should:

1. **Clone repo** - Gets shared configs automatically
2. **Set up personal config** - Create ~/.claude/CLAUDE.md
3. **Verify merging** - Check Claude understands project conventions
4. **Test skills** - Ensure team skills load correctly

### Periodic Review

Schedule regular config reviews:

```markdown
## Configuration Review Checklist (Quarterly)

- [ ] Remove outdated conventions
- [ ] Add newly adopted patterns
- [ ] Update deprecated commands
- [ ] Refresh technology versions
- [ ] Verify rules still apply to current structure
```

## Troubleshooting

### Config Not Loading

**Symptom:** Claude doesn't follow project conventions.

**Check:**
1. File is named exactly `CLAUDE.md` (case sensitive)
2. File is in repo root or `.claude/` directory
3. File is not in `.gitignore`
4. YAML frontmatter (if any) is valid

### Rules Not Matching

**Symptom:** File-specific rules don't apply.

**Check:**
1. Glob pattern matches file path
2. `alwaysApply` is set correctly
3. No syntax errors in YAML frontmatter
4. Rule file is in `.claude/rules/` directory

### Personal Overriding Project

**Symptom:** Personal preferences override team standards.

**Check:**
1. Project file has stronger language (REQUIRED, NEVER, ALWAYS)
2. Project file is being loaded (check file location)
3. No conflicting rules in same file

### Skills Not Found

**Symptom:** Team skills don't appear.

**Check:**
1. Skills are in `.claude/skills/` directory
2. Each skill has `SKILL.md` file
3. YAML frontmatter is valid
4. Skill name follows conventions (lowercase, hyphens)
