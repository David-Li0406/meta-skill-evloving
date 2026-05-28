---
name: kamal-production-console
description: Use when you need to open a production console or inspect production logs via Kamal for this Micelio app.
---

# Kamal production console + logs

Use this skill when the user asks how to open a production console or check logs.

## Prerequisite

- Load environment secrets before any Kamal command:

```bash
source .env
```

## Open a production console

- Start an interactive shell in the app container, then launch the release console:

```bash
source .env && kamal app exec --interactive "bin/micelio remote"
```

If the release script location differs, list the container filesystem and adjust the path before retrying.

## Tail production logs

- Stream application logs:

```bash
source .env && kamal app logs --follow
```

Use `--since` or `--lines` to narrow the output when needed.
