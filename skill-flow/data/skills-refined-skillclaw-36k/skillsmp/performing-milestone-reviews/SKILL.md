---
name: performing-milestone-reviews
description: Use when reviewing milestones in a design document or creating well-formed milestones from scratch. Covers job stories, descriptions, acceptance criteria, and demos.
command: start-milestone-review
---

# Performing Milestone Reviews

**ALWAYS** load `writing-effective-acceptance-criteria` before starting — it provides the AC format guidance this skill depends on.

## Overview

Milestones bridge design intent and implementation. A vague milestone ("implement the feature") provides no guidance; a well-formed milestone tells engineers (human and LLM) exactly what to build, why it matters, and how to know when it's done. This skill guides interactive review and refinement of milestones to ensure they're actionable and complete.

## When to Use

- Reviewing milestones in a design document before implementation
- Fleshing out vague milestone descriptions
- Creating milestones for a new feature or project
- When milestones lack job stories, clear descriptions, or testable AC

## Entry Point

When the user invokes `/start-milestone-review`, follow this sequence:

1. **Locate the source document.** If the user provided a path, read it. If not, use `AskUserQuestion`:
   - Point to a design document
   - Point to another document with milestones
   - Start an interactive session (no source document)
   - Stop

2. **Create a working document.** Create `<source-doc-name>-milestones-review.md` next to the source document. This working document captures the review process and iterations.

3. **Identify milestones.** Extract existing milestones from the source document, or work with the user to define them interactively. Write them to the working document.

