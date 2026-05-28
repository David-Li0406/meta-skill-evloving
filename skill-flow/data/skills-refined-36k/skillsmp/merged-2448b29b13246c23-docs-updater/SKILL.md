---
name: docs-updater
description: Use this skill to keep documentation synchronized with code changes in the KR92 Bible Voice project, including API docs, architecture diagrams, and README updates.
---

# Docs Updater

This skill assists in maintaining up-to-date documentation in sync with code changes. It generates concise summaries and ensures all relevant documentation files are updated accordingly.

## Context Files (Read First)

For current state, read from `Docs/context/`:
- `Docs/context/conventions.md` - Documentation standards
- `Docs/context/repo-structure.md` - File organization
- `Docs/ai/CHANGELOG.md` - Recent changes to sync

## Capabilities
- Update API docs when schemas change
- Maintain architecture diagrams
- Sync README with actual features
- Ensure CLAUDE.MD stays current
- Generate documentation from code

## Documentation Files

| File | Purpose | Update When |
|------|---------|-------------|
| `CLAUDE.MD` | AI context doc | Major architecture changes |
| `README.md` | Project overview | Feature/setup changes |
| `Docs/01-PRD.md` | Product requirements | Vision or scope changes |
| `Docs/02-DESIGN.md` | Architecture | System design changes |
| `Docs/03-API.md` | API contracts | Database/RPC/Edge Function changes |
| `Docs/04-DEV-WORKFLOW.md` | Dev process | Workflow or CI/CD changes |
| `Docs/05-DEV.md` | Bible lookups | RPC function changes |
| `Docs/06-AI-ARCHITECTURE.md` | AI system | AI feature or prompt changes |
| `Docs/07-ADMIN-GUIDE.md` | Admin panel | Admin feature changes |
| `Docs/08-WIDGET.md` | Widget docs | Widget API or features changes |

## Quick Summary Format

Every document should start with a **TL;DR section** for human readers:

```markdown
# Document Title

> **TL;DR:** [1-2 sentence summary of what this covers]
>
> **Key Points:**
> - [Most important fact 1]
> - [Most important fact 2]
> - [Most important fact 3]
>
> **Quick Links:** [Table](#tables) | [RPC](#rpc-functions) | [Edge Functions](#edge-functions)
```

## Update Workflow

1. **Identify change type** → Which docs are affected?
2. **Update TL;DR first** → Most critical information
3. **Update details** → Tables, examples, diagrams
4. **Cross-reference** → Update related docs
5. **Update changelog** → If significant
6. **Validate** → Run audit task

## Supported Tasks

| Task | Description | Output |
|------|-------------|--------|
| `audit` | Check all docs for staleness | Markdown report |
| `release-check` | Pre-release documentation verification | Pass/fail + issues |
| `sync-schemas` | Update docs from database schema | Updated doc files |
| `generate-api` | Generate API docs from Edge Functions | API documentation |

## Writing User-Friendly Summaries

### Good Summary (DO)
```markdown
> **TL;DR:** Token-based quota system limits AI usage per subscription plan.
>
> **Key Points:**
> - Users get tokens per 6-hour window (Guest: 50, Pro: 500)
> - Each AI operation costs fixed tokens (Search: 20, Study: 100)
> - Admin can adjust all limits via `/admin/subscriptions`
```

### Bad Summary (DON'T)
```markdown
## Overview
This document describes the token pool subscription system architecture...
```

## Documentation Checklist

When making changes, update docs in this order:

1. **Code Changes**
   - Write code
   - Add JSDoc/comments
   - Add TypeScript types

2. **API Documentation (if applicable)**
   - Update `Docs/03-API.md` with new tables/functions
   - Add request/response examples
   - Document error cases

3. **Architecture Documentation (if applicable)**
   - Update `Docs/02-DESIGN.md` with architectural changes
   - Update diagrams
   - Document new patterns

4. **Usage Documentation**
   - Update relevant guide (`05-DEV.md`, `06-AI-ARCHITECTURE.md`, etc.)
   - Add usage examples
   - Update best practices

5. **User-Facing Documentation**
   - Update `README.md` for feature changes
   - Update `Docs/07-ADMIN-GUIDE.md` for admin features
   - Update `Docs/08-WIDGET.md` for widget changes

6. **AI Context**
   - Update `CLAUDE.MD` for major changes
   - Keep schema reference current
   - Update common patterns

## Automation Opportunities

Create documentation generation scripts:
```typescript
// scripts/generate-api-docs.ts
// Reads database schema and generates API documentation

import { createClient } from '@supabase/supabase-js';

async function generateTableDocs() {
  const supabase = createClient(url, key);

  const { data: tables } = await supabase
    .from('information_schema.tables')
    .select('table_name, table_schema');

  // Generate markdown for each table
  // ...
}
```

## Documentation Quality Standards

### Good Documentation
- Clear and concise
- Includes examples
- Explains the "why" not just "what"
- Up-to-date with code
- Covers error cases
- Uses consistent formatting

### Bad Documentation
- Outdated information
- No examples
- Vague descriptions
- Missing error handling
- Inconsistent formatting
- Missing type information

## References

- **AI changelog guide**: See [references/ai-changelog-guide.md](references/ai-changelog-guide.md)
- **Update examples**: See [references/examples.md](references/examples.md)
- **Doc templates**: See [references/templates.md](references/templates.md)
- **Quality checklist**: See [references/checklist.md](references/checklist.md)