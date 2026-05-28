---
name: goal-check
description: Weekly review of long-term goals with progress assessment and action suggestions. Manual-only skill invoked with /goal-check. Use for weekly reviews, quarterly planning, when user asks 'how am I doing on my goals', or goal check-ins.
disable-model-invocation: true
user-invocable: true
---

# Goal Check

Conduct a comprehensive review of the user's long-term goals with progress assessment and actionable next steps.

## When to Use

This is a **manual-only skill**. User must explicitly invoke with `/goal-check`.

**Typical use cases:**
- 📅 Weekly goal reviews (Sunday evenings, Friday afternoons)
- 📊 Monthly/quarterly check-ins
- 🎯 User asks "How am I doing on my goals?"
- 🔄 Major life transitions (new job, new year, post-vacation)
- 🤔 User feels stuck or unmotivated

## Workflow

### 1. Read All Goals

Read `Goals/Goals.md` thoroughly:
- Identify all active goals
- Note status of each (not started, in progress, completed, paused)
- Understand timeframes (short-term, long-term, no deadline)
- Look for connections between goals

### 2. Gather Evidence from Diary

Scan `Diary/` entries from the past week (or month if monthly review):
- Look for activities related to each goal
- Find wins, progress, setbacks
- Identify patterns (consistent work, procrastination, blockers)
- Note user's energy/mood during goal-related activities

**Search for tags:**
- `[GOAL]` - Explicit goal mentions
- `[TASK]` - Completed tasks that advance goals
- `[DECISION]` - Decisions affecting goals
- Goal keywords (workout, code, write, etc.)

### 3. Assess Each Goal

For each active goal, determine:

**Progress Status:**
- 🚀 **Ahead** - Exceeding expectations, faster than planned
- ✅ **On Track** - Steady progress, meeting milestones
- ⚠️ **Behind** - Slower than expected, missing milestones
- 🔴 **Stalled** - No progress in 2+ weeks
- ❓ **Unclear** - Can't assess (need metrics/milestones)

**Evidence:**
- What specific actions were taken this week?
- Quantify if possible (e.g., "3 workouts", "2 chapters written")
- Compare to previous week/month

**Blockers (if any):**
- What's preventing progress?
- Is it internal (motivation, energy) or external (resources, time)?
- Is it temporary or systemic?

### 4. Build the Review Report

Structure with: Overall Progress → Individual Goal Reviews → Wins → Patterns → Recommended Focus → Suggested Adjustments

**Deliver as**: Detailed but scannable, 500-800 words, honest but supportive

### 5. Update Goals File & Log

- Update `Goals/Goals.md` if status changed
- Append review to `Diary/YYYY-MM-DD.md` with `[GOAL-CHECK]` tag

The goal is for the user to feel:
✅ Clear on progress (honest assessment)
✅ Motivated (wins celebrated, path forward clear)
✅ Supported (you see their effort)
✅ Accountable (data doesn't lie, but you're not judging)