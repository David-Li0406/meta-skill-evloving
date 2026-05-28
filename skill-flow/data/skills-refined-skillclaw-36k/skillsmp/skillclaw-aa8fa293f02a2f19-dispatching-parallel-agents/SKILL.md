---
name: dispatching-parallel-agents
description: Use this skill when facing 3+ independent failures that can be investigated without shared state or dependencies, allowing multiple agents to work concurrently on different problems.
---

# Skill Body

## Overview

When you have multiple unrelated failures (different test files, different subsystems, different bugs), investigating them sequentially wastes time. Each investigation is independent and can happen in parallel.

**Core principle:** Dispatch one agent per independent problem domain. Let them work concurrently.

## When to Use

Use this skill when:
- You have 3+ test files failing with different root causes.
- Multiple subsystems are broken independently.
- Each problem can be understood without context from others.
- There is no shared state between investigations.
- You've verified that failures are truly independent.

**Don't use this skill when:**
- Failures are related (fixing one might fix others).
- You need to understand the full system state first.
- Agents would interfere with each other (e.g., editing the same files).
- You haven't verified independence yet (exploratory phase).
- Failures share a root cause (one bug, multiple symptoms).
- You need to preserve investigation order (cascading failures).
- There are only 2 failures (overhead exceeds benefit).

## The Process

### Step 1: Identify Independent Domains

1. **Test for independence:**
   - Ask: "If I fix failure A, does it affect failure B?"
     - If NO → Independent
     - If YES → Related, investigate together.
   - Check: "Do failures touch the same code/files?"
     - If NO → Likely independent.
     - If YES → Check if they differ.

### Step 2: Create Focused Agent Tasks

Each agent should have:
- **Specific scope:** One test file or subsystem.
- **Clear goal:** Make these tests pass.
- **Constraints:** Don't change other code.
- **Expected output:** Summary of findings and fixes.

### Step 3: Dispatch Agents in Parallel

- Dispatch all agents in a single message using multiple Task() calls to ensure they run concurrently.

### Step 4: Monitor Progress

- Track the completion of each agent's task. If an agent is stuck for more than 5 minutes, investigate.

### Step 5: Review Results

- Read the summaries provided by each agent and check for conflicts. Resolve any conflicts manually.

### Step 6: Verify Integration

- Run a full test suite to ensure all changes are compatible and functioning as expected.

**Critical Note:** Always announce at the start of the session that you are using this skill to create an audit trail. For example: 
```
🔧 Using Skill: dispatching-parallel-agents | [brief purpose based on context]
```