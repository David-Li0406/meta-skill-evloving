---
name: cping
description: "Test connectivity with Codex via the `cping` CLI. Use when the user explicitly asks to check Codex status/connection (e.g. \"codex ping\", \"Codex 连上没\"), or when troubleshooting Codex not responding."
---

# cping (Ping Codex)

## Workflow (Mandatory)

1. Run `cping` (no extra analysis or follow-up actions).
2. Return stdout to the user.

## Notes

- If `cping` fails, ensure it runs in the same environment as `ccb` (WSL vs native Windows).
