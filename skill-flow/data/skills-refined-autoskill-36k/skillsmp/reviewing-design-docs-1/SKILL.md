---
name: reviewing-design-docs
description: Use when reviewing design documents before implementation. Validates structure, goals, technical approach, and milestones against Lyft tech spec template and C4 model principles.
command: review-and-validate-design
---

# Reviewing Design Documents

## Overview

Design documents prevent wasted implementation effort by surfacing unclear requirements, missing context, and unrealistic milestones before coding begins. This skill provides a structured review process that validates documents against the Lyft tech spec template while ensuring technical plans stay at appropriate abstraction levels.

## When to Use

- Before implementing a feature described in a design doc
- When asked to review or validate a design document
- When a design doc exists but implementation keeps stalling or scope keeps changing
- When `/review-and-validate-design` is invoked

## Core Pattern

The review process has four phases. Use task tracking to maintain progress across phases.

### Phase 1: Format Verification

1. Read the design document file
2. Create tasks for the review process using TaskCreate
3. Check for expected sections (see [section-checklist.md](section-checklist.md))
4. For missing or significantly deviant sections:
   - Flag the gap with specific observation
   - Use AskUserQuestion to ask if user wants to add the section or proceed with reason
   - Document any bypass reasons in the review notes

### Phase 2: Section-by-Section Review

Work through each section, validating content quality:

| Section | Key Questions | Quality Signal |
|---------|---------------|----------------|
| **Summary** | Does it stand alone? Could someone understand the project from this alone? | 2-3 sentences, captures what/why/outcome |
| **Background** | Does it motivate the project? Is context sufficient for a new team member? | Explains current state, pain points, why now |
| **Goals** | Are they SMART? Measurable? Time-bound? | Specific outcomes, not activities |
| **Non-Goals** | Do they prevent scope creep? Any contradict Goals? | Explicit exclusions that readers might assume |
| **Plan** | At appropriate abstraction level? Uses C4 concepts? | System/Container/Component, not code |
| **Milestones** | Demo-able? End in runnable artifacts? | Each produces something you can show |
| **Measurable Impact** | Map to Goals? Quantifiable? | Specific metrics, not vibes |
| **Open Questions** | Actually open? Blocking or non-blocking? | Genuine unknowns, not rhetorical |

For issues found:
- Present specific observations (not vague concerns)
- Use AskUserQuestion with concrete options and trade-offs
- Update task status as sections are reviewed

### Phase 3: Iterative Updates

As the user responds to questions:

1. Edit the design document to incorporate agreed changes
2. Re-validate affected sections if changes are significant
3. Track which sections have been reviewed/updated in task list
4. Continue until all sections pass review or user explicitly accepts current state

### Phase 4: Handoff

When review is complete:

1. Summarize changes made and any accepted gaps
2. Mark all review tasks as completed
3. Present the handoff instructions using the exact format below

**Handoff Instructions (present verbatim, substituting the actual filename):**

---

**Design review complete.**

Your design document is ready for C4 decomposition. This will break down your system into containers and components before milestone refinement.

**Next steps:**

1. **Copy this command now** (before clearing):
   ```
   /c4-the-design @path/to/your-design-doc.md
   ```

2. **Clear context:**
   ```
   /clear
   ```

3. **Paste and run** the command you copied in step 1

This hands off your approved design to the C4 decomposition phase, which will:
- Define system context, containers, and components
- Create architecture diagrams
- Prepare the foundation for milestone refinement

---

**The full workflow:**
```
/review-and-validate-design → /c4-the-design → /start-milestone-review → /build-work-plan → /execute-work-plan
```

**Why copy-then-clear?** Long conversations accumulate context that degrades planning quality. `/clear` gives the next phase a clean slate while the design doc file preserves all decisions made during review.

## Abstraction Level Guidance

Design documents should stay at C4 Levels 1-3. Flag content that drops to Level 4 (code).

**Appropriate in Plan section:**
- System context diagrams (what interacts with what)
- Container diagrams (what deploys where, what protocols)
- Component diagrams (what modules exist, responsibilities)
- Interface contracts (API shapes, data formats)

**Diagram format:** Use Mermaid syntax for all diagrams (flowcharts, sequence diagrams, etc.). Mermaid renders natively in most markdown viewers and is more maintainable than ASCII art.

