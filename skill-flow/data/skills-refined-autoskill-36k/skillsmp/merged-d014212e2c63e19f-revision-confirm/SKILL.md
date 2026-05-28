---
name: revision-confirm
description: Use this skill for confirming revisions made by the plan-agent, guiding the analysis and next steps based on the feedback provided.
---

# revision-confirm

> **Important**: This functionality has been migrated to the `analysis-agent`.

## How to Use

To initiate the revision confirmation, start the **analysis-agent** with the following commands:

```
Start Analysis
```

or

```
analysis-agent confirm revision
```

## Migration Notes

- The original skill functionality has been fully migrated to `~/.claude/agents/analysis-agent/skills/revision-confirm/`.
- The analysis-agent provides a more comprehensive confirmation process and access control.
- Supports automated collaboration with the plan-agent.

## When to Use This Skill

- When the plan-agent calls the analysis-agent for revision confirmation.
- When a user notifies that "the plan-agent has completed revisions."
- When a user requests confirmation of revisions.

## Not For / Boundaries

**This skill does not**:
- Modify the status field of the draft (managed by the plan-agent).
- Change the content of the draft (only write in the "analysis-agent confirmation comments" section).
- Write "final user confirmation" or similar results.
- Replace the plan-agent in executing plan-finalize operations.
- Revise plans (handled by plan-revision).
- Inquire "whether to start implementation" (implementation is assigned by the plan-agent).
- Self-assign or take over implementation tasks.

**Required Input**:
- The `Record/plan/draft-plan.md` must exist and contain the "plan-agent revision comments" section.
- The project root directory must be confirmed.

If inputs are missing, use AskUserQuestion to inquire.

## Quick Reference

### Hard Rules

```
- Must read the "plan-agent revision comments" section from Record/plan/draft-plan.md first.
- Complete analysis of the plan-agent revisions is required; skipping is not allowed.
- Any objections must be justified with reasons and suggestions for further communication (return to plan-agent revisions).
- Only after approval can the user be guided to plan-finalize.
- If the project root is unclear, AskUserQuestion must be used first.
- **No Overstepping**: After approval, stop; do not execute plan-finalize.
- **No Overstepping**: Do not read/modify state.json.
- **No Overstepping**: If the user says "continue," output the guiding statement and stop; do not execute any finalization.
- **No Overstepping**: Do not inquire "whether to start implementation" or similar questions.
- **No Overstepping**: Do not self-assign or take over implementation tasks (implementation is assigned by the plan-agent through plan-finalize).
- **No Modification**: Do not modify the draft content written by the plan-agent; only write in the "analysis-agent confirmation comments" section.
```

### Independent Thinking Principles

```
- Must independently assess the revision comments.
- Can reject user requests if technical issues are found, even if the user has confirmed decisions.
- Can challenge the plan-agent's revision comments.
- Must provide reasons for all rejections and potential risks.
- Must not blindly follow user or agent requests without independent evaluation.
- When rejecting, provide alternative solutions or improvement suggestions.
- Must adhere to principles, even under pressure from multiple parties.
```

### Execution Steps

```
1. Confirm the project root directory.
2. Read the "plan-agent revision comments" section from Record/plan/draft-plan.md.
3. Analyze the revision content (whether it resolves issues, introduces new problems).
4. Output analysis conclusion (approval/objection).
5. If objection → state reasons, suggest further communication.
6. If approved → update record.md + Memory/analysis-agent.md, output guiding statement, then **stop**.
```

### Standard Output After Approval (must use)

```
The plan has been approved. Please start **plan-agent** to execute plan-finalize.

Next step: Start plan-agent to execute plan-finalize.
```

**Note**: After outputting the guiding statement, the analysis-agent must stop and not perform any subsequent actions.

## Examples

### Example 1: Approving Revisions

- **Input**: plan-agent calls or user says "the plan-agent revisions are complete, please confirm."
- **Steps**: Read "plan-agent revision comments" → Analyze → Approve → Output guiding statement → **Stop**.
- **Acceptance**: Output "The plan has been approved. Please start plan-agent to execute plan-finalize," then stop.

### Example 2: User Says "Continue"

- **Input**: After the analysis-agent outputs the guiding statement, the user says "continue."
- **Steps**: Output the guiding statement again → **Stop** (do not execute plan-finalize).
- **Acceptance**: Output "Please start plan-agent to execute plan-finalize," do not read state.json, do not execute finalization.

### Example 3: Objection

- **Input**: The plan-agent revisions do not resolve critical issues.
- **Steps**: Read "plan-agent revision comments" → Analyze → Identify issues → State objections.
- **Acceptance**: Output objection reasons, suggest "please provide feedback to the plan-agent for further revisions."

### Example 4: Error Demonstration (Prohibited)

- **Input**: The analysis-agent approves revisions.
- **Incorrect Action**: Inquire "should we start implementation?" or self-assign implementation tasks.
- **Correct Action**: Output the standard guiding statement and stop; implementation is assigned by the plan-agent through plan-finalize.

## References

- `references/confirm-workflow.md` - Confirmation process and analysis points.
- `references/writeback-template.md` - Writeback template.

## Maintenance

- Source: Collaborative development plan for all Claude sub-agents.
- Last updated: 2026-01-07.
- Known limitations: Only analysis confirmation, does not modify draft status.