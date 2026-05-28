# Manus Task Orchestration (2026)

Manus AI excels at long-horizon, multi-step tasks. Effective orchestration requires understanding the logical flow of autonomous missions.

## 1. Defining Clear Objectives

Agents need high-level goals, not micro-instructions.
-   **Bad**: "Go to google.com, search for Apple stock, copy the price, put it in a sheet."
-   **Good**: "Research the current stock performance of Apple and generate a one-page investment summary PDF."

## 2. Multi-Step Execution Flow

Manus follows an internal loop:
1.  **Goal Analysis**: Deconstructing the user request into sub-tasks.
2.  **Tool Selection**: Identifying needed connectors (Search, File, Browser).
3.  **Iterative Execution**: Browsing, extracting, and synthesizing.
4.  **Refinement**: Reviewing its own output against the objective.

## 3. Asynchronous Workflow

Missions can take minutes or hours.
-   **Standard**: Use `POST /v1/tasks` to initiate.
-   **Notification**: Subscribe to the `task.completed` webhook.
-   **Payload**: Retrieve results from `GET /v1/tasks/{id}/result`.

## 4. Logical Timeouts

Never let a mission run indefinitely.
-   **Pattern**: If a mission hasn't transitioned from `running` in 30 minutes, trigger an application-level alert.

## 5. Metadata for Agent Intelligence

Provide `context_metadata` during task creation to give the agent project-specific facts (e.g., brand guidelines, target audience).

---
*Updated: January 22, 2026 - 21:10*
