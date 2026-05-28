---
name: pyjiraskill
description: Use the pyjiraskill Jira Cloud CLI via `uv tool run pyjiraskill ...` to list issues/epics/sprints, create issues, transition status, add comments, and emit JSON or tables. Use when a user wants to operate Jira Cloud from the terminal with this CLI.
---

# pyjiraskill

## Overview

Operate Jira Cloud from the terminal using the `pyjiraskill` CLI. Always run the CLI with `uv tool run`.

## Setup

Set required environment variables (no config files):

```bash
export JIRA_URL="https://your-domain.atlassian.net"
export JIRA_EMAIL="you@example.com"
export JIRA_API_TOKEN="your-api-token"
```

## Run commands (always via uv tool)

List open issues in a project:

```bash
uv tool run pyjiraskill issues list --project KEY
```

List open epics in a project:

```bash
uv tool run pyjiraskill epics list --project KEY
```

List open issues in an epic:

```bash
uv tool run pyjiraskill epic issues --epic EPIC-123
```

List open issues in a sprint (Sprint ID is numeric):

```bash
uv tool run pyjiraskill sprint issues --sprint 456
```

Sprint IDs are numeric. You can usually find them in Jira board URLs that include `?sprint=123`,\nor in the sprint report page. When listing sprints, use `sprint list` to see IDs.\n+
List all sprints in a project:

```bash
uv tool run pyjiraskill sprint list --project KEY
```

Filter sprint list by state:

```bash
uv tool run pyjiraskill sprint list --project KEY --state active
```

Get the current sprint for a project:

```bash
uv tool run pyjiraskill sprint current --project KEY
```

If board lookup fails or you have multiple boards, pass a board ID:

```bash
uv tool run pyjiraskill sprint current --project KEY --board 123
```

List issues in the current sprint:

```bash
uv tool run pyjiraskill sprint current-issues --project KEY
```

Create an issue:

```bash
uv tool run pyjiraskill issue add --project KEY --summary "Title" \
  --description "Details" --issuetype Task --parent ABC-1 --assignee user@example.com --labels a,b
```

Transition an issue:

```bash
uv tool run pyjiraskill issue transition --key ABC-123 --to "In Progress"
```

Move an issue to another sprint:

```bash
uv tool run pyjiraskill issue move-sprint --key ABC-123 --from-sprint 10 --to-sprint 12
```

Add a comment:

```bash
uv tool run pyjiraskill issue comment --key ABC-123 --text "Working on this."
```

List open issues assigned to a user:

```bash
uv tool run pyjiraskill issues assigned --user user@example.com
```

## Output and troubleshooting

- Add `--json` to any command for machine-readable output.
- Add `--debug` to show tracebacks on errors.
- If required env vars are missing, the CLI exits non-zero with a clear error.
