---
title: Sprint Schema Reference
description: Complete YAML schema for SPRINT.yaml definitions including all fields, types, and validation rules.
keywords: sprint, schema, yaml, steps, validation, types, SPRINT.yaml
skill: creating-sprints
---

# Sprint Schema Reference

## File Structure

Sprint files are YAML documents stored in sprint directories.

```yaml
# .claude/sprints/<sprint-dir>/SPRINT.yaml
name: <string>           # Optional
workflow: <string>       # Required
steps: <list>            # Required
sprint-id: <string>      # Optional (auto-generated)
created: <string>        # Optional (ISO date)
owner: <string>          # Optional
config: <object>         # Optional
```

## Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | Human-readable sprint name |
| `workflow` | string | Yes | Workflow reference (without .yaml extension) |
| `steps` | list[Step] | Yes | Ordered list of step definitions |
| `sprint-id` | string | No | Unique identifier (auto-generated if absent) |
| `created` | string | No | ISO 8601 date when sprint was created |
| `owner` | string | No | Sprint owner identifier |
| `config` | Config | No | Sprint configuration options |

## Step Schema

### String Step (Simple)

```yaml
steps:
  - "Implement feature X"
  - "Add tests for feature X"
```

### Object Step (With Metadata)

```yaml
steps:
  - prompt: "Implement feature X"
    id: feature-x
    workflow: feature-standard  # Optional per-step workflow override
```

## Step Fields Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | Yes | Step description/instructions |
| `id` | string | No | Unique step identifier (auto-generated: step-0, step-1) |
| `workflow` | string | No | Per-step workflow override |

## Config Schema

```yaml
config:
  max-tasks: <number>      # Optional
  time-box: <string>       # Optional (duration)
  auto-commit: <boolean>   # Optional
```

### Config Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `max-tasks` | number | - | Maximum tasks before pause |
| `time-box` | string | - | Time limit (e.g., "2h", "30m") |
| `auto-commit` | boolean | false | Auto-commit after each step |

## TypeScript Interface

```typescript
interface SprintDefinition {
  workflow: string;
  steps: SprintStep[];
  'sprint-id'?: string;
  name?: string;
  created?: string;
  owner?: string;
  config?: {
    'max-tasks'?: number;
    'time-box'?: string;
    'auto-commit'?: boolean;
  };
}

interface SprintStep {
  prompt: string;
  workflow?: string;
  id?: string;
}

// String steps are normalized to SprintStep during parsing
type RawStep = string | SprintStep;
```

## Validation Rules

### Sprint Level

1. `workflow` must be non-empty string
2. `steps` must be non-empty array
3. File must be valid YAML
4. `sprint-id` if present must be unique

### Step Level

1. String steps become `{ prompt: "<string>" }`
2. Object steps must have `prompt` field
3. Step `id` if present should be kebab-case
4. Per-step `workflow` overrides sprint workflow

### Reference Resolution

1. Workflow resolves from `.claude/workflows/<name>.yaml`
2. References should not include `.yaml` extension
3. Per-step workflow takes precedence over sprint workflow

## Valid Examples

### Minimal Sprint

```yaml
workflow: sprint-default
steps:
  - Implement the feature
```

### Standard Sprint

```yaml
name: User Authentication
workflow: sprint-default

steps:
  - Create User model
  - Implement login endpoint
  - Add authentication middleware
  - Create logout endpoint
```

### Sprint with Object Steps

```yaml
name: API Development
workflow: gherkin-verified-execution

steps:
  - prompt: Design API schema
    id: schema-design
  - prompt: Implement endpoints
    id: implementation
  - prompt: Add integration tests
    id: testing
```

### Sprint with Config

```yaml
name: Complex Feature
workflow: sprint-default

config:
  max-tasks: 50
  time-box: "4h"
  auto-commit: true

steps:
  - Phase 1 implementation
  - Phase 2 implementation
  - Integration and testing
```

### Sprint with Per-Step Workflows

```yaml
name: Mixed Workflow Sprint
workflow: sprint-default

steps:
  - prompt: Research best practices
    workflow: execute-step  # Simple execution
  - prompt: Implement feature
    workflow: gherkin-verified-execution  # Full verification
  - prompt: Quick bug fix
    workflow: bugfix-workflow  # Fast fix flow
```

## Invalid Examples

### Missing Required Fields

```yaml
# INVALID: Missing workflow
steps:
  - Do something
```

```yaml
# INVALID: Empty steps
workflow: sprint-default
steps: []
```

### Invalid Step Configuration

```yaml
# INVALID: Object step missing prompt
steps:
  - id: my-step
```

```yaml
# INVALID: Invalid workflow reference
workflow: non-existent-workflow
steps:
  - Something
```

## Directory Convention

```text
.claude/sprints/
├── YYYY-MM-DD_sprint-name/
│   ├── SPRINT.yaml       # Definition (you write)
│   ├── PROGRESS.yaml     # Compiled (generated)
│   ├── artifacts/        # Sprint artifacts
│   └── context/          # Context files
```

### Naming Pattern

| Pattern | Example | Description |
|---------|---------|-------------|
| `YYYY-MM-DD_name` | `2024-01-15_auth-feature` | Date-prefixed name |
| `sprint-N_name` | `sprint-1_initial-setup` | Sequential numbering |
| `epic-name_story` | `auth_login-flow` | Epic/story grouping |

## Schema Evolution

Current schema version supports:
- String and object step formats
- Workflow reference resolution
- Per-step workflow overrides
- Sprint configuration options

Future versions may add:
- Step dependencies
- Conditional steps
- Parallel step groups
- Step templates
