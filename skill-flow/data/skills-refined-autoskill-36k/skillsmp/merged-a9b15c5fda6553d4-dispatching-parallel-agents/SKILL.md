---
name: dispatching-parallel-agents
description: Use this skill to execute multiple independent tasks simultaneously, maximizing throughput and efficiency through parallel agent coordination.
---

# Dispatching Parallel Agents

**Iron Law:** Only parallelize tasks that have NO dependencies. Sequentialize when outputs flow to inputs.

## When to Use

- Multiple independent features to implement
- Separate bugs to fix that don't interact
- Different components that can be worked on simultaneously
- Research across different domains
- Testing multiple hypotheses
- Tasks with shared state or dependencies should be executed sequentially

## The Process

1. **IDENTIFY**: Find parallelizable work
2. **VALIDATE**: Confirm independence
3. **STRUCTURE**: Prepare Task tool calls
4. **DISPATCH**: Execute in parallel
5. **COLLECT**: Gather results
6. **SYNTHESIZE**: Combine insights

## Step 1: Identify Parallelizable Work

### Good Candidates for Parallel Execution

- Independent features: Authentication and payment systems
- Separate components: Frontend and backend work
- Different skill domains: Code review while writing documentation
- Isolated bug fixes: Login bug and API bug

### Bad Candidates (Must Be Sequential)

- Dependent features: Database migration then seeder
- Tasks modifying the same files
- Tasks with shared resources or data dependencies

## Step 2: Validate Independence

### Dependency Analysis Checklist

Before parallelizing, ask:
- Do these tasks touch the same files?
- Does Task B need Task A's results?
- Will these tasks create merge conflicts?
- Are there shared resources (database, cache, files)?
- Can these tasks be independently tested?

**If ANY answer is YES → Do NOT parallelize**

## Step 3: Structure Parallel Task Calls

**Single Message, Multiple Task Invocations:**

```markdown
Task: @agent1
## Task Description A
Instructions for Task A...

---

Task: @agent2
## Task Description B
Instructions for Task B...

---

Task: @agent3
## Task Description C
Instructions for Task C...
```

## Step 4: Dispatch Execution

**Execution Patterns:**

### Homogeneous (Same Agent Type)

```markdown
Task: @agent
Task A...

Task: @agent
Task B...

Task: @agent
Task C...
```

### Heterogeneous (Different Agent Types)

```markdown
Task: @agent1
Task A...

Task: @agent2
Task B...

Task: @agent3
Task C...
```

## Step 5: Result Collection

**Collect from each parallel task:**

```markdown
## Results: [Task Name]

### Agent: [agent-name]
### Status: SUCCESS | PARTIAL | FAILED

### Findings:
- Key finding 1
- Key finding 2

### Artifacts:
- File: /path/to/output.md

### Recommendations:
- Recommendation 1
```

## Step 6: Result Synthesis

**Combining Parallel Results:**

```markdown
## Synthesis: [Feature/Research Area]

### Completed Tasks: X/Y

### Aggregated Findings:
| Topic | Key Insight |
|-------|-------------|
| Topic A | Insight A |
| Topic B | Insight B |

### Recommended Next Steps:
1. Next step 1
2. Next step 2
```

## Error Handling

### Partial Failures

```markdown
## Parallel Execution Summary

### Succeeded: X/Y
- [x] Task A - Complete
- [ ] Task B - FAILED

### Failure Analysis:
- Task: Task B
- Error: Description of error
```

### Timeout Handling

```markdown
## Timeout Handling

### Completed: X/Y
### Timed Out: Y/Z

### Action:
- Preserve completed results
- Document timeout: Task B exceeded time limit
```

## Best Practices

- Verify independence before parallelizing
- Use single message with multiple Task calls
- Balance workload across agents
- Handle failures gracefully

## Red Flags

- Parallel tasks modifying the same file
- Missing independence validation
- Not waiting for all results

## Your Commitment

Before dispatching parallel agents:
- I have analyzed dependencies thoroughly
- I am certain tasks are independent
- I have a plan for integration
- I will monitor progress

---

**Bottom Line**: Parallel agents are powerful when tasks are truly independent. Analyze dependencies first, dispatch in parallel, and integrate carefully to achieve significant time reductions.