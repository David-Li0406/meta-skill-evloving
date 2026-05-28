# Parallel Execution Patterns

Detailed patterns for launching and coordinating parallel subagents.

## Single Message Rule

The MOST CRITICAL rule for parallel execution: All parallel subagents MUST be launched in a SINGLE message.

### Why This Matters

```
Sequential (Wrong):
  Message 1 -> Task A starts
  Message 2 -> Task B starts (waits for A to complete first)
  Total time: A + B

Parallel (Correct):
  Single Message -> Task A + Task B + Task C start simultaneously
  Total time: max(A, B, C)
```

### Implementation

When launching parallel tasks, include all Task tool invocations in a single response. Each Task should have:
- `description`: Short description (3-5 words)
- `prompt`: Detailed instructions for the subagent
- `subagent_type`: Usually "general-purpose" for analysis tasks
- `run_in_background`: Set to `true` for parallel execution

---

## Background Execution Pattern

### When to Use run_in_background

| Scenario | run_in_background | Reason |
|----------|-------------------|--------|
| Multi-perspective analysis | true | All perspectives independent |
| Sequential chain | false | Need result before next step |
| Single quick task | false | Overhead not worth it |
| Long-running analysis | true | Don't block main thread |

### Collecting Results

After launching background tasks, use TaskOutput to collect results:

```markdown
## Result Collection

1. Launch tasks with run_in_background: true
2. Note the task_id from each Task result
3. Use TaskOutput to retrieve results:
   - block: true (wait for completion)
   - timeout: Appropriate for task complexity
```

---

## Subagent Type Selection

### Available Types

| Type | Use Case | Tools Available |
|------|----------|-----------------|
| general-purpose | Analysis, research, multi-step tasks | All tools |
| Explore | Codebase exploration, file search | Read-only tools |
| Bash | Command execution, git operations | Bash only |
| Plan | Architecture design, planning | Read + planning tools |

### Selection Guide

```markdown
For Multi-Perspective Analysis:
  - Use "general-purpose" for each perspective
  - Each gets independent 200K token context
  - Full tool access for deep analysis

For Code Exploration:
  - Use "Explore" for quick searches
  - Faster, lower token overhead
  - Read-only prevents conflicts

For Build/Test Operations:
  - Use "Bash" for command execution
  - Isolated command environment
  - Good for parallel test runs
```

---

## Prompt Templates

### Analysis Subagent Template

```markdown
You are a [ROLE] Analyst. Your task is to analyze [TARGET] from the [PERSPECTIVE] perspective.

## Context
[Provide relevant context about the codebase/task]

## Analysis Requirements
1. [Specific requirement 1]
2. [Specific requirement 2]
3. [Specific requirement 3]

## Output Format
Provide your analysis in the following JSON structure:

{
  "perspective": "[PERSPECTIVE]",
  "score": [0-100],
  "summary": "Brief executive summary",
  "findings": [
    {
      "severity": "critical|high|medium|low",
      "category": "string",
      "location": "file:line",
      "description": "What was found",
      "impact": "Why it matters",
      "recommendation": "How to fix"
    }
  ],
  "metrics": {
    "files_analyzed": number,
    "issues_found": number,
    "coverage": "percentage or N/A"
  }
}

## Important
- Be thorough but focused on your perspective
- Provide actionable recommendations
- Include file:line references where applicable
- Rate severity objectively
```

### Adversarial Subagent Template

```markdown
You are an Adversarial Reviewer with role: [ROLE].

## Your Purpose
[Specific adversarial purpose - filter, find, validate]

## Input Data
[Findings from previous phases]

## Review Criteria
1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

## Output Format
{
  "role": "[ROLE]",
  "verdict": "pass|partial|fail",
  "adjustments": [
    {
      "original_finding": "reference",
      "adjustment": "false_positive|severity_change|confirmed",
      "reason": "explanation",
      "confidence": 0.0-1.0
    }
  ],
  "new_findings": [
    {
      "severity": "string",
      "description": "string",
      "evidence": "string"
    }
  ],
  "summary": "Overall assessment"
}
```

---

## Coordination Patterns

### Fan-Out / Fan-In

```
        ┌─── Subagent A ───┐
        │                  │
Main ───┼─── Subagent B ───┼─── Synthesis ─── Output
        │                  │
        └─── Subagent C ───┘

1. Fan-Out: Launch multiple subagents (single message)
2. Execute: Subagents run in parallel
3. Collect: TaskOutput gathers all results
4. Fan-In: Synthesis combines findings
```

### Pipeline with Parallel Stages

```
Stage 1          Stage 2           Stage 3
(Sequential)     (Parallel)        (Sequential)
    │               │                  │
    │         ┌─ Analysis A ─┐         │
 Prepare ───┤─ Analysis B ─├───── Synthesize
             └─ Analysis C ─┘

- Stage 1: Prepare context (sequential)
- Stage 2: Parallel analysis (fan-out)
- Stage 3: Synthesize results (sequential)
```

### Hierarchical Delegation

```
                  Orchestrator
                      │
        ┌─────────────┼─────────────┐
        │             │             │
    Domain A      Domain B      Domain C
        │             │             │
    ┌───┴───┐     ┌───┴───┐     ┌───┴───┐
   Sub1   Sub2   Sub1   Sub2   Sub1   Sub2

- Orchestrator decomposes by domain
- Each domain runs parallel sub-analyses
- Results bubble up through hierarchy
```

---

## Error Handling

### Timeout Management

```markdown
## Timeout Strategy

1. Set appropriate timeouts:
   - Quick analysis: 60s
   - Standard analysis: 180s
   - Deep analysis: 300s

2. Handle timeout gracefully:
   - Use TaskOutput with timeout parameter
   - Partial results are valuable
   - Note limitations in synthesis

3. Retry strategy:
   - Single retry with reduced scope
   - If still failing, skip that perspective
   - Document the gap in final report
```

### Partial Failure Handling

```markdown
## When Subagents Fail

Scenario 1: One subagent fails
  - Continue synthesis with available results
  - Mark that perspective as "incomplete"
  - Add caveat to final report

Scenario 2: Multiple subagents fail
  - If <50% succeed: Retry sequentially
  - If >50% fail: Report infrastructure issue
  - Always provide available analysis

Scenario 3: All fail
  - Fall back to direct analysis
  - Use simpler, single-threaded approach
  - Notify user of degraded mode
```

---

## Performance Optimization

### Minimize Context Transfer

```markdown
## Context Optimization

DO:
- Pass specific file paths, not entire contents
- Use concise requirement summaries
- Let subagents read files themselves

DON'T:
- Copy large code blocks into prompts
- Repeat full context for each subagent
- Include irrelevant background info
```

### Appropriate Parallelism

```markdown
## Parallelism Guidelines

| Codebase Size | Max Parallel | Reason |
|---------------|--------------|--------|
| < 10 files | 2 | Low overhead benefit |
| 10-100 files | 4 | Good balance |
| 100-500 files | 6 | Avoid resource contention |
| > 500 files | 8+ | Consider hierarchical |

Note: Adjust based on task complexity and available resources
```

---

Version: 1.0.0
Last Updated: 2026-01-25
