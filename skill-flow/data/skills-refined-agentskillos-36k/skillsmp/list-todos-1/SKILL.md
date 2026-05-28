---
name: list-todos
description: Analyze and prioritize TODO items from TODOS.md
allowed-tools: Read, Glob, Grep, AskUserQuestion, Edit
---

Analyze the TODO items in TODOS.md and produce a prioritized list with implementation guidance.

## Prerequisites

Before starting:
- Confirm `TODOS.md` exists in the current working directory. If it does not exist, **STOP** and ask the user where their project TODOs live.

## Process

1. **Read TODOS.md** from the project root
2. **Read project context (optional)** — Look for context files in this order of preference:
   - VISION.md (if exists, use for project alignment)
   - PRODUCT_SPEC.md (fallback if no VISION.md)
   - TECHNICAL_SPEC.md, AGENTS.md, EXECUTION_PLAN.md (additional context if they exist)
   - If none exist, proceed without project context — analyze based on TODO content alone
3. **Extract TODO items** — Parse all actionable items from TODOS.md
4. **Analyze each item** using the framework below
5. **Sort by priority score** (highest first), break ties by value to project
6. **Output the prioritized list**

## Analysis Framework

For each TODO item, evaluate:

### Ranking Factors

| Factor | Low | Medium | High |
|--------|-----|--------|------|
| **Requirements Clarity** | One-liner with no context, unclear intent | Some details but gaps remain | Detailed spec with acceptance criteria |
| **Ease of Implementation** | Can't assess without clearer requirements | Moderate effort, approach is clear | Straightforward, clear path |
| **Value to Project** (weighted 2×) | Can't assess without clearer requirements | Useful improvement | Core functionality, high impact |

**Assessing Value to Project:**
- If VISION.md or PRODUCT_SPEC.md exists, evaluate how strongly the item aligns with the stated vision and goals
- If no context files exist, assess value based on the TODO item's own description and apparent impact
- Items that directly advance the core vision/goals score higher than tangential improvements
- Consider both immediate utility and strategic alignment

### Critical Rule: Do NOT Infer

**If requirements clarity is LOW, do NOT attempt to infer what the item means.**

- Do NOT guess the implementation approach
- Do NOT assume what problem it solves
- Set Ease and Value to "Cannot assess"
- Focus Open Questions on understanding the basic intent

A one-liner TODO like "Add feature X" with no additional context = LOW clarity, regardless of how obvious it might seem.

### Priority Score Calculation

```
Priority = ((Clarity + Ease + (Value × 2)) / 4 × 10) × Personal Multiplier
```

Where each factor is scored 1-3 (Low=1, Medium=2, High=3). Value is weighted 2× because alignment with project goals is the strongest signal for prioritization.

**Personal Priority Multiplier:**
- Look for `[priority: N]` inline in the TODO item (e.g., `[priority: 1.5]`)
- Valid range: 0.5 to 2.0
- If not specified, default to 1.0
- Examples:
  - `[priority: 2]` — User considers this twice as important
  - `[priority: 0.5]` — User considers this half as important
  - `[priority: 1.5]` — User considers this 50% more important

**If Clarity is LOW, cap the Priority Score at 3/10 maximum** (applied before multiplier).

Adjust score based on:
- **Boost (+1-2):** Blocks other work, security-related, frequently requested
- **Reduce (-1-2):** Speculative, already has workaround, external dependency

## Output Format

### For items with HIGH or MEDIUM requirements clarity:

```markdown
## {N}. {TODO Title}

**Priority Score:** {N}/10 {if multiplier != 1.0: "(base {base}/10 × {multiplier})"}
**Ranking Factors:**
- Requirements Clarity: {Medium|High} — {one sentence explanation}
- Ease of Implementation: {Low|Medium|High} — {one sentence explanation}
- Value to Project: {Low|Medium|High} — {one sentence explanation}
{if multiplier != 1.0: "- Personal Priority: ×{multiplier}"}

**Implementation Notes:**
{2-4 sentences on how to implement: key files to modify, approach, dependencies, estimated scope}

**Open Questions:**
- {Question that would improve requirements clarity}
- {Another question, if applicable}

**Suggested Next Action:** {One of: "Ready to implement", "Needs research", "Consider deferring", "Consider removing"}
```

### For items with LOW requirements clarity:

```markdown
## {N}. {TODO Title}

**Priority Score:** {N}/10 (capped due to unclear requirements{if multiplier != 1.0: ", ×{multiplier} applied"})
**Ranking Factors:**
- Requirements Clarity: **Low** — {explain what's missing: no context, unclear intent, etc.}
- Ease of Implementation: Cannot assess
- Value to Project: Cannot assess
{if multiplier != 1.0: "- Personal Priority: ×{multiplier}"}

**What I understand:** {Brief statement of what little is clear, or "Only the title"}

**What I don't understand:**
- {Specific gap in understanding}
- {Another gap}

**Questions to clarify before proceeding:**
1. {Fundamental question about intent/purpose}
2. {Question about scope}
3. {Question about expected behavior}

**Suggested Next Action:** Clarify requirements first
```

### Summary section:

```markdown
# TODOS Analysis

**Generated:** {date}
**Items Analyzed:** {count}
**Project:** {project name from specs, or directory name}

---

{Individual item analyses, sorted by priority score}

---

## Summary

| Priority | Item | Score | Multiplier | Next Action |
|----------|------|-------|------------|-------------|
| 1 | {title} | {N}/10 | {×N or —} | {action} |
| 2 | {title} | {N}/10 | {×N or —} | {action} |
| ... | ... | ... | ... | ... |

**Ready to implement:** {count}
**Needs clarification:** {count}
**Consider deferring:** {count}
```

