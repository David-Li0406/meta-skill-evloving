---
name: create-plan
description: Plan-first workflow with upfront investigation and design. Use when the user asks for a thought-through plan, needs deep analysis before execution, or wants the plan captured as tasks/logs in bd.
---

# Plan First

## Apply the prompt

- Prepend the prompt content to the user request.
- Produce a short, actionable plan before doing any work.
- Stop after presenting the plan; do not implement, edit files, or run non-read-only commands until the user explicitly approves.
- Ask clarifying questions and iterate on the plan as needed; do not proceed until answers are received.
- Investigate and explore as needed (read-only); summarize findings to inform the plan.
- During planning, create and refine `bd` tasks as you work, updating them as needed as understanding evolves. Update description, notes, design, acceptance criteria, dependency ordering, or epic organization as needed.
- Completion for this skill is a fully refined set of `bd` tasks ready for another agent to implement without needing to
do further investigation and refinement.

## Planning checklist

- Gather requirements and constraints; ask clarifying questions.
- Investigate existing code, docs, and prior art.
- Explore alternatives and tradeoffs when design choices matter.
- Identify the main goal.
- Break the work into manageable steps.
- Call out risks or obstacles and how to address them.
- Note required tools or resources.
- If deadlines matter, estimate timing.
- Review the plan to confirm it is logical and feasible.
- Plan testing and verification steps.
- Plan rollout, deployment, and monitoring.
- Map steps to `bd` tasks when appropriate.
- Keep the plan concise and feasible.
