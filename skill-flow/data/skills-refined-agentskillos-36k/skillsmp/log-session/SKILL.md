---
name: log-session
description: "Log the current coding session to project memory. Use at the end of a session to record accomplishments, decisions, and follow-ups. Triggers on: log this session, save session, end session, record what we did."
---

# Session Logger

Record the current coding session to project memory for future context.

---

## The Job

1. Summarize what was accomplished in this session
2. Record files modified and decisions made
3. Note any follow-up tasks
4. Save to `~/aiconfig/memory/projects/{project}/sessions.json`

---

## Step 1: Gather Session Info

Review the conversation to identify:

- **Summary**: What was the main goal and outcome?
- **Files Modified**: Which files were created/changed?
- **Decisions Made**: What technical choices were made and why?
- **Follow-ups**: What remains to be done?

---

## Step 2: Determine Project Name

Ask if unclear:

```
Which project should I log this session to?
```

Or infer from:
- Current working directory name
- Package.json name
- Git remote name

---

## Step 3: Session Log Format

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
  "duration_estimate": "~30min",
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

---

## Step 4: Update Project Context

If significant changes were made, also update `context.json`:

- Update `current_focus` if it changed
- Add to `known_issues` if bugs were discovered
- Update `active_branches` if branch changed

---

## Step 5: Record Architectural Decisions

If major technical decisions were made, add to `decisions.json`:

```json
{
  "id": "ADR-001",
  "date": "2025-01-18",
  "title": "Use JWT for authentication",
  "context": "Need stateless auth for API that scales horizontally",
  "decision": "Use JWT with short-lived access tokens and refresh tokens",
  "rationale": "Stateless, scalable, industry standard",
  "alternatives_considered": ["Session cookies", "OAuth only", "API keys"],
  "consequences": [
    "Need secure token storage on client",
    "Must implement refresh flow",
    "Tokens cannot be invalidated without blacklist"
  ],
  "status": "accepted"
}
```

---

## Output

After logging:

```
Session logged to: ~/aiconfig/memory/projects/{project}/sessions.json

Recorded:
- Summary: {brief summary}
- Files: {count} modified
- Decisions: {count} recorded
- Follow-ups: {count} tasks

Next session hint: {context_for_next_session}
```

---

## Checklist

- [ ] Identified project name
- [ ] Summarized session accomplishments
- [ ] Listed all modified files
- [ ] Recorded decisions with rationale
- [ ] Noted follow-up tasks
- [ ] Updated context.json if needed
- [ ] Added ADRs for major decisions
