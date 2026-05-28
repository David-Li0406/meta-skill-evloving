---
name: docs-search
description: Index and search project documentation with semantic similarity. Use when you need to find relevant documentation, check if docs are indexed, or link documentation to code entities.
allowed-tools: Bash
---

# Documentation Search Skill

Index and semantically search project documentation using embeddings and vector similarity.

## Quick Reference (Copy-Paste)

```bash
# Shortcut (preferred)
bun run d:search "how to create a badge"
bun run d:search "workflow patterns"
bun run d:search "authentication"

# Long form (equivalent)
bun run checkpoint docs search "<query>"
bun run checkpoint docs for-code <entity-name>
```

**Use docs search instead of grepping markdown files. Semantic > literal.**

---

## When to Use

- Finding documentation relevant to a feature or code area
- Checking if specific documentation is already indexed
- Searching for examples, patterns, or explanations in docs
- Linking documentation to specific code entities
- Cleaning up orphaned documentation references
- Understanding what documentation exists before writing new docs

## CLI Reference

All commands use the checkpoint CLI:

```bash
bun run checkpoint docs <command> [args...]
```

## Commands

### Index Documentation

Index documentation files or directories for semantic search:

```bash
bun run checkpoint docs index <path> [--force]
```

What it does:

- Scans for markdown files (.md, .mdx)
- Extracts sections based on headings
- Generates embeddings for each section
- Stores in knowledge graph database
- Supports incremental indexing (only changed files)

Options:

- `--force` - Re-index even if file hasn't changed

Examples:

```bash
bun run checkpoint docs index docs/
bun run checkpoint docs index packages/openbadges-types/README.md
bun run checkpoint docs index .claude/agents/ --force
```

### Check Indexing Status

Check if a file is indexed and when it was last indexed:

```bash
bun run checkpoint docs status <file>
```

Example:

```bash
bun run checkpoint docs status docs/development-workflows.md
```

Returns:

- Whether file is indexed
- Last index timestamp
- Number of sections indexed
- File hash for change detection

### Clean Orphaned Docs

Remove documentation entries for files that no longer exist:

```bash
bun run checkpoint docs clean
```

What it does:

- Finds all indexed documentation paths
- Checks if each file still exists
- Removes entries for deleted files
- Reports cleanup statistics

### Semantic Search

Search indexed documentation using semantic similarity:

```bash
bun run checkpoint docs search <query>
```

Example:

```bash
bun run checkpoint docs search "how to create a badge"
bun run checkpoint docs search "workflow gate approval"
bun run checkpoint docs search "atomic commits best practices"
```

Returns:

- Matching documentation sections
- Similarity scores (0-1, higher is better)
- File paths and section headings
- Content preview

### Find Docs for Code

Find documentation linked to a specific code entity:

```bash
bun run checkpoint docs for-code <entity-id>
```

Example:

```bash
bun run checkpoint docs for-code createBadge
bun run checkpoint docs for-code OB3CredentialSubject
```

Returns:

- Documentation sections that reference the entity
- Relationship metadata (how docs link to code)
- Relevance scores

## Example: Documentation Search Workflow

```bash
# 1. Index project documentation
bun run checkpoint docs index docs/ --force
bun run checkpoint docs index packages/

# 2. Search for relevant docs before implementing
bun run checkpoint docs search "badge verification process"

# 3. Check if specific docs are indexed
bun run checkpoint docs status docs/development-workflows.md

# 4. Clean up after reorganizing docs
bun run checkpoint docs clean
```

## Example: Finding Context for Code Changes

```bash
# Before modifying a function, find related documentation
bun run checkpoint docs for-code validateBadge

# Search for documentation about the feature area
bun run checkpoint docs search "badge validation"

# Index any new docs you create
bun run checkpoint docs index docs/badge-validation.md
```

## Output Format

### Index Command

Returns:

- `indexed`: Number of files indexed
- `sections`: Number of doc sections processed
- `skipped`: Number of unchanged files (without --force)
- `errors`: Any indexing failures

### Status Command

Returns:

- `indexed`: Boolean indicating if file is indexed
- `timestamp`: Last index time (ISO 8601)
- `sections`: Number of sections in file
- `hash`: Content hash for change detection

### Search Command

Returns JSON array of results:

```json
[
  {
    "file": "docs/development-workflows.md",
    "section": "Gate Workflow Rules",
    "content": "Gates are checkpoints that require explicit user approval...",
    "similarity": 0.89
  }
]
```

### For-Code Command

Returns JSON array of documentation links:

```json
[
  {
    "entity": "createBadge",
    "docFile": "docs/badge-creation.md",
    "docSection": "Creating Badges",
    "relationship": "mentioned-in",
    "relevance": 0.92
  }
]
```

## Integration with Session Hooks

The documentation search integrates with session start hooks:

- `onSessionStart` automatically searches for docs related to:
  - Current branch's code area
  - Modified files
  - Issue being worked on

This automatic injection happens when session hooks are wired to Claude Code (currently manual invocation only).