## Notes

- If TODOS.md doesn't exist, report: "No TODOS.md found in project root."
- Skip items that are clearly completed (checked boxes)
- Group related items if they should be tackled together
- Consider project phase — items relevant to current phase score higher

---

## Interactive Q&A Phase

After displaying the prioritized list and summary, offer the user an interactive session to clarify requirements.

### Step 1: Offer to Start Q&A

Use the AskUserQuestion tool to ask:

```
Question: "Would you like to clarify requirements for any items?"
Header: "Q&A Mode"
Options:
  - Label: "Yes, let's clarify"
    Description: "I'll ask questions about specific items to improve their requirements"
  - Label: "No, I'm done"
    Description: "Exit without further clarification"
```

If the user selects "No", end the command.

### Step 2: Select Item to Clarify

If the user selects "Yes", use AskUserQuestion to let them pick an item:

```
Question: "Which item would you like to clarify? (Enter the priority number)"
Header: "Select Item"
Options:
  - Label: "1. {first item title}"
    Description: "Score: {N}/10 — {next action}"
  - Label: "2. {second item title}"
    Description: "Score: {N}/10 — {next action}"
  - Label: "3. {third item title}"
    Description: "Score: {N}/10 — {next action}"
  - Label: "4. {fourth item title}"
    Description: "Score: {N}/10 — {next action}"
```

Note: Only show up to 4 items per question (tool limit). If more items exist, include "Other" option for the user to type a number.

### Step 3: Summarize Current State

Before asking questions, output a summary of the selected item's current state so the user has context:

```markdown
---

## Clarifying: {Item Title}

**Current Score:** {N}/10 {multiplier if applicable}
**Requirements Clarity:** {Low|Medium|High}

**What's documented:**
{Summary of what's currently in TODOS.md for this item — existing description, any prior clarifications}

**What needs clarification:**
{List the open questions that will be asked}

---
```

This gives the user context before they start answering questions.

### Step 4: Ask Open Questions One at a Time

For the selected item, ask each open question individually using AskUserQuestion:

```
Question: "{The open question from the analysis}"
Header: "{Item title (truncated)}"
Options:
  - Label: "{Claude's recommended answer}"
    Description: "(Recommended) {Brief rationale for this recommendation}"
  - Label: "{Alternative answer 1}"
    Description: "{Why someone might choose this}"
  - Label: "{Alternative answer 2}"
    Description: "{Why someone might choose this}"
```

**Important guidelines for questions:**
- Ask ONE question at a time
- Always provide Claude's recommendation as the FIRST option with "(Recommended)" in the description
- Provide 2-3 reasonable alternatives as other options
- The user can always select "Other" to provide a custom answer
- Wait for each answer before asking the next question

### Step 5: Update TODOS.md with Clarifications

After all questions for an item are answered, update TODOS.md:

1. Find the item's section in TODOS.md
2. Add a new subsection or update the existing description with the clarifications
3. Format the clarifications clearly:

```markdown
### {Item Title}

{Original description}

**Clarifications (from Q&A {date}):**
- {Question 1}: {Answer 1}
- {Question 2}: {Answer 2}
- {Question 3}: {Answer 3}
```

Use the Edit tool to make these updates.

### Step 6: Summarize Understanding

After updating TODOS.md, output a summary of the clarified item:

```markdown
---

## Summary: {Item Title}

**Updated Score:** {N}/10 (re-evaluate based on new clarity)
**Requirements Clarity:** {Low|Medium|High} (updated)

**Current understanding:**
{2-4 sentences synthesizing what we now know about this item — the problem it solves, the approach, key decisions made}

**Implementation approach:**
{Brief description of how to implement, based on clarifications}

**Remaining questions (if any):**
- {Any questions still unanswered}

---
```

### Step 7: Check Implementation Readiness

Use AskUserQuestion to ask if the item is ready for implementation:

```
Question: "Is this item ready for implementation?"
Header: "Ready?"
Options:
  - Label: "Yes, mark as [ready]"
    Description: "Add [ready] tag to TODOS.md — item can be implemented"
  - Label: "No, needs more clarification"
    Description: "Continue Q&A on this item"
  - Label: "No, move to another item"
    Description: "Select a different item to clarify"
  - Label: "No, I'm done for now"
    Description: "Exit Q&A mode"
```

**If "Yes, mark as [ready]":**
- Add `[ready]` tag to the TODO item in TODOS.md
- Ask if the user wants to clarify another item (go to Step 8)

**If "No, needs more clarification":**
- Ask what additional questions need answering
- Return to Step 4 with new questions

**If "No, move to another item":**
- Return to Step 2 to select another item

**If "No, I'm done for now":**
- Go to Exit Summary

### Step 8: Continue or Exit

After marking an item ready, use AskUserQuestion to ask:

```
Question: "Item marked [ready]. Would you like to clarify another item?"
Header: "Continue?"
Options:
  - Label: "Yes, continue"
    Description: "Select another item to clarify"
  - Label: "No, I'm done"
    Description: "Exit Q&A mode"
```

If "Yes", return to Step 2. If "No", go to Exit Summary.

### Exit Summary

When exiting Q&A mode, output:

```markdown
## Q&A Session Complete

**Items clarified:** {count}
{List of items that were clarified with brief summary of decisions made}

TODOS.md has been updated with the clarifications above.
```
