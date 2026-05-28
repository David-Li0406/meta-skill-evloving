# ExecPlan Authoring Guide

This guide contains the detailed requirements for writing effective ExecPlans. Read this when creating or revising a plan.

## The Bar

A single, stateless agent—or a human novice—must be able to read your ExecPlan from top to bottom and produce a working, observable result.

**SELF-CONTAINED, SELF-SUFFICIENT, NOVICE-GUIDING, OUTCOME-FOCUSED.**


## Purpose and Intent Come First

Begin by explaining why the work matters from a user's perspective: what someone can do after this change that they could not do before, and how to see it working.

The agent executing your plan can list files, read files, search, run the project, and run tests. It does not know any prior context and cannot infer what you meant. Repeat any assumption you rely on.

Do not point to external blogs or docs. If knowledge is required, embed it in the plan in your own words.


## Anchoring to Observable Outcomes

State what the user can do after implementation, the commands to run, and the outputs they should see.

**Good**: "After starting the server, navigating to http://localhost:8080/health returns HTTP 200 with body OK"

**Bad**: "Added a HealthCheck struct"

If a change is internal, explain how to demonstrate its effect through tests or scenarios.


## Specifying Repository Context

Name files with full repository-relative paths. Name functions and modules precisely. Describe where new files should be created.

When touching multiple areas, include an orientation paragraph explaining how those parts fit together.

When running commands, show the working directory and exact command line. When outcomes depend on environment, state assumptions and provide alternatives.


## Avoiding Common Failure Modes

Do not rely on undefined jargon.

Do not describe a feature so narrowly that the code compiles but does nothing meaningful.

Do not outsource key decisions to the reader. Resolve ambiguity in the plan and explain why.

Err toward over-explaining user-visible effects and under-specifying incidental implementation details.


## Validation Requirements

Include instructions to run tests, start the system, and observe something useful.

Include expected outputs and error messages so a novice can distinguish success from failure.

State the exact test commands and how to interpret results.


## Idempotence and Safety

Write steps that can run multiple times without damage. If a step can fail halfway, include retry or recovery instructions. Prefer additive, testable changes.


## Capturing Evidence

When steps produce output, include concise transcripts focused on proving success. Prefer small excerpts over large blobs.


## Writing Milestones

Introduce each milestone with a paragraph describing:
- The scope
- What will exist at the end that did not exist before
- The commands to run
- The acceptance criteria

Keep it readable as a story: goal, work, result, proof.

Progress and milestones are distinct. Milestones tell the story; Progress tracks granular work. Both must exist.

Each milestone must be independently verifiable.


## Maintaining Living Sections

### Progress

Use checkboxes. Document every stopping point. Split partial tasks. Add timestamps to completed items.

    - [x] (2025-01-20 14:30Z) Completed example
    - [ ] Incomplete item
    - [ ] Partial (completed: X; remaining: Y)

### Surprises & Discoveries

Document unexpected behaviors with evidence. Test output is ideal.

    - Observation: Library throws instead of returning null
      Evidence: TokenExpiredError: jwt expired

### Decision Log

Record every decision with rationale and date.

    - Decision: Use HS256 instead of RS256
      Rationale: Single-server deployment; no cross-service verification needed
      Date: 2025-01-20

### Outcomes & Retrospective

At completion, summarize what was achieved, what remains, and lessons learned. Compare against original purpose.


## Prototyping

Include prototyping milestones when they de-risk a change. Clearly label scope as "prototyping." State criteria for promoting or discarding the prototype.

When working with multiple new libraries, create independent spikes proving each works in isolation.


## Parallel Implementations

Acceptable when they reduce risk or keep tests passing during migration. Describe how to validate both paths and retire one safely.


## Defining Terms

If you use "middleware," "daemon," "RPC," "gateway," or similar:
1. Define it immediately
2. Name the files or commands where it appears in this repository

Do not say "as defined previously" or "according to the architecture doc."


## Updating Plans

When revising:
1. Reflect changes across ALL sections
2. Update living document sections
3. Add a dated note at the bottom explaining what changed and why
4. Maintain self-containment

ExecPlans must describe not just the WHAT but the WHY.


## Required Sections Checklist

Every ExecPlan must contain:

- [ ] Purpose / Big Picture
- [ ] Progress (with checkboxes)
- [ ] Surprises & Discoveries
- [ ] Decision Log
- [ ] Outcomes & Retrospective
- [ ] Context and Orientation (with Key Files and Terms)
- [ ] Plan of Work
- [ ] At least one Milestone
- [ ] Concrete Steps
- [ ] Validation and Acceptance
- [ ] Interfaces and Dependencies

Use `scripts/validate_plan.py` to verify structure automatically.
