---
name: consultant-context
description: "Shared context loader for all consultant agents. Loads config, project-context, and workflow-status. Use automatically when any consultant agent starts."
invocation: auto
---

# Context Loader

This skill is automatically loaded by consultant agents to ensure consistent context.

## Files to Load

### 1. Configuration (REQUIRED)
```
_consultant/config.yaml
```
Extract and store:
- `consultant.name` - Consultant identity
- `communication_language` - Language for interaction
- `document_output_language` - Language for generated docs
- `rates.discovery`, `rates.development`, `rates.documentation` - Hourly rates
- `paths.*` - All configured paths

### 2. Project Context (IF EXISTS)
```
_consultant/project-context.md
```
The "bible" of the project containing:
- Executive summary
- Business context
- Scope definition
- Technical context
- Requirements registry
- Stories backlog

### 3. Workflow Status (IF EXISTS)
```
_consultant/workflow-status.yaml
```
Current state including:
- `project.name`, `project.phase`
- `workflow_status.*` - Status of each workflow
- `next_action` - Recommended next step
- `checkpoints_passed` - Validated checkpoints

### 4. Sprint Status (IF EXISTS)
```
_consultant/sprint-status.yaml
```
Sprint-level tracking:
- Current sprint info
- Stories with statuses
- Blockers

## Validation Rules

1. **config.yaml is MANDATORY**
   - If missing: STOP with "Config not found. Initialize with /consultant:init"

2. **project-context.md required for most workflows**
   - Discovery agents can proceed without it
   - Architect/Planner/Developer need it populated

3. **workflow-status.yaml tracks progress**
   - If missing: Treat as new project

## Language Rules

- Communicate in `{communication_language}`
- Generate documents in `{document_output_language}`
- Both default to "french" if not specified
