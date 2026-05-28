---
name: software-architecture
description: Use this skill when designing systems, evaluating architectures, making technology decisions, or planning for scale. It provides frameworks for technology selection, scalability planning, and architectural tradeoff analysis.
---

# Software Architecture

Design question → options with tradeoffs → documented decision.

<when_to_use>

- Designing new systems or major features
- Evaluating architectural approaches
- Making technology stack decisions
- Planning for scale and performance
- Analyzing design tradeoffs

NOT for: trivial tech choices, premature optimization, undocumented requirements

</when_to_use>

<phases>

Load the **maintain-tasks** skill for phase tracking. Phases advance only, never regress.

| Phase | Trigger | activeForm |
|-------|---------|------------|
| Discovery | Session start | "Gathering requirements" |
| Codebase Analysis | Requirements clear | "Analyzing codebase" |
| Constraint Evaluation | Codebase understood | "Evaluating constraints" |
| Solution Design | Constraints mapped | "Designing solutions" |
| Documentation | Design selected | "Documenting architecture" |

Situational (insert before Documentation when triggered):
- Review & Refinement → feedback cycles on complex designs

Edge cases:
- Small questions: skip to Solution Design
- Greenfield: skip Codebase Analysis
- No ADR needed: skip Documentation
- Iteration: Review & Refinement may repeat

Task format:

```text
- Discovery { problem domain }
- Analyze { codebase area }
- Evaluate { constraint type }
- Design { solution approach }
- Document { decision type }
```

Workflow:
- Start: Create Discovery as `in_progress`
- Transition: Mark current `completed`, add next `in_progress`
- High start: skip to Solution Design for clear problems
- Optional end: Documentation skippable if ADR not needed

</phases>

<principles>

## Proven over Novel

Favor battle-tested over bleeding-edge without strong justification.

Checklist:
- 3+ years production at scale?
- Strong community + active maintenance?
- Available experienced practitioners?
- Total cost of ownership (learning, tooling, hiring)?

Red flags: "Early adopters" without time budget, "Written in X" without benchmarks, "Everyone's talking" without case studies.

## Complexity Budget

Each abstraction must provide 10x value.

Questions:
- What specific problem does this solve?
- Can we solve with existing tools/patterns?
- Maintenance burden (docs, onboarding, debugging)?
- Impact on incident response?

</principles>