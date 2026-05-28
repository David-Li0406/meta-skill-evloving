# Evening Routine

End the day with reflection.

## Steps

### 1. Review Today's Tasks

```bash
curl -s "http://127.0.0.1:8090/api/tasks"
```

What got done? What didn't?

### 2. Check Morning Intentions

Read this morning's check-in:
```bash
cat "Daily/$(date +%Y-%m-%d). Morning Check-in.md" 2>/dev/null
```

Did they accomplish their main focus?

### 3. Evening Reflection

Ask:
- What did you accomplish today?
- What's one thing you learned?
- What's your priority for tomorrow?

### 4. Create Evening Note

Create `Daily/YYYY-MM-DD. Evening Check-in.md` using template:
`templates/evening-checkin.md`

Fill in their answers.

### 5. Wrap Up

> "Good work today. Rest well!"
