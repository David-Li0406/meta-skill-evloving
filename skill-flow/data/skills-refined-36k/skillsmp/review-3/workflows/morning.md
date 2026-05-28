# Morning Routine

Start the day with intention.

## Steps

### 1. Review Yesterday

Check if there's a note from yesterday:
```bash
cat "Daily/$(date -v-1d +%Y-%m-%d). Morning Check-in.md" 2>/dev/null
```

Briefly summarize what happened yesterday.

### 2. Check Projects

Read active projects:
```bash
for f in Projects/*.md; do
  echo "=== $(basename "$f" .md) ==="
  head -15 "$f"
done
```

Present: "You have X active projects: [list]"

### 3. Check Tasks

```bash
curl -s "http://127.0.0.1:8090/api/tasks?status=in-progress"
```

Show what's already in progress.

### 4. Morning Check-in

Ask:
- How are you feeling? (mood, energy 1-10)
- How did you sleep?
- What's your main focus today?

### 5. Create Morning Note

Create `Daily/YYYY-MM-DD. Morning Check-in.md` using template:
`templates/morning-checkin.md`

Fill in their answers.

### 6. Plan the Day

Based on energy and projects, suggest 1-3 tasks for today.

Ask: "Should I create these tasks?"

If yes:
```bash
curl -X POST "http://127.0.0.1:8090/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Task title", "status": "next-up", "priority": "high"}'
```

### 7. Wrap Up

> "Morning complete! Focus today: [main focus]"
> "Have a great day!"
