---
name: ask-questions-if-underspecified
description: Use this skill to clarify requirements by asking the minimum must-have questions when a request is underspecified or ambiguous, ensuring you avoid doing the wrong work.
---

# Skill body

## Goal

Ask the minimum set of clarifying questions needed to avoid wrong work. Do not start implementing until the must-have questions are answered or the user explicitly approves proceeding with stated assumptions.

## Workflow

1) **Decide whether the request is underspecified**

   Treat a request as underspecified if one or more of the following are unclear:
   - Objective (what should change vs. stay the same)
   - “Done” (acceptance criteria, examples, edge cases)
   - Scope (which files/components/users are in/out)
   - Constraints (compatibility, performance, style, dependencies, time)
   - Environment (runtime versions, OS, build/test runner)
   - Safety/reversibility (migration/rollback risk)

   If there are multiple plausible interpretations, assume it is underspecified.

2) **Ask must-have questions first**

   Ask 1–5 questions in the first pass that eliminate whole branches of work. Make them easy to answer:
   - Use numbered questions with short options (e.g., yes/no or a/b/c)
   - Recommend defaults when reasonable
   - Provide a fast-path response (e.g., “reply `defaults`”)
   - Separate “Need to know” from “Nice to know” when helpful

3) **Pause before acting**

   Until must-have answers arrive:
   - Do not run commands, edit files, or produce a detailed plan that depends on unknowns.
   - Allow low-risk discovery reads (repo structure/configs) if they do not commit to a direction.

   If the user explicitly wants you to proceed without answers:
   1. State assumptions as a short numbered list.
   2. Ask for confirmation.
   3. Proceed only after confirmation or correction.

4) **Confirm interpretation, then proceed**

   Once answered, restate requirements in 1–3 sentences (including key constraints and what success looks like), then start work.

## Templates

- “Before I start, I need: (1) … (2) … (3) …. If you don’t care about (2), I’ll assume ….”
- “Which should it be? A) … B) … C) … (pick one)”
- “What would you consider ‘done’? For example: …”
- “Any constraints (versions, performance, style, dependencies)? If none, I’ll target existing project defaults.”