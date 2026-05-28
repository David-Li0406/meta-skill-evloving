---
name: personal:implement-plan
description: Use this skill when you need to execute an approved implementation plan from the plans directory while tracking progress.
---

# Implement Plan

You are tasked with implementing an approved technical plan from `plans/`. These plans contain phases with specific changes and success criteria.

## Getting Started

When given a plan path:
- Read the plan completely and check for any existing checkmarks (- [x]).
- Read the original ticket and all files mentioned in the plan.
- **Read files fully** - never use limit/offset parameters; you need complete context.
- Think deeply about how the pieces fit together.
- Create a todo list to track your progress.
- Start implementing if you understand what needs to be done.

If no plan path is provided, ask for one.

## Implementation Philosophy

Plans are carefully designed, but reality can be messy. Your job is to:
- Follow the plan's intent while adapting to what you find.
- Implement each phase fully before moving to the next.
- Verify your work makes sense in the broader codebase context.
- Update checkboxes in the plan as you complete sections.

When things don't match the plan exactly, think about why and communicate clearly. The plan is your guide, but your judgment matters too.

## Keeping the Plan Updated

The plan is a living document that becomes the record of what was actually done. **The plan will be used as context for creating the pull request**, so keeping it accurate and up-to-date directly impacts the quality of the PR description.

As you implement, keep the **entire plan** current - not just checkboxes:

1. **Check off testing checkboxes** as tests pass.
2. **Fill in Test Results tables** with actual command output and status.
3. **Update the Implementation Approach** if you had to adapt or chose a different path.
4. **Revise Alternatives Considered** if you evaluated new options during implementation.
5. **Add discovered issues** or complications not anticipated in the plan.
6. **Update Motivation or Context** if you learned something that changes the "why".
7. **Adjust Non-Code Tasks** as you discover new ones or complete existing ones.
8. **Refine Guidance for Reviewers** based on what you learned needs careful review.

The goal: someone reading the plan after implementation should understand exactly what was done and why, not just what was originally planned.

If you encounter a mismatch:
- STOP and think deeply about why the plan can't be followed.