4. **Pressure test milestones.** Before fleshing out, validate the milestone set is correct (see [Pressure Testing](#pressure-testing-milestones)). Document findings in the working document.

5. **Review each milestone section by section.** For each milestone:
   - Propose job story with rationale → get approval
   - Propose description with rationale → get approval
   - Propose AC with rationale → get approval
   - Propose demo with rationale → get approval
   - Write completed milestone to working document
   - Check for conflicts with previous milestones

6. **Determine integration.** Ask the user how to integrate:
   - Update the source document in place
   - Keep the working document as the milestone reference
   - Both (update source + keep working doc for audit trail)

## Pressure Testing Milestones

**When**: Before fleshing out milestones with job stories and AC. Also during review when updates might conflict.

**Why**: Component design often reveals gaps, dependency issues, and scope ambiguity that invalidate milestones. Fleshing out milestones that are fundamentally wrong wastes effort.

**Prerequisites**: Ideally, system/container/component design has been done. If not, pressure testing will be limited to logical consistency checks.

### Pressure Test Questions

Ask these questions before proceeding to flesh out milestones:

| Question | What It Reveals |
|----------|-----------------|
| Do milestones cover all identified components? | Missing work (e.g., "Job Manager has no milestone") |
| Are milestones in correct dependency order? | Build sequence issues (e.g., "Can't build Activity Fetcher before Session Manager") |
| Do any milestones reference removed/changed features? | Stale descriptions (e.g., "M6 demos a command that was removed") |
| Are there unanswered questions that impact scope? | Ambiguity (e.g., "M4/M5 unclear if they persist or display-only") |
| Does each milestone map to at least one component? | Orphan milestones or wrong abstraction level |

### Pressure Test Process

1. **If component design exists**: Map components to milestones. Look for:
   - Components with no covering milestone → missing milestone
   - Milestones that don't map to components → wrong abstraction or orphan
   - Dependency violations → reorder milestones

2. **If no component design**: Check logical consistency:
   - Does each milestone have a clear deliverable?
   - Are there implicit dependencies between milestones?
   - Do milestone descriptions match the plan section?

3. **Surface issues to the user**: Present gaps and ask how to resolve:
   - Add missing milestones?
   - Remove/merge orphan milestones?
   - Reorder for dependencies?
   - Clarify scope ambiguity?

4. **Get approval before proceeding**: Don't flesh out milestones until the set is validated.

### During-Review Conflict Checks

When fleshing out each milestone, watch for:

| Conflict Type | Example | Resolution |
|---------------|---------|------------|
| Scope overlap | M4 and M5 both claim to "store shot data" | Clarify which milestone owns storage |
| Dependency violation | M5's AC assumes M6 is complete | Reorder or adjust AC |
| Demo inconsistency | M3's demo uses a command defined in M2's AC | Verify M2 is sequenced first |
| AC contradiction | M4 says "display only" but M6 says "query stored data from M4" | Clarify data flow |

If conflicts emerge during review, pause and resolve before continuing.

## Milestone Template (Enforced)

Every milestone must follow this structure:

```markdown
### M#: [Title]

**Job Story**: When [situation], I want [motivation], so I can [outcome].

**Description**: [What and why — include design requirements, omit implementation details]

**Acceptance Criteria**:
- [ ] AC1
- [ ] AC2
- [ ] ... (max 5, excluding tests)

**Demo**: [Observable demonstration that maps to the job story outcome]
```

## Core Pattern: Reviewing a Single Milestone

For each milestone, work through these steps **section by section**, getting user approval at each step before proceeding. This granular approach ensures alignment and catches issues early.

### Step 1: Write the Job Story

**Format**: When [situation], I want [motivation], so I can [outcome].

**Questions to surface**:
1. Who is the primary persona? (user, developer, future maintainer)
2. What situation triggers the need?
3. What outcome do they care about?

**If multiple personas apply**: Pick the primary one for the job story. Secondary needs can appear in AC.

**Validation**:
- [ ] Has all three parts (situation, motivation, outcome)
- [ ] Primary persona is clear
- [ ] Outcome is user-observable, not implementation-focused

**Review process**:
1. Present the proposed job story with rationale for each part
2. Use `AskUserQuestion` with options:
   - Keep proposed
   - Offer feedback (user provides changes)
   - Other (free-form input)
3. Iterate until approved, then proceed to Step 2

### Step 2: Write the Description

**Principle**: What and why, not how — except for design requirements.

**Questions to surface**:
1. What does this milestone deliver?
2. Why does it matter? (motivation for engineers)
3. Which "how" details are design requirements vs implementation details?

**Design requirement vs implementation detail**:
- Design requirement: Decided in the design doc's Plan section (e.g., "Use typer for CLI")
- Implementation detail: Developer's choice during coding (e.g., "Use `app.command()` decorator")

Descriptions should include design requirements but omit implementation details.

**Validation**:
- [ ] Explains WHY, not just WHAT
- [ ] Includes design requirements from the Plan section
- [ ] Omits implementation details (unless they're design requirements)
- [ ] Answers "why should I care about building this?"

**Review process**:
1. Present the proposed description with rationale for key phrases
2. Use `AskUserQuestion` with options:
   - Keep proposed
   - Offer feedback (user provides changes)
   - Other (free-form input)
3. Iterate until approved, then proceed to Step 3

### Step 3: Write Acceptance Criteria

**Constraints**:
- Testable (can verify pass/fail)
- Target 5 AC (excluding automated tests) — more is a signal, not a hard limit
- No compound conditions ("X and Y") — split these

**Format options** (ask user preference if unclear):

| Format | When to Use |
|--------|-------------|
| Checklist | Simple verification, scaffolding, setup |
| Given/When/Then | Behavior specs, test automation |
| Rules-based | Business logic, conditionals ("if X then Y") |
| Quantitative | Performance, SLAs, specific numbers |

**When you identify more than 5 AC**:

1. **Propose all AC first.** Don't silently drop criteria — they may be important.
2. **Use `AskUserQuestion`** to present options:
   - Keep all AC (justified if truly atomic and necessary)
   - Split into separate milestones (if AC cluster into distinct deliverables)
   - Demote some to task-level AC (if some are implementation details)
   - Consolidate redundant AC (if some overlap)
3. **Document the decision.** Note why the constraint was exceeded or how it was resolved.

**Validation**:
- [ ] Each AC is testable (clear pass/fail)
- [ ] AC count discussed with user if > 5
- [ ] AC match the specificity of the description
- [ ] No compound conditions ("X and Y") — split these

**Review process**:
1. Present each proposed AC with rationale for why it's testable and necessary
2. If count > 5, use `AskUserQuestion` to discuss options (see above)
3. Use `AskUserQuestion` with options:
   - Keep proposed
   - Offer feedback (user provides changes)
   - Other (free-form input)
4. Iterate until approved, then proceed to Step 4

### Step 4: Define the Demo

**Principle**: Observable demonstration that AC are met.

A good demo:
- Can be performed in front of a stakeholder (technical or non-technical, depending on the component)
- Shows the "so I can [outcome]" from the job story
- Exercises multiple AC at once

**Note**: Demos may target engineers (e.g., REPL demonstrations for internal components) or end-users (e.g., CLI workflows). Match the demo audience to the milestone's purpose.

**Validation**:
- [ ] Is observable (not "run tests")
- [ ] Maps to the job story outcome
- [ ] Audience is appropriate for the component (engineer vs end-user)

**Review process**:
1. Present the proposed demo with rationale for how it validates the job story outcome
2. Use `AskUserQuestion` with options:
   - Keep proposed
   - Offer feedback (user provides changes)
   - Other (free-form input)
3. Iterate until approved, then proceed to next milestone

## Milestone Grain

AC exists at multiple levels — don't confuse them:

| Level | Purpose | Specificity |
|-------|---------|-------------|
| Milestone AC | Verifies milestone is done (demo-focused) | Matches milestone description |
| Task AC | Verifies individual work item is done | Implementation-focused |

**Heuristic**: If your description says "command groups for auth, activities, export," then AC can enumerate those groups. Task-level AC (like "auth has login and status subcommands") emerge during work planning.

## Validation Checklist

Before finalizing each milestone, verify:

- [ ] Job story has all three parts (situation, motivation, outcome)
- [ ] Description explains WHY, not just WHAT
- [ ] Description includes design requirements, omits implementation details
- [ ] AC are testable (can verify pass/fail)
- [ ] AC count discussed with user if > 5
- [ ] Demo is observable and maps to job story outcome

Present this checklist to the user and get explicit approval before moving to the next milestone.

## Anti-Patterns

| Anti-pattern | Problem | Fix |
|--------------|---------|-----|
| No job story | No "why" context for engineers | Add situation/motivation/outcome |
| Description is all "how" | Prescriptive, not outcome-focused | Rewrite focusing on what and why |
| Vague AC ("works correctly") | Not testable | Specify observable behavior |
| 6+ AC without discussion | User didn't consciously choose scope | Propose all AC, then ask user how to handle |
| AC enumerate tasks | Wrong grain | Raise to milestone level; save details for task breakdown |
| Demo is "run tests" | Not stakeholder-observable | Describe user-visible behavior |
| Implementation detail in description | Constrains engineer's choices | Remove unless it's a design requirement |

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| Skipping job story | Milestone has no motivation | Always write the job story first |
| Copy-pasting AC from requirements | AC may not be testable or well-scoped | Rewrite each AC to be testable |
| "User can do X" without context | Missing the "why" | Full job story with outcome |
| Mixing milestone and task grain | Confusion about what's done | Keep milestone AC demo-focused |
| Description that's just a task list | Not explaining the milestone's purpose | Summarize what and why |

## Anti-Rationalizations

- "The job story is obvious" — If it's obvious, it's quick to write. Engineers (especially LLMs) benefit from explicit context.
- "We'll figure out AC during implementation" — AC discovered during implementation become bugs or scope creep. Define them now.
- "Five AC is too restrictive" — Five is a signal, not a prison. If you need more, propose them all and ask the user how to proceed. The constraint exists to surface scope conversations, not to silently drop important criteria.
- "The description in the design doc is enough" — Design doc descriptions are often vague. Flesh them out with why.
- "This milestone is too simple for a job story" — Simple milestones still serve a purpose. Articulate it.

## Output Options

After reviewing all milestones, ask the user:

1. **Update source document** — Replace the original milestone section with the fleshed-out versions
2. **Generate separate document** — Create a new `*-milestones.md` file with the complete milestone definitions

If updating the source document, preserve the document structure and only modify the Milestones section.

## Example: Before and After

**Before** (from design doc):
```markdown
### M2: CLI scaffolding with help output
Build the `typer`-based CLI skeleton with command groups (data collection,
configuration, reporting). Demo: Run `trackman --help` and see available
commands and subcommands.
```

**After** (fleshed out):
```markdown
### M2: CLI scaffolding with help output

**Job Story**: When I first install the Trackman tool, I want to see what
commands are available and how they're organized, so I can understand what
the tool is capable of and how to use it.

**Description**: A `typer`-based CLI organized into command groups (auth,
activities, export). The structure enables progressive discovery — `--help`
at any level reveals what's available, making the tool self-documenting and
learnable. This skeleton also guides future development: both human and LLM
engineers can see where new functionality belongs.

**Acceptance Criteria**:
- [ ] `trackman --help` displays available command groups with descriptions
- [ ] `trackman auth --help` displays auth subcommands (login, status)
- [ ] `trackman activities --help` displays activities subcommands
- [ ] `trackman export --help` displays export subcommands (csv, json)
- [ ] All commands return exit code 0 (no crashes on help)

**Demo**: Run `trackman --help`, then `trackman activities --help` to show
progressive discovery working.
```

## Handoff

When milestone review is complete:

1. Summarize the milestones (count, key changes, any accepted gaps)
2. Verify milestones are integrated into the design document
3. Present the handoff instructions using the exact format below

**Handoff Instructions (present verbatim, substituting the actual filename):**

---

**Milestone review complete.**

Your milestones now have job stories, descriptions, acceptance criteria, and demos. The next step is creating a detailed work plan for implementation.

**Next steps:**

1. **Copy this command now** (before clearing):
   ```
   /build-work-plan @path/to/your-design-doc.md
   ```

2. **Clear context:**
   ```
   /clear
   ```

3. **Paste and run** the command you copied in step 1

This hands off your refined milestones to work plan creation, which will:
- Investigate the codebase for testing patterns and design assumptions
- Decompose each milestone into granular, TDD-aligned tasks
- Create milestone files in `docs/work-plans/`

---

**The full workflow:**
```
/review-and-validate-design → /c4-the-design → /start-milestone-review → /build-work-plan → /execute-work-plan
```

## Summary

1. **Always write the job story first.** It provides the "why" that guides description and AC.
2. **Descriptions explain what and why, not how.** Include design requirements; omit implementation details.
3. **Target 5 AC per milestone.** More than 5 is a signal — propose all, then ask user how to proceed.
4. **Demos are stakeholder-observable.** Not "run tests" — describe what a user would see.
5. **Work interactively.** Review one milestone at a time; get user approval before proceeding.