**Inappropriate in Plan section (save for milestone planning):**
- Code snippets or pseudocode
- Class hierarchies or function signatures
- Implementation algorithms
- Database schemas (unless Container-level decision)

When you encounter code-level detail, use AskUserQuestion:
> "The Plan section includes [specific detail]. This level of detail typically belongs in milestone work plans rather than the design doc. Options:
> 1. Move to a 'Technical Notes' appendix (keeps doc focused, preserves detail)
> 2. Remove and defer to milestone planning (simplifies doc)
> 3. Keep as-is (document reason)"

## Demo-able Milestone Criteria

Each milestone must produce BOTH:
1. **Runnable code artifact** — Something executable: script, API endpoint, CLI command, UI
2. **Observable behavior change** — Something demonstrable to stakeholders

### Scaffolding Milestone (M0/M1)

Projects often start with a "sprint zero" milestone for infrastructure setup. This IS demo-able to technical stakeholders:

**Good scaffolding milestone:** "Project scaffolding and test infrastructure"
- Runnable: `pytest` runs with passing placeholder tests and coverage reporting
- Observable: Team can see repo structure, run tests, verify CI passes

This milestone should typically be first. Options:
- Build test infrastructure from scratch
- Integrate with existing team infrastructure
- Both: integrate existing patterns and add project-specific tooling

The key: the demo is "run pytest and see passing tests with coverage" — not just "test harness exists."

### Feature Milestones

**Good milestone:** "Users can reset passwords via email link"
- Runnable: Password reset endpoint works
- Observable: Can demo the email → click → new password flow

**Bad milestone:** "Implement password reset service class"
- Not observable (internal implementation detail)
- Can't demo to non-technical stakeholder

**Bad milestone:** "Research password reset best practices"
- Not runnable (no code artifact)
- Research belongs in Background, not Milestones

## Task Tracking Integration

Create tasks at the start of review to track progress:

```
TaskCreate: "Review design doc format"
TaskCreate: "Review Summary section"
TaskCreate: "Review Background section"
TaskCreate: "Review Goals section"
TaskCreate: "Review Non-Goals section"
TaskCreate: "Review Plan section"
TaskCreate: "Review Milestones section"
TaskCreate: "Review Measurable Impact section"
TaskCreate: "Review Open Questions section"
TaskCreate: "Complete review handoff"
```

Update task status as you work through each section. This provides visibility into review progress and ensures no section is skipped.

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| Reviewing without reading fully first | Miss cross-section inconsistencies | Read entire doc before starting review |
| Accepting vague goals | Can't measure success | Push for SMART criteria |
| Allowing code in Plan | Doc becomes stale, duplicates work | Keep at C4 Level 1-3 |
| Milestones without demos | Can't show progress to stakeholders | Every milestone needs observable output |
| Skipping Open Questions | Unknowns become surprises during implementation | Surface and categorize all unknowns |
| Making changes without asking | User loses ownership of their doc | Always use AskUserQuestion before editing |

## Anti-Rationalizations

- "This goal is understood implicitly" — If it's not written, it's not agreed. Make it explicit.
- "The code example clarifies the design" — Code clarifies implementation, not design. Use diagrams or interface contracts.
- "This milestone is too small to demo" — Then it's a task, not a milestone. Roll up into larger demo-able chunk.
- "Open questions will sort themselves out" — They'll sort themselves into scope creep or missed requirements. Decide now or mark as blocking.
- "The template is too rigid for this project" — The template is a checklist, not a straitjacket. Explain deviations, don't ignore sections.

## Supporting References

- [section-checklist.md](section-checklist.md) — Detailed criteria for each section
- [review-flow.md](review-flow.md) — Expanded process with example questions
- [designing-software](../designing-software/SKILL.md) — C4 model and design principles
- [Lyft Tech Specs Article](https://eng.lyft.com/how-to-write-awesome-tech-specs-86eea8e45bb9) — Original template source

## Summary

1. **Use task tracking.** Create tasks for each section at review start; update as you progress.
2. **Stay at C4 Level 1-3.** Flag code-level detail in Plan section for deferral to milestone planning.
3. **Every milestone must be demo-able.** Runnable code artifact AND observable behavior change.
4. **Use AskUserQuestion before making changes.** Present specific options with trade-offs; user owns the document.
