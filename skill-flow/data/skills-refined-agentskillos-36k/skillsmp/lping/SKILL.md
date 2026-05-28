---
name: lping
description: "Test connectivity with Claude via the `lping` CLI. Use when the user explicitly asks to check Claude status/connection (e.g. \"l ping\", \"Claude alive?\"), or when troubleshooting Claude not responding."
---

# lping (Ping Claude)

## Workflow (Mandatory)

1. Run `lping` (no extra analysis or follow-up actions).
2. Return stdout to the user.

## Notes

- If `lping` fails, ensure it runs in the same environment as `ccb` (WSL vs native Windows).
