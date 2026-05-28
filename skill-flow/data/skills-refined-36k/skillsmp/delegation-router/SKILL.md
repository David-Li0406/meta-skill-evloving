---
name: delegation-router
description: Determines appropriate agent routing based on task type, scale, and agent capabilities
---

# Delegation Router

A technology-agnostic skill for determining which agent should handle a given task or subtask.

## Core Purpose

Route tasks to the most appropriate agent based on:
- Task type and requirements
- Agent capabilities and specializations
- Workflow state and dependencies
- Resource efficiency

## Agent Routing Matrix

### Core Agents and Their Domains

```yaml
main-orchestrator:
  domain: "User interface and workflow initiation"
  receives_from:
    - "User directly"
  delegates_to:
    - task-scale-evaluator
    - goal-clarifier
    - workflow-orchestrator
  handles_directly:
    - "Trivial read/search tasks"
    - "Result summarization"

task-scale-evaluator:
  domain: "Task complexity assessment"
  receives_from:
    - main-orchestrator
  delegates_to:
    - workflow-orchestrator  # Automatic chain via SubagentStop hook
  handles_directly:
    - "Scale classification"
    - "Workflow recommendation"

goal-clarifier:
  domain: "Intent clarification and acceptance criteria drafts"
  receives_from:
    - main-orchestrator
  delegates_to: null  # Returns clarification to caller
  handles_directly:
    - "Ambiguity resolution"
    - "Quick acceptance criteria generation"

workflow-orchestrator:
  domain: "Workflow coordination and Git operations"
  receives_from:
    - main-orchestrator
    - deliverable-evaluator (on PASS)
  delegates_to:
    - design-architect
    - code-developer
    - quality-reviewer
    - deliverable-evaluator
  handles_directly:
    - "Progress tracking"
    - "Git commit/push"
    - "Agent coordination"

design-architect:
  domain: "Architecture and design specifications"
  receives_from:
    - workflow-orchestrator
  delegates_to: null
  handles_directly:
    - "Architecture design"
    - "Component specification"

code-developer:
  domain: "Code implementation"
  receives_from:
    - workflow-orchestrator
    - test-debugger (fix recommendations)
  delegates_to:
    - test-executor (after implementation)
  handles_directly:
    - "Feature implementation"
    - "Bug fixes"
    - "Test code creation"

test-executor:
  domain: "Test execution and result analysis"
  receives_from:
    - code-developer (automatic chain)
  delegates_to:
    - test-debugger (on failures)
  handles_directly:
    - "Test suite execution"
    - "Result categorization"

test-debugger:
  domain: "Test failure analysis"
  receives_from:
    - test-executor
  delegates_to:
    - code-developer (fix implementation)
  handles_directly:
    - "Root cause analysis"
    - "Fix recommendations"

quality-reviewer:
  domain: "Code quality assessment"
  receives_from:
    - workflow-orchestrator
  delegates_to: null
  handles_directly:
    - "Code review"
    - "Quality scoring"

deliverable-evaluator:
  domain: "Final deliverable evaluation"
  receives_from:
    - workflow-orchestrator
  delegates_to:
    - workflow-orchestrator (on PASS, for commit)
    - assigned agent (on FAIL, for rework)
  handles_directly:
    - "Acceptance criteria evaluation"
    - "Pass/fail verdict"
```

## Routing Decision Logic

### By Task Type

```yaml
task_type_routing:
  code_implementation:
    primary: code-developer
    prerequisites:
      large_tasks: [design-architect]
    followup: [test-executor, quality-reviewer]

  bug_fix:
    primary: code-developer
    prerequisites: []
    followup: [test-executor]

  test_execution:
    primary: test-executor
    on_failure: test-debugger
    on_success: quality-reviewer

  quality_review:
    primary: quality-reviewer
    on_issues: code-developer
    on_pass: deliverable-evaluator

  git_operations:
    exclusive: workflow-orchestrator
    never: [code-developer, test-executor]

  requirements:
    simple: goal-clarifier
    complex: goal-clarifier

  architecture:
    primary: design-architect
    when: "New module or significant changes"
```

### By Task Scale

