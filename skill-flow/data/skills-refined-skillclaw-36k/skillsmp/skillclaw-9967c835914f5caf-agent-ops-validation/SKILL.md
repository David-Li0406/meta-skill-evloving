---
name: agent-ops-validation
description: Use this skill before committing changes or declaring work complete to ensure all quality gates pass through a series of validation checks.
---

# Validation Workflow

**Works with or without `aoc` CLI installed.** Issue tracking can be done via direct file editing.

## Purpose

Ensure all quality gates pass before committing changes or declaring work complete. This skill consolidates all validation checks into a single, consistent procedure.

## Validation Commands (from constitution)

```bash
# Example commands — read actual commands from .agent/constitution.md
build: npm run build          # or: uv run python -m build
lint: npm run lint            # or: uv run ruff check .
test: npm run test            # or: uv run pytest
format: npm run format        # or: uv run ruff format .
```

## Issue Operations After Validation (File-Based — Default)

| Operation | How to Do It |
|-----------|--------------|
| Create regression issue | Append to `.agent/issues/high.md` with BUG type |
| Update issue status | Edit `status:` field directly in priority file |
| List blocking issues | Search priority files for `status: blocked` |

### Example: Post-Validation Issue Creation (File-Based)

1. Read `.agent/issues/.counter`, increment, write back.
2. Generate new ID: `BUG-{counter}@{hash}`.
3. Append issue to `.agent/issues/high.md`:
   ```yaml
   ## BUG-NNNN@HHHHHH — New test failure: UserService.login

   id: BUG-NNNN@HHHHHH
   type: BUG
   status: todo
   priority: high
   description: Regression detected during validation

   ### Log
   - YYYY-MM-DD: Created from validation failure
   ```

## CLI Integration (when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`, these commands provide convenience shortcuts:

| Operation | CLI Command |
|-----------|-------------|
| Create regression issue | `aoc issues create --type BUG --priority high --title "..."` |
| Update issue status | `aoc issues update <ID> --status done` |
| List blocking issues | `aoc issues list --status blocked` |

## API Detection

**Before running validation, check if project contains APIs:**

```yaml
api_indicators:
  - OpenAPI/Swagger spec (openapi.yaml, swagger.json, openapi.json)
  - API framework patterns
```