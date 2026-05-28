---
name: code-refactoring
description: Expert refactoring orchestrator for large-scale code changes with change tracking. Use when (1) renaming/moving files or directories, (2) restructuring database schemas, (3) refactoring APIs or Edge Functions, (4) splitting/merging components, (5) querying what changed in a system ("what critical changes were made to subscription system?"). Maintains changelog for docs-updater sync.
---

# Code Refactoring Wizard

Orchestrate large-scale refactoring with change tracking. Uses `code-wizard` for discovery.

## Context Files

For structure and conventions, read from `Docs/context/`:
- `Docs/context/conventions.md` - Architecture rules, refactor guidelines
- `Docs/context/repo-structure.md` - Where to place files
- `Docs/context/packages-map.md` - Package boundaries

## Changelog Location

**All significant changes logged to:** `Docs/ai/CHANGELOG.md`

This file is monitored by `docs-updater` skill for documentation sync.

## Change Categories

| Category | Tag | Example |
|----------|-----|---------|
| Schema | `[SCHEMA]` | New table, column rename, migration |
| Structure | `[STRUCTURE]` | File/folder move, directory reorganization |
| API | `[API]` | RPC signature change, Edge Function update |
| Breaking | `[BREAKING]` | Removed feature, renamed export |
| Component | `[COMPONENT]` | React component split/merge |
| Dependency | `[DEPS]` | Package upgrade, new import |

## Workflow

### 1. Discover (use code-wizard)

```
/code-wizard "find all usages of ai_plan_quotas table"
/code-wizard "where is subscription logic implemented"
```

### 2. Plan

- Current state → Target state
- Migration path
- Rollback strategy
- Affected files list

### 3. Execute

Order: Database → Backend → Frontend → Tests

### 4. Log to CHANGELOG.md

```markdown
## 2026-01-08 - Subscription System Refactor

### [SCHEMA] Replace per-feature quotas with token pools

**Before:**
- `ai_plan_quotas` table (40+ rows)
- Per-feature token limits

**After:**
- `subscription_plans` table
- `token_pools` table
- `ai_operations` table

**Impact:**
- Files: 15 | Migration: Yes | Breaking: Yes

**Related:** #20260108_token_pool_system
```

### 5. Sync Docs

```
/docs-updater "sync changelog to API docs"
```

## Query Changes

To answer "what changed in X system":

1. Read `Docs/ai/CHANGELOG.md`
2. Filter by date/category/system
3. Summarize

Example response:
```
## Subscription System Changes (Jan 2026)

1. [SCHEMA] Token pool migration (Jan 8)
   - Replaced ai_plan_quotas → unified token system
   - 15 files, breaking

2. [API] New check_token_balance RPC (Jan 8)
   - User token balance endpoint
   - Non-breaking
```

## Related Skills

| Skill | Use For |
|-------|---------|
| `code-wizard` | Find code before refactoring |
| `docs-updater` | Sync docs after changelog |
| `supabase-migration-writer` | Database migrations |
| `admin-panel-builder` | Admin page refactoring |

## References

- **Refactoring patterns**: See [references/patterns.md](references/patterns.md)
- **Changelog examples**: See [references/changelog-examples.md](references/changelog-examples.md)
