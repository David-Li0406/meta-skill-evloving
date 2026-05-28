---
name: exploration
description: Explore codebase based on complexity level
order: 3

skip_if:
  - flag: "--continue"
  - flag: "--refine-plan"
  - condition: "complexity == 'SIMPLE'"

next:
  default: create-plan

tools:
  - Read
  - Glob
  - Grep
  - Task
---

# Step: Exploration

<context>
This step explores the codebase to gather context for implementation planning.
The exploration depth depends on the complexity level determined in the previous step.
</context>

## Instructions

<instructions>

### 1. Determine Exploration Depth

Read `complexity` from status.json:

| Complexity | Action |
|------------|--------|
| SIMPLE | Skip this step entirely |
| MEDIUM | 1 explore agent, focused search |
| COMPLEX | Up to 3 parallel explore agents (AEP) |

### 2. MEDIUM: Light Exploration

Launch 1 explore agent:

```yaml
Task:
  subagent_type: Explore
  prompt: |
    Explore the codebase for ticket {ticket-id}.
    Ticket summary: {title}

    Find:
    1. Similar existing code patterns
    2. Files that will need modification
    3. Test patterns used in similar features

    Ticket details in: .claude/feature/{ticket-id}/ticket.md
```

### 3. COMPLEX: Full AEP Exploration

Launch 3 parallel explore agents:

**Agent 1: Implementation Patterns**
```yaml
Task:
  subagent_type: Explore
  prompt: |
    Search for similar features and implementation patterns.
    Find reusable code and coding conventions.
    Ticket: {ticket-id} - {title}
```

**Agent 2: Impact Analysis**
```yaml
Task:
  subagent_type: Explore
  prompt: |
    Trace dependencies and find all affected components.
    Check for potential breaking changes.
    Ticket: {ticket-id} - {title}
```

**Agent 3: Test Coverage**
```yaml
Task:
  subagent_type: Explore
  prompt: |
    Find related tests and testing patterns.
    Identify test utilities and fixtures.
    Ticket: {ticket-id} - {title}
```

### 4. Consolidate Findings

Append exploration results to `.claude/feature/{ticket-id}/analysis.md`:

```markdown
## Exploration Results

### Implementation Patterns
{agent 1 findings}

### Impact Analysis
{agent 2 findings}

### Test Coverage
{agent 3 findings}
```

### 5. Update Status

Update status: `phases.exploration = "completed"`

</instructions>

## Output

<output>
- File updated: `.claude/feature/{ticket-id}/analysis.md`
- Status: `phases.exploration = "completed"`
</output>

## Auto Behavior

<auto_behavior>
- Run exploration without user interaction
- Proceed to planning when complete
</auto_behavior>

## Interactive Behavior

<interactive_behavior>
- Display exploration progress
- Show key findings summary before continuing
</interactive_behavior>
