# Workflow: Revise

Address critiques and improve the draft.

## Prerequisites

- Draft exists in `/workspace/drafts/current.md`
- Critiques exist in `/workspace/critiques.json`
- Critiques have been reviewed and prioritized

## Mindset

Revision is not polishing—it's re-seeing. You may need to:
- Restructure sections
- Cut significant material
- Add new content
- Rewrite entirely

Be willing to "kill your darlings."

## Steps

### 1. Triage Critiques

Review `/workspace/critiques.json` and sort by severity:

**BLOCKING** (must fix before proceeding):
- These are fatal flaws
- Nothing else matters until these are resolved
- May require new research or fundamental restructuring

**HIGH** (must fix before finalizing):
- Serious weaknesses
- Significantly impact argument quality
- Address all of these

**MEDIUM** (should fix):
- Notable concerns
- Address if possible
- Acknowledge if can't fully resolve

**LOW** (nice to fix):
- Minor issues
- Fix during polish pass
- Don't spend significant time

### 2. Address BLOCKING Issues First

For each BLOCKING critique:

1. **Understand the issue fully**
   - What exactly is the problem?
   - Why is it fatal?
   - What would resolution look like?

2. **Determine the fix**
   - Does this require new research? → Flag for RESEARCHER
   - Does this require restructuring? → Plan the restructure
   - Does this require rewriting? → Mark the section

3. **Execute the fix**
   - Make the change
   - Verify it actually resolves the issue

4. **Mark as resolved**
   ```json
   {
     "id": "cr_001",
     "resolved": true,
     "resolution_notes": "Restructured Section 2 to address logical gap. Added new evidence ev_015 to support claim."
   }
   ```

### 3. Address HIGH Issues

Same process, but these don't block other work.

Group related critiques:
- If multiple critiques target the same section, address together
- If critiques contradict each other, flag for judgment call

For each HIGH critique:
- Understand → Plan → Execute → Mark resolved

### 4. Address MEDIUM Issues

Be strategic:
- Quick fixes: just do them
- Larger changes: assess if worth the time
- If can't resolve: acknowledge in text or note limitation

### 5. Integration Pass

After addressing individual critiques, do an integration pass:

**Check for consistency**:
- Do changes contradict other parts of the draft?
- Does the flow still work?
- Are references updated?

**Check for completeness**:
- Did addressing one critique create new gaps?
- Are there orphaned paragraphs?
- Do transitions still work?

**Check against original goals**:
- Does the draft still accomplish what brief.md specified?
- Is The Turn still clear and well-supported?
- Does the argument still hold together?

### 6. Mark Unresolved Issues

For critiques you couldn't fully resolve:

Option A: Acknowledge in text
```markdown
While evidence suggests X, this finding is limited by [acknowledge limitation].
```

Option B: Note as limitation
```markdown
<!-- LIMITATION: Could not find evidence to fully support claim about Y. Current support is moderate confidence only. -->
```

Option C: Flag for future
```json
{
  "id": "cr_007",
  "resolved": false,
  "resolution_notes": "Could not find stronger evidence. Marked as moderate confidence in text. May need to revisit if stronger claims are made elsewhere."
}
```

### 7. Save New Version

Copy `current.md` to `v[N+1].md`

Update `current.md` with revised draft

Update state:
```json
{
  "current_state": "revising",
  "draft_version": 2,
  "critiques_addressed": {
    "blocking": 0,
    "high": 3,
    "medium": 4,
    "low": 0,
    "unresolved": 2
  },
  "ready_for_styling": true
}
```

### 8. Revision Notes

Add to the draft:

```markdown
<!--
REVISION NOTES (v1 → v2)

Changes made:
- Restructured Section 2 to address logical gap
- Added evidence from ev_015, ev_016
- Softened claim in paragraph 4.2 (was overstated)
- Cut Section 5 (redundant with Section 3)

Unresolved:
- cr_007: Limited evidence for claim X (marked moderate confidence)
- cr_012: Opposing view not fully addressed (acknowledged in text)

Questions for next review:
- Is the new Section 2 structure clear?
- Does cutting Section 5 leave a gap?
-->
```

## Common Revision Patterns

### "Evidence doesn't support claim"
- Option A: Find stronger evidence (→ RESEARCHER)
- Option B: Soften the claim to match evidence
- Option C: Cut the claim

### "Missing context"
- Option A: Add a paragraph/section with context
- Option B: Add a parenthetical or footnote
- Option C: Acknowledge limitation

### "Logical leap"
- Option A: Add intermediate reasoning
- Option B: Add evidence for the leap
- Option C: Make the leap explicit ("This assumes...")

### "Contradicts other section"
- Option A: Reconcile the contradiction
- Option B: Acknowledge and explain the tension
- Option C: Cut one of the contradicting claims

### "Weak opening/closing"
- Rewrite with The Turn in mind
- Ensure opening hooks
- Ensure closing lands (doesn't trail off)

## Quality Check

Before marking revision complete:

- [ ] All BLOCKING critiques resolved
- [ ] All HIGH critiques resolved or justified
- [ ] MEDIUM critiques addressed where possible
- [ ] Integration pass completed
- [ ] Draft still serves original goals
- [ ] The Turn still clear and supported
- [ ] Version saved and documented

## Next Steps

→ Draft goes to STYLIST for craft pass
→ Or back to CRITIC if major changes made
