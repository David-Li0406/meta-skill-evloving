---
name: dispatching-parallel-agents
description: "Use when multiple independent tasks can run simultaneously. Maximizes throughput through parallel Task tool invocations."
---

# Dispatching Parallel Agents

**Iron Law:** Parallelize when tasks have NO dependencies. Sequentialize when outputs flow to inputs.

## When to Use

| Scenario | Use This Skill |
|----------|----------------|
| Multiple independent research tasks | YES |
| Exploring different solution approaches | YES |
| Validating across multiple files/domains | YES |
| Testing multiple hypotheses | YES |
| Tasks with shared state/dependencies | NO - use sequential |
| Output of task A is input to task B | NO - use sequential |

## The Process

```
1. IDENTIFY   -> Find parallelizable work
2. VALIDATE   -> Confirm independence
3. STRUCTURE  -> Prepare Task tool calls
4. DISPATCH   -> Execute in parallel
5. COLLECT    -> Gather results
6. SYNTHESIZE -> Combine insights
```

## Step 1: Identify Parallelizable Work

**Good Candidates:**

```markdown
## Feature: Multi-Platform Integration

### Parallelizable:
- [ ] Research Stripe API patterns (deep-researcher)
- [ ] Research SendGrid email patterns (deep-researcher)
- [ ] Research Twilio SMS patterns (deep-researcher)

### Sequential (depends on above):
- [ ] Design unified integration layer (backend-engineer)
```

**Parallelization Checklist:**
- [ ] Tasks don't modify same files
- [ ] Tasks don't depend on each other's output
- [ ] Tasks don't require shared state
- [ ] Order of completion doesn't matter
- [ ] Failures can be handled independently

## Step 2: Validate Independence

**Dependency Matrix:**

| Task | Reads | Writes | Blocks | Blocked By |
|------|-------|--------|--------|------------|
| Research A | docs | notes | - | - |
| Research B | docs | notes | - | - |
| Implement | code | code | Research A, B | - |

**Independence Rules:**
- Read-only tasks are always parallelizable
- Write tasks to DIFFERENT files are parallelizable
- Write tasks to SAME files are NOT parallelizable
- Tasks with upstream dependencies are NOT parallelizable

## Step 3: Structure Parallel Task Calls

**Single Message, Multiple Task Invocations:**

```markdown
I'll dispatch three research tasks in parallel.

Task: @deep-researcher
## Research: Stripe Payment Patterns
Load skills: documentation-research, api-design
Investigate best practices for Stripe webhook handling,
idempotency, and error recovery.

---

Task: @deep-researcher
## Research: SendGrid Email Patterns
Load skills: documentation-research, api-design
Investigate best practices for SendGrid template management,
tracking, and bounce handling.

---

Task: @deep-researcher
## Research: Twilio SMS Patterns
Load skills: documentation-research, api-design
Investigate best practices for Twilio message delivery,
status callbacks, and rate limiting.
```

**Structuring Rules:**
- All Task invocations in SAME message
- Each task gets complete, independent context
- Include all required skills per task
- Define clear deliverables per task
- Specify consistent output format

## Step 4: Dispatch Execution

**Execution Patterns:**

### Pattern A: Homogeneous (Same Agent Type)

```markdown
Task: @deep-researcher
Research topic A...

Task: @deep-researcher
Research topic B...

Task: @deep-researcher
Research topic C...
```

Use when: Same type of work across different domains.

### Pattern B: Heterogeneous (Different Agent Types)

```markdown
Task: @security-auditor
Audit authentication flow...

Task: @performance-optimizer
Analyze bundle size...

Task: @quality-engineer
Review test coverage...
```

Use when: Different expertise needed for independent validations.

### Pattern C: Exploration (Multiple Approaches)

```markdown
Task: @backend-engineer
Implement using approach A (Redux)...

Task: @backend-engineer
Implement using approach B (Zustand)...

Task: @backend-engineer
Implement using approach C (Jotai)...
```

