---
name: schedule-followup
description: Schedule a follow-up pulse for later checking. Use when user says 'remind me', 'check back', 'follow up', something needs verification later, or waiting for a response/action. Handles both aperiodic pulses (non-hour times) and Diary entries (hour-aligned times).
disable-model-invocation: false
---

# Schedule Follow-Up

Schedule future wake-ups for checking on tasks, responses, or events.

## When to Use

Invoke this skill when:
- 🔔 User says "remind me..." or "check back in..."
- ⏰ User says "follow up on..." or "ping me about..."
- 📬 Waiting for a response (email, message, PR review)
- ✅ Need to verify something later (task completion, event outcome)
- 🔄 Periodic checks needed (every hour, daily, weekly)
- 📅 Time-sensitive item coming up (meeting in 30 min)

## Workflow

### 1. Parse the Request

Extract from $ARGUMENTS or context:
- **What** to follow up on (the task/item)
- **When** to follow up (time/duration)
- **Why** following up (what to check/verify)
- **Priority** level (how urgent)

Examples:
- "Remind me to call John at 2:30 PM" → What: call John, When: 2:30 PM, Why: make the call
- "Check if Sarah replied in an hour" → What: Sarah's response, When: 1 hour, Why: verify reply
- "Follow up on the PR review tomorrow morning" → What: PR review, When: tomorrow 8-9 AM, Why: check status

### 2. Decide: Aperiodic Pulse vs Diary Entry

**Use Aperiodic Pulse when:**
- Time is NOT on the hour (e.g., 2:30 PM, 6:45 AM, 11:15 PM)
- Urgent and can't wait for next periodic pulse
- Specific deadline or time-sensitive

**Use Diary Entry when:**
- Time IS on the hour (8:00 AM, 2:00 PM, 6:00 PM)
- Part of daily routine
- Can be bundled with other periodic checks

**Why this matters:** Aperiodic pulses at hour-aligned times will collide with automatic periodic pulses, causing duplicate wake-ups.

### 3. Determine Priority

Map urgency to priority levels:

**Critical** (🚨):
- Safety/emergency related
- User explicitly said "URGENT" or "ASAP"
- Financial/legal deadline

**High** (🔔):
- User is waiting/blocked
- Important meeting/call reminder
- Time-sensitive (within 2 hours)

**Normal** (⏰):
- Standard reminders
- Non-urgent follow-ups
- Daily routine checks

**Low** (📋):
- Nice-to-have checks
- Long-term follow-ups (weeks/months)

### 4. Build the Follow-Up

#### For Aperiodic Pulses:

Use `schedule_pulse()` MCP tool:

```python
schedule_pulse(
  scheduled_at="[parsed time]",
  prompt="[what to check/do]",
  priority="[critical/high/normal/low]",
  sticky_notes=["[context line 1]", "[context line 2]"]
)
```

**Prompt format:**
Be specific about what to do when pulse fires:
- ✅ "Check if Sarah replied to the ski trip message in group chat"
- ✅ "Remind user to call John at 555-1234 re: project proposal"
- ❌ "Follow up" (too vague)
- ❌ "Reminder" (what for?)

**Sticky notes:**
Include context you'll need later:
- Original request from user
- Relevant details (names, numbers, links)
- Why this matters (connection to goals)

Example:
```python
schedule_pulse(
  scheduled_at="in 1 hour",
  prompt="Check if Sarah replied to ski trip proposal in group chat",
  priority="normal",
  sticky_notes=[
    "User asked group about weekend trip to Mammoth",
    "Waiting for Alex and Jamie to confirm",
    "Need to book by Friday if going"
  ]
)
```

#### For Diary Entries:

Append to `Diary/YYYY-MM-DD.md`:

```markdown
## Scheduled for [TIME]
- **Task**: [what to do]
- **Context**: [why/details]
- **Priority**: [level]
```

Example:
```markdown
## Scheduled for 08:00 AM
- **Task**: Remind user about team standup at 9 AM
- **Context**: Weekly standup, user sometimes forgets
- **Priority**: Normal

## Scheduled for 14:00 PM
- **Task**: Check if PR #123 was reviewed
- **Context**: Blocking deployment, need review by EOD
- **Priority**: High
```

