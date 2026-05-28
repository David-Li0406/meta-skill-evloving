---
name: creating-sprints
description: Guide for creating sprint definitions in SPRINT.yaml. This skill should be used when users want to create sprint, new sprint planning, sprint definition best practices, or define steps for autonomous execution. Triggers on "create sprint", "new sprint", "sprint definition", "define steps".
---

# Creating Sprints

Guide for authoring SPRINT.yaml definitions for autonomous execution.

## What is a Sprint?

| Concept | Description |
|---------|-------------|
| Sprint | YAML file defining steps and workflow reference |
| Step | Individual task with prompt description |
| Workflow | Execution phases applied to sprint steps |
| PROGRESS.yaml | Compiled sprint with expanded phases |

## Sprint Location

```text
.claude/sprints/
├── 2024-01-15_feature-auth/
│   ├── SPRINT.yaml       # Sprint definition (you create)
│   └── PROGRESS.yaml     # Compiled progress (generated)
└── 2024-01-20_bugfix-login/
    ├── SPRINT.yaml
    └── PROGRESS.yaml
```

## Quick Start

### 1. Create Sprint Directory

```bash
mkdir -p .claude/sprints/$(date +%Y-%m-%d)_my-sprint
```

### 2. Create SPRINT.yaml

```yaml
# .claude/sprints/YYYY-MM-DD_name/SPRINT.yaml
name: My Sprint
workflow: sprint-default

steps:
  - Implement user authentication
  - Add login form validation
  - Create session management
```

### 3. Compile and Run

```bash
/run-sprint
```

## Sprint Sizing Guidelines

Sprints should have 3-8 steps with a single focused purpose.

| Guideline | Recommendation |
|-----------|----------------|
| Step count | 3-8 steps per sprint |
| Focus | Single responsibility or goal |
| Duration | Complete in one session |
| Granularity | Each step = 1 atomic task |

### Why 3-8 Steps?

- **< 3 steps**: Too small, use direct commands instead
- **3-8 steps**: Optimal range for autonomous execution
- **> 8 steps**: Break into multiple sprints or add sub-steps

### Single Responsibility

Each sprint should have one focused goal:

| Good | Bad |
|------|-----|
| "Implement authentication" | "Implement auth and add logging and fix bugs" |
| "Add API endpoints for users" | "Add API endpoints and refactor database" |
| "Create dashboard UI" | "Create dashboard and optimize backend" |

## Step Writing Principles

Good steps are:
- **Clear**: Unambiguous intent
- **Actionable**: Concrete deliverable
- **Scoped**: Bounded in scope

See `references/step-writing-guide.md` for detailed guidance.

## Workflow Selection

| Workflow | Best For | Step Count |
|----------|----------|------------|
| `sprint-default` | Multi-step features | 5-8 |
| `gherkin-verified-execution` | Complex autonomous work | 5-10 |
| `execute-with-qa` | Steps needing verification | 3-6 |
| `flat-foreach` | Simple step iteration | 3-5 |

See `references/workflow-selection.md` for workflow decision tree.

## SPRINT.yaml Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | Human-readable sprint name |
| `workflow` | string | Yes | Workflow reference |
| `steps` | list | Yes | Step prompts or objects |
| `sprint-id` | string | No | Unique identifier (auto-generated) |
| `config` | object | No | Sprint configuration |

See `references/sprint-schema.md` for complete schema.

## Step Formats

### Simple String Steps

```yaml
steps:
  - Implement user login endpoint
  - Add JWT token validation
  - Create logout functionality
```

### Object Steps (with metadata)

```yaml
steps:
  - prompt: Implement user login endpoint
    id: login-endpoint
  - prompt: Add JWT token validation
    id: jwt-validation
  - prompt: Create logout functionality
    id: logout
```

## Example Sprints

### Feature Sprint

```yaml
name: User Authentication Feature
workflow: sprint-default

steps:
  - Create User model with password hashing
  - Implement /auth/register endpoint
  - Implement /auth/login endpoint with JWT
  - Add authentication middleware
  - Create /auth/me endpoint for user profile
```

### Bug Fix Sprint

```yaml
name: Fix Login Validation
workflow: execute-with-qa

steps:
  - Investigate login validation bug
  - Fix email format validation
  - Add comprehensive test cases
```

### Refactoring Sprint

```yaml
name: API Response Standardization
workflow: gherkin-verified-execution

steps:
  - Define standard response envelope
  - Refactor user endpoints to use envelope
  - Refactor product endpoints to use envelope
  - Update API documentation
```

## References

- `references/sprint-schema.md` - Complete SPRINT.yaml schema
- `references/step-writing-guide.md` - Writing effective step prompts
- `references/workflow-selection.md` - Choosing the right workflow

## Assets

- `assets/sprint-template.yaml` - Annotated sprint template

## Validation

Before running a sprint:

1. Verify YAML syntax is valid
2. Ensure workflow reference exists
3. Check step count is in 3-8 range
4. Confirm each step is actionable
5. Verify sprint has single focus

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|------------|
| Workflow not found | Invalid workflow reference | Check `.claude/workflows/` for available workflows |
| Steps not executing | Missing steps array | Add `steps:` field with step list |
| Sprint too long | Too many steps | Break into multiple focused sprints |
| Unclear progress | Steps too vague | Rewrite steps with clear deliverables |

## Related

- **creating-workflows** - Authoring workflow definitions
- **orchestrating-sprints** - Running and managing sprints