Use when: Evaluating different solutions before committing.

## Step 5: Result Collection

**Collect from each parallel task:**

```markdown
## Results: [Task Name]

### Agent: [agent-name]
### Status: SUCCESS | PARTIAL | FAILED

### Findings:
- Key finding 1
- Key finding 2
- Key finding 3

### Artifacts:
- File: /path/to/output.md
- Notes: Inline summary

### Recommendations:
- Recommendation 1
- Recommendation 2

### Confidence: HIGH | MEDIUM | LOW
```

**Collection Rules:**
- Wait for ALL parallel tasks to complete
- Document failures separately from successes
- Preserve all artifacts and findings
- Note confidence levels for each result

## Step 6: Result Synthesis

**Combining Parallel Results:**

```markdown
## Synthesis: [Feature/Research Area]

### Completed Tasks: 3/3

### Aggregated Findings:
| Topic | Key Insight | Confidence |
|-------|-------------|------------|
| Stripe | Use webhooks with idempotency keys | HIGH |
| SendGrid | Template versioning required | MEDIUM |
| Twilio | Status callbacks essential | HIGH |

### Patterns Identified:
- All services require idempotent handling
- Webhook verification is critical for all
- Error retry with exponential backoff needed

### Conflicts/Divergence:
- None | [Describe any conflicting findings]

### Recommended Next Steps:
1. Design unified webhook handler
2. Implement idempotency layer
3. Create service abstraction

### Tasks for Sequential Phase:
- [ ] Unified integration design (depends on all research)
```

## Error Handling

### Partial Failures

```markdown
## Parallel Execution Summary

### Succeeded: 2/3
- [x] Research A - Complete
- [x] Research B - Complete
- [ ] Research C - FAILED

### Failure Analysis:
- Task: Research C
- Error: API documentation unavailable
- Impact: Cannot proceed with C integration

### Recovery Options:
1. Retry with different source
2. Proceed without C (if optional)
3. Block and escalate to user
```

**Failure Handling Rules:**
- Successes are valid even if some tasks fail
- Document failure reasons clearly
- Assess impact on dependent work
- Offer recovery options to user
- Don't retry automatically without user consent

### Timeout Handling

```markdown
## Timeout Handling

### Completed: 2/3
### Timed Out: 1/3

### Action:
- Preserve completed results
- Document timeout: Task C exceeded 5 min limit
- Options:
  1. Retry with simpler scope
  2. Continue without result
  3. Increase timeout and retry
```

## Common Use Cases

### Use Case: Codebase Exploration

```markdown
Task: @deep-researcher
Find all authentication implementations...

Task: @deep-researcher
Find all database query patterns...

Task: @deep-researcher
Find all error handling patterns...
```

### Use Case: Multi-File Validation

```markdown
Task: @quality-engineer
Validate frontend test coverage...

Task: @quality-engineer
Validate backend test coverage...

Task: @quality-engineer
Validate E2E test coverage...
```

### Use Case: Solution Comparison

```markdown
Task: @backend-engineer
Prototype solution using ORM A...

Task: @backend-engineer
Prototype solution using ORM B...
```

## Red Flags

- Parallel tasks modifying same file -> Race condition
- Missing independence validation -> Hidden dependencies
- Not waiting for all results -> Incomplete synthesis
- Ignoring partial failures -> Lost information
- Sequential data flow in parallel -> Incorrect ordering

## Decision Criteria

| Situation | Action |
|-----------|--------|
| One task blocks others | Switch to sequential |
| All tasks truly independent | Use full parallelization |
| Uncertain about dependencies | Start with 2 parallel, validate |
| High failure risk | Add redundant research tasks |

## Integration

**Pairs with:** subagent-driven-development (for complex orchestration), debug (parallel hypothesis testing), brainstorm (parallel ideation)
