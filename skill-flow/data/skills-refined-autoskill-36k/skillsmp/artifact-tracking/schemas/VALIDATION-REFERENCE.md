# Artifact Schema Validation Reference

Quick reference for validating MeatyPrompts tracking artifacts against JSON schemas.

## Schema Files

All schemas are JSON Schema (draft-07) in YAML format:

```
schemas/
├── progress.schema.yaml      # Progress tracking frontmatter
├── context.schema.yaml       # Context notes frontmatter
├── bug-fix.schema.yaml       # Bug fix tracking frontmatter
└── observation.schema.yaml   # Observation log frontmatter
```

## Quick Validation

### Extract Frontmatter

All tracking artifacts follow this markdown structure:

```markdown
---
[YAML FRONTMATTER HERE]
---

# Document Title

[Markdown content...]
```

Extract frontmatter (lines between `---` markers) for validation.

### Validate Using Node.js + AJV

```bash
npm install ajv yaml
node validate.js path/to/artifact.md
```

See `scripts/validate.js` in skill for implementation.

## Field Validation Rules

### 1. Progress Tracking (progress.schema.yaml)

**Required Fields**:
- `type`: Must be "progress"
- `prd`: Kebab-case, 3-64 chars
- `phase`: Integer 1-99
- `title`: String 5-256 chars
- `status`: One of [planning, in-progress, review, complete, blocked]
- `started`: YYYY-MM-DD format
- `overall_progress`: Integer 0-100
- `total_tasks`, `completed_tasks`, `in_progress_tasks`, `blocked_tasks`: Integers >= 0

**Optional Fields**:
- `completed`: Date (YYYY-MM-DD) or null
- `completion_estimate`: One of [on-track, at-risk, blocked, ahead]
- `owners`: Array of 1-10 kebab-case agent names
- `contributors`: Array of up to 20 kebab-case names
- `blockers`: Array (max 50) with fields:
  - `id`: Pattern "^[A-Z]+-[0-9]+$" (e.g., BLOCKER-1)
  - `title`: String 5-256 chars
  - `status`: One of [active, resolved, workaround]
  - `severity`: One of [critical, high, medium, low]
  - `depends_on`: Array of task IDs or null
- `success_criteria`: Array (max 50) with fields:
  - `id`: Pattern "^SC-[0-9]+$"
  - `description`: String 10-512 chars
  - `status`: One of [pending, met]
- `notes`: String up to 2048 chars

**Field Naming Examples**:
```yaml
prd: "advanced-editing-v2"
phase: 1
status: "in-progress"
started: "2025-11-09"
completed: null
overall_progress: 65
completion_estimate: "on-track"
owners: ["ui-engineer-enhanced"]
blockers:
  - id: "BLOCKER-1"
    title: "Missing Backend Endpoint"
    status: "active"
    severity: "critical"
success_criteria:
  - id: "SC-1"
    description: "All blocks attached to prompts"
    status: "met"
```

### 2. Context Notes (context.schema.yaml)

**Required Fields**:
- `type`: Must be "context"
- `prd`: Kebab-case, 3-64 chars
- `title`: String 5-256 chars
- `status`: One of [complete, blocked, in-progress]

**Optional Fields**:
- `phase`: Integer 1-99 or null
- `phase_status`: Array (max 99) with fields:
  - `phase`: Integer 1-99
  - `status`: One of [complete, blocked, in-progress]
  - `reason`: String or null
- `blockers`: Array (max 50) with fields:
  - `id`: Pattern "^[A-Z]+-[0-9]+$"
  - `title`: String 5-256 chars
  - `description`: String 20-2048 chars
  - `blocking`: Array of phase references (e.g., ["phase-3", "phase-4"])
  - `depends_on`: Array of strings or null
  - `severity`: One of [critical, high, medium, low]
- `decisions`: Array (max 100) with fields:
  - `id`: Pattern "^DECISION-[0-9]+$"
  - `question`: String 10-512 chars
  - `decision`: String 10-512 chars
  - `rationale`: String 10-1024 chars
  - `tradeoffs`: String 10-1024 chars
  - `location`: File path with optional line numbers (e.g., "BlockEditor.tsx:45" or "path/to/file.ts:105-125")
  - `phase`: Integer 1-99
- `integrations`: Array (max 50) with fields:
  - `system`: String 3-64 chars
  - `component`: String 3-256 chars
  - `calls`: Array of API endpoints or function names
  - `status`: One of [waiting-on-backend, waiting-on-frontend, waiting-on-external, complete, in-progress]
  - `notes`: String up to 512 chars
