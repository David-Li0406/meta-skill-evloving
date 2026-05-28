# Minto Pyramid Principle

Barbara Minto's framework for clear, persuasive business communication.

## Core Principle

**Start with the answer.** Executives and decision-makers want the conclusion first, then supporting logic. The pyramid inverts how most people naturally think (bottom-up) into how decisions are made (top-down).

## Pyramid Structure

```
Level 1: GOVERNING THOUGHT
         Your main point / recommendation / insight
         (What should we do? What's the answer?)
                        │
         ┌──────────────┼──────────────┐
         │              │              │
Level 2: KEY LINE POINTS (3-5 max)
         Supporting arguments that directly prove Level 1
         │              │              │
Level 3: SUPPORTING DATA
         Evidence, examples, analysis for each key point
```

## SCQA Framework

Structure narratives with Situation-Complication-Question-Answer:

| Element | Purpose | Product Example |
|---------|---------|-----------------|
| **Situation** | Stable context | "We launched feature X in Q1. Adoption reached 40% of active users." |
| **Complication** | What changed/broke | "However, retention after 30 days dropped 25% vs. baseline." |
| **Question** | Implicit question raised | (Why? What do we do?) |
| **Answer** | Your recommendation | "We should simplify onboarding—users who complete it retain 3x better." |

**Variations**:
- **Standard SCQA**: Problem-focused, leads to recommendation
- **Direct Answer**: Skip to A when audience wants speed
- **SCA**: When complication is obvious

## Grouping Logic

Ideas at same level must share logical relationship:

### Deductive Grouping
Each point builds on previous → "Therefore"
```
1. Users are churning after trial
2. Exit surveys cite "too complex"
3. Therefore: Simplify onboarding
```

### Inductive Grouping
Points share common attribute → "For example"
```
Main: Three factors drive churn
  - Price (25% cite cost)
  - Complexity (40% cite confusion)
  - Missing features (20% cite gaps)
```

## MECE Principle

Groups must be **Mutually Exclusive, Collectively Exhaustive**:
- No overlap between items
- All relevant items included
- Forces clean categorization

**Bad** (overlapping):
- Technical issues
- UX problems
- Frontend bugs ← overlaps with both

**Good** (MECE):
- Acquisition issues
- Activation issues
- Retention issues

## The "So What?" Test

Every point must answer "so what?" from the level above:

```
"Churn increased 15% last month"
    └── So what?
        "This threatens our Q4 revenue target"
            └── So what?
                "We need to prioritize retention immediately"
                    └── (This is the governing thought)
```

## Synthesis vs. Summary

| Summary | Synthesis |
|---------|-----------|
| Lists what you found | Extracts meaning |
| "We interviewed 12 users" | "Users want X, not Y" |
| Repeats input | Advances argument |
| Bottom of pyramid | Top of pyramid |

**Always synthesize.** The answer is not "here's what we learned"—it's "here's what this means and what we should do."

## Pyramid Patterns for Product Documents

### PRD Opening
```
ANSWER: Build [X] to solve [job] → expected impact [Y]

KEY POINTS:
1. User problem evidence (struggling moment + data)
2. Solution approach (how it addresses job)
3. Why now (complication/opportunity)
```

### Executive Update
```
ANSWER: [Status] + [Key Decision Needed]

KEY POINTS:
1. Progress since last update
2. Current blockers
3. Help needed / decisions required
```

### Feature Proposal
```
ANSWER: We should build [X] because [job insight]

KEY POINTS:
1. Job to be done (circumstance + progress)
2. Why current solutions fail
3. Proposed approach
4. Success metrics
```

## Common Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Burying the lead | "First, some background..." | Start with recommendation |
| Too many key points | 7+ supporting arguments | Max 5, ideally 3 |
| Data without synthesis | "Here are the survey results" | "Survey shows users want X" |
| Horizontal logic gaps | Points don't connect | Apply "so what?" test |
| Overlapping categories | Non-MECE grouping | Restructure until exclusive |

## Presentation Tip

**Pyramid on a slide**:
- Headline = Answer (what you want them to remember)
- Body = Key points only
- Appendix = Supporting data

Audience should understand your point from headline alone.
