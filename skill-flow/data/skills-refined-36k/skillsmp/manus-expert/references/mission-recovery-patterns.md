# Mission Recovery Patterns (2026)

Autonomous missions can fail due to network glitches, rate limits, or unpredicted UI changes. Recovery patterns ensure data isn't lost.

## 1. Checkpointing

For long missions, Manus provides internal "Checkpoints."
-   **Pattern**: Save the `mission_state_hash` in your local DB after every major step.

## 2. Automatic Retries

Implement exponential backoff for transient API errors (e.g., 502, 503, 429).
-   *Limit*: Maximum 3 retries before escalating to human intervention.

## 3. Human-in-the-Loop (HITL) Handoff

If an agent is blocked (e.g., encountered an unknown MFA screen):
1.  **State**: Mission transitions to `task_stopped` with `reason: human_input_needed`.
2.  **Alert**: Application notifies the user.
3.  **Resume**: User provides input; mission resumes with `PUT /v1/tasks/{id}/resume`.

## 4. State Rehydration

If your server crashes, re-sync with Manus using the `taskId`.
-   **Sync**: `GET /v1/tasks/{id}` to find current status.

## 5. Idempotent Result Handling

Ensure your system can handle receiving the same `task.completed` webhook multiple times without duplicate data entries.

---
*Updated: January 22, 2026 - 21:10*
