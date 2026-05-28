---
name: log-session
description: Use this skill at the end of a coding session to log accomplishments, decisions, and follow-up tasks to project memory.
---

# Skill body

## The Job

1. Summarize what was accomplished in this session.
2. Record files modified and decisions made.
3. Note any follow-up tasks.
4. Save to `~/aiconfig/memory/projects/{project}/sessions.json`.

## Step 1: Gather Session Info

Review the conversation to identify:

- **Summary**: What was the main goal and outcome?
- **Files Modified**: Which files were created/changed?
- **Decisions Made**: What technical choices were made and why?
- **Follow-ups**: What remains to be done?

## Step 2: Determine Project Name

Ask if unclear:

```
Which project should I log this session to?
```

Or infer from:
- Current working directory name
- Package.json name
- Git remote name

## Step 3: Create Session Entry

Add entry to `sessions.json` using atomic writes to prevent corruption:

```bash
# Use atomic write for safe file updates
~/aiconfig/scripts/atomic-write.sh ~/aiconfig/memory/projects/{project}/sessions.json --backup
```

Session entry format:

```json
{
  "id": "session-YYYYMMDD-HHMMSS",
  "date": "2025-01-18",
  "client": "claude-code",
  "summary": "Implemented user authentication with JWT tokens",
  "files_modified": [
    "src/auth/jwt.ts",
    "src/middleware/auth.ts",
    "src/routes/login.ts"
  ],
  "decisions_made": [
    {
      "decision": "Used jose library for JWT",
      "rationale": "Type-safe, well-maintained, no native dependencies"
    },
    {
      "decision": "15-minute access token expiry",
      "rationale": "Balance security with UX, refresh tokens handle longer sessions"
    }
  ],
  "follow_up": [
    "Add refresh token rotation",
    "Implement logout endpoint",
    "Add rate limiting to login"
  ],
  "tags": ["auth", "security", "feature"],
  "context_for_next_session": "Auth middleware is complete. Next session should focus on refresh token logic in src/auth/refresh.ts"
}
```

## Step 4: Update Project Context

If significant changes were made, also update `context.json`:

- Update `current_focus` if it changed.
- Add to `known_issues` if bugs were discovered.
- Update `active_branches` if branch changed.

## Step 5: Record Architectural Decisions (if any)

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

## Checklist

- [ ] Reviewed session accomplishments.
- [ ] Listed modified files.
- [ ] Captured decisions made.
- [ ] Noted follow-up tasks.
- [ ] Appended to sessions.json.
- [ ] Added ADRs to decisions.json (if applicable).