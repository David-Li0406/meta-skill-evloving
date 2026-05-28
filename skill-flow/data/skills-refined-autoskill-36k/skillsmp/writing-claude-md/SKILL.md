---
name: writing-claude-md
description: "Use when creating or updating CLAUDE.md files at any level (global, project, folder). Covers inheritance rules and token budgets."
---

# Writing CLAUDE.md Files

## Overview

CLAUDE.md files provide context at different scopes. They follow hierarchical inheritance: global -> project -> folder.

## When to Create

**Create CLAUDE.md when:**
- Project has specific conventions
- Folder has specialized context
- Team patterns need documentation
- Repeated instructions should be automated

**Levels:**
- `~/.claude/CLAUDE.md` - Global (all projects)
- `project/CLAUDE.md` - Project-level
- `project/folder/CLAUDE.md` - Folder-specific

## Structure Template

```markdown
# [Project/Folder Name]

## Overview
[Brief description of scope]

## Key Conventions
[Most important rules - loaded every session]

## File Patterns
[Naming, organization, structure]

## Common Tasks
[Frequent operations with guidance]

## Dependencies
[Key libraries, versions, integrations]

## Anti-Patterns
[What to avoid in this context]
```

## Quality Checklist

- [ ] Scope clearly defined (global/project/folder)
- [ ] Under 500 tokens for always-loaded sections
- [ ] Most critical rules first (may be truncated)
- [ ] Folder detection patterns if folder-specific
- [ ] No duplication of parent-level content
- [ ] Anti-patterns documented
- [ ] Tested with real prompts

## Inheritance Rules

```
Global CLAUDE.md (always loaded)
    |
    v
Project CLAUDE.md (loaded in project)
    |
    v
Folder CLAUDE.md (loaded in folder context)
```

**Child overrides parent** for conflicting rules.
**Child extends parent** for non-conflicting rules.

## Token Budget Guidelines

| Level | Target | Max |
|-------|--------|-----|
| Global | 200 | 500 |
| Project | 500 | 1500 |
| Folder | 300 | 800 |

**Tips:**
- Lead with most critical content
- Use bullet points over prose
- Reference skills instead of duplicating
- Move verbose content to referenced files

## Examples

**Good Project CLAUDE.md:**
```markdown
# MyApp

## Key Conventions
- TypeScript strict mode
- React Server Components by default
- Supabase for backend

## File Patterns
- Components: src/components/{name}/{name}.tsx
- Server actions: src/actions/{domain}.ts
- Database: supabase/migrations/*.sql

## Common Tasks
- New component: Use shadcn/ui, check existing patterns
- Database change: Create migration, test locally first

## Anti-Patterns
- No client-side data fetching (use RSC)
- No raw SQL (use Supabase client)
```

**Bad CLAUDE.md:**
```markdown
# Instructions

This is a project. It uses various technologies.
Please be careful and write good code.
Follow best practices and industry standards.
```
(Vague, no actionable content, wastes tokens)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too verbose | Trim to token budget |
| Duplicates parent | Only add new/override content |
| Generic advice | Project-specific conventions only |
| Critical content buried | Lead with most important rules |
| No anti-patterns | Document what to avoid |
| Not tested | Verify with real prompts |
