---
name: brainstorming
description: Use before creative PM work to explore problem space, generate options, and validate thinking before committing to solutions
---

# Brainstorming

## Why This Matters

PMs often jump to solutions before fully exploring the problem space. This skill enforces divergent thinking before convergent thinking - generating multiple options before committing to one.

## When to Use

- Before defining a new feature or capability
- Before writing charters or PRDs
- When stuck on a problem
- To explore problem space before committing to solutions
- Any time you're about to make a significant product decision

## Algorithm Phase

This is a **THINK phase skill**:
- **Requires:** None (can brainstorm anytime, but better with context)
- **Recommended:** Run synthesizing-voc first for customer grounding

## Core Pattern

### Step 1: Frame the Problem

Before generating options, clearly define what you're solving:

| Element | Question to Answer |
|---------|-------------------|
| Problem | What are we trying to solve? |
| Who | Who is affected? (users, stakeholders) |
| Why Now | What's driving the urgency? |
| Context | What do we already know? (VOC, KTLO, truth base) |

**Output:** Write a 2-3 sentence problem statement.

### Step 2: Diverge (Generate 5+ Options)

Generate at least 5 potential approaches. Rules:
- No judgment at this stage
- Include at least one unconventional option
- Include "do nothing" as an option
- Quantity over quality initially

**Format:**
```markdown
## Options

1. **[Option Name]**
   - Description: [What this approach does]
   - Key assumption: [What must be true for this to work]

2. **[Option Name]**
   ...
```

### Step 3: Evaluate

Score each option against criteria. Common criteria:

| Criterion | Description |
|-----------|-------------|
| Customer Impact | How much does this solve customer pain? |
| Feasibility | Can we build this with current resources? |
| Strategic Fit | Does this align with COMPASS goals? |
| Risk | What could go wrong? |
| Reversibility | One-way door vs two-way door? |

**Format:**
```markdown
## Evaluation Matrix

| Option | Customer Impact | Feasibility | Strategic Fit | Risk | Score |
|--------|----------------|-------------|---------------|------|-------|
| Option 1 | High [E] | Medium [A] | High [E] | Low | 8/10 |
| Option 2 | Medium [A] | High [E] | Medium [A] | Medium | 6/10 |
```

Tag each evaluation: `[E]` = Evidence, `[A]` = Assumption

### Step 4: Converge

Select top 2-3 options for deeper exploration:
- Document why these rose to the top
- Identify key questions to resolve before deciding
- Note what evidence would change the ranking

### Step 5: Output

Write to `outputs/insights/brainstorm-YYYY-MM-DD-[topic].md`

**Template:**
```markdown
---
generated: YYYY-MM-DD HH:MM
skill: brainstorming
topic: [short topic name]
sources:
  - [any VOC, KTLO, or truth base files consulted]
---

# Brainstorm: [Topic]

## Problem Statement
[2-3 sentence problem framing]

## Context Consulted
- VOC: [key themes relevant]
- KTLO: [relevant tickets/themes]
- Truth Base: [relevant capabilities/constraints]

## Options Generated

### 1. [Option Name]
- Description:
- Key assumption:
- Pros:
- Cons:

[... repeat for 5+ options ...]

## Evaluation Matrix

| Option | Customer Impact | Feasibility | Strategic Fit | Risk | Score |
|--------|----------------|-------------|---------------|------|-------|

## Recommended for Deep Dive

1. **[Top Option]** - Why: [rationale]
2. **[Second Option]** - Why: [rationale]

## Key Questions to Resolve

- [ ] [Question 1]
- [ ] [Question 2]
- [ ] [Question 3]

## Claims Ledger

| Claim | Type | Source |
|-------|------|--------|
| [claim] | Evidence/Assumption | [source] |
```

## Verification Checklist

Before marking complete:
- [ ] Problem clearly framed (2-3 sentences)
- [ ] 5+ options generated (including unconventional)
- [ ] "Do nothing" considered
- [ ] Evaluations tagged as Evidence/Assumption
- [ ] Top 2-3 options selected with rationale
- [ ] Key questions identified
- [ ] Claims Ledger present with sources

## Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| Jumping to favorite option | Confirmation bias | Force 5+ options first |
| Evaluating while generating | Kills creativity | Separate diverge/converge |
| All options are variations | Not true divergence | Include one "crazy" option |
| No "do nothing" option | Ignores opportunity cost | Always include it |
| Unmarked assumptions | False confidence | Tag every evaluation |

## Output Location

- Brainstorm outputs: `outputs/insights/brainstorm-YYYY-MM-DD-[topic].md`
- History: `history/brainstorming/brainstorm-YYYY-MM-DD-[topic].md`

## Integration with Other Skills

Brainstorming often feeds into:
- `generating-quarterly-charters` - Brainstorm before defining bets
- `writing-prds-from-charters` - Brainstorm implementation approaches
- `competitive-analysis` - Brainstorm competitive responses
