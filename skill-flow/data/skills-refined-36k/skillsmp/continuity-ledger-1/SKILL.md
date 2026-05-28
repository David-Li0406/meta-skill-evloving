---
name: continuity-ledger
description: MANDATORY. Maintain context and project state across context window compactions. ALWAYS activate this skill when starting any task, managing project progress, or coordinating between multiple agents. Essential for long-running workflows.
license: MIT
compatibility: opencode 1.0.193
metadata:
  note: Currently it is not possible to read scripts, references, etc. So they're inlined. Later you should eject scipts/init-ledger.sh and LEDGER_FORMAT.md
---

# Continuity Ledger Skill

Maintain a single Continuity Ledger for this workspace in CONTINUITY.md. The ledger is the canonical session briefing designed to survive context compaction; do not rely on earlier chat text unless it’s reflected in the ledger.

## Instructions

### 1. Initialization

When starting a new session or task, check for the existence of `.opencode/CONTINUITY.md` in the project root.

- If the ledger is missing, **create it based on Continuity Ledger Format chapter**.
- Ensure the file is created at the root level of the workspace.

### 2. Format Adherence

When updating or creating the ledger, you **must strictly follow the schema** defined in the reference guide:

- Refer to Continuity Ledger Format chapter for the exact Markdown structure and required sections.
- Do not add top-level headers that are not defined in the specification unless absolutely necessary for the task.

### 3. The "Read-Act-Update" Cycle

For every significant turn or sub-task completion:

- **Read**: Load the current state from the ledger.
- **Act**: Perform the required task (planning, coding, or delegating).
- **Update**: Update the ledger with any new decisions, progress changes (Done/Now/Next), or discovered constraints.

### 4. Compaction Awareness

When you detect that the conversation history is long or has been summarized:

- Rely on the `.opencode/CONTINUITY.md` file as the definitive state.
- Do not trust summarized history for critical technical decisions or project constraints if they conflict with the ledger.
- If you notice missing recall or a compaction/summary event: refresh/rebuild the ledger from visible context, mark gaps in AGENTS.md, ask up to 1–3 targeted questions, then continue.

### 5. Multi-Agent Coordination

- **Orchestrator**: Maintains the master ledger for high-level goals.
- **Sub-agents**: Update specific sections or maintain task-specific sub-ledgers.
- Always include a "Ledger Snapshot" (Goal + Now/Next) when handing off tasks between agents.

### todowrite vs the Ledger

- `todowrite` is for short-term execution scaffolding while you work (a small 3–7 step plan with pending/in_progress/completed).
- CONTINUITY.md is for long-running continuity across compaction (the "what/why/current state"), not a step-by-step task list.
- Keep them consistent: when the plan or state changes, update the ledger at the intent/progress level (not every micro-step).

### In replies

- Begin with a brief "Ledger Snapshot" (Goal + Now/Next + Open Questions). Print the full ledger only when it materially changes or when the user asks.

## Examples

### Updating Following the Format

"Based on LEDGER_FORMAT, I am updating the 'Execution State' section to mark 'Task A' as Done."

# References

## Continuity Ledger Format

The `.opencode/CONTINUITY.md` file must follow this structure. Keep it short and stable: facts only, no transcripts. Prefer bullets. Mark uncertainty as UNCONFIRMED (never guess).

### Project Goal

- **Objective**: [Clear statement of the end goal]
- **Success Criteria**: [List of measurable outcomes]

### Context & Constraints

- **Tech Stack**: [e.g., Python, FastAPI, etc.]
- **Constraints**: [Security requirements, hardware tokens, etc.]

### Key Decisions

- [YYYY-MM-DD]: [Decision] - [Reasoning]

### Execution State

- **Done**:
  - [x] Task 1
- **Now**:
  - [ ] Task 2 (Current focus)
- **Next**:
  - [ ] Task 3

### Open Questions (UNCONFIRMED)

- [ ] Question regarding X...

### Working Set

- **Files**: [List of relevant paths]
- **Commands**: [Last used/useful CLI commands]
