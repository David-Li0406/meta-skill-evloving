# Subagent Coordination Patterns

## Table of Contents

- [🚨 MANDATORY: Read BEFORE Coordination](#mandatory-read-before-coordination)
- [Coordination Patterns](#coordination-patterns)
- [State Management](#state-management)
- [Implementation Guide](#implementation-guide)
- [Error Handling](#error-handling)
- [Performance Optimization](#performance-optimization)
- [Best Practices](#best-practices)
- [Pattern Summary](#pattern-summary)
- [Complete Examples](#complete-examples)
- [Related Skills](#related-skills)

Coordinate multiple subagents using proven patterns and state management strategies.

## 🚨 MANDATORY: Read BEFORE Coordination

**CRITICAL**: You MUST read and understand these URLs:

### Primary Documentation (MUST READ)
- **[MUST READ] Official Subagents Guide**: https://code.claude.com/docs/en/sub-agents
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: Before subagent coordination
  - **Content**: Agent coordination patterns, state management, orchestration
  - **Cache**: 15 minutes minimum

- **[MUST READ] Task Tool Documentation**: https://code.claude.com/docs/en/cli-reference
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: Before using Task tool
  - **Content**: Task tool usage, subagent types, invocation patterns
  - **Cache**: 15 minutes minimum

### ⚠️ BLOCKING RULES
- **DO NOT proceed** without understanding coordination needs
- **MUST validate** pattern selection before implementation
- **REQUIRED** to understand state management requirements

## Coordination Patterns

### Pattern 1: Orchestrator-Worker
**Description**: Central coordination with specialized workers

**Use When**:
- Central coordinator manages multiple specialists
- Workers handle specific domains
- Orchestrator delegates and combines results

**Example**:
```yaml
---
name: orchestrator
description: "Coordinate multiple specialists"
context: fork
agent: Plan
---

Orchestrate workflow:
1. Delegate to code-analyzer agent
2. Delegate to test-specialist agent
3. Delegate to doc-generator agent
4. Combine results into final report
```

### Pattern 2: Pipeline
**Description**: Sequential data transformation

**Use When**:
- Sequential processing stages
- Output of one stage feeds next
- Linear workflow

**Example**:
```yaml
---
name: data-pipeline
description: "Process data through sequential stages"
context: fork
agent: Plan
---

Pipeline stages:
Stage 1: Analyze → Stage 2: Transform → Stage 3: Validate → Result
```

### Pattern 3: Parallel
**Description**: Independent concurrent work

**Use When**:
- Independent tasks
- Can run simultaneously
- Results combined later

**Example**:
```yaml
---
name: parallel-analysis
description: "Analyze components in parallel"
context: fork
agent: Plan
---

Parallel execution:
Task A: Analyze frontend code (Explore)
Task B: Analyze backend code (Explore)
Task C: Analyze database schema (Explore)
Combine all results
```

### Pattern 4: Handoff
**Description**: Context transfer to specialists

**Use When**:
- Specialized expertise needed
- Context transferred to specialist
- Specialist completes and returns

**Example**:
```yaml
---
name: handoff-workflow
description: "Handoff to specialist and receive results"
context: fork
agent: Plan
---

Handoff pattern:
1. Prepare context for specialist
2. Handoff to security-specialist (Explore)
3. Receive and process results
4. Continue main workflow
```

### Context: Fork Mechanism

**CRITICAL**: Understanding forked subagent execution:

In a context: fork Skill run, the forked subagent's system prompt comes from the chosen agent (built-in or custom), while the Skill's SKILL.md becomes the task prompt that drives that subagent. If the chosen custom subagent also has `skills:` configured, those Skills' full contents are also injected into that forked subagent's context at startup—they don't get "replaced" by the forked Skill; they sit alongside it.

**Composition Model**:
```yaml
# Forked Skill + Custom Subagent = Combined Context
System Prompt: From chosen agent (Explore, Plan, Bash, custom)
Task Prompt: From forked Skill's SKILL.md
Additional Skills: From custom subagent's skills: config (injected at startup)

# Result: Additive context, not replacement
```

**Design Implications**:
- Skills from custom subagent remain active alongside forked Skill
- No skill conflicts—each contributes its domain expertise
- Custom subagent's built-in capabilities stay intact
- Forked Skill provides specific task direction

## State Management

### 1. Shared State Store
Centralized state accessible to all agents

```yaml
# Shared state in orchestrator
shared_state = {
    "findings": [],
    "recommendations": [],
    "metrics": {}
}

# Workers update shared state
worker_1.update("findings", [...])
worker_2.update("metrics", {...})
```

### 2. Message Chain
Sequential passing of state

```yaml
# Stage 1 output
stage_1_result = process(input)

# Stage 2 input
stage_2_result = transform(stage_1_result)

# Stage 3 input
final_result = validate(stage_2_result)
```

### 3. Hybrid
Combine shared state and message chain

```yaml
# Shared configuration
shared_config = {...}

# Sequential processing
result = stage_1(input, shared_config)
result = stage_2(result, shared_config)
result = stage_3(result, shared_config)
```

## Implementation Guide

### Step 1: Choose Pattern
- Analyze coordination requirements
- Select appropriate pattern:
  - Orchestrator-Worker: For centralized coordination
  - Pipeline: For sequential data transformation
  - Parallel: For independent concurrent work
  - Handoff: For context transfer to specialists

### Step 2: Design State Management
- Determine state sharing needs
- Choose approach:
  - Shared state: For central coordination
  - Message chain: For linear workflows
  - Hybrid: For complex workflows

### Step 3: Implement Coordination
```yaml
---
name: coordinated-analysis
description: "Coordinate multiple specialists"
context: fork
agent: Plan
---

Coordinate workflow:
1. Delegate to code-analyzer
2. Delegate to test-specialist
3. Combine results
```

### Step 4: Test Coordination
- Verify pattern implementation
- Test state management
- Validate isolation and autonomy
- Check result combination

## Error Handling

### Failure Propagation
```yaml
# Handle agent failures
try:
    result = await delegate_to_agent(task)
except Exception as e:
    # Handle error
    logger.error(f"Agent failed: {e}")
    # Decide: retry, continue, or abort
```

### Retry Logic
```yaml
# Retry failed tasks
for attempt in range(3):
    try:
        result = await delegate_to_agent(task)
        break
    except Exception:
        if attempt == 2:
            raise
```

## Performance Optimization

### Minimize Spawns
- Limit subagent spawns
- Batch similar operations
- Reuse agents when possible

### Efficient Communication
- Minimize data transfer
- Send structured summaries
- Avoid raw file dumps

## Best Practices

### DO ✅
- Choose appropriate coordination pattern
- Design clear state management
- Limit parallel subagent spawns
- Implement error handling
- Test coordination thoroughly

### DON'T ❌
- Don't over-coordinate simple tasks
- Don't share unnecessary state
- Don't ignore failure modes
- Don't spawn excessive subagents

## Pattern Summary

| Pattern             | Use Case              | State         | Complexity |
| ------------------- | --------------------- | ------------- | ---------- |
| Orchestrator-Worker | Multiple specialists  | Shared        | Medium     |
| Pipeline            | Sequential processing | Message chain | Low        |
| Parallel            | Independent tasks     | Minimal       | Medium     |
| Handoff            | Specialized expertise | Transfer      | Low        |

## Complete Examples

See **examples.md** for:
- Full implementation examples
- Multi-stage orchestration
- Context management patterns
- Advanced coordination strategies

## Related Skills

- **[when-to-use.md](when-to-use.md)** - When to use subagents
- **meta-architect-claudecode** - Layer selection
