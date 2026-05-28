---
name: emergency-response
description: Handle critical/emergency events requiring immediate user attention. Use when flight delays detected, family emergency messages, system failures, safety issues, or anything marked URGENT that needs immediate action within minutes.
disable-model-invocation: false
---

# Emergency Response

Handle critical events that require immediate user attention and action.

## When to Invoke

Use this skill when you detect:
- 🚨 **Safety issues** - Anything affecting user's physical safety
- 👨‍👩‍👧 **Family emergencies** - Messages from family marked urgent/emergency
- ✈️ **Travel disruptions** - Flight delays, cancellations, gate changes
- 🏥 **Health alerts** - Medical appointments, prescription reminders (if urgent)
- 💻 **System failures** - Critical system down, data loss, security breach
- 📱 **Time-critical messages** - "Call me NOW", "Emergency", "ASAP"
- ⏰ **Missed critical deadlines** - Something due in <15 minutes

**NOT emergencies:**
- Regular work tasks (even if high priority)
- Standard meeting reminders
- Normal email/messages
- Routine notifications

## Workflow

### 1. Assess the Situation

**Determine urgency:**
- Life/safety issue → CRITICAL
- Financial/legal deadline → CRITICAL
- Travel disruption → HIGH
- Work emergency → HIGH
- Ambiguous → Ask yourself: "Does user need to know THIS MINUTE?"

**Gather context:**
- What happened?
- When did it happen / when does user need to act?
- What information does user need to make a decision?
- What are the immediate options/actions?

### 2. Check Preferences
Read `Preferences/Preferences.md`:
- Emergency contacts? (family members who can call through)
- DND override rules? (what breaks through Do Not Disturb)
- Travel preferences? (auto-rebook flights? call airline?)
- Decision authority? (what can you handle vs user must decide)

### 3. Build Emergency Notification

**Structure:**

**1. Alert Line** (Clear, direct)
```
🚨 URGENT: [What happened in 5-8 words]
```

**2. Critical Info** (What user needs to know NOW)
```
- What: [The event]
- When: [Time/deadline]
- Impact: [Why this matters]
```

**3. Immediate Options** (2-3 actionable choices)
```
Options:
1. [Action A] - [Consequence]
2. [Action B] - [Consequence]
3. [Action C] - [Consequence]
```

**4. What You've Done** (Actions you've already taken)
```
✓ Already done:
- [Action 1]
- [Action 2]
```

**5. Follow-Up** (What happens next)
```
I'll [automatic follow-up action]
```

### 4. Send Critical Notification

Use `send_notification()`:
- **Priority**: critical (🚨 - overrides Do Not Disturb)
- **Format**: MarkdownV2 or plain text for readability
- **Length**: Concise but complete (under 200 words)
- **Tone**: Calm, clear, action-oriented (NO panic)

Example:
```
🚨 URGENT: Flight UA123 delayed 3 hours

What:
• Your 6:45 AM flight to NYC now departs at 9:45 AM
• You'll miss your 10:30 AM meeting

Impact:
• Client presentation will need to reschedule
• Hotel check-in still okay (3 PM)

Options:
1. Take delayed flight → Reschedule client to afternoon
2. Book earlier flight ($200 change fee) → Make morning meeting
3. Cancel trip → Full refund, reschedule everything

✓ Already done:
• Found alternative UA flight at 7:30 AM (2 seats left)
• Draft email to client explaining situation

What do you want to do? I can book/email once you decide.

I'll check status again in 30 minutes.
```

### 5. Schedule Automatic Follow-Up

Use `/schedule-followup` or `schedule_pulse()`:
- **When**: 15-30 minutes for critical, 1-2 hours for urgent
- **What**: Check if user responded, update situation, offer help
- **Priority**: high

Example:
```
schedule_pulse(
  scheduled_at="in 30 minutes",
  prompt="Follow up on flight delay emergency - check if user made decision",
  priority="high"
)
```

### 6. Log Emergency
Append to `Diary/YYYY-MM-DD.md`:
```
[HH:MM] 🚨 EMERGENCY: [Brief description]
Context: [What happened]
Notification sent: [What user was told]
Options provided: [What choices given]
Follow-up scheduled: [When checking back]
Status: [Waiting for user response]
```

## Response Patterns

### Flight Delay/Cancellation
```
🚨 URGENT: Flight [number] [status]

• Original: [time] → New: [time] or Cancelled
• Impact: [what meetings/plans affected]

Options:
1. Alternative flights: [list with times]
2. Refund + reschedule trip
3. Wait it out if minor delay

✓ Checked: [other flights, hotel policy, etc.]

Need help booking or rescheduling?
```

### Family Emergency Message
```
🚨 URGENT: Message from [family member]

• Received: [X minutes ago]
• They said: "[quote key part]"
• Marked as: [Emergency/Urgent]

Immediate action:
Call them at [number] NOW

✓ Already done:
• Cleared your next 30 minutes on calendar
• Located their contact info

I'll hold all non-critical notifications.
```

### System Failure
```
🚨 CRITICAL: [System] is down

• What: [service/system name]
• Impact: [who/what affected]
• Since: [how long]

Immediate:
[Specific action needed from user]

✓ Status:
• [What you've checked]
• [Current state]

I'm monitoring and will update every [interval].
```

### Deadline Crisis
```
🚨 URGENT: [Task] due in [time]

• Deadline: [exact time]
• Status: [current state]
• Gap: [what's missing]

Options:
1. Rush completion - [what's needed, how long]
2. Request extension - [who to contact]
3. Submit partial - [what's ready]

I can [help action - draft email, gather materials, etc.]

What's the call?
```

## Guidelines

**DO:**
- ✅ Be calm and clear (user may be stressed)
- ✅ Provide specific options (not just "what do you want?")
- ✅ Show what you've already handled
- ✅ Set up automatic follow-up
- ✅ Clear user's immediate calendar if needed

**DON'T:**
- ❌ Panic or use excessive caps/exclamation marks
- ❌ Provide too many options (max 3)
- ❌ Give vague information
- ❌ Forget to follow up
- ❌ Cry wolf (only use for real emergencies)

**Tone calibration:**
- Life/safety: Direct, calm, supportive
- Travel: Helpful, solution-focused
- Work: Professional, clear options
- Family: Empathetic, action-oriented

## Edge Cases

**False alarm** (thought it was emergency, wasn't):
- Send quick correction: "Update: False alarm on [X]. All clear!"
- Log it to learn patterns
- Don't apologize excessively

**User doesn't respond** (after 30 min):
- Send one follow-up: "Still need a decision on [X]"
- If truly critical and no response after 1 hour, escalate per Preferences/
- Log the situation

**Multiple emergencies at once**:
- Send ONE notification with all items
- Prioritize by urgency (safety first)
- Number them clearly

**User on vacation/OOO**:
- Check Preferences/ for OOO protocols
- Still notify if truly critical
- Handle more autonomously if user granted authority

The goal is for the user to:
✅ Immediately understand what happened
✅ Know their options clearly
✅ Feel supported (you've done groundwork)
✅ Be able to decide and act quickly
