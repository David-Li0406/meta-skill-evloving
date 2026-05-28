---
name: diary-log
description: Log activities, decisions, or important events to Diary/ for future reference and pattern detection. Auto-invoke when completing tasks, making decisions, important events occur, or context should be preserved for next pulse. Creates timestamped entries with tags.
disable-model-invocation: false
---

# Diary Log

Log activities, decisions, and events to Diary/ for memory and pattern detection.

## When to Use

Invoke this skill when:
- ✅ **Task completed** - Log what was done and outcome
- 🤔 **Decision made** - Record decision and reasoning
- 📌 **Important event** - Meeting, conversation, milestone
- 💡 **Insight discovered** - Learning or realization
- 🔄 **Context to preserve** - Info needed for next pulse
- 🎯 **Goal progress** - Action advancing a goal

## Workflow

### 1. Determine Today's Date

Calculate current date for filename: `Diary/YYYY-MM-DD.md`

### 2. Structure the Entry

**Format:**
```markdown
[HH:MM] [CATEGORY] Brief headline

Details:
- Key point 1
- Key point 2
- Key point 3

Related: [Link to Goals/ or Responsibilities/ if applicable]
```

**Categories (use tags):**
- `[TASK]` - Completed task
- `[DECISION]` - Decision made
- `[EVENT]` - Meeting, conversation, milestone
- `[GOAL]` - Progress on goal
- `[INSIGHT]` - Learning or realization
- `[EMERGENCY]` - Critical event
- `[BLOCKED]` - Hit a blocker
- `[WIN]` - Celebration-worthy accomplishment

### 3. Write Concise Entry

**Good entries:**
- ✅ Clear headline describing what happened
- ✅ 2-5 bullet points with details
- ✅ Links to related Goals/Responsibilities
- ✅ Outcome or next steps

**Avoid:**
- ❌ Vague ("did stuff")
- ❌ Too much detail (essay-length)
- ❌ Missing context (what/why)

**Examples:**

```markdown
[14:30] [TASK] Completed Q1 proposal slides

Details:
- Finalized revenue projections (15% growth target)
- Added competitive analysis section
- Reviewed with Sarah, incorporated feedback
- Ready for client presentation tomorrow

Related: Goals/Q1-Revenue-Target.md
```

```markdown
[09:15] [DECISION] Chose React over Vue for new project

Reasoning:
- Team has more React experience
- Better TypeScript support
- Larger ecosystem for our needs
- Client already using React

Trade-off: Steeper learning curve for 2 junior devs
Next: Set up project scaffold this afternoon
```

```markdown
[16:00] [GOAL] Marathon training - Week 5 Day 3

- 6-mile long run completed
- Pace: 9:45/mile (comfortable)
- Felt strong, no injuries
- Total weekly mileage: 18 miles

Related: Goals/Marathon-Training.md
Status: On track for April race
```

### 4. Append to Diary File

Use Write or Edit tool to append entry to `Diary/YYYY-MM-DD.md`

If file doesn't exist, create it with header:
```markdown
# Diary: YYYY-MM-DD (Day of Week)

[entries go here]
```

### 5. Confirm (if user-facing)

For user-initiated logs, confirm:
```
✓ Logged to Diary: [brief description]
```

## Entry Guidelines

**When to log:**
- After completing significant tasks
- Immediately after important decisions
- At end of meetings/conversations
- When goals advance
- When patterns emerge
- When context needed later

**When NOT to log:**
- Trivial routine actions
- Every single pulse (too noisy)
- Redundant info already captured
- Personal/private user info without consent

**Level of detail:**
- **Critical events**: More detail
- **Routine tasks**: Brief
- **Decisions**: Include reasoning
- **Goals**: Include metrics

## Pattern Detection

Over time, Diary entries enable:
- Goal progress tracking
- Energy/productivity patterns
- Decision-making quality
- Time management insights
- Blocker identification

Review past entries during:
- `/goal-check` reviews
- Morning briefings (check yesterday)
- Evening wrap-ups (summarize today)

## Example Diary File

```markdown
# Diary: 2026-01-22 (Wednesday)

[08:00] [EVENT] Morning briefing sent
- 3 meetings today
- Key focus: Q1 proposal prep
- Urgent: Budget approval by EOD

[10:30] [TASK] Team standup completed
- Reviewed sprint progress (80% done)
- Blocked: PR #456 needs security review
- Next: Follow up with security team this afternoon

[14:00] [WIN] Client presentation went great!
- Client loved revenue projections
- Approved Q1 proposal
- Next steps: Contract by Friday

Related: Goals/Q1-Revenue-Target.md
Impact: On track for Q1 target, ahead by 10%

[15:30] [DECISION] Approved budget for new hires
- 2 engineers, 1 designer
- Total: $300K
- Start date: March 1

Reasoning: Team bandwidth critical for Q2 goals
Risk: Budget tight, but worth it

[18:00] [GOAL] Evening wrap-up sent
- Productive day, 3 major wins
- Tomorrow: Light morning, focus afternoon
- User should feel accomplished

[18:30] [INSIGHT] User most productive before noon
- Pattern observed over 2 weeks
- 80% of goal progress happens AM
- Suggestion: Schedule deep work mornings only
```

The goal is to:
✅ Preserve context between pulses
✅ Enable pattern detection over time
✅ Support goal tracking and reviews
✅ Create searchable memory of actions