---
name: agent-browser-cookies
description: This skill should be used when exporting, storing, or reapplying agent-browser cookies across sessions, especially for localhost login states.
---

# Agent Browser Cookie Manager

Use this skill to export cookies from an agent-browser session, store them under this skill’s folder, and reapply them to another session.

## What This Skill Provides

- Deterministic export of cookies to `assets/cookies/`
- Reapplication of cookies to another session (with optional base URL)
- Safe filtering by domain when reapplying

## Files and Locations

- Exported cookies live in `assets/cookies/` as JSON files.
- Use `scripts/export_cookies.py` and `scripts/import_cookies.py`.

## Workflow

### Export cookies from a session

1) Ensure the session you want to export from is active.
2) Run:
   ```bash
   python /Users/jace/.codex/skills/agent-browser-cookies/scripts/export_cookies.py \
     --session default \
     --name default-localhost
   ```
3) Verify output file in:
   ```
   /Users/jace/.codex/skills/agent-browser-cookies/assets/cookies/default-localhost.local.json
   ```

### Import cookies into a different session

1) Decide the base URL (origin) the cookies should apply to, e.g. `http://localhost:3208`.
2) Run:
   ```bash
   python /Users/jace/.codex/skills/agent-browser-cookies/scripts/import_cookies.py \
     --session test-cookie \
    --file /Users/jace/.codex/skills/agent-browser-cookies/assets/cookies/default-localhost.local.json \
    --base-url http://localhost:3208
   ```
3) Open the target page in that session and verify login state.

## Notes and Constraints

- `agent-browser cookies set` only sets name/value for the current origin.
- The import script filters cookies to the base URL host and applies them after opening that URL.
- If login still fails, cookies may be missing attributes; re-login manually and re-export.
- Cookie files are stored as `*.local.json` and are ignored by `assets/cookies/.gitignore`.
