---
name: dispatching-parallel-agents
description: Use when facing 3+ independent failures that can be investigated without shared state or dependencies - dispatches multiple agents to investigate and fix independent problems concurrently.
---

# Dispatching Parallel Agents

## Overview

When you have multiple unrelated failures (different test files, different subsystems, different bugs), investigating them sequentially wastes time. Each investigation is independent and can happen in parallel.

**Core principle:** Dispatch one agent per independent problem domain. Let them work concurrently.

## When to Use

Use when:
- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No shared state between investigations
- You've verified failures are truly independent
- Each domain has clear boundaries (different files, modules, features)

Don't use when:
- Failures are related (fix one might fix others)
- Need to understand full system state first
- Agents would interfere (editing same files)
- Haven't verified independence yet (exploratory phase)
- Failures share root cause (one bug, multiple symptoms)
- Need to preserve investigation order (cascading failures)
- Only 2 failures (overhead exceeds benefit)

## The Process

### Step 1: Identify Independent Domains

**Announce:** "I'm using dispatching-parallel-agents to investigate these independent failures concurrently."

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

### Step 2: Create Focused Agent Tasks

Each agent prompt must have:
1. **Specific scope:** One test file or subsystem
2. **Clear goal:** Make these tests pass
3. **Constraints:** Don't change other code
4. **Expected output:** Summary of what you found and fixed

### Step 3: Dispatch All Agents in Parallel

**CRITICAL:** You must dispatch all agents in a SINGLE message with multiple Task() calls.

```typescript
// Correct - Single message with multiple parallel tasks
Task("Fix agent-tool-abort.test.ts failures", prompt1)
Task("Fix batch-completion-behavior.test.ts failures", prompt2)
Task("Fix tool-approval-race-conditions.test.ts failures", prompt3)
// All three run concurrently
```

### Step 4: Monitor Progress

As agents work:
- Note which agents have completed
- Note which are still running
- Don't start integration until ALL agents done

### Step 5: Review Results and Check Conflicts

**When all agents return:**
1. **Read each summary carefully**
2. **Check for conflicts**
   - Did multiple agents edit same files?
   - Did agents make contradictory assumptions?
3. **Integration strategy:**
   - If no conflicts: Apply all changes
   - If conflicts: Resolve manually before applying

### Step 6: Verify Integration

**Run full test suite:**
- Not just the fixed tests
- Verify no regressions in other areas

## Common Mistakes

- **Too broad:** "Fix all the tests" - agent gets lost
- **No context:** "Fix the race condition" - agent doesn't know where
- **No constraints:** Agent might refactor everything
- **Vague output:** "Fix it" - you don't know what changed

## Verification Checklist

Before completing parallel agent work:
- [ ] Verified independence with 3 questions (fix A affects B? same code? same error pattern?)
- [ ] 3+ independent domains identified (not 2 or fewer)
- [ ] Created focused agent prompts (scope, goal, constraints, output)
- [ ] Dispatched all agents in single message (multiple Task() calls)
- [ ] Waited for ALL agents to complete (didn't integrate early)
- [ ] Read all agent summaries carefully
- [ ] Checked for conflicts (same files, contradictory assumptions)
- [ ] Resolved any conflicts manually before integration
- [ ] Ran full test suite (not just fixed tests)

## Resources

**Key principles:**
- Parallelization only wins with 3+ independent problems
- Independence verification prevents wasted parallel work
- Single message dispatch is critical for true parallelism
- Conflict checking prevents integration disasters
- Full verification catches agent mistakes