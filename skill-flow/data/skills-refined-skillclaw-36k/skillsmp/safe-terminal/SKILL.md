---
name: safe-terminal
description: Use whenever proposing terminal commands. Prevents destructive actions and requires approval gates.
---

Rules:
- Never run commands automatically.
- Never include destructive commands.
- Always output:
  1) Purpose
  2) Exact command
  3) Why safe
  4) Expected output
  5) Rollback/undo if applicable