- `gotchas`: Array (max 100) with fields:
  - `id`: Pattern "^GOTCHA-[0-9]+$"
  - `title`: String 5-256 chars
  - `description`: String 20-2048 chars
  - `solution`: String 10-1024 chars
  - `location`: File path with optional line numbers
  - `severity`: One of [critical, high, medium, low]
  - `affects`: Array of component names
- `modified_files`: Array (max 200) with fields:
  - `path`: File path (required)
  - `changes`: String 5-512 chars
  - `phase`: Integer 1-99
  - `impact`: One of [critical, high, medium, low]
- `updated`: ISO 8601 timestamp
- `notes`: String up to 2048 chars

**Field Naming Examples**:
```yaml
prd: "blocks-v2"
phase: 3
status: "blocked"
blockers:
  - id: "BLOCKER-1"
    title: "Missing Backend Association Layer"
    blocking: ["phase-3", "phase-4"]
decisions:
  - id: "DECISION-1"
    question: "How to handle editor initialization?"
    location: "BlockEditor.tsx:201-203"
gotchas:
  - id: "GOTCHA-1"
    title: "MarkdownInitPlugin Re-initialization"
    location: "BlockEditor.tsx:105-125"
modified_files:
  - path: "apps/web/src/components/editor/BlockEditor.tsx"
    changes: "Fixed state initialization"
    phase: 1
    impact: "critical"
```

### 3. Bug Fix Tracking (bug-fix.schema.yaml)

**Required Fields**:
- `type`: Must be "bug-fixes"
- `month`: String, pattern "^(0[1-9]|1[0-2]|[1-9])$" (1-12)
- `year`: String, pattern "^[0-9]{4}$"
- `total_fixes`: Integer >= 0

**Optional Fields**:
- `severity_breakdown`: Object with keys [critical, high, medium, low], each integer >= 0
- `component_breakdown`: Object with component names as keys, each integer >= 0
- `fixes_by_component`: Object with component names as keys, each value is array of fix IDs
- `fixes_by_date`: Object with dates as keys (YYYY-MM-DD), each value is array of fix IDs
- `fixes_by_severity`: Object with severity levels as keys, each value is array of fix IDs
- `fixes`: Object with fix IDs as keys, each containing:
  - `id`: Pattern "^fix-[0-9]+$"
  - `date`: ISO 8601 timestamp
  - `severity`: One of [critical, high, medium, low]
  - `component`: String 3-64 chars
  - `type`: One of [bug, performance, security, policy, refactor, other]
  - `status`: One of [completed, in-progress, reverted]
  - `issue`: String 10-1024 chars
  - `fix`: String 10-2048 chars
  - `root_causes`: Array (max 20) of strings 10-512 chars
  - `files_modified`: Array (max 100) of file paths
  - `commit`: Git hash (7-40 hex chars) or null
  - `impact`: String up to 512 chars
  - `related_fixes`: Array of fix IDs
  - `notes`: String up to 512 chars
- `updated`: ISO 8601 timestamp
- `notes`: String up to 2048 chars

**Field Naming Examples**:
```yaml
type: "bug-fixes"
month: "11"
year: "2025"
total_fixes: 12
severity_breakdown:
  critical: 5
  high: 4
  medium: 3
  low: 0
component_breakdown:
  editor: 4
  blocks: 3
fixes:
  fix-2:
    id: "fix-2"
    date: "2025-11-07T09:30:00Z"
    severity: "critical"
    component: "editor"
    type: "bug"
    commit: "783388e9"
    files_modified:
      - "apps/web/src/components/editor/BlockEditor.tsx"
```

### 4. Observation Logs (observation.schema.yaml)

**Required Fields**:
- `type`: Must be "observations"
- `month`: String, pattern "^(0[1-9]|1[0-2]|[1-9])$" (1-12)
- `year`: String, pattern "^[0-9]{4}$"
- `period`: String in format "YYYY-MM-DD to YYYY-MM-DD"

**Optional Fields**:
- `observation_counts`: Object with category names as keys, each integer >= 0
- `observations_by_category`: Object with category names as keys, each array of observation IDs
- `observations_by_impact`: Object with impact levels [high, medium, low] as keys, each array of observation IDs
- `observations`: Object with observation IDs as keys, each containing:
  - `id`: Pattern "^OBS-[0-9]+$"
  - `date`: ISO 8601 timestamp
  - `category`: One of [pattern-discoveries, performance-insights, architectural-learnings, tools-techniques, process-improvements, other]
  - `impact`: One of [high, medium, low]
  - `title`: String 5-256 chars
  - `observation`: String 10-2048 chars
  - `affects`: Array (max 20) of component names
  - `solution_applied`: String up to 512 chars
  - `related_work`: Array (max 10) of links/references
  - `follow_up`: Boolean
  - `follow_up_notes`: String up to 512 chars
  - `tags`: Array (max 10) of kebab-case tags
