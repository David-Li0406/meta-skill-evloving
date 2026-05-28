---
name: log-session
description: Use this skill to log the current coding session to project memory, capturing accomplishments, decisions, and follow-ups at the end of a session.
---

# Log Session to Memory

Record the current session's work to project memory for future reference.

## The Job

1. Summarize what was accomplished in this session.
2. List files that were modified.
3. Record any decisions made.
4. Note follow-up tasks.
5. Append to `sessions.json`.

## Steps

### 1. Gather Session Info

Review the conversation to identify:
- **Summary**: What was the main goal and outcome?
- **Files Modified**: Which files were created or changed?
- **Decisions Made**: What technical choices were made and why?
- **Follow-ups**: What remains to be done?

### 2. Create Session Entry

Add an entry to `sessions.json` using the following format:

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

Read `~/aiconfig/memory/projects/{project}/sessions.json`, append the new session entry, and write back.

### 4. Record Architectural Decisions (if any)

If significant architectural decisions were made, also add to `decisions.json` using the following format:

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

### 5. Update Project Context

If significant changes were made, also update `context.json`:
- Update `current_focus` if it changed.
- Add to `known_issues` if bugs were discovered.
- Update `active_branches` if branch changed.

## Output

After logging, the output should indicate:

```
Session logged to: ~/aiconfig/memory/projects/{project}/sessions.json

Recorded:
- Summary: {brief summary}
- Files: {count} modified
- Decisions: {count} recorded
- Follow-ups: {count} tasks
```

## Checklist

- [ ] Identified project name
- [ ] Summarized session accomplishments
- [ ] Listed all modified files
- [ ] Recorded decisions with rationale
- [ ] Noted follow-up tasks
- [ ] Updated context.json if needed
- [ ] Added ADRs for major decisions