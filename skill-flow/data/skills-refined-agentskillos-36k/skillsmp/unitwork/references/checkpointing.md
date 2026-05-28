# Checkpointing Reference

This document is the single source of truth for checkpoint-related protocols in Unit Work.

## Checkpoint Commit Format

```
checkpoint({unit-number}): {brief description}

Unit: {unit-name from plan}
Confidence: {percentage}%
Verification: {test-runner|api-prober|browser|manual}

See: .unitwork/verify/{DD-MM-YYYY}-{checkpoint-number}-{short-name}.md
```

**For PR comment fixes**, use this numbering:
```
checkpoint(pr-{PR_NUMBER}-{fix_number}): {brief description}
```

Example: `checkpoint(pr-123-1): handle null email addresses`

## When to Checkpoint

See [decision-trees.md](./decision-trees.md#when-to-checkpoint) for the complete decision flow.

**Summary:** A checkpoint is required after ANY code change:
- Completing a unit from the spec
- Fixing an issue found during verification
- Implementing user feedback or corrections
- Any code change, no matter how small

**There is no "minor change" exemption.**

## Verification Document

Create `.unitwork/verify/{DD-MM-YYYY}-{checkpoint-number}-{short-name}.md` using the template at [templates/verify.md](../templates/verify.md).

**CRITICAL: Minimize human review.** If you can verify something with 100% certainty (grep, read, test output), verify it yourself and list in "AI-Verified". Only put items in "Human QA Checklist" that genuinely require human judgment.

## Self-Correcting Review (Fix Checkpoints Only)

See [verification-flow.md](./verification-flow.md#self-correcting-review-fix-checkpoints-only) for the complete self-correcting review protocol including:
- Risk Assessment (when to skip, light review, or full review)
- Selective Agent Invocation (which agents to spawn based on issue type)
- Cycle Handling (max 3 cycles, user options when limit reached)

## Confidence Calculation

See [verification-flow.md](./verification-flow.md#confidence-calculation) for confidence calculation rules and thresholds.
