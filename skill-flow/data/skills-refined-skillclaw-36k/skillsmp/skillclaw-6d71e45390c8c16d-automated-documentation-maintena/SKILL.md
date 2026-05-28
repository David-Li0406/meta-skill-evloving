---
name: automated-documentation-maintenance
description: Use this skill when you need to automatically maintain and generate documentation in response to code changes, ensuring that all documentation is synchronized with the codebase.
---

# Skill body

Intelligent documentation maintenance agent that automatically detects code changes across skills and the repository, then updates, upgrades, or generates documentation to keep everything synchronized.

## Quick Start

```bash
# Detect changes and generate a documentation update report
python skills/documentation/scripts/detect_changes.py \
  --scope skills/ \
  --output .tmp/docs/change-report.md

# Update documentation for a specific skill after changes
python skills/documentation/scripts/update_skill_docs.py \
  --skill <skill-name> \
  --changelog

# Full repository documentation sync
python skills/documentation/scripts/sync_docs.py \
  --skills-dir skills/ \
  --update-catalog \
  --update-readme
```

## Core Workflow

1. **Detect Changes** — Scan for code changes (added, modified, deleted files).
2. **Analyze Impact** — Determine which documentation needs updating.
3. **Generate Updates** — Produce updated or new documentation.
4. **Synchronize Catalog** — Update SKILLS_CATALOG.md if skills changed.
5. **Produce Changelog** — Create a changelog entry for significant changes.
6. **Validate** — Verify all documentation is synchronized.

## Scripts

### `detect_changes.py` — Change Detection Engine

Scans the repository or specific directories to detect code changes since the last documentation update.

```bash
python skills/documentation/scripts/detect_changes.py \
  --scope <path>              # Directory to scan (required)
  --since <commit|date>       # Compare since commit/date (default: last tag)
  --output <file>             # Output report file (default: stdout)
  --format <md|json>          # Output format (default: md)
  --include-git               # Use git diff for precise changes (default: true)
```

**Outputs:**

- List of added files with paths
- List of modified files with change summaries
```