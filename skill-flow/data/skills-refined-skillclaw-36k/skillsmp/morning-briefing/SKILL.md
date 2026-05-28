---
name: morning-briefing
description: Daily morning briefing at 8:00 AM (or when user wakes up). Provides calendar summary, priorities from Responsibilities, urgent items, and suggested focus areas. Auto-invoke when it's 8 AM periodic pulse, user says 'morning briefing', or user just woke up.
disable-model-invocation: false
---

# Morning Briefing

Provide a comprehensive morning briefing to start the user's day with clarity and focus.

## Workflow

### 1. Read Context
- Read `Goals/Goals.md` for current priorities and active goals
- Read `Responsibilities/Responsibilities.md` for today's recurring duties
- Check `Diary/` for any pending items from yesterday or instructions left for today
- Read `Preferences/Preferences.md` for communication preferences

### 2. Gather Information
- Check calendar (via memory/integration tools if available)
- Identify meetings, appointments, deadlines for today
- Look for upcoming deadlines this week
- Scan Diary/ for follow-up items marked for today

### 3. Build the Briefing

Structure your briefing with these sections:

**Greeting**
- Warm, energetic greeting appropriate for morning
- Example: "Good morning! Ready to make today count?"

**Today's Schedule**
- List meetings/appointments with times
- Highlight the most important meeting
- Note any preparation needed

**Priorities** (from Responsibilities/)
- 2-3 key tasks or responsibilities for today
- Connect to active Goals when possible
- Example: "Client presentation at 2 PM (ties to Q1 revenue goal)"

**Urgent Items**
- Anything due today or overdue
- Follow-ups waiting for action
- Time-sensitive matters

**Focus Suggestion**
- Suggest 1-2 focus areas for the day
- Consider energy levels (mornings are good for deep work)
- Example: "Focus block: 9-11 AM for strategy doc (before meetings start)"

**Weather/Context** (if relevant)
- Briefly mention if weather affects plans
- Transportation alerts if applicable

### 4. Deliver the Briefing

Send as a notification using `send_notification()`:
- **Priority**: normal (unless something urgent → high)
- **Format**: Use MarkdownV2 for structure
- **Length**: Keep it scannable (under 300 words)
- **Tone**: Energizing and action-oriented

Example format:
```
Good morning! Here's your day at a glance:

📅 Schedule (3 meetings)
• 10:00 AM: Team standup
• 2:00 PM: Client presentation (Q1 proposal)
• 4:30 PM: 1-on-1 with Sarah

🎯 Top Priorities
• Finalize Q1 proposal slides (for 2 PM meeting)
• Review pull requests (team is waiting)
• Call dentist to reschedule

⚠️ Urgent
• Budget approval needed by EOD

💡 Suggested Focus
Deep work block: 9-11 AM for proposal prep
(Your calendar is clear then - perfect timing!)

You've got this! 🚀
```

### 5. Log Activity
Use the `/diary-log` skill or append to `Diary/YYYY-MM-DD.md`:
```
[08:00] Morning briefing sent
- 3 meetings today
- Key focus: Q1 proposal prep
- Urgent: Budget approval by EOD
```

## Edge Cases

**User wakes up late (after 10 AM)**
- Adjust greeting: "Good late morning!"
- Focus on what's left in the day
- Don't overwhelm with missed items

**No calendar access**
- Focus on Responsibilities/ and Diary/ items
- Suggest user check their calendar
- Be helpful with what you know

**Weekend**
- Still provide briefing but adjust tone
- Focus on personal goals and projects
- Keep it light and optional

**User traveling**
- Note timezone if different
- Highlight travel-related items
- Consider jet lag in tone

## Tips

- **Be concise** - Morning time is precious
- **Prioritize ruthlessly** - Show what truly matters
- **Be energizing** - Set a positive tone for the day
- **Connect to goals** - Remind user of the bigger picture
- **Actionable** - Make it clear what to do first

The goal is for the user to feel:
✅ Informed about their day
✅ Clear on priorities
✅ Energized to start
✅ Connected to their goals
