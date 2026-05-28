---
name: bead-fix
description: Apply fixes from BEADS_LEDGER.md to BEADS.md. Use after bead-review identifies blockers or should-fixes. Does not update ledger status - that happens on next bead-review pass.
---

# Bead Fix Workflow

Apply fixes from a bead review ledger to the BEADS.md file. This skill reads open issues from `BEADS_LEDGER.md` and mechanically applies the required fixes.

## When to use

Use when you have:
- A `BEADS_LEDGER.md` with OPEN blockers or should-fixes from `/bead-review`
- A `BEADS.md` that needs fixes applied
- Need to iterate toward approval

Do NOT use:
- Before running `/bead-review` at least once
- If ledger shows no OPEN blockers
- To update ledger status (that's `/bead-review`'s job)

## Role

You are a mechanical fix applicator. Apply exactly what the ledger specifies, no more, no less.

## Required inputs

- `docs/plans/<project>/BEADS_LEDGER.md` - Must exist with OPEN issues
- `docs/plans/<project>/BEADS.md` - The file to fix
- `docs/plans/<project>/TECHNICAL_DESIGN.md` - Reference for fixes that need TDD content

## Workflow

### Step 1: Read the Ledger

Read `BEADS_LEDGER.md` and extract all issues with `Status: OPEN`:
- Blockers (must fix)
- Should-fixes (should fix)
- Minor (may fix)

### Step 2: Categorize Fixes

Group fixes by type:

**Global fixes** (apply to all/many beads):
- Missing metadata fields (Parallelism, Confidence)
- Missing labels
- Format issues

**Targeted fixes** (apply to specific beads):
- Coverage gaps (add content to specific bead)
- Context issues (clarify specific sections)
- Atomicity issues (split beads)

### Step 3: Apply Global Fixes First

For metadata issues affecting all beads:

1. Read the ledger's "Recommended Metadata Values" table (if present)
2. For each bead section (`## BEAD-ID: Title`), locate the `### Context` section
3. Add the missing fields after existing content:

```markdown
### Context

[existing content]

**Parallelism:** <value from ledger table>
**Confidence:** <value from ledger table>
```

Valid Parallelism values: `parallelizable`, `requires-sequence`, `decision-gated`
Valid Confidence values: `verified`, `assumed`, `unverified`

### Step 4: Apply Targeted Fixes

For each targeted fix:

1. Locate the specific bead by ID
2. Apply the fix as specified in the ledger's "Required Fix" field
3. Common fix patterns:

**Coverage gap (add to Implementation Notes):**
```markdown
### Implementation Notes

> **From review ({issue-id}):**
> - {fix content from ledger}
```

**Context issue (clarify section):**
- Add missing imports to Tasks
- Clarify ambiguous references
- Add data structure specifications

**Atomicity issue (split bead):**
- Create new bead sections with IDs like `ORIG-01a`, `ORIG-01b`
- Update dependency graph (Mermaid diagram)
- Update dependency script (`bd dep add` commands)

### Step 5: Update Dependency Script (if beads were split)

If any beads were split:
1. Add new `bd dep add` commands for new beads
2. Update existing commands that referenced the original bead
3. Ensure graph remains acyclic

### Step 6: Verify Fixes

After applying all fixes, verify:
- [ ] All beads have required metadata fields
- [ ] No syntax errors in markdown
- [ ] Mermaid diagram is valid (if modified)
- [ ] Dependency script matches diagram (if modified)

## Output

Modified `BEADS.md` with fixes applied.

Do NOT:
- Modify `BEADS_LEDGER.md` (status updates are done by `/bead-review`)
- Add fixes beyond what the ledger specifies
- Change bead content unrelated to ledger issues

## After Completion

Inform the user to run `/bead-review` again to:
1. Verify fixes were applied correctly
2. Update ledger with new pass results
3. Check for convergence (0 blockers in two consecutive passes)

## Common Fix Patterns

### Pattern: Add Parallelism/Confidence to All Beads

When ledger shows `META-GLOBAL-01` and `META-GLOBAL-02`:

```markdown
### Context

{existing context content}

**Parallelism:** requires-sequence
**Confidence:** verified
```

### Pattern: Add Circuit Breaker/Retry Coverage

When ledger shows coverage gap for resilience patterns:

Add to the relevant bead's Implementation Notes:

```markdown
### Implementation Notes

> **From review (COV-001, COV-002):**
> - **Circuit Breaker**: Track consecutive connection failures. After 5 failures, open circuit for 30s. After cooldown, allow 1 test request (half-open). If succeeds, close circuit.
> - **Retry/Backoff**: For connection timeout, retry 3x with exponential backoff (1s, 2s, 4s) before raising.
```

### Pattern: Clarify Ambiguous Reference

When ledger shows context issue for vague pronoun/reference:

Before:
```markdown
Set timeout if needed (inline or via event)
```

After:
```markdown
Timeout is handled by checkout/checkin events established in SS-DS-01; no additional timeout code needed here.
```
