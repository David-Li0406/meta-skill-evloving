---
name: executing-plans
description: Execute a written implementation plan with batch processing and human review checkpoints. Use when you have a plan file ready for implementation in a parallel session.
---

# Executing Plans

## Description
Execute a written implementation plan with batch processing and review checkpoints. Use when you have a plan file ready for implementation.

## When to Use
- After `/brainstorming` produces a design doc
- When you have a written implementation plan
- For any multi-step implementation needing oversight

## Announcement
Say at start: **"I'm using the executing-plans skill to implement this plan."**

## The Process

### Step 1: Load and Review Plan
1. Read the plan file
2. Review critically - identify questions or concerns
3. **If concerns:** Raise them before starting
4. **If no concerns:** Create TodoWrite and proceed

### Step 2: Execute Batch
**Default: First 3 tasks**

For each task:
1. Mark as `in_progress` in TodoWrite
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as `completed`

### Step 3: Report
When batch complete:
```
## Batch Complete

### Implemented
- [what was done]

### Verification Output
[test results, build output, etc.]

Ready for feedback.
```

### Step 4: Continue
Based on feedback:
- Apply changes if needed
- Execute next batch
- Repeat until complete

### Step 5: Complete
After all tasks verified:
- Run final verification
- Clean up any temporary code
- Prepare for commit/PR

## When to STOP and Ask

**Stop immediately when:**
- Hit a blocker mid-batch
- Missing dependency or unclear instruction
- Test fails repeatedly
- Plan has critical gaps

**Ask for clarification rather than guessing.**

## When to Revisit Step 1

Return to plan review when:
- Partner updates the plan based on feedback
- Fundamental approach needs rethinking

## Key Principles

| Principle | Why |
|-----------|-----|
| Review plan critically first | Catch issues early |
| Follow steps exactly | Plan was validated |
| Don't skip verifications | Catch regressions |
| Batch + checkpoint | Human oversight |
| Stop when blocked | Don't guess |

## Example Flow

```
User: "Execute the plan in docs/plans/2026-01-03-notifications-design.md"

Claude: "I'm using the executing-plans skill to implement this plan.

        Let me review the plan first...
        [reads plan]

        The plan looks solid. I have one question:
        - Step 4 mentions 'existing notification service' but I don't see one.
          Should I create it, or is this referencing something else?"

User: "Create it from scratch"

Claude: "Got it. Creating TodoWrite with tasks from the plan.

        Starting batch 1 (tasks 1-3):
        1. Create notification service interface
        2. Implement in-memory notification store
        3. Add notification event types

        [executes tasks...]

        ## Batch Complete

        ### Implemented
        - NotificationService interface in src/services/notifications.ts
        - InMemoryNotificationStore with add/get/markRead
        - NotificationEvent types (alert, info, warning)

        ### Verification Output
        ✓ npm run typecheck - passed
        ✓ npm test - 3 new tests passing

        Ready for feedback."

User: "Looks good, continue"

Claude: "Starting batch 2 (tasks 4-6)..."
```

## Batch Size

- **Default:** 3 tasks
- **Adjust based on:** task complexity, risk level, user preference
- **Smaller batches:** for risky changes or unfamiliar code
- **Larger batches:** for mechanical/repetitive tasks
