---
name: parallel-agents
description: Use when facing 3+ independent failures that can be investigated without shared state - dispatches multiple agents concurrently to investigate and fix problems in parallel
---

# Parallel Agent Dispatch

## Overview

When facing 3+ independent failures, dispatch one agent per problem domain to investigate concurrently. Verify independence first, dispatch all in single message, wait for all agents, check conflicts, verify integration.

**Core principle:** Independence verification BEFORE dispatch. Single message dispatch for true parallelism.

**Announce at start:** "I'm using gambit:parallel-agents to investigate these independent failures concurrently."

## Rigidity Level

MEDIUM FREEDOM - Follow the 6-step process strictly. Independence verification mandatory. Parallel dispatch in single message required. Adapt agent prompt content to problem domain.

## Quick Reference

| Step | Action | STOP If |
|------|--------|---------|
| 1 | Identify domains | < 3 independent domains |
| 2 | Create agent tasks | Prompts incomplete |
| 3 | Dispatch in SINGLE message | - |
| 4 | Monitor progress | Agent stuck > 5 min |
| 5 | Review results | Conflicts found |
| 6 | Verify integration | Tests fail |

**Why 3+?** With only 2 failures, coordination overhead often exceeds sequential time.

**Critical:** Dispatch all agents in single message with multiple Task() calls, or they run sequentially.

## When to Use

**Use when:**
- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No shared state between investigations
- You've verified failures are truly independent
- Each domain has clear boundaries (different files, modules, features)

**Don't use when:**
- Failures are related (fix one might fix others)
- Need to understand full system state first
- Agents would interfere (editing same files)
- Haven't verified independence yet (exploratory phase)
- Failures share root cause (one bug, multiple symptoms)
- Need to preserve investigation order (cascading failures)
- Only 2 failures (overhead exceeds benefit)

## The Process

### Step 1: Identify Independent Domains

**Test for independence:**

1. **Ask:** "If I fix failure A, does it affect failure B?"
   - If NO → Independent
   - If YES → Related, investigate together

2. **Check:** "Do failures touch same code/files?"
   - If NO → Likely independent
   - If YES → Check if different functions/areas

3. **Verify:** "Do failures share error patterns?"
   - If NO → Independent
   - If YES → Might be same root cause

**Example independence check:**

```
Failure 1: Authentication tests failing (auth_test.go)
Failure 2: Database query tests failing (db_test.go)
Failure 3: API endpoint tests failing (api_test.go)

Check: Does fixing auth affect db queries? NO
Check: Does fixing db affect API? YES - API uses db

Result: 2 independent domains:
  Domain 1: Authentication (auth_test.go)
  Domain 2: Database + API (db_test.go + api_test.go together)

NOT 3 domains - don't use parallel dispatch.
```

**Another example:**

```
Failure 1: Tool abort tests failing (timing issues)
Failure 2: Batch completion tests failing (state management)
Failure 3: Tool approval tests failing (race conditions)

Check: Do these share code? Different test files, different modules
Check: Same error pattern? No - different symptoms
Check: Fix one affects others? No - isolated functionality

Result: 3 independent domains ✓
```

**Create coordination Task to track the parallel work:**

```
TaskCreate
  subject: "Parallel Investigation: [N] independent failures"
  description: |
    ## Independent Domains
    1. [Domain 1]: [files/tests]
    2. [Domain 2]: [files/tests]
    3. [Domain 3]: [files/tests]

    ## Independence Verification
    - Domain 1 vs 2: [why independent]
    - Domain 2 vs 3: [why independent]
    - Domain 1 vs 3: [why independent]

    ## Agent Status
    - [ ] Agent 1 ([Domain 1]): dispatched / returned / result summary
    - [ ] Agent 2 ([Domain 2]): dispatched / returned / result summary
    - [ ] Agent 3 ([Domain 3]): dispatched / returned / result summary

    ## Progress
    - [ ] All agents dispatched (single message)
    - [ ] All agents returned
    - [ ] No conflicts found
    - [ ] Integration verified (full test suite)
  activeForm: "Coordinating parallel investigation"
```

**Mark in progress:**

