---
name: dx-alerts
description: Lightweight “news wire” implemented **via Agent Mail threads**, not a separate bespoke system.
---

# dx-alerts

Lightweight “news wire” implemented **via Agent Mail threads**, not a separate bespoke system.

Pattern:
- Publish alerts into an Agent Mail thread id: `dx-alerts`
- Each alert message should start with a tag:
  - `[DX-ALERT][blocker] ...`
  - `[DX-ALERT][high] ...`
  - `[DX-ALERT][medium] ...`
  - `[DX-ALERT][low] ...`
- Include repo scope in the body (prime-radiant-ai / affordabot / llm-common) and an expiry if relevant.

Consumption:
- `dx-doctor` should optionally surface the latest N `dx-alerts` messages (best-effort; never block).

Why:
- Avoids “agents don’t pull agent-skills” problems by pushing time-sensitive info into a mailbox.

