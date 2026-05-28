---
name: design-guardrails-skill
description: Shape engineering designs by clarifying problems, comparing options, managing architectural boundaries, and planning validation.
---

# Design Guardrails Skill

Invoke this when drafting or reviewing an architecture plan, refactor proposal, or integration strategy. The goal is to reach a minimal, testable design that aligns with existing systems.

## Process

1. **Clarify the problem**
   - Restate desired behavior, inputs/outputs, constraints, and success metrics.
   - Confirm the current failure mode; prioritize solving root causes over layering new abstractions.
2. **Map context**
   - Identify affected services, libraries, data stores, and external dependencies.
   - Surface coupling or boundary assumptions that must hold.
3. **Explore options**
   - Draft at least two viable approaches.
   - For each, note complexity, required migrations, and operational impact.
4. **Select direction**
   - Choose the simplest option that satisfies invariants and fits the architecture roadmap.
   - Document why alternatives were rejected and any prerequisite work.
5. **Plan validation & rollout**
   - Outline unit/integration tests, observability hooks, rollout steps, and fallback plans.
   - Specify ownership for follow-up tasks (docs, migrations, feature flags).
6. **Communicate clearly**
   - Provide diagrams or tables when they clarify relationships.
   - Highlight risks, open questions, and decisions needing stakeholder input.

## Deliverable template

```
### Problem & Goals
- summary + constraints

### Current State
- key components & pain points

### Options
- Option A — pros/cons
- Option B — pros/cons

### Recommendation
- chosen approach + invariants + validation plan

### Risks & Follow-ups
- mitigations, owners, timeline signals
```

## Safeguards

- If context is stale or contradictory, ask the user to reconcile before finalizing.
- Do not recommend broad rewrites when a contained fix solves the root issue.
- Call out monitoring or rollback gaps explicitly; never assume they exist.
