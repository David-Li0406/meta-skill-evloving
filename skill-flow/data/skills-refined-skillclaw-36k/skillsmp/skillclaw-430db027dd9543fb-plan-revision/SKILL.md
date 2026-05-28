---
name: plan-revision
description: Use this skill when the plan-agent needs to review and revise the analysis results provided by the analysis-agent after the analysis is complete.
---

# Skill body

## When to Use This Skill

- When notified that "analysis-agent has completed the analysis."
- When the plan-agent needs to review the analysis results from the analysis-agent.
- During the revision phase of the planning cycle.

## Not For / Boundaries

**Does Not:**
- Create Record structures (handled by project-bootstrap).
- Execute reviews by Claude (handled by draft-plan-review).
- Finalize plans (handled by plan-finalize).

**Required Input:**
- `Record/plan/draft-plan.md` must exist and contain the "Claude Review Supplement" section.
- The project root directory must be confirmed.

If inputs are missing, prompt the user.

## Quick Reference

### Hard Rules

```
- Must read the "Claude Review Supplement" section of draft-plan.md first.
- Must clearly state approval/disapproval/partial approval for each analysis by Claude.
- Disapproved points must be explained (in Chinese).
- After revisions, draft-plan.md must be updated.
- If the project root is unclear, the user must be asked first.
```

### Independent Thinking Principles

```
- Must independently assess Claude's analysis and user decisions.
- Can challenge user decisions if technical issues are found.
- Can dispute analysis-agent's conclusions.
- Must provide reasons for all objections and potential risks.
- Must not blindly follow user or agent directives.
- When denying, constructive alternatives or improvement suggestions must be provided.
- Must maintain principles, even under pressure from all parties.
```

### Execution Steps

```
1. Read the "Claude Review Supplement" section of draft-plan.md.
2. Evaluate Claude's analysis results item by item.
3. Explain reasons for any disapproved points.
4. Write back the revision results to the "plan-agent revision comments" section of draft-plan.md.
5. Update record.md and Memory/plan-agent.md.
6. Notify the user that the revision is complete and guide them to revision-confirm.
```

## Examples

### Example 1: Full Approval

- **Input**: Claude's analysis results are reasonable.
- **Steps**: Read analysis → Evaluate (full approval) → Write back "full approval" → Notify user.
- **Acceptance**: draft-plan.md contains "plan-agent revision comments: full approval."

### Example 2: Partial Disapproval

- **Input**: There is an issue with Claude's analysis.
- **Steps**: Read analysis → Evaluate → Explain reasons for disapproved points → Write back revision comments.
- **Acceptance**: draft-plan.md contains specific reasons for disapproval and revision suggestions.

### Example 3: Need for Additional Information

- **Input**: Claude's analysis lacks key information.
- **Steps**: Read analysis → Identify missing information → Write back "need to supplement xxx information" → Notify user.
- **Acceptance**: draft-plan.md marks the information that needs to be supplemented, and the user knows the next step.