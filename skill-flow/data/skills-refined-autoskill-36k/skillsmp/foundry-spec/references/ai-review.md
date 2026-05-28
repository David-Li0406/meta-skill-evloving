# AI Plan Review

Get AI-powered feedback on markdown plans before converting to JSON specs.

## Running a Review

```bash
# Full comprehensive review (standard practice)
mcp__plugin_foundry_foundry-mcp__plan action="review" plan_path="specs/.plans/feature-name.md" review_type="full"

# Quick review for blockers only
mcp__plugin_foundry_foundry-mcp__plan action="review" plan_path="specs/.plans/feature-name.md" review_type="quick"
```

## Review Types

| Type | Dimensions | Use When |
|------|------------|----------|
| `full` | Completeness, Architecture, Sequencing, Feasibility, Risk, Clarity | Initial review, major changes |
| `quick` | Critical blockers, Key questions | Iteration, minor updates |
| `security` | Auth, Input validation, Data handling, Secrets | Security-sensitive features |
| `feasibility` | Complexity, Dependencies, Unknown risks | Novel or risky implementations |

## Review Output Location

Reviews are saved to: `specs/.plan-reviews/<plan-name>-<review-type>.md`

## Review Output Structure

```markdown
# Plan Review: {Plan Name}

## Summary
{Overall assessment}

## Dimensions

### Completeness
**Score:** {1-5}
**Findings:**
- {Finding 1}
- {Finding 2}
**Recommendations:**
- {Recommendation 1}

### Architecture
**Score:** {1-5}
**Findings:**
- {Finding 1}
**Recommendations:**
- {Recommendation 1}

[... additional dimensions ...]

## Critical Blockers
1. {Blocker requiring resolution before proceeding}

## Questions for Stakeholder
1. {Question needing clarification}

## Verdict
{APPROVED | NEEDS_REVISION | BLOCKED}
```

## Iteration Workflow

```
1. Create plan → plan action="create" (MANDATORY)
2. Fill in content → Read + Edit
3. Run AI review → plan action="review"
4. Read feedback → specs/.plan-reviews/
5. Revise plan → Edit based on feedback
6. Re-review → plan action="review"
7. Repeat until no critical blockers
8. HUMAN APPROVAL GATE → AskUserQuestion
   - [approved] → continue
   - [revise] → back to step 2
   - [abort] → exit
9. Convert to spec → authoring action="spec-create"
```

## Common Review Feedback

| Issue | Typical Recommendation |
|-------|------------------------|
| Vague tasks | Add specific acceptance criteria |
| Missing dependencies | Explicit task ordering needed |
| No verification | Add test requirements |
| Scope creep | Split into multiple specs |
| Missing risks | Add risk assessment section |
