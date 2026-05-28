---
name: self-updating
description: How cc-prime automatically stays current with Claude Code evolution. Use when discussing showcase maintenance, documentation sync, or keeping the showcase updated.
---

# Self-Updating System

cc-prime automatically maintains itself as Claude Code evolves.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Weekly Cron    │────▶│ docs-researcher  │────▶│ Research Report │
│  (GitHub Action)│     │     Agent        │     │  .claude/tasks/ │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Pull Request   │◀────│ showcase-updater │◀────│ Compare to      │
│  for Review     │     │     Agent        │     │ Feature Ref     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## Components

### 1. docs-researcher Agent
Fetches and analyzes Claude Code documentation.

### 2. showcase-updater Agent
Updates showcase files based on research.

### 3. Feature Reference
`.claude/skills/claude-code-features/SKILL.md` - canonical list of features.

### 4. /sync-docs Command
Manual trigger for self-update.

### 5. GitHub Actions
- `scheduled-docs-check.yml` - Weekly check
- `scheduled-showcase-update.yml` - Monthly comprehensive update

## Manual Sync

```
/sync-docs
```

## Automated Sync

GitHub Action runs weekly and creates PRs for human review.

## Adding New Features

1. Update feature reference
2. Create demonstration files
3. Update documentation
4. Add to changelog
