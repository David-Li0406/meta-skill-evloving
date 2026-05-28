---
name: dping
description: "Test connectivity with Droid via the `dping` CLI. Use when the user explicitly asks to check Droid status/connection (e.g. \"d ping\", \"Droid 连上没\"), or when troubleshooting Droid not responding."
---

# dping (Ping Droid)

## Workflow (Mandatory)

1. Run `dping` (no extra analysis or follow-up actions).
2. Return stdout to the user.

## Notes

- If `dping` fails, ensure it runs in the same environment as `ccb` (WSL vs native Windows).
