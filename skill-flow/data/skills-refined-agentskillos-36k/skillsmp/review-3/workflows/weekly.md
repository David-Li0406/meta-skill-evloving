# Weekly Review

Reflect on the week and plan ahead.

## Steps

### 1. Review the Week

Read all daily notes from this week:
```bash
ls -t Daily/*.md | head -7
```

Summarize:
- What went well?
- What didn't?
- Patterns in mood/energy?

### 2. Project Progress

For each project, check:
- What moved forward?
- What's stuck?
- Any deadlines coming up?

### 3. Task Review

```bash
curl -s "http://127.0.0.1:8090/api/tasks?status=done"
```

Celebrate completions.

### 4. Weekly Reflection

Ask:
- What was your biggest win this week?
- What would you do differently?
- What's your main focus for next week?

### 5. Create Weekly Note

Create `Daily/YYYY-MM-DD. Weekly Review.md` using template:
`templates/weekly-review.md`

### 6. Plan Next Week

Based on projects and reflection:
- What are the 3 most important things for next week?
- Any deadlines to be aware of?

> "Week reviewed. Main focus next week: [focus]"
