---
name: mapcoder
description: Solve coding problems using multi-agent retrieval, planning, coding, and debugging pipeline. Use when solving algorithmic problems, implementing features from specifications, or when code needs iterative refinement.
argument-hint: "[--lang <language>] [--sandbox] <problem description or file path>"
---

# MapCoder: Multi-Agent Code Generation Pipeline

You are orchestrating the MapCoder pipeline, a multi-agent system that replicates the human programming cycle through four specialized agents:

1. **Retrieval Agent** - Generates similar problems from knowledge
2. **Planning Agent** - Creates step-by-step algorithmic plans
3. **Coding Agent** - Translates plans into executable code
4. **Debugging Agent** - Fixes bugs using plans and test feedback

## Argument Parsing

Parse `$ARGUMENTS` to extract:
- `--lang <language>`: Target programming language (default: Python)
- `--sandbox`: Use Docker sandbox for code execution (safer)
- Remaining text: The problem description or file path

Example inputs:
- `/mapcoder implement binary search` → Python, direct execution
- `/mapcoder --lang javascript implement binary search` → JavaScript
- `/mapcoder --sandbox --lang rust implement linked list` → Rust, sandboxed

## Pipeline Execution

### Step 1: Problem Analysis

First, analyze the input:
- If it's a file path, read the file to get the problem description
- Extract any sample test cases from the problem
- Identify the target language from arguments (default: Python)

### Step 2: Retrieval Phase

Use the Task tool to spawn the retrieval agent:

```
Spawn a retrieval agent to generate 3-5 similar problems for:
[problem description]

The agent should return:
- Similar problem descriptions
- Solution patterns/approaches used
- Key algorithmic concepts
```

Use subagent_type: "general-purpose" with the retrieval-agent.md system prompt.

### Step 3: Planning Phase

Use the Task tool to spawn the planning agent with the retrieved examples:

```
Spawn a planning agent to create step-by-step plans for:
[problem description]

Using these similar problems as reference:
[retrieved examples]

Generate 2-3 alternative algorithmic plans.
```

### Step 4: Coding Phase

Use the Task tool to spawn the coding agent:

```
Spawn a coding agent to implement the solution in [language]:
[problem description]

Following this plan:
[selected plan]

Test against these sample cases:
[test cases]
```

If `--sandbox` flag is set, instruct the agent to use `scripts/sandbox-runner.sh` instead of direct execution.

### Step 5: Validation Loop

After coding completes:

**If tests pass**: Return the solution with explanation.

**If tests fail**: Enter debugging loop (max 3 iterations):

```
Spawn a debugging agent to fix the failing code:

Original problem: [problem]
Current code: [code]
Error output: [errors]
Original plan: [plan]

Identify the bug and generate corrected code.
```

### Step 6: Solution Output

When successful, output using the solution template:

```markdown
## Solution

**Language**: [language]
**Status**: [Passed/Failed after N attempts]

### Code
[final code]

### Explanation
[step-by-step explanation of the approach]

### Test Results
[test output]
```

## Adaptive Traversal

The pipeline supports adaptive routing:

- If retrieval produces highly relevant examples → use single best plan
- If planning produces uncertain results → try multiple plans in parallel
- If debugging fails 3 times → try alternative plan from Step 3
- If all plans exhausted → report failure with analysis

## Configuration

- **MAX_DEBUG_ITERATIONS**: 3
- **MAX_PLAN_ATTEMPTS**: 3
- **DEFAULT_LANGUAGE**: Python

## Error Handling

- If any agent fails to spawn, report the error and suggest manual intervention
- If code execution times out, treat as test failure and enter debugging
- If problem is ambiguous, ask user for clarification before proceeding
