# Diátaxis Framework - Complete Guide

## Table of Contents

1. [Tutorials (Learning-Oriented)](#tutorials)
2. [How-to Guides (Task-Oriented)](#how-to-guides)
3. [Reference (Information-Oriented)](#reference)
4. [Explanation (Understanding-Oriented)](#explanation)
5. [Anti-Patterns to Avoid](#anti-patterns)
6. [Quality Checklist](#quality-checklist)

## Tutorials

Tutorials are **lessons** that guide learners through practical activities under your guidance. Think of a cookbook recipe that a cooking student would follow while learning.

### Purpose

- Teach skills through guided practice
- Build confidence and competence
- Create the "feeling of doing" — joined-up purpose, action, and result
- Minimize cognitive load while maximizing practical progress

### Key Principles

✓ **Show the destination upfront** — "By the end, you'll have X"

✓ **Deliver visible results early and often** — Users see progress quickly

✓ **Maintain narrative of expectations** — "You will notice that…", "You should see…"

✓ **Point out what learners should observe** — Guide attention to important details

✓ **Focus on the concrete, not abstract** — Use specific, tangible examples

✓ **Ruthlessly minimize explanation** — Link to it, don't embed it

✓ **Encourage and permit repetition** — Let users practice multiple times

✓ **Ignore options and alternatives** — Teach one way; link to alternatives elsewhere

✓ **Aspire to perfect reliability** — Every step must work as described

### Language Patterns

- "We will…" (first-person plural, tutor-learner relationship)
- "In this tutorial, we will create…"
- "First, do X. Now, do Y."
- "The output should look something like…"
- "Notice that… Remember that… Let's check…"
- Imperative: "Click", "Type", "Choose"
- Use numbered steps: 1, 2, 3

### Structure Template

```markdown
# Getting Started with [Topic]

Learn how to [specific skill] in [timeframe].

## What you'll build
[Clear description of the end result]

## Before you start
[Prerequisites, no more than 3-4 items]

## Step 1: [Concrete task]
[Instructions with expected output]

## Step 2: [Concrete task]
[Instructions with expected output]

## What you've learned
[Summary of skills acquired]

## Next steps
- [Link to how-to guide for next goal]
- [Link to explanation for deeper understanding]
```

### What to Avoid

- Don't explain why things work — link to Explanation instead
- Don't offer choices or alternatives — teach one way
- Don't assume prior knowledge — link to Tutorials for prerequisites
- Don't jump to advanced topics
- Don't say "you might want to" — be directive

---

## How-to Guides

How-to guides are **directions** that solve real-world problems. They assume competence and focus on accomplishing a specific task. Think of a recipe a chef uses to make a dish they already know how to make.

### Purpose

- Solve specific, practical problems
- Address real-world complexity and edge cases
- Serve as a reference while doing work
- Provide executable instructions as a contract

### Key Principles

✓ **Goal-oriented** — Solve a clear, concrete problem

✓ **Assume competence** — User knows the basics; don't teach foundational skills

✓ **Omit the unnecessary** — Practical usability over completeness

✓ **Logical sequence** — Steps flow in a natural, thinking-driven order

✓ **Seek flow** — Smooth progress grounded in how users actually think

✓ **Executable instructions** — Every step works; it's a contract

✓ **Real-world complexity** — Address common variations and edge cases

✓ **Clear naming** — "How to [achieve specific outcome]"

### Language Patterns

- "This guide shows you how to…"
- "If you want X, do Y. To achieve W, do Z."
- "Refer to the X reference guide for full options."
- "When you encounter [situation], [action]"
- "To accomplish X, follow these steps:"
- Conditional: "If X, then do Y"

### Structure Template

```
# How to [Achieve Specific Outcome]

This guide shows you how to [outcome] without [common pitfall].

## When to use this guide
[Who this is for, what problem it solves]

## Before you start
[Minimal prerequisites]

## Steps

### [Subtask 1]
[Instructions]

### [Subtask 2]
[Instructions]

## Troubleshooting

**Problem: X**
Solution: Y

## Next steps
- [Link to related how-to guides]
- [Link to reference for advanced options]
- [Link to explanation for conceptual background]
```

### What to Avoid

- Don't teach basic skills — link to Tutorials
- Don't explain why things work — link to Explanation
- Don't offer unnecessary alternatives — focus on the most direct path
- Don't assume prior knowledge — link to Tutorial prerequisites
- Don't be overly comprehensive — link to Reference for full options

---

## Reference

Reference guides are **technical descriptions** of machinery. They are austere, accurate, and consulted rather than read. Think of a dictionary or API documentation.

### Purpose

- Provide complete, accurate information
- Describe how things work, not how to use them
- Support lookups and exploration
- Be authoritative and unambiguous

### Key Principles

✓ **Describe and only describe** — No instructions, only facts

✓ **Neutral and objective** — No opinions, preferences, or guidance

✓ **Precise and accurate** — No approximations or "mostly correct"

✓ **Structured by machinery** — Mirror how the system is actually built

✓ **Adopt standard patterns** — Use consistent structure throughout

✓ **Comprehensive** — Include all significant options and parameters

✓ **Wholly authoritative** — No doubt or ambiguity

✓ **Examples for illustration** — Show without instructing

### Language Patterns

- "X is a [noun] that [describes function]"
- "X inherits from Y and is defined in Z"
- "Sub-commands are: a, b, c, d, e, f"
- "Must use A. Must not apply B unless C."
- "Optional. Default: X"
- Lists and tables for comparison
- Definitions that stand alone

### Structure Template

```
# [Component] Reference

[One-sentence description of what this is]

## Overview
[Concise technical description]

## [Category 1]

### [Item 1]
- Description
- Parameters/options
- Examples (illustrative, not instructional)

### [Item 2]
[Same structure]

## [Category 2]

[Same structure]

## Related references
- [Other reference pages]
```

### What to Avoid

- Don't include how-to instructions — link to How-to Guides
- Don't explain philosophy or design decisions — link to Explanation
- Don't organize by use case — organize by structure
- Don't simplify for beginners — be complete and precise
- Don't offer opinions or recommendations

---

## Explanation

Explanation is **discursive discussion** that deepens understanding. It answers "Why?" and "Can you tell me about…?" Think of an essay or research paper.

### Purpose

- Provide conceptual clarity
- Explain design decisions and tradeoffs
- Connect to broader context
- Acknowledge complexity and alternatives

### Key Principles

✓ **Make connections** — Relate to other concepts and contexts

✓ **Provide background** — Design decisions, history, constraints, tradeoffs

✓ **Talk about the subject** — Titles should work with "About…" prefix

✓ **Admit perspective** — Acknowledge limitations and alternatives

✓ **Weigh alternatives** — Show why one approach is chosen over others

✓ **Bound the discussion** — Don't absorb instructions or reference

✓ **Answer "why" questions** — Not "how" or "what"

### Language Patterns

- "The reason for X is because historically, Y…"
- "W is better than Z, because…"
- "X in system Y is analogous to W in system Z. However…"
- "Some users prefer W (because Z). This can work well, but…"
- "The tradeoff is…"
- "An important design decision was…"
- "Historically, X…"

### Structure Template

```
# About [Subject]

[One sentence explaining what this is about]

## Background
[Historical context or why this matters]

## The core concept
[What is this, fundamentally]

## [Design aspect 1]

[Discussion of why this was chosen, tradeoffs, alternatives]

## [Design aspect 2]

[Discussion of why this was chosen, tradeoffs, alternatives]

## Comparison to [similar concept]
[How this relates to similar ideas]

## Further reading
- [Tutorial for learning]
- [How-to guide for using]
- [Reference for details]
```

### What to Avoid

- Don't write instructions — link to How-to Guides
- Don't describe machinery — link to Reference
- Don't teach from scratch — link to Tutorials
- Don't be neutral/objective — acknowledge perspective
- Don't try to be complete — bound the discussion

---

## Anti-Patterns to Avoid

### Problem: Mixed Categories

Content that tries to serve multiple user needs at once confuses readers.

**Example:** A tutorial that explains why each step works (mixing Tutorial + Explanation)

**Solution:** Keep tutorial concrete and focused. Link to Explanation for deeper understanding.

---

### Problem: Tutorials That Teach Too Little

Tutorials that treat readers as complete beginners and provide extensive explanation.

**Example:** "In step 1, we will click the button. The button is a UI element that when clicked performs an action. Buttons are important in software…"

**Solution:** Focus on action. Link to Explanation for background.

---

### Problem: How-to Guides That Teach

How-to guides that assume no prior knowledge and over-explain basics.

**Example:** "To configure X, you need to understand Y first. Y is a fundamental concept in…"

**Solution:** Link to Tutorial for fundamentals. Assume reader knows basics.

---

### Problem: Reference That Instructs

Reference that includes steps and guidance instead of just describing machinery.

**Example:** "To use the API endpoint X, first set up authentication. Here's how…"

**Solution:** Keep Reference purely descriptive. Link to How-to Guide for instructions.

---

### Problem: Explanation That Instructs

Explanation that embeds how-to steps instead of linking to them.

**Example:** "The reason we use caching is to improve performance. To implement caching, follow these steps…"

**Solution:** Explain the "why". Link to How-to Guide for implementation.

---

## Quality Checklist

For each documentation piece, verify:

- [ ] **Single category** — Serves exactly one user need
- [ ] **No category pollution** — Other categories are linked, not embedded
- [ ] **Correct orientation** — Matches the right cell in the matrix
- [ ] **Appropriate language** — Uses category-specific patterns and tone
- [ ] **Proper structure** — Follows category conventions
- [ ] **Complete within scope** — Serves its purpose fully
- [ ] **Clear naming** — Title reflects content and category
- [ ] **Minimal links** — Relates to all four categories without being cluttered
- [ ] **Tested execution** — For tutorials/how-to guides, steps actually work
- [ ] **Accuracy verified** — For reference/explanation, facts are correct

---

## Matrix Quick Reference

|              | Practical                           | Theoretical                        |
| ------------ | ----------------------------------- | ---------------------------------- |
| **Learning** | **Tutorials** — "We will…"          | **Explanation** — "Why is…"        |
| **Working**  | **How-to Guides** — "To achieve X…" | **Reference** — "X is defined as…" |

Choose the right quadrant, follow its principles, and everything else falls into place.