- `high_impact_count`: Integer >= 0
- `total_observations`: Integer >= 0
- `actionable_observations`: Array of observation IDs
- `updated`: ISO 8601 timestamp
- `notes`: String up to 2048 chars

**Field Naming Examples**:
```yaml
type: "observations"
month: "11"
year: "2025"
period: "2025-11-01 to 2025-11-30"
total_observations: 23
high_impact_count: 8
observations:
  OBS-1:
    id: "OBS-1"
    date: "2025-11-07T10:30:00Z"
    category: "pattern-discoveries"
    impact: "high"
    title: "MarkdownInitPlugin Re-initialization"
    affects: ["BlockEditor"]
    tags:
      - "react"
      - "state-management"
observations_by_category:
  pattern-discoveries:
    - OBS-1
    - OBS-3
observations_by_impact:
  high:
    - OBS-1
    - OBS-2
```

## Common Validation Errors

### Missing Required Fields
```
Error: data must have required property 'prd'
Fix: Add missing required field to frontmatter
```

### Invalid Enum Value
```
Error: data.status must be equal to one of the allowed values
Allowed: ["planning", "in-progress", "review", "complete", "blocked"]
Fix: Use exact enum value from schema
```

### Pattern Mismatch
```
Error: data.prd must match pattern "^[a-z0-9]([a-z0-9-]*[a-z0-9])?$"
Fix: Use kebab-case (lowercase, hyphens, no special chars)
```

### Type Mismatch
```
Error: data.phase must be integer
Fix: Use integer type (e.g., 1, 2, 3) not string ("1", "2", "3")
```

### String Length
```
Error: data.title must NOT be shorter than 5 characters
Fix: Ensure string meets minLength requirement
```

### Array Constraints
```
Error: data.blockers must NOT have more than 50 items
Fix: Reduce array size or split across documents
```

## Date/Time Formats

### Date Format (YYYY-MM-DD)
```yaml
started: "2025-11-09"
completed: "2025-11-15"
```

### ISO 8601 Timestamp Format
```yaml
date: "2025-11-07T09:30:00Z"
updated: "2025-11-17T10:30:00Z"
```

### Date Range Format (YYYY-MM-DD to YYYY-MM-DD)
```yaml
period: "2025-11-01 to 2025-11-30"
```

## ID Patterns

### Task IDs
```
Pattern: TASK-[phase].[number]
Examples: TASK-1.1, TASK-2.5, TASK-3.12
```

### Blocker/Gotcha/Decision IDs
```
Pattern: [TYPE]-[number]
Examples: BLOCKER-1, GOTCHA-3, DECISION-5
Success Criteria: SC-1, SC-2
```

### Fix IDs
```
Pattern: fix-[number]
Examples: fix-1, fix-2, fix-123
```

### Observation IDs
```
Pattern: OBS-[number]
Examples: OBS-1, OBS-5, OBS-42
```

## File Paths in Schemas

### Relative File Paths
```yaml
path: "apps/web/src/components/editor/BlockEditor.tsx"
location: "BlockEditor.tsx:201-203"
location: "BlockEditor.tsx:105-125"
```

### Path with Line Numbers
```
Format: path/to/file.ext:[start_line]-[end_line]
Examples:
  - "BlockEditor.tsx:105-125"
  - "apps/web/src/lib/editor/serialization.ts:29"
  - "/api/services/blocks.py:45"
```

## Testing Validation

### Valid Frontmatter Example
```yaml
---
type: progress
prd: "advanced-editing-v2"
phase: 1
title: "Prompt Creation Modal Enhancements"
status: "in-progress"
started: "2025-11-09"
completed: null
overall_progress: 65
completion_estimate: "on-track"
total_tasks: 12
completed_tasks: 8
in_progress_tasks: 3
blocked_tasks: 1
owners: ["ui-engineer-enhanced"]
blockers:
  - id: "BLOCKER-1"
    title: "Missing Backend Association Endpoint"
    status: "active"
    severity: "critical"
    depends_on: null
success_criteria:
  - id: "SC-1"
    description: "All blocks can be attached to prompts"
    status: "met"
notes: "Phase proceeding on schedule"
---
```

This frontmatter will pass validation against `progress.schema.yaml`.

---

**Last Updated**: 2025-11-17
**Schema Version**: 1.0
**Status**: Published
