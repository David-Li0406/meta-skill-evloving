# Schema: Task Tracking

**Version**: 1
**Status**: ACTIVE

---

## Purpose

This schema defines the YAML structure for persistent task tracking. tasks tracked in `.dialogue/tasks.yaml` conform to this schema.

This is the **authoritative schema** for deployed frameworks. See [SKILL.md](./SKILL.md) for operational guidance on using this schema.

---

## Design Rationale

The Work Coordination concept (O-3) provides a comprehensive schema for queue-based and interactive coordination. This schema provides a simplified subset appropriate for:

1. **File-based storage** — YAML readable and editable by humans
2. **Cross-session continuity** — Persistent work tracking between sessions
3. **TodoWrite complement** — Session-level tracking via TodoWrite; persistent tracking via this schema
4. **Future extensibility** — Can evolve to database backends when needed

---

## Schema Definition

### File Structure

```yaml
---
version: string                  # Schema version (e.g., "1.0")
last_updated: ISO8601            # File last modification timestamp

prefixes:                        # task ID prefix definitions
  - prefix: string               # 2-4 uppercase letters
    name: string                 # Human-readable name
    description: string          # Purpose of this prefix

items:                           # Array of tasks
  - <WorkItem>
---
```

### WorkItem Schema

#### Required Fields

All tasks MUST include these fields:

```yaml
id: string          # Unique identifier: [PREFIX]-[NNN]
title: string       # Brief descriptive title
status: enum        # Current lifecycle status
created: ISO8601    # Creation timestamp
```

| Field | Type | Constraints | Example |
|-------|------|-------------|---------|
| `id` | string | Pattern: `[A-Z]{2,4}-[0-9]{3}` | `SH-001`, `CD-001` |
| `title` | string | Non-empty, human-readable | `Information Reference Schema` |
| `status` | enum | One of: BACKLOG, READY, IN_PROGRESS, BLOCKED, COMPLETED, CANCELLED | `READY` |
| `created` | string | ISO 8601 datetime | `2026-01-14T12:00:00Z` |

#### Recommended Fields

tasks SHOULD include these fields where applicable:

```yaml
updated: ISO8601         # Last update timestamp
type: enum               # task classification
phase: integer           # SDLC phase (1-7) if applicable
priority: enum           # Urgency level
description: string      # Full description (multiline)
objective: string        # Success criteria
rationale: string        # Why this work is needed
```

| Field | Type | Constraints | Example |
|-------|------|-------------|---------|
| `updated` | string | ISO 8601 datetime | `2026-01-14T14:00:00Z` |
| `type` | enum | One of: CAPABILITY, SCHEMA, DOCUMENT, RESEARCH, DEBT, DECISION | `SCHEMA` |
| `phase` | integer | 1-7 (SDLC phase) | `3` |
| `priority` | enum | One of: CRITICAL, HIGH, MEDIUM, LOW | `HIGH` |
| `description` | string | Multiline allowed | See examples |
| `objective` | string | What success looks like | `REF-002 published` |
| `rationale` | string | Why this work is needed | `Required for capability flows` |

#### Optional Fields

tasks MAY include these fields:

```yaml
blocked_by: string[]     # IDs of blocking tasks
blocks: string[]         # IDs of items this blocks
assigned_to: string      # Actor identifier
completed: ISO8601       # Completion timestamp (if status = COMPLETED)
notes: string            # Free-form notes, history, context
```

| Field | Type | Constraints | Example |
|-------|------|-------------|---------|
| `blocked_by` | array | Array of task IDs | `["SH-001", "SH-002"]` |
| `blocks` | array | Array of task IDs | `["SH-003"]` |
| `assigned_to` | string | Actor reference | `human:pid`, `ai:claude` |
| `completed` | string | ISO 8601 datetime | `2026-01-14T15:00:00Z` |
| `notes` | string | Multiline allowed | See examples |

---

## Enumeration Values

### Status

| Value | Meaning | Valid Transitions |
|-------|---------|-------------------|
| `BACKLOG` | Identified but not ready to work | → READY, CANCELLED |
| `READY` | Ready to be started | → IN_PROGRESS, BLOCKED, CANCELLED |
| `IN_PROGRESS` | Currently being worked | → COMPLETED, BLOCKED, CANCELLED |
| `BLOCKED` | Cannot proceed; dependency or issue | → READY, IN_PROGRESS, CANCELLED |
| `COMPLETED` | Work finished successfully | (terminal) |
| `CANCELLED` | No longer needed | (terminal) |

### Type

| Value | Meaning | Example |
|-------|---------|---------|
| `CAPABILITY` | Capability implementation work | Implement Elicit skill |
| `SCHEMA` | Schema definition work | Create reference schema |
| `DOCUMENT` | Document creation work | Write THY-001 |
| `RESEARCH` | Investigation work | Evaluate graph databases |
| `DEBT` | Technical/conceptual debt | Address THY-003 items |
| `DECISION` | Decision-requiring work | Choose retrofit approach |

### Priority

