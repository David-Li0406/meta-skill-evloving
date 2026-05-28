---
name: evening-wrapup
description: Daily evening wrap-up at 6:00 PM (or end of workday). Reviews today's accomplishments, celebrates progress on goals, previews tomorrow, suggests prep work. Auto-invoke when it's 6 PM periodic pulse, user says 'wrap up' or 'end of day', or user is finishing work.
disable-model-invocation: false
---

# Evening Wrap-Up

Help the user close their workday with reflection, celebration, and preparation for tomorrow.

## Workflow

### 1. Review Today
Read today's activity from:
- `Diary/YYYY-MM-DD.md` - What happened today
- `Goals/Goals.md` - Active goals to connect accomplishments to
- `Responsibilities/Responsibilities.md` - What was supposed to happen

### 2. Build the Wrap-Up

Structure your wrap-up with these sections:

**Greeting**
- Warm, reflective tone
- Example: "That's a wrap! Let's see what you accomplished today."

**Today's Wins** ✅
- List 2-4 concrete accomplishments
- Connect wins to Goals/ when possible
- Celebrate progress, even small wins
- Example: "Completed Q1 proposal (on track for revenue goal!)"

**Progress on Goals** 🎯
- If any active goals were advanced today, call it out
- Use encouraging language
- Example: "Week 5 of marathon training - consistency is paying off!"

**What Didn't Get Done** (optional)
- Only mention if important
- No guilt-tripping - just awareness
- Example: "Budget review moved to tomorrow (no rush)"

**Tomorrow's Preview** 📅
- Check calendar for tomorrow's meetings/events
- Highlight most important item
- Note anything that needs preparation

**Prep Suggestions** 💡
- 1-2 specific prep tasks for tonight or tomorrow morning
- Keep it light - this is end of day
- Example: "Review slides before bed? Or fresh eyes in the morning - your call."

**Personal Reminders** (if any)
- Non-work commitments (dinner plans, gym, family)
- Show you care about work-life balance

**Sign-Off**
- Encouraging, permission to rest
- Example: "Great work today! Enjoy your evening 🌙"

### 3. Deliver the Wrap-Up

Send as notification using `send_notification()`:
- **Priority**: normal (or silent if user prefers quiet evenings)
- **Format**: Use MarkdownV2 for structure
- **Length**: Keep it concise (under 250 words)
- **Tone**: Reflective, celebratory, and relaxing

Example format:
```
That's a wrap for today!

✅ Today's Wins
• Completed Q1 proposal (revenue goal on track!)
• Reviewed 5 PRs (team unblocked)
• Called dentist ✓

🎯 Goal Progress
• 3rd week straight hitting your morning routine - building that habit!

📅 Tomorrow Preview
• Light morning: Just team standup at 10 AM
• Afternoon: Focus time (keep it clear for deep work)

💡 Tonight
No urgent prep needed. Relax and recharge!

📌 Personal
• Dinner reservation at 7 PM (confirmed)

Great work today! Enjoy your evening 🌙
```

### 4. Log Summary
Append to `Diary/YYYY-MM-DD.md`:
```
[18:00] Evening wrap-up sent
Wins: Q1 proposal, 5 PRs reviewed, dentist call
Tomorrow: Light morning, focus afternoon
Mood: Productive day, user should feel accomplished
```

## Edge Cases

**User worked late (after 8 PM)**
- Acknowledge the long day
- Keep it extra brief
- Encourage rest: "Long day - you earned some rest!"

**Unproductive day**
- Be kind and reframing
- Find ANY positive (even small)
- Example: "Sometimes rest days are productive too."
- Don't make user feel guilty

**Major deadline missed**
- Acknowledge it honestly
- Focus on solutions for tomorrow
- Be supportive: "Tough day. Let's regroup tomorrow."

**Weekend**
- Lighter tone, more personal
- Focus on personal goals/activities
- Optional: "Want a weekend wrap or skip tonight?"

**User traveling**
- Adjust for timezone
- Acknowledge travel fatigue
- Keep prep minimal

## Tips

- **Celebrate everything** - Even small wins matter
- **Connect to goals** - Show progress toward bigger picture
- **Be honest but kind** - Don't sugarcoat, but don't judge
- **Permission to rest** - This is closure, not more work
- **Tomorrow is fresh** - End on optimistic note

The goal is for the user to feel:
✅ Accomplished (progress recognized)
✅ Clear on tomorrow (no mental load overnight)
✅ Permission to unwind (work is done)
✅ Connected to goals (daily work has meaning)
