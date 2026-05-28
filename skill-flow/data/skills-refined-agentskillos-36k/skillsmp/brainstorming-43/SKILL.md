---
name: brainstorming
description: Design and planning before coding. Explores problem space, generates approaches, evaluates tradeoffs, and recommends a path forward.
---

# Brainstorming

## Core Purpose

Explore the problem space thoroughly BEFORE writing any code. Generate multiple approaches, evaluate tradeoffs, and recommend a clear path forward with rationale. This prevents wasted effort on wrong approaches.

## Operating Philosophy

### What This Skill IS

- **Problem explorer** who fully understands the requirements
- **Option generator** who produces multiple viable approaches
- **Tradeoff analyst** who honestly evaluates each option
- **Decision recommender** who provides clear guidance
- **Risk identifier** who surfaces potential issues early

### What This Skill IS NOT

- A rubber stamp for the first idea
- A perfectionist who demands the "best" solution
- A delayer who explores indefinitely
- A decision-avoider who presents options without recommendation

## Activation Protocol

When activated:

1. **Clarify the goal** - What are we trying to achieve?
2. **Identify constraints** - Time, tech, team, existing patterns
3. **Explore the problem space** - Research relevant code, patterns, dependencies
4. **Generate options** - At least 2-3 viable approaches
5. **Evaluate tradeoffs** - Honest pros/cons for each
6. **Recommend** - Clear recommendation with rationale

---

## Phase 1: Problem Understanding

### Gather Context

**Questions to answer:**

- What exactly needs to be built or changed?
- Who/what will use this? (users, other code, external systems)
- What are the success criteria?
- What constraints exist? (performance, compatibility, timeline)
- What existing patterns should be followed?

**Context to gather:**

- Read relevant project CLAUDE.md
- Check existing similar implementations
- Understand data flow and dependencies
- Identify integration points

### Define Scope Boundaries

Be explicit about:

- What IS in scope
- What is NOT in scope
- What assumptions are being made

---

## Phase 2: Option Generation

### Generate Multiple Approaches

Always produce at least 2-3 options. Force yourself to think beyond the obvious first answer.

**Option generation techniques:**

1. **The obvious approach** - What would a typical implementation look like?
2. **The simple approach** - What's the minimum viable solution?
3. **The robust approach** - What handles all edge cases elegantly?
4. **The existing pattern** - What does this codebase already do for similar problems?
5. **The opposite approach** - What if we inverted our assumptions?

### For Each Option, Document:

| Aspect         | Description                               |
| -------------- | ----------------------------------------- |
| Summary        | One-line description                      |
| Implementation | Key steps/changes required                |
| Pros           | Advantages of this approach               |
| Cons           | Disadvantages and risks                   |
| Effort         | Relative complexity (Low/Med/High)        |
| Fits Pattern   | Does it match existing codebase patterns? |

---

## Phase 3: Tradeoff Analysis

### Evaluation Criteria

Rate each option against relevant criteria:

| Criterion              | Weight | Option A | Option B | Option C |
| ---------------------- | ------ | -------- | -------- | -------- |
| Simplicity             |        |          |          |          |
| Maintainability        |        |          |          |          |
| Performance            |        |          |          |          |
| Testability            |        |          |          |          |
| Fits existing patterns |        |          |          |          |
| Future flexibility     |        |          |          |          |
| Risk level             |        |          |          |          |

### Risk Assessment

For each option, identify:

- **Technical risks** - What could go wrong during implementation?
- **Integration risks** - What could break existing functionality?
- **Maintenance risks** - What creates future pain?

---

## Phase 4: Recommendation

### Make a Clear Recommendation

Don't just present options - recommend one with clear rationale.

```markdown
## Recommendation: Option [X]

**Why this option:**

- [Primary reason]
- [Secondary reason]

**Key tradeoffs accepted:**

- [What we're giving up and why it's acceptable]

**Risks to monitor:**

- [What could still go wrong]

**Implementation approach:**

1. [First step]
2. [Second step]
3. [etc.]
```

### When to Escalate

Escalate to human decision if:

- Options have dramatically different long-term implications
- Technical constraints conflict with stated requirements
- No clear winner emerges from analysis
- Decision requires business/product context you don't have

---

## Output Format

```markdown
# Brainstorming: [Feature/Change Name]

## Problem Statement

[Clear description of what we're trying to achieve]

**Success criteria:**

- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Constraints:**

- [Constraint 1]
- [Constraint 2]

**Scope:**

- IN: [What's included]
- OUT: [What's explicitly excluded]

---

## Context Gathered

- [Relevant existing patterns found]
- [Dependencies identified]
- [Integration points]

---

## Options

### Option A: [Name]

**Summary:** [One line]

**Implementation:**

1. [Step]
2. [Step]

**Pros:**

- [Pro]

**Cons:**

- [Con]

**Effort:** Low / Medium / High

---

### Option B: [Name]

[Same structure]

---

### Option C: [Name]

[Same structure]

---

## Comparison

| Criterion       | Option A | Option B | Option C |
| --------------- | -------- | -------- | -------- |
| Simplicity      |          |          |          |
| Maintainability |          |          |          |
| Fits patterns   |          |          |          |
| Risk            |          |          |          |

---

## Recommendation

**Recommended:** Option [X]

**Rationale:**
[Why this is the best path forward]

**Tradeoffs accepted:**
[What we're consciously giving up]

**Next steps:**

1. [First implementation step]
2. [Second step]
3. [etc.]

---

## Open Questions

- [Any remaining uncertainties for human input]
```

---

## Integration with Workflow

This skill should be invoked:

1. BEFORE starting any non-trivial implementation
2. When requirements are ambiguous
3. When multiple approaches seem viable
4. When changing existing architecture
5. When the "obvious" solution feels too simple

The output of this skill feeds directly into implementation planning.

---

## Calibration Guidelines

### Match Depth to Complexity

| Task Complexity          | Brainstorming Depth                    |
| ------------------------ | -------------------------------------- |
| Simple change            | 5 min - Quick sanity check             |
| Standard feature         | 15-20 min - Full analysis              |
| Architectural change     | 30+ min - Deep exploration             |
| Multi-system integration | Extensive - May need multiple sessions |

### Avoid Common Pitfalls

- Don't skip brainstorming for "obvious" solutions (they often aren't)
- Don't generate options just to generate options (each must be viable)
- Don't hide behind analysis paralysis (make a recommendation)
- Don't ignore existing codebase patterns (consistency matters)
- Don't over-engineer the analysis (match effort to stakes)

### Time-Boxing

If analysis is taking too long:

1. Document what's known so far
2. Identify the key uncertainty blocking progress
3. Make a provisional recommendation
4. Note what would change the recommendation
5. Move forward with implementation

---

## Special Protocols

### When Existing Code Constrains Options

If the codebase strongly suggests a particular approach:

- Acknowledge it as the "path of least resistance"
- Still generate at least one alternative
- Evaluate whether the constraint is worth challenging
- Default to consistency unless there's strong reason to deviate

### When Time Pressure Exists

- Focus on viable vs non-viable rather than optimal
- Reduce to 2 options maximum
- Make faster recommendation with noted assumptions
- Flag what analysis was skipped for later review

### When Requirements Are Unclear

- Document assumptions explicitly
- Present options that cover different interpretations
- Recommend asking for clarification on specific points
- Don't proceed with implementation until key ambiguities resolved
