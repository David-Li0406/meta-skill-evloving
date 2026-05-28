---
name: foundry-note
description: Fast-capture intake queue for ideas and follow-up tasks. Add items quickly, list pending items, or dismiss resolved ones.
---

# Note: Fast Capture Skill

## Overview

`Skill(foundry:foundry-note)` provides a low-friction intake queue for capturing ideas, bugs, and follow-up tasks without disrupting your current workflow. Items are stored for later review and can be promoted to spec tasks.

**Core capabilities:**
- Quick capture of ideas, bugs, and documentation gaps
- List and review pending intake items
- Dismiss or promote items to spec tasks
- Priority-based organization

## When to Use This Skill

**Use when:**
- User asks to capture an idea or issue
- User wants to review the intake queue
- User wants to dismiss or promote intake items

**Autonomous capture (no skill invocation needed):**
During implementation, proactively add items using MCP directly - do NOT prompt the user.

### Flow

> `[x?]`=decision · `(GATE)`=user approval · `→`=sequence

```
- **Entry** → [action?]
  - [add] → Capture item → `authoring action="intake-add"` → Confirm → **Exit**
  - [list] → `authoring action="intake-list"` → Display items → **Exit**
  - [dismiss] → `authoring action="intake-dismiss"` → Confirm → **Exit**
  - [promote] → Select item → Add to spec → Dismiss original → **Exit**
```

## MCP Tooling

This skill uses the Foundry MCP server with router+action pattern: `mcp__plugin_foundry_foundry-mcp__authoring`.

| Action | Purpose | Key Parameters |
|--------|---------|----------------|
| `intake-add` | Create intake item | `title` (required), `description`, `priority`, `tags`, `source` |
| `intake-list` | List pending items | `limit`, `cursor` (FIFO pagination) |
| `intake-dismiss` | Mark item dismissed | `item_id`, `reason` |

## Core Workflows

### Add Item

Capture an idea, bug, or task for later:

```bash
mcp__plugin_foundry_foundry-mcp__authoring action="intake-add" title="[Type] description" priority="p2"
```

**Title prefixes:**
| Prefix | Use When |
|--------|----------|
| `[Idea]` | Feature ideas beyond current scope |
| `[Bug]` | Bugs noticed but not immediately actionable |
| `[Docs]` | Documentation gaps or confusing behavior |
| `[Error]` | MCP tool errors or unexpected failures |
| `[Feature]` | Missing or wished-for tools |

### List Items

Review pending intake items:

```bash
mcp__plugin_foundry_foundry-mcp__authoring action="intake-list" limit=20
```

### Dismiss Item

Mark an item as resolved or no longer relevant:

```bash
mcp__plugin_foundry_foundry-mcp__authoring action="intake-dismiss" item_id="{item-id}" reason="Resolved in PR #123"
```

### Promote to Spec

Add intake item to an existing spec, then dismiss:

```bash
# Add to spec
mcp__plugin_foundry_foundry-mcp__authoring action="task-add" spec_id="{spec-id}" phase_id="{phase-id}" title="{intake-title}" description="{intake-description}"

# Dismiss intake item
mcp__plugin_foundry_foundry-mcp__authoring action="intake-dismiss" item_id="{item-id}" reason="Promoted to {spec-id}/{task-id}"
```

## Priority Levels

| Priority | Meaning | Use When |
|----------|---------|----------|
| `p0` | Critical | Blocking future work |
| `p1` | High | Should address soon |
| `p2` | Medium | Normal priority (default) |
| `p3` | Low | Nice to have |
| `p4` | Backlog | Someday/maybe |

## Example Invocations

**Add an idea:**
```
Skill(foundry:foundry-note) "Add idea: implement caching layer for API responses"
```

**List pending items:**
```
Skill(foundry:foundry-note) "Show me the intake queue"
```

**Dismiss an item:**
```
Skill(foundry:foundry-note) "Dismiss item intake-001, it was fixed in the last PR"
```
