---
name: observation-capture-cycle
description: 4 questions for genuine reflection before work closure. Hard gate on
  non-empty.
recipes:
- scaffold-observations
generated: 2026-01-10
last_updated: '2026-01-18T22:10:20'
---
# Observation Capture

Capture observations before closing work. Invoked by `/close` command.

## Questions

Answer these 4 questions about the work just completed:

1. **What surprised you?**
   - Unexpected behaviors, bugs encountered
   - Things easier or harder than anticipated
   - Assumptions that proved wrong
   - Principles revealed through the work
   - Operator insights that shifted understanding

2. **What's missing?**
   - Gaps in tooling, docs, or infrastructure
   - Features that would have helped
   - AgentUX friction points
   - Schema or architectural concepts not yet codified
   - Patterns that should exist but don't

3. **What should we remember?**
   - Learnings for future work
   - Patterns worth reusing or naming
   - Warnings for similar tasks
   - Decisions that should become ADRs
   - Principles worth adding to L3/L4

4. **What drift did you notice?**
   - Reality vs documented behavior
   - Code vs spec misalignment
   - Principles violated or bent
   - Patterns that have evolved past their docs

## Gate

**MUST** provide:
- At least one substantive answer, OR
- Explicit "None observed" with brief justification

Empty responses BLOCK closure.

## Output

Write answers to `docs/work/active/{id}/observations.md` using simplified template.
