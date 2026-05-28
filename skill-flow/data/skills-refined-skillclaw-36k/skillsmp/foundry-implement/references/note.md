# Note Integration

Fast-capture intake queue for ideas/tasks that arise during implementation.

## Overview

Note provides low-friction capture without disrupting workflow. Items are stored in `specs/.bikelane/intake.jsonl` for later review.

**Key principle:** Capture autonomously. Do NOT prompt the user - just add items when you identify something worth capturing.

## MCP Tooling

| Action | Purpose | Key Parameters |
|--------|---------|----------------|
| `authoring action="intake-add"` | Create intake item | `title` (required), `description`, `priority`, `tags`, `source` |
| `authoring action="intake-list"` | List pending items | `limit`, `cursor` (FIFO pagination) |
| `authoring action="intake-dismiss"` | Mark item dismissed | `item_id`, `reason` |

## Autonomous Capture During Implementation

**Proactively add notes** whenever you encounter:

| Trigger | Title Prefix | Example |
|---------|--------------|---------|
| Idea beyond current scope | `[Idea]` | `[Idea] Add retry logic to API calls` |
| Bug noticed, not actionable now | `[Bug]` | `[Bug] Race condition in cache invalidation` |
| Documentation gap | `[Docs]` | `[Docs] Missing examples for batch operations` |

**Capture silently and continue working:**
```bash
mcp__plugin_foundry_foundry-mcp__authoring action="intake-add" title="[Type] description" source="foundry-implement"
```

## Priority Levels

| Priority | Meaning | Use When |
|----------|---------|----------|
| `p0` | Critical | Blocking future work |
| `p1` | High | Should address soon |
| `p2` | Medium | Normal priority (default) |
| `p3` | Low | Nice to have |
| `p4` | Backlog | Someday/maybe |

## Promotion Workflow

When reviewing note items, promote actionable ones to spec tasks:

**Add to existing spec:**
```bash
mcp__plugin_foundry_foundry-mcp__authoring action="task-add" spec_id="{spec-id}" phase_id="{phase-id}" title="{intake-title}" description="{intake-description}"
mcp__plugin_foundry_foundry-mcp__authoring action="intake-dismiss" item_id="{item-id}" reason="Promoted to {spec-id}/{task-id}"
```

**Create new spec:**
Use `foundry-spec` skill with intake item context, then dismiss the intake item.

## Example Captures

**Idea beyond scope:**
```bash
mcp__plugin_foundry_foundry-mcp__authoring action="intake-add" title="[Idea] Add caching layer to reduce API calls" priority="p2"
```

**Bug noticed:**
```bash
mcp__plugin_foundry_foundry-mcp__authoring action="intake-add" title="[Bug] Stale data after concurrent updates" description="Noticed during task-2-3 implementation" priority="p1"
```