```
TaskUpdate
  taskId: "[coordination-task-id]"
  status: "in_progress"
```

**Why track with a Task (not mental tracking):**
- See all agent statuses at a glance with TaskGet
- Document which agents fixed what
- Track conflicts and integration decisions
- Provides audit trail for complex investigations

---

### Step 2: Create Focused Agent Prompts

Each agent prompt must have:

1. **Specific scope:** One test file or subsystem
2. **Clear goal:** Make these tests pass
3. **Constraints:** Don't change other code
4. **Expected output:** Summary of what you found and fixed

**Good agent prompt example:**

```markdown
Fix the 3 failing tests in src/agents/tool_abort_test.go:

1. "TestAbortWithPartialOutput" - expects 'interrupted at' in message
2. "TestMixedCompletedAndAborted" - fast tool aborted instead of completed
3. "TestPendingToolCount" - expects 3 results but gets 0

These are timing/race condition issues. Your task:

1. Read the test file and understand what each test verifies
2. Identify root cause - timing issues or actual bugs?
3. Fix by:
   - Replacing arbitrary timeouts with event-based waiting
   - Fixing bugs in abort implementation if found
   - Adjusting test expectations if testing changed behavior

Constraints:
- Do NOT just increase timeouts - find the real issue
- Do NOT modify files outside src/agents/
- Do NOT change behavior, only fix tests or bugs

Return: Summary of root cause and what you fixed.
```

