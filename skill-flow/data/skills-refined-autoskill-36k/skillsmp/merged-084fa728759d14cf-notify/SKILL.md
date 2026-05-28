---
name: notify
description: Use this skill to send push notifications via ntfy.sh for completed tasks, errors, or important events.
---

# Notify Skill

Send push notifications when user attention is needed, such as for completed tasks, errors, or any important events.

## Usage

Use this skill when:

- A long-running task has completed
- An error or issue needs attention
- The user explicitly asks to be notified
- Any event that warrants alerting the user

## How to Send Notifications

Execute the following command with an appropriate message:

```bash
echo '{"title": "<TITLE>", "message": "<MESSAGE>"}' | .claude/scripts/notify
```

or, for fish shell:

```bash
fish -c 'curl -d "<MESSAGE>" "ntfy.sh/$NTFY_SUB_TOPIC"'
```

Replace `<TITLE>` and `<MESSAGE>` with a concise, descriptive message about the event. Note that `$NTFY_SUB_TOPIC` is a private fish shell variable.

## Input

- `title` - optional
- `message` - required

## Message Guidelines

- Keep messages short and actionable (under 100 characters when possible)
- Include relevant context (e.g., task name, file, error type)
- Use clear language

## Output

```json
{"success": true, "status": 200}
{"success": false, "status": 401, "error": "..."}
```

## Example Messages

- "Build completed successfully"
- "Tests passed: 42/42"
- "Error: TypeScript compilation failed in src/index.ts"
- "PR #123 is ready for review"
- "Task complete: Database migration finished"