---
name: lpend
description: "Fetch the latest reply from Claude storage via the `lpend` CLI. Use only when the user explicitly asks to view the Claude reply/response (e.g. \"看下 Claude 回复/输出\"); do not run proactively after `lask` unless requested."
---

# lpend (Read Claude Reply)

## Quick Start

- `lpend` / `lpend N` (optional override: `lpend --session-file /path/to/.claude-session`)

## Workflow (Mandatory)

1. Run `lpend` (or `lpend N` if the user explicitly asks for N conversations).
2. Return stdout to the user verbatim.
3. If `lpend` exits `2`, report “no reply available” (do not invent output).

## Notes

- Prefer `lping` when the user’s intent is “check Claude is up”.
