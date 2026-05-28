---
name: beans-issue-tracking
description: Tracks work with beans CLI for audit trails and agent memory. Use when starting tasks, finding next work, or recording discovered issues during implementation.
---

## When to Use Beans

Use Beans for all non-trivial work (3+ steps). Skip for trivial single-step fixes.

## Finding Work

```bash
beans list --ready              # Not blocked, ready to start
beans show <id>                 # Full details
beans list -p high,critical -t bug,feature -s todo
beans list -S "search term"
```

## Types & Statuses

**Types:** `milestone` (releases) → `epic` (large initiatives) → `feature` (capabilities) → `task`/`bug` (units of work)

**Statuses:** `draft` → `todo` → `in-progress` → `completed` (or `scrapped` with reason)

## Task Granularity

**Critical:** Do NOT over-split tasks. Each bean should be a complete, logical unit of work.

- **Wrong:** 5 beans for "add validation" → "write test" → "update docs" → "refactor" → "cleanup"
- **Right:** 1 bean with checklist covering all steps

Over-splitting forces excessive CLI calls to gather fragmented context. Prefer 1-2 mid-sized beans over 5+ tiny ones.

## Lifecycle

### Starting
```bash
beans create "Title" -t <type> -s in-progress
```

### During Work
Update checklist items `- [x]` immediately after completing each step.

### Completing
```bash
beans update <id> -s completed    # Add "## Summary of Changes" section
beans update <id> -s scrapped     # Add "## Reasons for Scrapping" section
```

## Discovered Work

Create beans immediately when new tasks are identified:
```bash
beans create "Title" --tag discovered -t task -s todo
beans create "Subtask" -t task --parent <current-id> --tag discovered
```

## Relationships

Use `--parent <id>` for hierarchy, `--blocking <id>` for dependencies.

```bash
beans list --is-blocked      # Cannot start (blocked by others)
beans list --has-blocking    # Blocks others
beans list --ready           # Not blocked, ready to start
```

## Tags

Use for cross-cutting concerns: `discovered`, `frontend`, `backend`, `security`, `performance`, `docs`

```bash
beans create "Fix XSS" -t bug --tag security --tag backend
```

## CLI Reference

See `reference/cli.md` for full command reference and recovery steps.
