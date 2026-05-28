# Collaboration Skill Domain

This skill domain provides behavioral workflows and collaboration patterns for code review, agent coordination, and development process management.

## Purpose

The collaboration skill groups six related behavioral skills that were previously top-level skills. These skills focus on **process and coordination** rather than technical implementation, making them distinct from domain-specific skills like frontend-design or test-driven-development.

## Why These Skills Are Grouped Together

All six workflows share common characteristics:

1. **Process-Oriented** - Guide how to work, not what to build
2. **Domain-Independent** - Apply across all technical domains
3. **Coordination-Focused** - Manage multi-agent workflows and reviews
4. **Behavioral** - Define patterns for handling feedback and decisions
5. **Quality-Enhancing** - Layer on top of domain skills for better outcomes

## Available Workflows

### Code Review Workflows

**Request Review** (`workflows/request-review.md`)
- **When**: After completing tasks, implementing features, or before merging
- **Purpose**: Dispatch code-reviewer subagent to validate implementation
- **Benefit**: Catch issues before they cascade into larger problems

**Receive Review** (`workflows/receive-review.md`)
- **When**: Receiving code review feedback, especially if unclear or questionable
- **Purpose**: Process feedback with technical rigor, not performative agreement
- **Benefit**: Ensures thoughtful implementation vs blind acceptance

### Agent Coordination Workflows

**Dispatch Parallel Agents** (`workflows/dispatch-agents.md`)
- **When**: Facing 3+ independent failures without shared state or dependencies
- **Purpose**: Use multiple Claude agents to investigate problems concurrently
- **Benefit**: Accelerates resolution of unrelated issues

**Subagent-Driven Development** (`workflows/subagent-dev.md`)
- **When**: Executing implementation plans with independent tasks
- **Purpose**: Dispatch fresh subagents for each task with review gates between
- **Benefit**: Maintains focus, enables parallel progress, catches issues early

### Development Process Workflows

**Finish Development Branch** (`workflows/finish-branch.md`)
- **When**: Implementation is complete, tests pass, ready to integrate
- **Purpose**: Complete feature development with structured options (merge, PR, cleanup)
- **Benefit**: Provides clear decision framework for branch completion

**Preserve Productive Tensions** (`workflows/preserve-tensions.md`)
- **When**: Oscillating between equally valid approaches with different priorities
- **Purpose**: Recognize when disagreements reveal valuable context
- **Benefit**: Preserves multiple valid approaches vs forcing premature resolution

## Common Usage Patterns

### Feature Development Lifecycle

```
1. Plan feature implementation
2. Use subagent-dev to execute tasks in parallel
3. Request review after each task completion
4. Receive and process review feedback
5. Finish branch when all work is validated
```

### Parallel Investigation

```
1. Identify 3+ independent failures
2. Dispatch parallel agents to investigate each
3. Collect findings from all agents
4. Request review of proposed fixes
5. Implement validated solutions
```

### Handling Productive Disagreement

```
1. Notice oscillation between valid approaches
2. Preserve tensions to capture both perspectives
3. Document trade-offs and priorities
4. Choose approach based on current context
5. Request review to validate decision
```

## Workflow Relationships

**Paired Workflows:**
- `request-review` + `receive-review` = Complete code review cycle
- `dispatch-agents` + `subagent-dev` = Parallel work coordination

**Sequential Workflows:**
- `subagent-dev` → `request-review` → `receive-review` → `finish-branch`

**Cross-Cutting:**
- `preserve-tensions` applies throughout all workflows (decision-making)

## Integration with Domain Skills

Collaboration workflows complement domain-specific skills:

- **With frontend-design**: Request review after implementing UI components
- **With test-driven-development**: Use subagent-dev to implement test-first workflows
- **With specification-writing**: Request review of generated documents
- **With any technical work**: Finish branch when feature is complete

The collaboration domain provides the **how** of working effectively, while domain skills provide the **what** of technical implementation.

## When to Use Each Workflow

### Just Completed Implementation
1. **All tests passing, ready to integrate?** → `finish-branch`
2. **Want validation before proceeding?** → `request-review`
3. **Received feedback to process?** → `receive-review`

### Managing Multiple Tasks
1. **Executing a multi-task plan?** → `subagent-dev`
2. **Multiple independent failures?** → `dispatch-agents`

### Facing Disagreement or Uncertainty
1. **Oscillating between valid approaches?** → `preserve-tensions`
2. **Review feedback seems questionable?** → `receive-review`

## Migration from Top-Level Skills

This skill consolidates six previously top-level skills:

| Old Path | New Path | Notes |
|----------|----------|-------|
| `requesting-code-review/` | `workflows/request-review.md` | Content preserved exactly |
| `receiving-code-review/` | `workflows/receive-review.md` | Content preserved exactly |
| `dispatching-parallel-agents/` | `workflows/dispatch-agents.md` | Content preserved exactly |
| `subagent-driven-development/` | `workflows/subagent-dev.md` | Content preserved exactly |
| `finishing-a-development-branch/` | `workflows/finish-branch.md` | Content preserved exactly |
| `preserving-productive-tensions/` | `workflows/preserve-tensions.md` | Content preserved exactly |

The old skill directories remain temporarily for backward compatibility. All functionality has been preserved - this is purely a reorganization for better discoverability.

## Key Design Principles

1. **No Functionality Changes** - All workflow content preserved exactly
2. **Better Discoverability** - Related skills grouped in one domain
3. **Clear Domain Boundary** - Process/coordination vs technical implementation
4. **Easy to Extend** - Add new collaboration patterns to clear location
5. **Backward Compatible** - Old paths still work during transition period

## Notes

- These workflows can be combined - request review during subagent-dev
- Not all workflows apply to every situation - use judgment
- Collaboration skills enhance but don't replace technical judgment
- When in doubt, requesting review is rarely wrong