```yaml
scale_routing:
  trivial:
    can_handle: [main-orchestrator]
    skip: [workflow-orchestrator, design-architect, quality-reviewer]

  # All non-trivial tasks go through workflow-orchestrator (automatic chain from task-scale-evaluator)
  small:
    entry_point: workflow-orchestrator
    required: [code-developer, test-executor, deliverable-evaluator]
    optional: [quality-reviewer]
    skip: [design-architect]

  medium:
    entry_point: workflow-orchestrator
    required: [code-developer, test-executor, quality-reviewer, deliverable-evaluator]
    optional: [design-architect]

  large:
    entry_point: workflow-orchestrator
    required: [design-architect, code-developer, test-executor, quality-reviewer, deliverable-evaluator]
    iterative: true
```

### Chain Patterns

```yaml
common_chains:
  standard_implementation:
    - workflow-orchestrator
    - code-developer
    - test-executor
    - quality-reviewer
    - deliverable-evaluator

  with_debugging:
    - workflow-orchestrator
    - code-developer
    - test-executor
    - test-debugger  # on failure
    - code-developer  # apply fix
    - test-executor  # verify
    - quality-reviewer
    - deliverable-evaluator

  full_feature:
    - workflow-orchestrator
    - design-architect
    - code-developer
    - test-executor
    - quality-reviewer
    - deliverable-evaluator
```

## Routing Algorithm

### Step 1: Identify Task Type

```yaml
classify_task:
  implementation:
    indicators: ["implement", "add", "create", "build"]
  bug_fix:
    indicators: ["fix", "resolve", "correct", "debug"]
  review:
    indicators: ["review", "check", "assess"]
  test:
    indicators: ["test", "verify", "validate"]
  git:
    indicators: ["commit", "push", "branch"]
  requirements:
    indicators: ["clarify", "define", "specify"]
```

### Step 2: Check Scale Requirements

```yaml
scale_check:
  - Get scale from task-scale-evaluator
  - Apply scale_routing rules
  - Identify required agents
  - Identify optional agents
```

### Step 3: Determine Sequence

```yaml
sequence_rules:
  dependencies_first:
    - design-architect before code-developer (large)
    - code-developer before test-executor

  parallel_when_possible:
    - "Independent subtasks can run in parallel"
    - "Example: multiple file fixes"

  iterative_when_needed:
    - "test-debugger → code-developer loop"
    - "deliverable-evaluator → rework loop"
```

### Step 4: Generate Routing Plan

```yaml
routing_plan:
  sequential:
    - agent: "<agent_name>"
      task: "<specific task>"
      depends_on: ["<previous agents>"]

  parallel_groups:
    - group: 1
      agents: ["<independent agents>"]
    - group: 2
      agents: ["<agents depending on group 1>"]
```

## Output Format

```yaml
routing_decision:
  task_type: "<classified type>"
  scale: "<task scale>"

  routing_plan:
    - step: 1
      agent: "<agent_name>"
      task: "<what to do>"
      required: true|false
      depends_on: []

    - step: 2
      agent: "<agent_name>"
      task: "<what to do>"
      required: true|false
      depends_on: [1]

  chain_pattern: "<pattern name if applicable>"

  skip_agents:
    - agent: "<agent_name>"
      reason: "<why skipped>"

  parallel_opportunities:
    - group: ["<agent1>", "<agent2>"]
      reason: "<why parallel is possible>"
```

## Prohibited Routing

```yaml
never_route:
  git_operations:
    to: [code-developer, test-executor, quality-reviewer]
    exclusive: workflow-orchestrator

  implementation:
    to: [main-orchestrator, workflow-orchestrator]
    exclusive: code-developer

  quality_judgment:
    to: [main-orchestrator, code-developer]
    exclusive: [quality-reviewer, deliverable-evaluator]
```

## Integration

### Used By Agents

```yaml
primary_users:
  - main-orchestrator: "Initial routing decisions"
  - workflow-orchestrator: "Chain management"

secondary_users:
  - task-scale-evaluator: "Routing recommendations"
```

### Configuration Reference

```yaml
# Project-specific routing in .claude/config.yaml
delegation:
  custom_routes:
    specific_task_type:
      primary: custom-agent
      fallback: default-agent

  disabled_agents:
    - "design-architect"  # Small projects may skip

  required_agents:
    - "deliverable-evaluator"  # Always required
```
