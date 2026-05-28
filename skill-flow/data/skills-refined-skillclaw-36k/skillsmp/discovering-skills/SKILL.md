---
name: discovering-skills
description: Use when you sense a pattern but can't articulate it, or when adapting a process from another domain. Guides interactive prototyping to discover what a skill should contain.
command: discover-skill
---

# Discovering Skills Through Prototyping

## Overview

Skills emerge from patterns in real work. When you can't yet articulate the pattern, don't guess — prototype it. This skill guides interactive sessions where you work through a real example to discover what a skill should contain. The output is working notes that feed into `writing-skills`.

## When to Use

- You sense a pattern but can't articulate it clearly
- You're adapting a process from another domain to Claude workflows
- A workflow has unclear decision points you need to surface
- You want to create a skill but aren't sure what it should cover

**When NOT to use**: If you've already explained a pattern 3+ times and it's clear in your head, skip discovery and use `writing-skills` directly.

## Entry Point

When the user invokes `/discover-skill`, ask them to describe:

1. **The action**: What workflow or process do they want to work through?
2. **The suspected skill**: What do they think the skill might help with?

Example invocation:
```
/discover-skill "help me work through reviewing milestones to discover a skill for turning vague milestones into well-formed ones"
```

If the user doesn't provide both parts, use `AskUserQuestion` to clarify.

## Core Pattern: The Discovery Session

### Phase 1: Set Up the Real Example

Don't work with hypotheticals. Ask the user for:

1. **A concrete artifact** — A real document, codebase, or problem to work through
2. **The desired outcome** — What should be different when we're done?

If no artifact exists, offer to create a realistic example together, but prefer real work over synthetic examples.

### Phase 2: Work Through the Example

Work through the real problem step by step. As you go:

1. **Narrate your reasoning.** Explain why you're making each choice.
2. **Pause at decision points.** When multiple approaches seem valid, surface them:
   ```
   I see two ways to handle this:
   - Option A: [approach] — better when [condition]
   - Option B: [approach] — better when [condition]
   Which fits your context?
   ```
3. **Flag surprises.** When something isn't obvious, note it explicitly:
   ```
   This wasn't obvious: [observation]. This might be an insight worth capturing.
   ```

### Phase 3: Capture Insights

Throughout the session, maintain a running "Skill Development Notes" section. Use this format:

```markdown
## Skill Development Notes

### Insight 1: [Pattern Name]

[What you observed and why it matters]

**Skill implication**: [How this should appear in the final skill]
```

**What makes a good insight**:
- It wasn't obvious before working through the example
- It would apply to other instances of this workflow
- Missing it would lead to worse outcomes

**Capture questions and resolutions**:
```markdown
### Question: [What wasn't clear]

**Options considered**: [A, B, C]

**Resolution**: [Which option and why]

**Skill implication**: [Should the skill prescribe this, or present options?]
```

### Phase 4: Note Cross-Skill Updates

Discovery sessions often reveal gaps in upstream skills. Capture these explicitly:

```markdown
## Cross-Skill Notes

- **`reviewing-design-docs`**: Should also cover [gap discovered here]
- **`writing-effective-acceptance-criteria`**: Add anti-pattern for [issue observed]
```

Don't ignore these. Either file them as follow-up work or address them in the same session.

### Phase 5: Synthesize the Process Summary

After working through the example (or partway through, if the pattern is clear), write a Process Summary:

```markdown
## Process Summary: [Skill Name]

### Inputs Required

Before starting, you need:
- [Input 1]
- [Input 2]

### Step-by-Step Process

#### Step 1: [Name]

[What to do]

**Questions to ask**:
1. [Question that surfaces important information]
2. [Question that reveals decision points]

#### Step 2: [Name]

[Continue for each step...]

### Output Format

[What the deliverable looks like — template or example]

### Validation Checks

Before finalizing:
- [ ] [Check 1]
- [ ] [Check 2]
```

The Process Summary is the skeleton of the skill's Core Pattern.

### Phase 6: Produce the Working Notes Document

Compile everything into a `*-working-notes.md` file:

```markdown
# [Topic]: Working Notes for Skill Discovery

Working notes from a discovery session on [date/context].

---

## Skill Development Notes

[All numbered insights]

---

## Questions and Resolutions

[All questions with their resolutions]

---

## Cross-Skill Notes

[Updates needed for other skills]

---

## Process Summary: [Skill Name]

[The synthesized process]

---

## Next Steps

- [ ] Create skill using `writing-skills`
- [ ] Address cross-skill updates
- [ ] Pressure test with RED-GREEN-REFACTOR
```

## Validation: Is Discovery Complete?

Before ending the session, verify:

- [ ] At least one real example worked through completely
- [ ] 3+ insights captured (fewer suggests the pattern was already clear)
- [ ] Decision points surfaced and resolved (or flagged as user-choice)
- [ ] Process Summary written with steps and validation checks
- [ ] Cross-skill notes captured (even if "none identified")

## When to Stop Discovery and Start Writing

Discovery is complete when:
- The Process Summary feels repeatable
- You could explain the pattern to someone else
- New examples would refine, not reveal, the pattern

If after working through 2-3 examples you're still discovering fundamental insights, the scope may be too broad — consider splitting into multiple skills.

## Anti-Patterns

| Anti-pattern | Problem | Fix |
|--------------|---------|-----|
| Working with hypotheticals | Miss real-world edge cases | Use a concrete artifact |
| Capturing every observation | Bloats notes with noise | Only capture non-obvious patterns |
| Skipping the Process Summary | No clear structure for skill | Always synthesize before ending |
| Ignoring cross-skill insights | Upstream skills stay incomplete | Capture and address them |
| Endless discovery | Perfectionism delays value | Stop after 2-3 examples if pattern is clear |

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| Starting with skill structure | Premature commitment to format | Let the example reveal the structure |
| Not narrating reasoning | Insights stay tacit | Explain choices as you make them |
| Skipping decision points | Skill won't handle variations | Surface and resolve (or flag) them |
| Treating working notes as the skill | Too verbose, example-specific | Extract patterns via `writing-skills` |

## Relationship to Other Skills

```
┌─────────────────────┐
│  discovering-skills │  ← You are here
│  /discover-skill    │
└─────────┬───────────┘
          │ produces working notes
          ▼
┌─────────────────────┐
│   writing-skills    │
│   (structure skill) │
└─────────┬───────────┘
          │ produces skill draft
          ▼
┌─────────────────────┐
│  RED-GREEN-REFACTOR │
│  (pressure testing) │
└─────────────────────┘
```

## Summary

1. **Use real examples, not hypotheticals.** Concrete artifacts reveal edge cases.
2. **Narrate your reasoning.** Tacit knowledge becomes explicit insights.
3. **Capture insights as you go.** Don't wait until the end — you'll forget.
4. **Write the Process Summary.** This becomes the skill's Core Pattern skeleton.
5. **Working notes are raw material, not the skill.** Feed them into `writing-skills` to produce the actual skill.
