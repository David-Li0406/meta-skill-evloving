# Text Entry Handler

Process plain text log entries and short voice memos into capture notes.

## Detection

**Pattern:** `- [time] - [text]` (no 🎤 or URL)
**Or:** `- [time] - 🎤 [short text]` (< 200 words)

## Entry Classification

### Reminder/Task Signals → Capture with Task

Look for these patterns:
- "remind me to..."
- "don't forget..."
- "remember to..."
- "I need to..."
- "tomorrow I should..."
- "should probably..."
- "have to..."

Create capture note with Obsidian Tasks checkbox.

### Thought/Idea → Capture Note

General thoughts, ideas, observations without task signals.

Create capture note with `source: thought`.

### Noise → Delete

Filler entries, incomplete thoughts, audio artifacts.

Just delete from daily note, don't create a note.

## Note Creation

**For reminders/tasks:**

```
para_create({
  template: "capture",
  title: "Take out the trash",
  dest: "00 Inbox",
  args: {},
  content: {
    "Capture": "- [ ] Take out the trash 🔔 2026-01-06 22:00"
  },
  response_format: "json"
})
```

```
para_frontmatter_set({
  file: "00 Inbox/📥 Take out the trash.md",
  set: {
    source: "reminder",
    resonance: "useful",
    urgency: "high"
  }
})
```

**For thoughts/ideas:**

```
para_create({
  template: "capture",
  title: "Tomorrow is a new day",
  dest: "00 Inbox",
  args: {},
  content: {
    "Capture": "Don't forget tomorrow is a new day."
  },
  response_format: "json"
})
```

```
para_frontmatter_set({
  file: "00 Inbox/📥 Tomorrow is a new day.md",
  set: {
    source: "thought",
    resonance: "inspiring",
    urgency: "low"
  }
})
```

**CRITICAL:** The capture template uses `## Capture` heading. Always use `"Capture"` as the content key.

## Task Emoji Format (Obsidian Tasks)

| Emoji | Meaning |
|-------|---------|
| `📅` | Due date |
| `🔔` | Reminder/scheduled |
| `⏳` | Scheduled date |
| `🔁` | Recurring |

Example: `- [ ] Call dentist 📅 2026-01-10`

## Template Output

**Reminder:**
```markdown
---
type: capture
status: inbox
source: reminder
resonance: useful
urgency: high
template_version: 1
---

# Take out the trash

## Capture

- [ ] Take out the trash 🔔 2026-01-06 22:00

## Why I Saved This

From daily log on [[2026-01-06]]
```

**Thought:**
```markdown
---
type: capture
status: inbox
source: thought
resonance: inspiring
urgency: low
template_version: 1
---

# Tomorrow is a new day

## Capture

Don't forget tomorrow is a new day.

## Why I Saved This

From daily log on [[2026-01-06]]
```