**What makes this good:**
- Specific test failures listed
- Context provided (timing/race conditions)
- Clear methodology (read, identify, fix)
- Constraints (don't just increase timeouts)
- Output format (summary)

**Bad prompts:**

❌ **Too broad:** "Fix all the tests"
✅ **Specific:** "Fix tool_abort_test.go"

❌ **No context:** "Fix the race condition"
✅ **Context:** Paste the error messages and test names

❌ **No constraints:** Agent might refactor everything
✅ **Constraints:** "Do NOT change production code"

---

### Step 3: Dispatch All Agents in SINGLE Message

**CRITICAL:** You must dispatch all agents in a SINGLE message with multiple Task() calls.

```
// ✅ CORRECT - Single message with multiple parallel tasks
Task
  subagent_type: "general-purpose"
  description: "Fix tool_abort_test.go failures"
  prompt: "[prompt 1]"

Task
  subagent_type: "general-purpose"
  description: "Fix batch_completion_test.go failures"
  prompt: "[prompt 2]"

Task
  subagent_type: "general-purpose"
  description: "Fix tool_approval_test.go failures"
  prompt: "[prompt 3]"

// All three run concurrently
```

```
// ❌ WRONG - Sequential messages
Task prompt1
[Wait for response]
Task prompt2  // This is sequential, not parallel!
```

---

### Step 4: Monitor Progress

As agents work:
- Note which agents have completed
- Note which are still running
- Don't start integration until ALL agents done

**Check agent progress with TaskOutput:**

```
TaskOutput
  task_id: "[agent-task-id]"
  block: false
  timeout: 5000
```

This returns current status without waiting for completion.

**If an agent gets stuck (>5 minutes):**

1. Check TaskOutput to see what it's doing:
   ```
   TaskOutput
     task_id: "[stuck-agent-id]"
     block: false
     timeout: 5000
   ```
2. If stuck on wrong path: KillShell and retry with clearer prompt
3. If needs context from other domain: Wait for other agent, then restart with context
4. If hit real blocker: Investigate blocker yourself, then retry

**If agent completes with errors:**
- Read the full output with `block: true`
- Determine if it's a real failure or needs refinement
- Consider retrying with more context from what it learned

---

### Step 5: Review Results and Check Conflicts

**When all agents return:**

1. **Read each summary carefully**
   - What was the root cause?
   - What did the agent change?
   - Were there any uncertainties?

2. **Check for conflicts**
   - Did multiple agents edit same files?
   - Did agents make contradictory assumptions?
   - Are there integration points between domains?

3. **Integration strategy:**
   - If no conflicts: Apply all changes
   - If conflicts: Resolve manually before applying
   - If assumptions conflict: Verify with user

4. **Document what happened**
   - Which agents fixed what
   - Any conflicts found
   - Integration decisions made

**Conflict detection example:**

```
Agent 1: "Fixed timeout issue by increasing wait time to 5000ms"
- File: src/executor.go, DEFAULT_TIMEOUT = 5000

Agent 3: "Fixed timing issue by reducing wait time to 1000ms"
- File: src/executor.go, DEFAULT_TIMEOUT = 1000

CONFLICT DETECTED:
- Same file, same constant
- Contradictory changes

Resolution: Investigate why both agents had different needs.
Maybe need separate timeouts for different operations.
```

---

### Step 6: Verify Integration

**Run full test suite:**

```
Task
  subagent_type: "hyperpowers:test-runner"
  prompt: "Run: go test ./..."
```

**Decision tree:**
- All pass? → Mark coordination Task complete
- Failures? → Identify which agent's change caused regression

**Update coordination Task:**

```
TaskUpdate
  taskId: "[coordination-task-id]"
  description: |
    [Original description]

    ## Results
    - Agent 1: Fixed [X] in [files]
    - Agent 2: Fixed [Y] in [files]
    - Agent 3: Fixed [Z] in [files]

    ## Conflicts
    [None / Description of conflicts and resolution]

    ## Integration
    All tests pass. Changes integrated successfully.
  status: "completed"
```

---

## Critical Rules

### Rules That Have No Exceptions

1. **Verify independence first** → Test with 3 questions before dispatching
2. **3+ domains required** → 2 failures: do sequentially, overhead exceeds benefit
3. **Single message dispatch** → All agents in one message with multiple Task() calls
4. **Wait for ALL agents** → Don't integrate until all complete
5. **Check conflicts manually** → Read summaries, verify no contradictions
6. **Verify integration** → Run full suite yourself, don't trust agents

### Common Excuses

All of these mean: **STOP. Follow the process.**

| Excuse | Reality |
|--------|---------|
| "Just 2 failures, can still parallelize" | Overhead exceeds benefit, do sequentially |
| "Probably independent, will dispatch and see" | Verify independence FIRST |
| "Can dispatch sequentially to save syntax" | WRONG - must dispatch in single message |
| "Agent failed, but others succeeded - ship it" | All agents must succeed or re-investigate |
| "Conflicts are minor, can ignore" | Resolve all conflicts explicitly |
| "Can skip verification, agents ran tests" | Agents can make mistakes, YOU verify |

---

## Examples

### Bad: Dispatch Sequentially

```
# Developer sees 3 independent failures

Task prompt1
[Wait for response from agent 1]

Task prompt2
[Wait for response from agent 2]

Task prompt3
[Wait for response from agent 3]

# Total time: Sum of all three (sequential)
# No parallelization benefit
```

### Good: Dispatch in Single Message

```
# All in ONE message:

Task
  subagent_type: "general-purpose"
  prompt: "[prompt 1]"

Task
  subagent_type: "general-purpose"
  prompt: "[prompt 2]"

Task
  subagent_type: "general-purpose"
  prompt: "[prompt 3]"

# All three run concurrently
# Total time: Max(agent1, agent2, agent3) instead of Sum
```

### Bad: Assume Independence

```
# 3 test failures:
# - API endpoint tests failing
# - Database query tests failing
# - Cache invalidation tests failing

# Thinks: "Different subsystems, must be independent"
# Dispatches 3 agents immediately without checking

# All three failures caused by same root cause: schema change
# Agents make conflicting fixes based on different assumptions
# Integration fails
```

### Good: Verify Independence First

```
# 3 test failures observed

Check: Does fixing API affect database?
- API uses database
- If database schema changes, API breaks
- YES - related

Check: Does fixing database affect cache?
- Cache stores database results
- YES - related

Check: Same error pattern?
- All mention "column not found"
- YES - shared root cause

Result: NOT INDEPENDENT
These are one problem (schema change) manifesting in 3 places.

Solution: Single agent investigates all three together.
```

### Bad: Integrate Without Checking Conflicts

```
# 3 agents complete

Agent 1: "Increased timeout to 5000ms"
Agent 2: "Added mutex lock"
Agent 3: "Reduced timeout to 1000ms"

Developer: "All succeeded, ship it"
[Applies all changes without reading]

# Agent 1 and 3 changed same constant with different values
# Final code has inconsistent state
# Tests still fail
```

### Good: Check for Conflicts

```
# Review each agent's changes

Agent 1: timeout = 5000ms in executor.go
Agent 2: added mutex in executor.go
Agent 3: timeout = 1000ms in executor.go

CONFLICT: Agent 1 and 3 both edited timeout

Investigation:
- Agent 1's tests were slow due to unrelated issue
- Agent 3 found correct timeout value
- Fix Agent 1's slow tests separately

Resolution:
- Apply Agent 2's mutex ✓
- Apply Agent 3's 1000ms timeout ✓
- Fix Agent 1's slow tests (don't apply 5000ms)
```

---

## Failure Modes

### Agent Gets Stuck

**Symptoms:** No progress after 5+ minutes

**Recovery:**
1. Check TaskOutput to see what it's doing
2. If stuck on wrong path: Cancel and retry with clearer prompt
3. If needs context from other domain: Wait for other agent, then restart
4. If hit blocker: Investigate yourself, then retry

### Agents Return Conflicting Fixes

**Symptoms:** Same code edited differently

**Recovery:**
1. Don't apply either fix automatically
2. Read both fixes carefully
3. Identify the conflict point
4. Resolve manually based on which assumption is correct
5. Consider if domains should be merged

### Integration Breaks Other Tests

**Symptoms:** Fixed tests pass, others fail

**Recovery:**
1. Identify which agent's change caused regression
2. Read agent's summary - did they mention this?
3. Evaluate if change is correct but tests need updating
4. Or if change broke something, refine the fix

### False Independence

**Symptoms:** Fixing one domain revealed it affected another

**Recovery:**
1. Merge the domains
2. Have one agent investigate both together
3. Learn: Better independence test needed upfront

---

## Verification Checklist

Before completing parallel agent work:

- [ ] Verified independence with 3 questions (fix A affects B? same code? same error?)
- [ ] 3+ independent domains identified (not 2 or fewer)
- [ ] Created focused agent prompts (scope, goal, constraints, output)
- [ ] Dispatched all agents in single message (multiple Task() calls)
- [ ] Waited for ALL agents to complete (didn't integrate early)
- [ ] Read all agent summaries carefully
- [ ] Checked for conflicts (same files, contradictory assumptions)
- [ ] Resolved any conflicts manually before integration
- [ ] Ran full test suite (not just fixed tests)
- [ ] Documented which agents fixed what
- [ ] Coordination Task marked complete

**Can't check all boxes?** Return to process.

---

## Integration

**This skill calls:**
- `gambit:debugging` (how to investigate individual failures)
- `gambit:verify` (verify integration)
- test-runner agent (run tests without context pollution)
- general-purpose agents (for parallel investigation)

**This skill is called when:**
- Multiple independent test failures
- Multiple subsystems broken
- Need to parallelize investigation

**Workflow:**
```
Multiple failures detected
    ↓
gambit:parallel-agents (this skill)
    ↓
Step 1: Verify independence (3+ domains)
    ↓
Step 2: Create agent prompts
    ↓
Step 3: Dispatch in SINGLE message
    ↓
Step 4: Monitor progress
    ↓
Step 5: Review results, check conflicts
    ↓
Step 6: Verify integration
    ↓
All failures resolved
```

---

## Resources

**Independence verification questions:**
- "If I fix A, does it affect B?"
- "Do they touch same code/files?"
- "Do they share error patterns?"

**Agent prompt structure:**
- Specific scope (one test file/module)
- Clear goal (make tests pass)
- Constraints (don't change other code)
- Expected output (summary of findings)

**When stuck:**
- Agent not making progress → Check TaskOutput, retry clearer prompt
- Conflicts after dispatch → Domains weren't independent, merge and retry
- Integration fails tests → Identify which agent caused regression
- < 3 domains → Don't use parallel dispatch, investigate sequentially