| Value | Meaning | Response Time |
|-------|---------|---------------|
| `CRITICAL` | Blocks other work; immediate attention | Same session |
| `HIGH` | Important; should be addressed soon | Next few sessions |
| `MEDIUM` | Normal priority (default) | When capacity allows |
| `LOW` | Can wait; no time pressure | Opportunistic |

---

## Prefix Conventions

### Format

task IDs follow pattern `PREFIX-NNN` where:
- `PREFIX`: 2-4 uppercase letters identifying work stream
- `NNN`: Zero-padded sequence number (001, 002, etc.)

### Standard Prefixes

| Prefix | Name | Description |
|--------|------|-------------|
| `SH` | Self-Hosting | Framework self-application work |
| `CD` | Conceptual Debt | Framework concept gaps |
| `FW` | Framework | Core framework development |
| `DOC` | Documentation | Documentation tasks |
| `VAL` | Validation | Validation and testing |

**Note**: New prefixes MUST be defined in the `prefixes` section before use.

---

## Complete Example

```yaml
# .dialogue/tasks.yaml
version: "1.0"
last_updated: "2026-01-14T14:00:00Z"

prefixes:
  - prefix: "SH"
    name: "Self-Hosting"
    description: "Framework self-application tasks"
  - prefix: "CD"
    name: "Conceptual Debt"
    description: "Framework concept gaps and improvements"

items:
  - id: "SH-001"
    title: "Information Reference Schema"
    status: READY
    created: "2026-01-13T10:00:00Z"
    updated: "2026-01-14T12:00:00Z"
    type: SCHEMA
    phase: 3
    priority: HIGH
    description: |
      Create schema for information references used in capability flow
      specifications. Should define how to reference documents, decisions,
      observations, and external sources.
    objective: "REF-002 published with complete reference schema"
    rationale: "Required for capability flow specifications to reference inputs/outputs"
    blocked_by: []
    blocks: ["SH-002"]
    notes: "Part of Phase 3 self-hosting work."

  - id: "SH-004"
    title: "Graph Storage Investigation"
    status: COMPLETED
    created: "2026-01-13T10:00:00Z"
    updated: "2026-01-13T15:00:00Z"
    completed: "2026-01-13T15:00:00Z"
    type: RESEARCH
    priority: HIGH
    description: "Investigate graph storage options for Context Graph"
    objective: "Storage approach decided"
    notes: |
      Decision (13 January 2026): Start with filesystem + YAML.
      Kuzu identified for future evolution.
```

---

## Validation Rules

### Required Field Validation

1. All required fields (`id`, `title`, `status`, `created`) must be present
2. `id` must match pattern `[A-Z]{2,4}-[0-9]{3}`
3. `id` prefix must be defined in `prefixes` section
4. `status` must be a valid status enum value
5. `created` must be valid ISO 8601 datetime

### Consistency Validation

1. If `status` is COMPLETED, `completed` timestamp SHOULD be present
2. If `blocked_by` is non-empty, `status` SHOULD be BACKLOG or BLOCKED
3. All IDs in `blocked_by` and `blocks` SHOULD exist in `items`
4. `updated` SHOULD be >= `created`
5. `completed` SHOULD be >= `created`

### Sequence Validation

1. IDs within same prefix SHOULD be sequential (SH-001, SH-002, SH-003)
2. Gaps in sequence are allowed (for cancelled items)
3. IDs MUST NOT be reused

---

## Operations

### Loading at Session Start

AI agents SHOULD:
1. Read `.dialogue/tasks.yaml`
2. Identify items with status `IN_PROGRESS` or `READY` with high priority
3. Load relevant items into TodoWrite for session visibility
4. Note any items in BLOCKED status for context

### Updating During Session

When task status changes:
1. Update `status` field
2. Update `updated` timestamp
3. If completing: set `completed` timestamp
4. Add relevant information to `notes`

### Creating New Items

When creating a new task:
1. Check `prefixes` for appropriate prefix (add if needed)
2. Determine next sequence number for that prefix
3. Set `status` to BACKLOG or READY as appropriate
4. Set `created` to current timestamp
5. Set `priority` (default: MEDIUM)

---

## Relationship to O-3

This schema implements a subset of the Work Coordination concept (O-3):

| O-3 Feature | This Schema | Status |
|-------------|-------------|--------|
| WorkItem core fields | ✓ Implemented | Full |
| WorkStatus state machine | ✓ Implemented | Simplified |
| Dependencies (blocked_by/blocks) | ✓ Implemented | Full |
| Assignment tracking | ✓ Implemented | Simplified |
| Context packaging | ✗ Not implemented | Future |
| Assignment history | ✗ Not implemented | Future |
| Queue-based coordination | ✗ Not implemented | Future |
| Escalation tracking | ✗ Not implemented | Future |

---

## Validation Status

- ✓ **Core fields**: Aligned with O-3 WorkItem schema
- ✓ **Status state machine**: Simplified but consistent with O-3
- ✓ **Dependency tracking**: Full bidirectional support
- ⚠ **Type-specific fields**: Initial specification; may need extension
- ⚠ **Validation tooling**: Schema defined; validator not yet implemented

---

*This schema enables persistent task tracking while remaining human-readable and editable. It complements the session-level TodoWrite tool for cross-session continuity.*
