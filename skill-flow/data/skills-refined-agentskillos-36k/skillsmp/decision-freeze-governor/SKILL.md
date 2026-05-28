---
name: decision-freeze-governor
description: Determines whether documentation is sufficient to proceed without human clarification. Use before implementation to prevent rework.
triggers: [spec-ready, task-start, planning-complete]
outputs: [go-nogo-decision, frozen-decision-list]
---

# Decision Freeze Governor

## Purpose

Prevents "starting line errors" by ensuring the AI and Human are in 100% agreement before expensive implementation work begins. It acts as the final gate for spec stability.

## When to use this skill
- Immediately before moving from PLANNING to EXECUTION mode
- When a specification has reached its final draft
- When high-impact decisions are identified by the `risk-hunter`

## Governance Steps

1. **Check for Ambiguity**: Use the `spec-linter` output to identify any "maybe" or "TBD" items.
2. **Identify Blocking Questions**: Separate "nice-to-know" items from "must-know-to-code" items.
3. **Decide GO / NO-GO**: If a critical decision is unfrozen, the path is NO-GO.
4. **Summarize Frozen Decisions**: Create a concise list of exactly what has been agreed upon.

## Decision Tree

```mermaid
flowchart TD
    A[Start Gate] --> B{Spec Frozen?}
    B -->|No| C[NO-GO: Stabilize Spec]
    B -->|Yes| D{Open Questions?}
    D -->|Blocking| E[NO-GO: Request Clarification]
    D -->|Non-Blocking| F[GO: Proceed with Assumptions]
    D -->|No| G[GO: Clean Path]
    F --> H[Summarize Agreements]
    G --> H
```

## Review Checklist

1. **Stability**: How likely is this decision to change in the next 48 hours?
2. **Commitment**: Has the human explicitly said "Proceed" or similar?
3. **Traceability**: Is the frozen decision linked to a specific requirement ID?
4. **Scope**: Does the freeze cover the *entire* task, or just a part?

## How to provide feedback
- **Be specific**: "The governor approved the task even though the API endpoint name is still TBD."
- **Explain why**: "Implementing with a TBD endpoint name leads to massive refactoring later."
- **Suggest alternatives**: "Mark 'Endpoint Naming' as a blocking question in the `spec-linter`."

Do not ask humans unless blocking.
