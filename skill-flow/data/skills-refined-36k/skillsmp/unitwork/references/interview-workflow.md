# Interview Workflow

This document is the single source of truth for interview-related protocols in Unit Work, including when to interview, confidence-based depth assessment, question guidelines, and stop conditions.

## When to Interview

```
Context requiring clarification:
                    |
+-----------------------------------------------+
| Initial planning (uw:plan)?                   |
|   YES -> Full interview workflow              |
|         (Phase 2 of uw:plan)                  |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| Gap-detector found P1/P2 gaps?                |
|   YES -> Interview to resolve gaps            |
|         (uw:work Step 0.5, uw:plan review)    |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| Can't determine fix approach (uw:review)?     |
|   YES -> Interview before implementing        |
|         (fix loop clarification)              |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| User feedback reveals ambiguity?              |
|   YES -> Interview to clarify                 |
|         (any workflow phase)                  |
+-----------------------------------------------+
```

## Confidence-Based Depth Assessment

Assess confidence BEFORE interviewing to determine depth:

```
Agent confidence in understanding:
                    |
+-----------------------------------------------+
| HIGH (>80%): Spec is clear, scope is bounded  |
|   -> MINIMAL interview                        |
|      - 1-2 targeted questions                 |
|      - Confirm understanding only             |
|      - Can proceed quickly                    |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| MEDIUM (50-80%): Some ambiguity exists        |
|   -> STANDARD interview                       |
|      - Clarify scope and boundaries           |
|      - Ask about key edge cases               |
|      - 3-5 rounds max                         |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| LOW (<50%): Significant unknowns              |
|   -> COMPREHENSIVE interview                  |
|      - Understand the "why" behind request    |
|      - Explore all ambiguities                |
|      - Get explicit decisions on trade-offs   |
|      - Up to 10 rounds                        |
+-----------------------------------------------+
```

### Confidence Assessment Factors

Start at 50%, adjust based on:
- +20% if similar feature exists in codebase (can follow pattern)
- +15% if user provided detailed description
- +10% if scope is explicitly bounded ("just X, not Y")
- -20% if feature touches unfamiliar domain
- -15% if multiple valid implementation approaches
- -10% if integration with external systems

## Interview Guidelines

**These 6 rules apply to ALL interview contexts:**

1. **Research before asking** - Check Hindsight, codebase, and web docs before asking user to explain
2. **Group related questions** - Batch related questions together using AskUserQuestion
3. **Push back on scope** - If something sounds like a separate feature, say: "That sounds like a separate feature - should we defer it?"
4. **Advocate once** - State recommendation with reasoning, then accept user decision
5. **No premature solutions** - Don't propose implementation during requirements gathering
6. **Confirm understanding** - Summarize requirements back before proceeding

## Question Categories

### 1. Implementation Details
Questions that affect how code will be written:
- "How should errors be surfaced to the user?"
- "What data format should X use?"
- "Should this operation be sync or async?"
- "What's the expected latency/performance requirement?"
- "How should this integrate with existing X?"

### 2. Edge Cases
Questions about boundary conditions and error states:
- "What happens when X is empty or null?"
- "How should we handle partial failures?"
- "What's the behavior at size/rate limits?"
- "What if the user cancels mid-operation?"
- "How should concurrent requests be handled?"

### 3. Testing Strategy
Questions about verification approach:
- "What edge cases need explicit test coverage?"
- "Should we mock X or use real instances?"
- "Is integration testing needed for this?"
- "What's the acceptance criteria for 'done'?"
- "Are there existing test fixtures we should use?"

### 4. Dependencies & Integration
Questions about external factors:
- "Are there external services involved?"
- "What happens if a dependency fails?"
- "Are there rate limits or quotas to consider?"
- "Does this need backwards compatibility?"

### 5. UI/UX (skip for backend-only)
Questions when feature involves UI:
- "What should the loading state look like?"
- "How should validation errors be displayed?"
- "Is there existing UI we should match?"
- "What's the mobile/responsive behavior?"

## Stop Conditions

Interview stops when ALL conditions are true:
1. **No P1/P2 gaps remain** - Re-run gap-detector to validate
2. **Agent can describe implementation steps** - Can articulate what code changes are needed
3. **Edge cases enumerated** - Know what error states to handle
4. **Success criteria clear** - Know what "done" looks like

**OR** when:
- User explicitly says "proceed with what you have"
- Maximum rounds reached (based on depth level)

### Validation Loop

```
After interview round:
                    |
+-----------------------------------------------+
| Run gap-detector on current understanding     |
|                                               |
| P1/P2 gaps found?                             |
|   YES -> Continue interviewing                |
|   NO  -> Stop, proceed to next phase          |
+-----------------------------------------------+
```

## AskUserQuestion Patterns

### Batching Questions
Group related questions in single call (max 4 options per question):

```markdown
Use AskUserQuestion with:
questions: [
  {
    question: "How should errors be handled?",
    options: ["Show inline", "Show toast", "Show modal", "Silent log"]
  },
  {
    question: "What's the scope boundary?",
    options: ["Just this feature", "Include related refactor", "Defer related work"]
  }
]
```

### Offering Options with Escape Hatch
Always include an option for user to provide different answer:

```markdown
questions: [
  {
    question: "Which approach for X?",
    options: ["Option A", "Option B", "Option C"]
  }
]
```

Note: AskUserQuestion automatically provides an "Other" option for free-form input.

### Context-Specific Patterns

**For gap resolution (uw:work Step 0.5, uw:plan):**
```markdown
questions: [
  {
    question: "Gap found: {gap description}. How to resolve?",
    options: ["Clarify now", "Proceed anyway", "Create full spec first"]
  }
]
```

**For fix approach (uw:review):**
```markdown
questions: [
  {
    question: "Multiple fix approaches for {issue}. Which to use?",
    options: ["Approach A: {description}", "Approach B: {description}", "Need more context"]
  }
]
```
