---
name: task-scaler
description: Evaluates task complexity and determines appropriate scale classification for workflow optimization
hooks:
  SessionStart:
    - type: command
      command: |
        if command -v yq &> /dev/null && [ -f ".claude/config.yaml" ]; then
          echo "=== Scale Configuration ==="
          yq -o=json '.task_scaling.thresholds' .claude/config.yaml 2>/dev/null || true
        fi
---

# Task Scaler

A technology-agnostic skill for evaluating task complexity and determining appropriate workflow scale.

## Core Purpose

Classify tasks into appropriate scale categories to optimize:
- Agent utilization
- Workflow complexity
- Resource allocation
- Token consumption

## Scale Classification

### Categories

```yaml
trivial:
  description: "Minimal changes with obvious implementation"
  characteristics:
    - Single-line or few-line changes
    - Typo fixes, whitespace corrections
    - Simple variable renames
    - Clear, obvious modifications
  metrics:
    lines_of_change: "< 3"
    files_affected: 1
    complexity_score: "< 5"
  workflow:
    direct_execution: true
    agents_required: 0
    rai_required: false
    deliverable_evaluation: false

small:
  description: "Single-component changes with clear scope"
  characteristics:
    - Single function implementation
    - Bug fix in one file
    - Simple feature addition
    - Minor refactoring
  metrics:
    lines_of_change: "3-50"
    files_affected: "1-3"
    complexity_score: "5-14"
  workflow:
    direct_execution: false
    agents_required: "1-2"
    rai_required: false
    deliverable_evaluation: true

medium:
  description: "Multi-component changes requiring coordination"
  characteristics:
    - Multiple function implementations
    - Cross-file changes
    - Feature with multiple components
    - Significant refactoring
  metrics:
    lines_of_change: "50-200"
    files_affected: "3-10"
    complexity_score: "15-29"
  workflow:
    direct_execution: false
    agents_required: "3-4"
    rai_required: true
    deliverable_evaluation: true

large:
  description: "Architectural changes with system-wide impact"
  characteristics:
    - Architecture modifications
    - New module or service
    - Multi-tenant considerations
    - System-wide impact
  metrics:
    lines_of_change: "200+"
    files_affected: "10+"
    complexity_score: "30+"
  workflow:
    direct_execution: false
    agents_required: "minimum needed"
    rai_required: true
    deliverable_evaluation: true
    full_workflow: true
```

## Complexity Scoring

### Scoring Factors

```yaml
factors:
  file_count:
    weight: 2
    calculation: "2 points per affected file"

  dependency_depth:
    weight: 3
    calculation: "3 points per dependency level"

  test_requirement:
    weight: 5
    calculation: "5 points if tests needed"

  user_interaction:
    weight: 3
    calculation: "3 points if user input needed"

  integration_complexity:
    weight: 4
    calculation: "4 points per external integration"

  database_changes:
    weight: 5
    calculation: "5 points if schema changes"
```

### Score Thresholds

```yaml
thresholds:
  trivial: "score < 5"
  small: "5 <= score < 15"
  medium: "15 <= score < 30"
  large: "score >= 30"
```

## Classification Algorithm

### Step 1: Initial Classification

```yaml
Parse user request for indicators:

trivial_indicators:
  keywords:
    - "typo", "fix typo", "correct spelling"
    - "whitespace", "formatting"
    - "single line", "one line"
  patterns:
    - Change target is explicit and simple
    - No logic changes required

small_indicators:
  keywords:
    - "add function", "implement method"
    - "fix bug", "resolve issue"
    - "single component", "one file"
  patterns:
    - Single component scope
    - Clear implementation path

medium_indicators:
  keywords:
    - "add feature", "implement"
    - "multiple components", "create tests"
    - "refactor"
  patterns:
    - Multiple files affected
    - Testing required

large_indicators:
  keywords:
    - "architecture", "system"
    - "new module", "new service"
    - "multi-tenant", "system-wide"
  patterns:
    - Architectural decisions needed
    - Broad impact scope
```

### Step 2: Complexity Analysis

```yaml
Analyze for complexity factors:
  1. Count estimated files affected
  2. Assess dependency depth
  3. Determine test requirements
  4. Identify user interaction needs
  5. Check for external integrations
  6. Evaluate database impact
  7. Calculate total score
```

### Step 3: Context Adjustments

```yaml
adjustments:
  scale_up_if:
    - "High integration with existing code"
    - "Ambiguous requirements"
    - "Multiple valid approaches"
    - "Security implications"

  scale_down_if:
    - "Established pattern/template exists"
    - "User provided detailed instructions"
    - "Similar change done recently"
    - "Well-documented requirements"
```

## Output Format

```yaml
scale_evaluation:
  task_scale: trivial|small|medium|large
  complexity_score: <number>

  factors:
    file_count: <number>
    dependency_depth: <number>
    test_required: true|false
    user_interaction: true|false
    integrations: <number>
    database_changes: true|false

  reasoning:
    initial_classification: "<based on keywords/patterns>"
    complexity_analysis: "<factor breakdown>"
    context_adjustments: "<any scale changes>"

  workflow_recommendation:
    agents_required: <number or range>
    rai_required: true|false
    parallel_possible: true|false
    estimated_iterations: <number>
```

## Anti-Fragmentation Principles

### Minimal Agent Usage

```yaml
principle: "Use minimum agents needed for task"

by_scale:
  trivial: "Direct execution, no agents"
  small: "1-2 agents maximum"
  medium: "3-4 agents, batch similar work"
  large: "Minimum needed, maximize parallel"

anti_pattern: "Using 5+ agents for every task"
```

### Purposeful Delegation

```yaml
valid_delegation_reasons:
  - "Specialized skill required"
  - "Session isolation needed"
  - "Parallel processing benefit"

invalid_delegation_reasons:
  - "Just in case"
  - "For confirmation"
  - "Protocol says so"
```

### Batch Similar Tasks

```yaml
batching_principle: "Group similar tasks for single agent"

example:
  bad: "3 file fixes → 3 separate agents"
  good: "3 file fixes → 1 agent batch"
```

## Integration

### Used By Agents

```yaml
primary_users:
  - task-scale-evaluator: "Core skill for scale assessment"
  - main-orchestrator: "Workflow routing decisions"

secondary_users:
  - workflow-orchestrator: "Progress estimation"
```

### Configuration Reference

```yaml
# Project-specific scaling overrides in .claude/config.yaml
task_scaling:
  thresholds:
    trivial_max: 5
    small_max: 15
    medium_max: 30

  adjustments:
    always_rai_for_scale: medium  # or large
    max_direct_execution_lines: 10
```

## Best Practices

1. **Be Conservative**: When uncertain, scale up
2. **Consider Context**: Same task varies by codebase familiarity
3. **Avoid Over-Engineering**: Match workflow to actual complexity
4. **Review History**: Similar tasks inform classification
5. **Account for Risk**: Security/data tasks scale up
