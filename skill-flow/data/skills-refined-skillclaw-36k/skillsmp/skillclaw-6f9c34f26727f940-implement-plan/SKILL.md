---
name: implement-plan
description: Use this skill when you need to implement an approved technical plan from `thoughts/shared/plans/`, ensuring thorough verification and adaptation to real-world conditions.
---

# Skill body

## Execution Modes

You have two execution modes:

### Mode 1: Direct Implementation (Default)
For small plans (3 or fewer tasks) or when user requests direct implementation.
- You implement each phase yourself.
- Context accumulates in the main conversation.
- Use this for quick, focused implementations.

### Mode 2: Agent Orchestration (Recommended for larger plans)
For plans with 4+ tasks or when context preservation is critical.
- You act as a thin orchestrator.
- Agents execute each task and create handoffs.
- Compaction-resistant: handoffs persist even if context compacts.
- Use this for multi-phase implementations.

**To use agent orchestration mode**, say: "I'll use agent orchestration for this plan" and follow the Agent Orchestration section below.

---

## Getting Started

When given a plan path:
- Read the plan completely and check for any existing checkmarks (- [x]).
- Read the original ticket and all files mentioned in the plan.
- **Read files fully** - never use limit/offset parameters; you need complete context.
- Think deeply about how the pieces fit together.
- Create a todo list to track your progress.

### Pre-Implementation Risk Check

Before starting implementation, run a deep pre-mortem:

```
/premortem deep <plan-path>
```

This analyzes the plan against comprehensive checklists:
- Technical risks (scalability, dependencies, data, security).
- Integration risks (breaking changes, migration, rollback).
- Process risks (unclear requirements, stakeholder input).
- Testing risks (coverage gaps, load testing needs).

**If HIGH severity risks are identified:**
- The premortem will block via AskUserQuestion.
- User must: accept risks explicitly, add mitigations, or research solutions.
- If mitigations are added, update the plan before proceeding.

**Skip premortem if:**
- Plan already has a "## Risks (Pre-Mortem)" section with mitigations.
- User explicitly requests to skip (`--skip-premortem`).

After the premortem passes, start implementing if you understand what needs to be done.

If no plan path is provided, ask for one.

## Implementation Philosophy

Plans are carefully designed, but reality can be messy. Your job is to:
- Follow the plan's intent while adapting to what you find.
- Implement each phase fully before moving to the next.
- Verify your work makes sense in the broader codebase context.
- Update checkboxes in the plan as you complete sections.

When things don't match the plan exactly, think about why and communicate clearly. The plan is your guide, but your judgment matters too.

If you encounter a mismatch:
- STOP and think deeply about why the plan can't be followed.
- Present the issue clearly:
  ```
  Issue in Phase [N]:
  Expected: [what the plan says]
  Found: [actual situation]
  Why this matters: [explanation]

  How should I proceed?
  ```

## Verification Approach

After implementing a phase:
- Run the success criteria checks (usually `make check test` covers everything).
- Fix any issues before proceeding.
- Update your progress in both the plan and your todos.
- Check off completed items in the plan file itself using Edit.
- **Pause for human verification**: After completing all automated verification for a phase, pause and inform the human that the phase is ready for manual testing. Use this format:
  ```
  Phase [N] Complete - Ready for Manual Verification

  Automated verification passed:
  - [List automated checks that passed]

  Please perform the manual verification steps listed in the plan:
  - [List manual verification items from the plan]

  Let me know when manual testing is complete so I can proceed to Phase [N+1].
  ```

If instructed to execute multiple phases consecutively, skip the pause until the last phase. Otherwise, assume you are just doing one phase.