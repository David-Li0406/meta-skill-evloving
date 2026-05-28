---
name: planning-revision-and-confirmation
description: Use this skill when you need to evaluate and revise project plans based on analysis results, and confirm those revisions with stakeholders.
---

# planning-revision-and-confirmation

> **Access Control**: This skill is intended for internal use by plan-agent and analysis-agent only.

This skill encompasses the processes of revising project plans based on analysis results and confirming those revisions with stakeholders.

## When to Use This Skill

- When the user notifies that the analysis is complete.
- When the plan-agent needs to review analysis results and revise the draft plan.
- When the analysis-agent is required to confirm the revisions made by the plan-agent.

## Not For / Boundaries

**Does Not**:
- Create Record structures (handled by project-bootstrap).
- Execute reviews (handled by draft-plan-review).
- Finalize plans (handled by plan-finalize).
- Modify the original draft plan content (only append analysis results).

**Required Inputs**:
- `Record/plan/draft-plan.md` must exist and contain the relevant sections.
- The project root directory must be confirmed.

If inputs are missing, prompt the user for clarification.

## Quick Reference

### Hard Rules

```
- Must read the "Claude Review Supplement" section of draft-plan.md.
- Must evaluate each analysis point with a clear stance: agree/disagree/partially agree.
- Disagreements must be justified (in Chinese).
- Revisions must be written back to draft-plan.md.
- If the project root is unclear, ask the user first.
```

### Independent Thinking Principles

```
- Must independently assess the analysis and user decisions.
- Can challenge user decisions if technical issues are found.
- Can dispute analysis-agent conclusions.
- Must provide reasons for all disagreements and potential risks.
- Must not blindly accept decisions based on authority.
- Must offer constructive alternatives or improvements when disagreeing.
- Must uphold principles even under pressure from stakeholders.
```

### Execution Steps

```
1. Read the "Claude Review Supplement" section of draft-plan.md.
2. Evaluate the analysis results point by point.
3. Justify any disagreements.
4. Write back the revision results to the "plan-agent revision comments" section of draft-plan.md.
5. Update record.md and Memory/plan-agent.md.
6. Notify the user that the revision is complete and guide them to the confirmation process.
```

## Examples

### Example 1: Full Agreement

- **Input**: Analysis results are reasonable.
- **Steps**: Read analysis → Evaluate (full agreement) → Write back "Full agreement" → Notify user.
- **Acceptance**: draft-plan.md includes "plan-agent revision comments: Full agreement".

### Example 2: Partial Disagreement

- **Input**: Some analysis points are problematic.
- **Steps**: Read analysis → Evaluate → Justify disagreements → Write back revision comments.
- **Acceptance**: draft-plan.md includes specific disagreement reasons and revision suggestions.

### Example 3: Need for Additional Information

- **Input**: Analysis lacks critical information.
- **Steps**: Read analysis → Identify missing information → Write back "Need to supplement xxx information" → Notify user.
- **Acceptance**: draft-plan.md notes the need for additional information, and the user is informed of the next steps.

## References

- `references/revision-workflow.md` - Evaluation and revision process.
- `references/writeback-template.md` - Template for writing back revision results.

## Maintenance

- Source: Dual AI Collaborative Development Plan.
- Last Updated: 2026-01-07.
- Known Limitations: Only revises plans, does not execute code.