# Workflow: Draft

Write a first draft from an outline.

## Prerequisites

- `/workspace/outline.md` exists with structure
- `/workspace/evidence.json` has sufficient evidence
- The Turn is identified (or flagged as needed)

## Mindset

First drafts are meant to be revised. The goal is to:
- Get ideas on paper
- Follow the outline structure
- Incorporate key evidence
- Maintain momentum

Do NOT:
- Agonize over word choice
- Polish sentences prematurely
- Let perfect be enemy of done

## Steps

### 1. Review Materials

Read through:
- `brief.md` - Remind yourself of audience, goals
- `outline.md` - The structure you're following
- `evidence.json` - Key evidence to incorporate

Note:
- Which evidence maps to which section
- Where The Turn appears
- Any gaps that need flagging

### 2. Set Up the Draft

Create `/workspace/drafts/v1.md`:

```markdown
---
version: 1
date: [today]
status: first_draft
---

# [Title]

<!-- The Turn: [state it here for reference] -->

## [Section 1]

## [Section 2]

...
```

### 3. Write the Opening

The opening must:
- Hook the reader
- Establish The Turn (or set it up)
- Promise what they'll gain

**Structure option: Before-After-Bridge**
```markdown
[BEFORE: The current problematic state - make it vivid]

[AFTER: The ideal state the reader wants]

[BRIDGE: This piece will show you how to get there]
```

**Structure option: The Turn upfront**
```markdown
[CONVENTIONAL WISDOM: What most people assume]

[THE TURN: But here's what they're missing]

[PROMISE: By the end, you'll understand...]
```

Write fast. You'll revise later.

### 4. Draft Body Sections

For each section in the outline:

**Step A: State the section's purpose**
Write one sentence (to yourself) about what this section accomplishes.

**Step B: Write the topic paragraph**
- What's the main claim of this section?
- Write 3-4 sentences introducing it

**Step C: Incorporate evidence**
- Pull relevant evidence from evidence.json
- Weave quotes/data into the argument
- Cite sources (informal notes for now)

**Step D: Develop the argument**
- Add reasoning that connects evidence to claim
- Address obvious objections if relevant
- Add examples that make abstractions concrete

**Step E: Bridge to next section**
- Last sentence should connect to what's coming

**Mark uncertainties as you go:**
- `[VERIFY]` - Need to fact-check
- `[NEEDS EVIDENCE]` - Claim lacks support
- `[LOW CONFIDENCE]` - Speculative
- `[EXPAND]` - Needs more development
- `[CUT?]` - Maybe unnecessary

### 5. Draft the Conclusion

The conclusion should:
- Return to The Turn
- Synthesize (not summarize) the argument
- Look forward (implications, next steps)
- Land with strength

**Avoid**:
- "In conclusion..."
- Repeating the introduction
- Introducing new evidence
- Trailing off weakly

### 6. Draft the P.S.

If using a P.S.:
- Save a high-value insight that didn't fit
- Or a compelling call to action
- Or the "real" point stated plainly

### 7. Add Confidence Markers

Go back through and add confidence markers to key claims:

```markdown
Evidence strongly suggests that friction improves decision quality in high-stakes contexts [HIGH CONFIDENCE].

This may also apply to consumer contexts, though evidence is limited [MODERATE CONFIDENCE - verify].
```

### 8. Self-Assessment

Before finishing, note:

```markdown
<!-- 
DRAFT SELF-ASSESSMENT

Strengths:
- [what works]

Weaknesses I already see:
- [what needs work]

Questions for Critic:
- [specific feedback needed]

Sections that feel weak:
- [list]
-->
```

### 9. Save and Update State

Save to `/workspace/drafts/v1.md`

Copy to `/workspace/drafts/current.md`

Update `/workspace/state.json`:
```json
{
  "current_state": "drafting",
  "draft_version": 1,
  "draft_complete": true,
  "ready_for_critique": true
}
```

## Quality Checklist

Before marking draft complete:

- [ ] All outline sections drafted
- [ ] Key evidence incorporated
- [ ] The Turn is present and clear
- [ ] Opening hooks the reader
- [ ] Conclusion lands (doesn't trail off)
- [ ] Uncertainty markers added
- [ ] Self-assessment completed

## Word Count Guidance

| Document Type | Target Range |
|---------------|--------------|
| Blog post | 1,000-2,000 |
| Analysis | 2,500-4,000 |
| Deep dive | 4,000-6,000 |
| Report | 5,000-10,000 |

Don't pad to hit count. Don't cut substance to stay under.

## Next Steps

→ Draft goes to CRITIC for full critique
→ Then WRITER returns for revision workflow
