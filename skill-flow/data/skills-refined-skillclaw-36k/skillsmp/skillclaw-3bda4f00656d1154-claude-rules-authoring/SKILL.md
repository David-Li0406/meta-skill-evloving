---
name: claude-rules-authoring
description: Use this skill when creating reusable rule files for project conventions in the `.claude/rules/` directory.
---

# Skill body

Create reusable instruction files in `.claude/rules/` for project conventions.

## Rules vs CLAUDE.md

| Aspect | CLAUDE.md | .claude/rules/ |
|--------|-----------|----------------|
| Loading | Automatic at session start | On-demand via reference |
| Content | Project setup, key commands | Reusable conventions |
| Size | Concise (~200-500 lines) | Can be detailed |
| Scope | This specific project | Patterns across files |

**Put in CLAUDE.md**: One-off instructions, project-specific commands, key file locations.

**Put in rules/**: Formatting conventions, architecture patterns, workflow guidelines, commit standards.

## File Conventions

### Naming

- **UPPERCASE.md** - All caps with `.md` extension
- **Topic-focused** - One concern per file
- **Kebab-case for multi-word** - `API-PATTERNS.md`, `CODE-REVIEW.md`

**Good**: `FORMATTING.md`, `TESTING.md`, `COMMITS.md`  
**Bad**: `formatting.md`, `MyRules.md`, `everything.md`

### Structure

```
.claude/rules/
├── FORMATTING.md      # Code style, output conventions
├── TESTING.md         # Test patterns, coverage requirements
├── COMMITS.md         # Commit message format, PR conventions
├── ARCHITECTURE.md    # Component structure, file organization
└── SECURITY.md        # Security guidelines, auth patterns
```

## Content Structure

Rules files should be scannable and actionable:

```markdown
# Topic Name

Brief description of what this covers.

## Section 1

| Pattern | Example | Notes |
|---------|---------|-------|
| ... | ... | ... |

## Section 2

**Do:**
- Specific guideline

**Don't:**
- Anti-pattern to avoid

## Examples

{ concrete examples }
```

## Referencing Rules

### From CLAUDE.md

Reference rules explicitly - they're not auto-loaded:

```markdown
# CLAUDE.md

## Code Style
Follow `.claude/rules/FORMATTING.md` for all code conventions.

## Testing
See `.claude/rules/TESTING.md` for TDD patterns.
```

### Cross-file References

Use `@` syntax to include content from other files:

```markdown
# .claude/rules/FORMATTING.md

@../../baselayer/shared/rules/FORMATTING.md
```

This keeps rules DRY by pointing to authoritative sources.