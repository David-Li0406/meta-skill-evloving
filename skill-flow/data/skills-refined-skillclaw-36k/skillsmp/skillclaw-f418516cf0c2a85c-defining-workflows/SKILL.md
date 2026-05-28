---
name: defining-workflows
description: Use this skill when you need to create and document multi-agent orchestrations, including defining execution phases and parameters for complex tasks.
---

# Skill body

## Purpose

This Skill provides comprehensive guidance for **defining workflows** - multi-agent orchestrations that coordinate multiple agents in sequence, parallel, or conditionally to accomplish complex tasks. Workflows enable reusable, validated processes.

**When to use this Skill:**

- Creating new workflow documents
- Defining multi-agent coordination patterns
- Structuring sequential or parallel agent execution
- Writing workflow acceptance criteria
- Documenting workflow parameters and inputs

## Workflow Structure

### YAML Frontmatter (Required)

```yaml
---
name: workflow-name
description: Clear description of workflow purpose and outcomes
tags:
  - workflow-category
  - domain-area
status: active | draft | deprecated
agents:
  - agent-name-1
  - agent-name-2
parameters:
  - name: param-name
    type: string | number | boolean
    required: true | false
    default: value
    description: Parameter purpose
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Critical YAML Syntax**: Values containing colons (`:`) must be quoted.

✅ **Good**:

```yaml
description: "Workflow name: detailed description here"
parameter: "key: value pairs"
```

❌ **Bad** (breaks YAML parsing):

```yaml
description: Workflow name: detailed description
```

### Workflow Content

````markdown
# Workflow Name

## Purpose

What this workflow accomplishes and when to use it.

## Agents Involved

- **agent-name-1**: Role and responsibility
- **agent-name-2**: Role and responsibility

## Input Parameters

| Parameter | Type   | Required | Default | Description |
| --------- | ------ | -------- | ------- | ----------- |
| param1    | string | Yes      | -       | Purpose     |
| param2    | number | No       | 5       | Purpose     |

## Execution Phases

### Phase 1: Name (Sequential)

1. Run agent-name-1 with parameters
2. Wait for completion
3. Run agent-name-2 with results from agent-name-1

### Phase 2: Name (Parallel)

Run in parallel:

- agent-name-3
- agent-name-4

Wait for all to complete before proceeding.

### Phase 3: Name (Conditional)

If condition A:

- Run agent-name-5
Else:
- Run agent-name-6

## Success Criteria

Define the criteria for successful execution of the workflow, using Gherkin syntax where applicable.
````