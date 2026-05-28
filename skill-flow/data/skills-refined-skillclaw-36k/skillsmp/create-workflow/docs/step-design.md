# Step Design Guide

Detailed guidance for designing workflow steps.

## Step Types

### Action Steps

Use for: doing something, executing commands, producing output.

```yaml
- type: action
  content: |
    Run the tests and fix any failures.
    Use: npm test
```

**Best practices:**
- Start with a verb (Run, Create, Review, Update)
- Include the command if there's a specific one
- Can be multiline for complex instructions

### Check Steps

Use for: verifying a condition, gates that must pass.

```yaml
- type: check
  content: All tests pass
  on_fail: Fix failing tests before proceeding
```

**Best practices:**
- State the condition positively (what should be true)
- `on_fail` describes what to do if condition is false
- Keep checks binary - either it passes or it doesn't

### Decision Steps

Use for: choosing between paths, user/agent judgment calls.

```yaml
- type: decision
  content: What type of change is this?
  options:
    - "Bug fix - use fix/ branch prefix"
    - "New feature - use feat/ branch prefix"
    - "Refactor - use refactor/ branch prefix"
```

**Best practices:**
- Phrase as a question
- 2-4 options that cover the likely cases
- Each option can include guidance on what to do

## Step Content

Content can be multiline using YAML `|` syntax:

```yaml
content: |
  First line of instructions.
  Second line with more detail.

  Can include blank lines for readability.
  - Bullet points work too
  - Another point
```

**Guidelines:**
- First line should be the main instruction
- Additional lines provide context/detail
- Include commands when specific ones are needed
- Reference docs for complex guidance: See [Doc Name](docs/file.md)

## Entry & Exit Criteria

Use criteria when a step needs verification:

```yaml
- type: action
  content: Search for existing coverage
  entry_criteria:
    - Have identified friction points to search for
  exit_criteria:
    - Searched specs for relevant features
    - Searched tasks for existing work
    - Searched inbox for captured ideas
```

**When to use:**
- Entry criteria: step has prerequisites
- Exit criteria: step has specific things that must be done

**Enforcement modes:**
- `advisory` (default): criteria shown as guidance
- `strict`: requires `--confirm` flag to proceed

## Step Inputs

Capture structured data at a step:

```yaml
- type: action
  content: Choose a task to work on
  inputs:
    - name: task_ref
      description: Reference to the task
      type: ref
    - name: approach
      description: Brief description of your approach
      type: string
      required: true
    - name: notes
      description: Any additional context
      type: string
      required: false
```

**Input properties:**
- `name`: key for the input (used in --input name=value)
- `description`: shown to user when input is required
- `type`: `string` (default), `ref`, or `number`
- `required`: `true` (default) or `false`

**When to use inputs:**
- Capturing decisions for audit trail
- Data needed by later steps
- Structured info vs free-form notes

## Patterns

### Sequential Actions

```yaml
steps:
  - type: action
    content: Step 1
  - type: action
    content: Step 2
  - type: action
    content: Step 3
```

### Gate Pattern

```yaml
steps:
  - type: action
    content: Make changes
  - type: check
    content: Changes are valid
    on_fail: Fix validation errors
  - type: action
    content: Commit changes
```

### Branch Pattern

```yaml
steps:
  - type: decision
    content: What type of work?
    options:
      - "Type A - do X"
      - "Type B - do Y"
  - type: action
    content: Proceed based on decision above
```

### Capture Pattern

```yaml
steps:
  - type: action
    content: Identify items
  - type: action
    content: Discuss with user
    inputs:
      - name: approved_items
        description: Comma-separated list of approved items
  - type: action
    content: Capture approved items
```
