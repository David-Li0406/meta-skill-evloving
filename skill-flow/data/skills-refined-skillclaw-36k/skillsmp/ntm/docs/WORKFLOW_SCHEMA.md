# Workflow Schema Reference

NTM workflows define multi-step automation pipelines for orchestrating AI agents. This document describes the complete workflow schema for version 2.0.

## Table of Contents

- [Quick Start](#quick-start)
- [Root Structure](#root-structure)
- [Variables](#variables)
- [Settings](#settings)
- [Steps](#steps)
- [Agent Selection](#agent-selection)
- [Wait Configuration](#wait-configuration)
- [Error Handling](#error-handling)
- [Parallel Execution](#parallel-execution)
- [Conditional Steps](#conditional-steps)
- [Output Parsing](#output-parsing)
- [Variable Substitution](#variable-substitution)
- [Examples](#examples)

## Quick Start

```yaml
# minimal-workflow.yaml
schema_version: "2.0"
name: simple-review
description: Run a code review with Claude

steps:
  - id: review
    agent: claude
    prompt: Review the code in this repository for bugs and suggest improvements.
```

## Root Structure

```yaml
schema_version: "2.0"          # Required: Schema version
name: workflow-name            # Required: Unique identifier
description: What this does    # Optional: Human-readable description
version: "1.0"                 # Optional: Workflow version

vars:                          # Optional: Variable definitions
  var_name:
    description: What this is
    required: true
    default: null
    type: string

settings:                      # Optional: Global settings
  timeout: 30m
  on_error: fail
  notify_on_complete: true

steps:                         # Required: Step definitions
  - id: step_id
    # ... step configuration
```

## Variables

Variables allow workflows to be parameterized at runtime.

### Variable Definition

```yaml
vars:
  project_name:
    description: Name of the project to analyze
    required: true
    type: string

  max_files:
    description: Maximum files to process
    required: false
    default: 100
    type: number

  verbose:
    description: Enable verbose output
    default: false
    type: boolean

  file_patterns:
    description: File patterns to include
    default: ["*.go", "*.py"]
    type: array
```

### Variable Types

| Type | Description | Example Values |
|------|-------------|----------------|
| `string` | Text value | `"hello"`, `"path/to/file"` |
| `number` | Numeric value | `42`, `3.14` |
| `boolean` | True/false | `true`, `false` |
| `array` | List of values | `["a", "b", "c"]` |

### Providing Variables at Runtime

```bash
ntm pipeline run workflow.yaml --var project_name=myapp --var max_files=50
ntm pipeline run workflow.yaml --var-file vars.yaml
```

## Settings

Global settings apply to the entire workflow.

```yaml
settings:
  timeout: 30m                 # Global timeout for entire workflow
  on_error: fail               # fail | continue
  notify_on_complete: true     # Send notification on completion
  notify_on_error: true        # Send notification on error
  notify_channels:             # Notification channels
    - desktop
    - webhook
    - mail
  webhook_url: https://...     # Webhook endpoint
  mail_recipient: user         # Agent mail recipient
```

### Error Actions

| Action | Behavior |
|--------|----------|
| `fail` | Stop workflow immediately on error (default) |
| `continue` | Log error and continue to next step |

## Steps

Each step defines a unit of work in the workflow.

### Basic Step Structure

```yaml
steps:
  - id: step_id              # Required: Unique identifier
    name: Human Name         # Optional: Display name

    # Agent selection (choose one)
    agent: claude            # Agent type
    pane: 1                  # OR specific pane index
    route: least-loaded      # OR routing strategy

    # Prompt (choose one)
    prompt: |
      Inline prompt text
    prompt_file: prompts/step1.md

    # Wait configuration
    wait: completion
    timeout: 5m

    # Dependencies
    depends_on: [previous_step]

    # Error handling
    on_error: fail
    retry_count: 3
    retry_delay: 30s

    # Conditionals
    when: ${vars.run_tests}

    # Output handling
    output_var: result
    output_parse: json
```

## Agent Selection

Three ways to specify which agent should execute a step:

### By Agent Type

```yaml
- id: design
  agent: claude              # Use any Claude agent
  prompt: Design the API
```

Agent types:
- `claude` / `cc` / `claude-code`
- `codex` / `cod` / `openai`
- `gemini` / `gmi` / `google`

### By Pane Index

```yaml
- id: implement
  pane: 1                    # Use specific pane (0=user, 1+=agents)
  prompt: Implement the API
```

### By Routing Strategy

```yaml
- id: test
  route: least-loaded        # Smart agent selection
  prompt: Write tests
```

Routing strategies:
- `least-loaded` - Choose agent with lowest context usage
- `first-available` - Choose first idle agent
- `round-robin` - Rotate through agents

## Wait Configuration

Define when a step is considered complete:

```yaml
- id: step
  wait: completion           # Wait for agent to finish
  timeout: 5m                # Maximum wait time
```

### Wait Conditions

| Condition | Behavior |
|-----------|----------|
| `completion` | Wait for agent to return to idle state (default) |
| `idle` | Same as completion |
| `time` | Wait for timeout duration only |
| `none` | Fire and forget (don't wait) |

## Error Handling

### Step-Level Error Handling

```yaml
- id: flaky_step
  prompt: Call external API
  on_error: retry
  retry_count: 3
  retry_delay: 10s
  retry_backoff: exponential  # linear | exponential | none
```

### Retry Backoff

| Type | Behavior |
|------|----------|
| `none` | Fixed delay between retries |
| `linear` | Delay increases linearly (delay * attempt) |
| `exponential` | Delay doubles each attempt |

### Error Modes

| Mode | Behavior |
|------|----------|
| `fail` | Stop workflow, mark as failed |
| `continue` | Log error, continue to next step |
| `retry` | Retry step up to retry_count times |

## Parallel Execution

Run multiple steps concurrently using the `parallel` block:

```yaml
- id: parallel_work
  parallel:
    - id: research
      agent: claude
      prompt: Research the problem

    - id: prototype
      agent: codex
      prompt: Write initial code

    - id: review
      agent: gemini
      prompt: Review architecture

- id: combine
  depends_on: [parallel_work]
  prompt: |
    Combine results from:
    - Research: ${steps.research.output}
    - Prototype: ${steps.prototype.output}
    - Review: ${steps.review.output}
```

### Parallel Execution Rules

1. All parallel steps run concurrently on different agents
2. The parallel group completes when all sub-steps finish
3. If any sub-step fails, the group fails (unless `on_error: continue`)
4. Outputs are accessible via `${steps.<sub_id>.output}`

## Conditional Steps

Skip steps based on runtime conditions:

```yaml
- id: check_type
  prompt: Is this a bug fix? Reply YES or NO.
  output_var: is_bugfix
  output_parse: first_line

- id: run_tests
  when: ${vars.is_bugfix} == "YES"
  prompt: Run the test suite

- id: skip_tests
  when: ${vars.is_bugfix} == "NO"
  prompt: Skip tests, proceed to review
```

### Condition Syntax

- `${vars.variable}` - Check variable truthiness
- `${vars.x} == "value"` - String equality
- `${vars.count} > 10` - Numeric comparison
- Boolean operators: `&&`, `||`, `!`

## Output Parsing

Capture and parse step outputs for use in later steps:

```yaml
- id: get_data
  prompt: Return a JSON object with count and items
  output_var: data
  output_parse: json

- id: use_data
  prompt: Process ${vars.data.count} items
```

### Parse Types

| Type | Behavior |
|------|----------|
| `none` | Raw string (default) |
| `json` | Parse as JSON, access fields with dots |
| `yaml` | Parse as YAML |
| `lines` | Split into array by newlines |
| `first_line` | First line only |
| `regex` | Extract with named capture groups |

### Regex Parsing

```yaml
- id: extract
  prompt: The count is 42.
  output_var: result
  output_parse:
    type: regex
    pattern: "count is (?P<count>\\d+)"

- id: use
  prompt: Count was ${vars.result.count}
```

## Variable Substitution

Variables can be referenced throughout the workflow using `${...}` syntax.

### Variable Types

| Variable | Example | Description |
|----------|---------|-------------|
| `${vars.X}` | `${vars.name}` | User-provided variable |
| `${steps.X.output}` | `${steps.design.output}` | Raw step output |
| `${steps.X.pane}` | `${steps.design.pane}` | Pane ID used |
| `${steps.X.duration}` | `${steps.design.duration}` | Step duration |
| `${steps.X.status}` | `${steps.design.status}` | Step status |
| `${env.X}` | `${env.HOME}` | Environment variable |
| `${session}` | `myproject` | Session name |
| `${timestamp}` | `2025-01-15T10:00:00Z` | Current time |
| `${run_id}` | `abc123` | Pipeline run ID |
| `${workflow}` | `my-workflow` | Workflow name |

### Default Values

Provide fallback values for undefined variables:

```yaml
prompt: Hello ${vars.name | "World"}
```

### Escaping

Use backslash to include literal `${`:

```yaml
prompt: The syntax is \${variable}
```

## Examples

### Code Review Workflow

```yaml
schema_version: "2.0"
name: code-review
description: Automated code review with multiple agents

vars:
  branch:
    description: Branch to review
    required: true
    type: string

steps:
  - id: security_review
    agent: claude
    prompt: |
      Review the changes on branch ${vars.branch} for security issues.
      Focus on: injection, authentication, data exposure.
    output_var: security_issues

  - id: code_quality
    agent: codex
    prompt: |
      Review the changes on branch ${vars.branch} for code quality.
      Check: naming, structure, complexity, test coverage.
    output_var: quality_issues

  - id: compile_report
    agent: claude
    depends_on: [security_review, code_quality]
    prompt: |
      Compile a review report from:

      Security findings:
      ${vars.security_issues}

      Quality findings:
      ${vars.quality_issues}
```

### Red-Green-Refactor Workflow

```yaml
schema_version: "2.0"
name: red-green-refactor
description: TDD workflow with parallel test writing

steps:
  - id: write_test
    agent: claude
    prompt: Write a failing test for the new feature
    wait: completion

  - id: verify_red
    agent: codex
    depends_on: [write_test]
    prompt: Run the test and verify it fails
    output_var: test_result

  - id: implement
    agent: claude
    depends_on: [verify_red]
    when: ${vars.test_result} contains "FAIL"
    prompt: Implement the minimum code to pass the test

  - id: verify_green
    agent: codex
    depends_on: [implement]
    prompt: Run the test and verify it passes
    on_error: retry
    retry_count: 3

  - id: refactor
    agent: claude
    depends_on: [verify_green]
    prompt: Refactor the implementation while keeping tests green
```

### Parallel Investigation

```yaml
schema_version: "2.0"
name: parallel-investigate
description: Investigate an issue from multiple angles

vars:
  issue:
    description: Issue to investigate
    required: true

steps:
  - id: investigate
    parallel:
      - id: code_search
        agent: claude
        prompt: Search the codebase for code related to: ${vars.issue}

      - id: git_history
        agent: codex
        prompt: Check git history for changes related to: ${vars.issue}

      - id: log_search
        agent: gemini
        prompt: Search logs for errors related to: ${vars.issue}

  - id: synthesize
    depends_on: [investigate]
    agent: claude
    prompt: |
      Synthesize findings from parallel investigation:

      Code search: ${steps.code_search.output}
      Git history: ${steps.git_history.output}
      Log search: ${steps.log_search.output}

      Provide a root cause analysis.
```

## Schema Versioning

The `schema_version` field ensures forward compatibility. NTM will:

1. Validate workflows against the declared schema version
2. Warn if the workflow uses a newer schema than supported
3. Apply migrations for older schemas when possible

Current version: **2.0**
