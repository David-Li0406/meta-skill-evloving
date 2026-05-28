---
name: write-project-file
description: Create or update PROJECT.md files for this repo. Use when authoring or maintaining PROJECT.md.
---

# PROJECT.md Authoring Guide

## Structure

PROJECT.md should contain:
1. **Project Overview** - One-line description, tech stack
2. **Feature Registry** - List of features with status (✅ complete, ⚠️ partial, ❌ not built)
3. **Test Status** - Test coverage summary
4. **Development Info** - Quick start, common tasks
5. **Post-MVP Roadmap** - Future features (if any)

## Guidelines

- Remove meta-documentation about how to write PROJECT.md (that's what this skill is for)
- Focus on current state only - no historical information
- Keep it scannable with headers, lists, and status emojis
- Link to detailed docs when needed (don't duplicate)
- Update feature registry when features are added/completed
- Remove features that are no longer relevant

## Example Format

```markdown
# Project Name

One-line description. Tech stack.

## Feature Registry

### Core Features
- ✅ Feature 1 - Brief description
- ✅ Feature 2 - Brief description
- ❌ Feature 3 - Not yet implemented

### Test Status
- ✅ Integration tests (input→output)
- ❌ E2E tests (not needed yet)

## Development

Quick start commands...

## Post-MVP Roadmap

Future features...
```
