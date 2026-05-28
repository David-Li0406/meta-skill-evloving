---
name: doc-sync
description: >
  Documentation synchronization knowledge. Use when analyzing documentation
  patterns, understanding how code changes map to documentation needs, or
  determining documentation structure for different project types.
allowed-tools:
  - Read
  - Glob
  - Grep
metadata:
  author: erikb
  version: 1.0.0
  category: documentation
  created: 2026-01-21
---

# Doc-Sync Skill

Knowledge base for documentation synchronization, covering patterns for
different project types and how code changes typically map to documentation
needs.

## When This Skill Applies

- Analyzing documentation structure in a project
- Determining what documentation is needed for code changes
- Understanding common documentation patterns by project type
- Mapping code changes to documentation categories

## Core Concepts

### Documentation as Code

Good documentation:

- Lives near the code it documents
- Updates when the code updates
- Has consistent structure and style
- Is discoverable and navigable

### The Documentation Gap Problem

Documentation drift happens when:

- Features are implemented but not documented
- Architecture changes without ADRs
- Dependencies are added without noting them
- Status markers (PLANNED, IMPLEMENTED) become stale

### Change-to-Doc Mapping

Different types of code changes require different documentation updates:

| Code Change            | Documentation Need                 |
| ---------------------- | ---------------------------------- |
| New feature            | Feature doc, routes, API reference |
| Architectural decision | ADR (Architecture Decision Record) |
| New dependency         | Tech stack reference               |
| Config change          | Guides, deployment docs            |
| Schema change          | Data model docs                    |

## Reference Materials

For detailed patterns and mappings, see:

- `references/doc-patterns.md` - Documentation patterns by project type
- `references/change-mapping.md` - How code changes map to doc types

## Integration Points

This skill supports the `/update-docs` command and its agents:

- `git-change-analyzer` - Uses change mappings
- `doc-gap-analyzer` - Uses doc patterns
- `doc-updater` - Uses both for context
