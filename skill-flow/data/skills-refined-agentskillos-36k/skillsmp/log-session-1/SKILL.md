---
name: log-session
description: "Log the current coding session to project memory. Use at the end of a session to record accomplishments, decisions, and follow-ups. Triggers on: log this session, save session, end session, record what we did."
---

# Log Session to Memory

Record the current session's work to project memory.

---

## The Job

1. Summarize what was accomplished this session
2. List files that were modified
3. Record any decisions made
4. Note follow-up tasks
5. Append to sessions.json

---

## Steps

### 1. Gather Session Info

Review the conversation and identify:
- Main accomplishments
- Files created or modified
- Technical decisions made
- Outstanding tasks or follow-ups

### 2. Create Session Entry

```json
{
  "id": "session-{YYYYMMDD}-{HHMMSS}",
  "date": "{YYYY-MM-DD}",
  "client": "cursor",
  "summary": "Brief description of what was accomplished",
  "files_modified": [
    "path/to/file1.ts",
    "path/to/file2.ts"
  ],
  "decisions_made": [
    "Used X library for Y reason",
    "Chose approach A over B because..."
  ],
  "follow_up": [
    "Add tests for new feature",
    "Refactor X when time permits"
  ],
  "tags": ["feature", "auth", "refactor"]
}
```

### 3. Append to sessions.json

Read `~/aiconfig/memory/projects/{project}/sessions.json`, append new session, write back.

### 4. Record Architectural Decisions (if any)

If significant architectural decisions were made, also add to `decisions.json`:

```json
{
  "id": "decision-{YYYYMMDD}-{NNN}",
  "date": "{YYYY-MM-DD}",
  "title": "Decision title",
  "context": "Why this decision was needed",
  "decision": "What was decided",
  "rationale": "Why this approach was chosen",
  "alternatives_considered": ["Option B", "Option C"],
  "status": "accepted"
}
```

---

## Output

```
Session logged to memory.

Summary: {summary}

Files modified:
- {file1}
- {file2}

Decisions recorded:
- {decision1}

Follow-up tasks:
- {task1}
- {task2}

Location: ~/aiconfig/memory/projects/{project}/sessions.json
```

---

## Checklist

- [ ] Reviewed session accomplishments
- [ ] Listed modified files
- [ ] Captured decisions made
- [ ] Noted follow-up tasks
- [ ] Appended to sessions.json
- [ ] Added ADRs to decisions.json (if applicable)
