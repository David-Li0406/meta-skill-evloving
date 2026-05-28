---
name: cpend
description: "Fetch the latest reply from Codex via the `cpend` CLI. Use only when the user explicitly asks to view the Codex reply/response (e.g. \"看下 codex 回复/输出\"); do not run proactively after `cask` unless requested."
---

# cpend (Read Codex Reply)

## Quick Start

- `cpend` / `cpend N` (optional override: `cpend --session-file /path/to/.codex-session`)

## Workflow (Mandatory)

1. Run `cpend` (or `cpend N` if the user explicitly asks for N conversations).
2. Return stdout to the user verbatim.
3. If `cpend` exits `2`, report "no reply available" (do not invent output).

## Notes

- Prefer `cping` when the user's intent is "check Codex is up".
