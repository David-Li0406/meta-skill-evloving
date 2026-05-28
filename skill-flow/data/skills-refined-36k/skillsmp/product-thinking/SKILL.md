---
name: product-thinking
description: Strategic product thinking framework combining the Minto Pyramid Principle (structured top-down communication) with Clayton Christensen's Jobs-to-be-Done theory. Use when evaluating product ideas, generating new concepts, structuring PRDs/briefs, conducting discovery interviews, or refining product strategy. Supports two modes - interactive Q&A discovery and structured document output.
---

# Product Thinking Framework

Combines two complementary frameworks:
- **Jobs-to-be-Done (JTBD)**: Understand *what progress* customers seek
- **Minto Pyramid**: Communicate product thinking *clearly and persuasively*

## When to Use

| Trigger | Mode |
|---------|------|
| "Help me think through this product idea" | Interactive Q&A |
| "Evaluate this feature concept" | Interactive Q&A |
| "Write a PRD/brief/one-pager" | Document Output |
| "Structure my product thinking" | Either (ask user) |
| "Interview me about my product" | Interactive Q&A |

## Core Workflow

### Step 1: Establish Mode

Ask: **"Would you like me to guide you through discovery questions, or produce a structured document?"**

- **Interactive Q&A**: Walk through JTBD discovery → synthesize → structure via Minto
- **Document Output**: Gather inputs → produce pyramid-structured artifact

### Step 2: JTBD Discovery

The goal is to uncover the **job** the customer is hiring the product to do.

**The Job Statement Formula:**
```
When [circumstance], I want to [progress/outcome], so I can [higher purpose].
```

**Core Questions** (ask 2-3 at a time, not all at once):

1. **Struggling Moment**: "What's the specific moment when someone realizes they need this?"
2. **Current Workarounds**: "What are people cobbling together today to make progress?"
3. **Functional Job**: "What task are they literally trying to accomplish?"
4. **Emotional Job**: "How do they want to feel during/after?"
5. **Social Job**: "How do they want to be perceived by others?"
6. **Hiring Criteria**: "What would make them 'fire' their current solution and 'hire' yours?"
7. **Anxieties**: "What fears would prevent them from switching?"
8. **Circumstances**: "When/where does this job arise? What's the context?"

See `references/jtbd-framework.md` for deeper guidance on JTBD theory.

### Step 3: Synthesize the Job

After discovery, articulate:

```
JOB STATEMENT
━━━━━━━━━━━━━
When: [specific circumstance/trigger]
I want to: [desired progress]
So I can: [ultimate outcome/feeling]

FORCES OF PROGRESS
━━━━━━━━━━━━━━━━━━
Push (pain of current): [what's broken]
Pull (appeal of new): [what's attractive]
Anxiety (fear of new): [what holds them back]
Habit (comfort of current): [what keeps them stuck]
```

### Step 4: Structure via Minto Pyramid

Organize all thinking top-down:

```
           ┌─────────────────┐
           │   ANSWER FIRST  │  ← Lead with the conclusion
           │   (So What?)    │
           └────────┬────────┘
                    │
     ┌──────────────┼──────────────┐
     │              │              │
┌────▼────┐   ┌────▼────┐   ┌────▼────┐
│ Key     │   │ Key     │   │ Key     │  ← 3-5 supporting arguments
│ Point 1 │   │ Point 2 │   │ Point 3 │
└────┬────┘   └────┬────┘   └────┬────┘
     │             │             │
  Evidence      Evidence      Evidence  ← Data, examples, research
```

**SCQA Framework** for framing the narrative:
- **Situation**: Stable context everyone agrees on
- **Complication**: What changed or went wrong
- **Question**: The question this raises (implicit)
- **Answer**: Your recommendation/insight

See `references/minto-pyramid.md` for communication patterns.

## Document Output Templates

### Product Brief (1-pager)

```markdown
# [Product/Feature Name]

## Recommendation
[One sentence: what to build and why it matters]

## The Job to Be Done
When [circumstance], [user] wants to [progress], so they can [outcome].

## Why Now
- [Complication 1]: [evidence]
- [Complication 2]: [evidence]

## Solution Approach
1. [Key capability] → addresses [job dimension]
2. [Key capability] → addresses [job dimension]
3. [Key capability] → addresses [job dimension]

## Success Metrics
- [Leading indicator]: [target]
- [Lagging indicator]: [target]

## Key Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| [Anxiety/obstacle] | [How addressed] |
```

### Idea Evaluation Scorecard

```markdown
# Evaluation: [Idea Name]

## JTBD Fit (1-5): __
- [ ] Clear struggling moment identified
- [ ] Job is recurring, not one-time
- [ ] Emotional/social dimensions understood
- [ ] Current alternatives are inadequate

## Market Forces (1-5): __
- [ ] Push from current pain is strong
- [ ] Pull toward solution is compelling
- [ ] Anxieties can be addressed
- [ ] Habits can be overcome

## Strategic Fit (1-5): __
- [ ] Aligns with company capabilities
- [ ] Defensible differentiation exists
- [ ] Viable business model apparent

## Verdict
[PURSUE / ITERATE / PASS]

## Reasoning (Pyramid Structure)
[Answer]: [One sentence verdict with "because..."]
- [Supporting point 1]
- [Supporting point 2]
- [Supporting point 3]
```

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Better Approach |
|--------------|--------------|-----------------|
| Feature-first thinking | "Build X" without job context | Start with struggling moment |
| Demographic segmentation | "Millennials want..." | Segment by job, not persona |
| Solution validation | "Do you like this?" | "Tell me about last time you..." |
| Bottom-up docs | Burying the lead | Answer first, then support |
| Correlation as causation | "Users who do X also Y" | Understand the *why* behind behavior |

## Interactive Session Flow

When in Q&A mode, follow this arc:

1. **Open**: "Tell me about the problem you're trying to solve"
2. **Struggling Moment**: "Walk me through a specific moment when this became painful"
3. **Current State**: "What are people doing today to cope?"
4. **Dimensions**: Probe functional, emotional, social jobs
5. **Forces**: Map push, pull, anxiety, habit
6. **Synthesize**: Reflect back the job statement for validation
7. **Structure**: Organize insights into pyramid for next steps

Limit to 2-3 questions per turn. Reflect understanding before probing deeper.

## References

- `references/jtbd-framework.md` - Deep dive on Jobs-to-be-Done theory
- `references/minto-pyramid.md` - Detailed Minto communication patterns
- `references/interview-guide.md` - Full discovery interview script
