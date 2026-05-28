---
name: writing-planning
description: Use this skill when you have specifications or requirements for a multi-step writing task before starting the actual writing process.
---

# Skill body

## Overview

Create a detailed writing implementation plan, assuming the research assistant executing the plan has no background knowledge of our literature database and questionable academic taste. Document everything they need to know: which sections and files each task involves, core arguments, evidence to consult, and how to verify logic. Break the entire plan into manageable tasks. Avoid redundancy (DRY) and unnecessary elements (YAGNI). Focus on argument-driven writing (ADW) and frequent submissions.

**Start with the statement:** “I am using the writing-planning skill to create a writing implementation plan.”

**Context:** This should be executed within a dedicated workspace created by the ideation skill.

**Save the plan to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Task Granularity

**Each step is an action (2-5 minutes):**
- “Write the claim for missing evidence (failing test)” - Step
- “Read it to ensure it lacks support” - Step
- “Draft minimal content to provide evidence support” - Step
- “Check logic and ensure the argument holds” - Step
- “Submit” - Step

## Plan Document Header

**Each plan must start with the following header:**

```markdown
# [Section/Topic Name] Writing Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:sa-execution to implement this plan task-by-task.

**Goal:** [One-sentence description of what this section aims to argue]

**Logical Structure:** [2-3 sentences describing the argument method]

**Theoretical Framework/Tools:** [Key theories/cited sources]

---
```

## Task Structure

```markdown
### Task N: [Subsection Name]

**Files:**
- Create: `exact/path/to/section.tex` (or .md)
- Modify: `exact/path/to/existing.tex:123-145`
- Validate: `tests/exact/path/to/validation_checklist.md`

**Step 1: Propose the claim to be validated (Write the failing test)**

```markdown
<!-- Expected Argument -->
Claim: Variable X has a significant positive effect on Variable Y.
Current Status: There is no empirical support for this claim in the document.
```

**Step 2: Validate the claim's lack of support (Run test to verify it fails)**

Check: Read the current draft
Expectation: No paragraphs or data references found to support this claim.

**Step 3: Draft minimal content (Write minimal implementation)**

```markdown
According to study Z (2023), an increase in X is typically associated with improvements in Y...
```

**Step 4: Validate the argument holds (Run test to verify it passes)**

Check: Read the newly drafted paragraph
Expectation: The claim now has clear evidence support and logical coherence.

**Step 5: Submit (Commit)**

```bash
git add tests/path/validation.md src/path/section.tex
git commit -m "feat: add specific argument about X and Y"
```
```

## Remember
- Always use exact file paths
- The plan should include complete text drafts (not just "add argument")
- Include precise validation instructions and expected outcomes
- Use @ syntax to reference relevant skills
- DRY (Don't Repeat Yourself), YAGNI (You Aren't Gonna Need It), ADW (Argument-Driven Writing), frequent submissions

## Execution Handoff

After saving the plan, provide execution options:

**“The plan is complete and saved to `docs/plans/<filename>.md`. Two execution options:**

**1. Sub-agent driven (this session)** - I will assign a new sub-agent for each task and review between tasks for rapid iteration.

**2. Parallel sessions (independent)** - Use execution to open a new session for batch execution with checkpoints.

**Which method do you choose?”**

**If choosing sub-agent driven:**
- **REQUIRED SUB-SKILL:** Use superpowers:sa-drafting
- Stay in this session
- Each task uses a new sub-agent + peer review

**If choosing parallel sessions:**
- Guide them to open a new session in the workspace
- **REQUIRED SUB-SKILL:** New session uses superpowers:sa-execution
```