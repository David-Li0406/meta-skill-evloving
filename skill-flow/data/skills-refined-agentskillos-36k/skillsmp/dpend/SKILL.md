---
name: dpend
description: "Fetch the latest reply from Droid via the `dpend` CLI. Use only when the user explicitly asks to view the Droid reply/response (e.g. \"看下 d 回复/输出\"); do not run proactively after `dask` unless requested."
---

# dpend (Read Droid Reply)

## Quick Start

- `dpend` / `dpend N` (optional override: `dpend --session-file /path/to/.droid-session`)

## Workflow (Mandatory)

1. Run `dpend` (or `dpend N` if the user explicitly asks for N conversations).
2. Return stdout to the user verbatim.
3. If `dpend` exits `2`, report “no reply available” (do not invent output).

## Notes

- Prefer `dping` when the user’s intent is “check Droid is up”.
