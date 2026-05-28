---
name: ralph-prd
description: Use this skill to generate structured `prd.json` files for autonomous agent loops when planning bulk tasks, migrations, or any work that can be decomposed into independent, verifiable items.
---

# Skill body

Generate `prd.json` files that define scoped work items for autonomous agent execution. Each item includes explicit completion criteria and verification steps.

## When to Use

- Batch migrations (API changes, library upgrades, lint fixes)
- Large-scale refactoring across many files
- Any task that can be decomposed into independent, verifiable units
- Work that benefits from having "done" explicitly defined

## PRD Structure

```json
{
  "instructions": "<markdown with context, examples, constraints>",
  "items": [
    {
      "id": "<unique identifier>",
      "category": "<task category>",
      "description": "<what needs to be done>",
      "file": "<target file path>",
      "steps": [
        "<action step>",
        "<verification step>"
      ],
      "passes": false,
      "skipped": null
    }
  ]
}
```

### Field Reference

| Field | Purpose |
|-------|---------|
| `instructions` | Markdown embedded in PRD - transformation examples, documentation links, constraints |
| `id` | Unique identifier (typically file path or task name) |
| `category` | Groups related items |
| `description` | Human-readable summary |
| `steps` | Actions + verification commands |
| `passes` | `false` initially, `true` when complete |
| `skipped` | `null` or `"<reason>"` if task cannot be completed |

## Generation Workflow

```
PRD Generation Progress:
- [ ] Step 1: Define scope (what files/items are affected?)
- [ ] Step 2: Gather input data (lint output, file list, API changes)
- [ ] Step 3: Design item granularity (per-file, per-error, per-component?)
- [ ] Step 4: Define verification steps (type-check, tests, lint)
- [ ] Step 5: Write instructions (examples, constraints, skip conditions)
- [ ] Step 6: Generate items (script or manual)
- [ ] Step 7: Review sample items
```

## Clarifying Questions

Before generating, resolve these with the user:

### Granularity
- Should items be per-file, per-error, or per-component?
- Trade-off: fewer items = less overhead, more items = finer progress tracking

### Verification Steps  
- What commands confirm completion?
- Should it include type-checks, tests, linting, or builds?
- Which tests are relevant - related test file only, or broader?

### Instructions Content
- What context does the executing agent need?
- What examples or constraints should be included?