---
name: decision-making
description: "Use when facing a significant decision with multiple viable paths - choosing between approaches, architectures, tools, or solutions. Applies the 1-3-1 method for structured decision-making."
---

# Decision-Making with the 1-3-1 Method

## Overview

A structured framework for making significant decisions. Prevents analysis paralysis while ensuring thorough consideration of alternatives.

**Core principle:** One problem, three options, one recommendation.

## When to Use

- Choosing between technical approaches or architectures
- Selecting tools, frameworks, or libraries
- Deciding on implementation strategies
- Resolving design trade-offs
- Any decision where multiple viable paths exist

## The 1-3-1 Method

### Step 1: Identify 1 Core Problem

Distill the decision into a single, clear problem statement.

**Good:** "Which authentication strategy balances security with implementation speed?"
**Bad:** "How should we build the login system?"

### Step 2: Propose 3 Options

Generate three distinctly different approaches. Each must:
- Be viable and address the core problem
- Represent a genuinely different path (not variations of the same idea)
- Include trade-offs (pros/cons)

### Step 3: Give 1 Recommendation

Evaluate options against relevant criteria and recommend one.

**Evaluation criteria** (select relevant ones):
- Implementation complexity
- Time to delivery
- Maintainability
- Scalability
- Risk level
- Cost
- Team expertise

## Output Format

```
**Core Problem:** [Clear, specific problem statement]

**Option 1:** [Name]
[Description]
- Pros: [advantages]
- Cons: [disadvantages]

**Option 2:** [Name]
[Description]
- Pros: [advantages]
- Cons: [disadvantages]

**Option 3:** [Name]
[Description]
- Pros: [advantages]
- Cons: [disadvantages]

**Recommendation:** [Chosen option]
**Reasoning:** [Brief explanation of why this is the best approach]
```

## Prerequisites (for complex decisions)

For significant decisions, gather these 4 inputs first:

1. **Context** – Why is this decision being made? What triggered it?
2. **Constraints** – What are the non-negotiables? (time, budget, tech stack)
3. **Stakeholders** – Who is affected? What do they care about?
4. **Success criteria** – How will we know we made the right choice?

## Examples

### Quick Decision

**Core Problem:** Which HTTP client library for our Node.js API?

**Option 1:** Axios - Popular, promise-based, good interceptors
**Option 2:** node-fetch - Minimal, native fetch API
**Option 3:** Got - Feature-rich, retry built-in, TypeScript native

**Recommendation:** Got
**Reasoning:** TypeScript-first, built-in retry logic reduces boilerplate, active maintenance.

### Complex Decision

When the decision has significant impact, use the full format with prerequisites gathered first.

## Red Flags

- **Only 1-2 options considered** – You're not exploring the solution space
- **Options are too similar** – Push for genuinely different approaches
- **No clear recommendation** – Take a stance; "it depends" isn't helpful
- **Recommendation doesn't match reasoning** – Ensure logic supports conclusion
- **Skipping the problem statement** – Unclear problem leads to unclear solutions

## Integration

This skill is used by these workflows:
- `/create-feature` – Feature development decisions
- `/create-epic` – Epic decomposition strategies
- `/create-bugfix` – Root cause and fix approach selection
- `/suggest-solutions` – General problem-solving

Invoke with `@decision-making` for standalone use.