### 5. Confirm to User

Send confirmation via `send_notification()` or direct response:
- **Priority**: silent or normal (don't interrupt)
- **Content**: What, when, why

Examples:
```
✓ Set follow-up: Check Sarah's response in 1 hour
I'll ping you at 3:15 PM if no reply yet.
```

```
✓ Reminder added to Diary for tomorrow 8 AM:
"Call John re: project proposal"
The periodic pulse will remind you then.
```

```
✓ Scheduled 3 follow-ups:
• In 30 min: Check PR review status
• At 2 PM: Remind about client call
• Tomorrow 9 AM: Review weekend plans

I've got you covered!
```

### 6. Log the Follow-Up

Append to `Diary/YYYY-MM-DD.md`:
```markdown
[HH:MM] Scheduled follow-up
- What: [description]
- When: [time]
- Type: [aperiodic pulse / diary entry]
- Priority: [level]
- Reason: [user request or proactive]
```

## Time Parsing Examples

**Relative times:**
- "in 30 minutes" → 30 minutes from now
- "in 2 hours" → 2 hours from now
- "tomorrow" → Tomorrow at 8 AM (or Diary entry)
- "next week" → Next Monday at 9 AM

**Absolute times:**
- "at 2:30 PM" → Today at 2:30 PM
- "tomorrow at 9 AM" → Tomorrow at 9:00 AM
- "Friday at 3 PM" → This Friday at 3:00 PM

**Ambiguous times:**
- "this afternoon" → Today at 2 PM
- "tonight" → Today at 8 PM
- "tomorrow morning" → Tomorrow at 8 AM (Diary entry)
- "end of day" → Today at 6 PM (Diary entry)

**Recurring:**
- "every hour" → Multiple aperiodic pulses OR note in Responsibilities/
- "daily at 8 AM" → Diary entry + update Responsibilities/
- "weekly" → Suggest Goal/Responsibility instead

## Edge Cases

**User says "remind me later"** (vague):
- Ask: "When would you like me to remind you? (e.g., in 1 hour, tomorrow morning)"
- Offer common options: 1 hour, end of day, tomorrow morning

**Time conflict with existing pulse**:
- Check `list_upcoming_pulses()`
- If same time/purpose, don't duplicate
- Merge context if relevant

**Past time** ("remind me at 2 PM" but it's already 3 PM):
- Clarify: "It's already 3 PM. Did you mean tomorrow at 2 PM?"
- Or assume: "tomorrow at 2 PM"

**Recurring follow-ups**:
- For daily/weekly: Suggest adding to Responsibilities/
- For short-term (every hour for 3 hours): Schedule multiple pulses
- Document pattern in Goals/ if long-term

**User cancels or changes mind**:
- Use `cancel_pulse(pulse_id)` for aperiodic
- Edit Diary/ entry if diary-based
- Confirm cancellation: "✓ Cancelled reminder about [X]"

## Quick Reference

| Time Type | Hour-Aligned? | Method | Example |
|-----------|---------------|--------|---------|
| 2:30 PM today | No | Aperiodic pulse | `schedule_pulse("today at 2:30 PM", ...)` |
| 8:00 AM tomorrow | Yes | Diary entry | Append to tomorrow's Diary |
| In 45 minutes | Maybe | Check result time, choose method | If lands on hour → Diary, else → Pulse |
| Next Monday 9 AM | Yes | Diary entry | Append to Monday's Diary |
| In 2 hours | Maybe | Calculate, then choose | If result is hour-aligned → Diary |

## Tips

- **Be specific in prompts** - Future you needs context
- **Use sticky notes liberally** - Better too much context than too little
- **Confirm to user** - Show what was scheduled
- **Check for duplicates** - Don't schedule twice
- **Prioritize correctly** - Don't make everything high priority

The goal is for the user to:
✅ Trust you'll remember (mental load reduced)
✅ Know exactly when you'll follow up
✅ Be reminded at the right time
✅ Have full context when reminder fires
