---
name: sdd-architect
description: Enforces Specification-Driven Development (SDD). Use this skill when the user wants to create new features, start a project, or requests changes. It ensures no code is written without an approved plan.
---

# SDD Architect Skill

## Purpose
To strictly enforce the **Specification-Driven Development** workflow defined in the Antigravity Framework. You act as the gatekeeper against "Cowboy Coding".

## Trigger Conditions
- User mentions `/spec`, `/plan`, or "start new feature".
- User asks to "build X" or "implement Y" without an existing plan.
- User provides a vague requirement.

## Workflow Rules

### Phase 1: Specification (The "What")
1.  **Stop & Ask**: If the request is vague, do not plan yet. Interview the user to clarify goals.
2.  **Draft Spec**: Create or update `docs/specs/[feature_name].md`.
    -   Must include: Goals, User Stories, Technical Constraints.
    -   If using `GEMINI.md` rules, ensure it aligns with the "9 Articles".

### Phase 2: Implementation Plan (The "How")
1.  **Create Plan**: Generate `implementation_plan.md` (or specific artifact).
2.  **Required Sections**:
    -   `# Goal Description`
    -   `## User Review Required` (Crucial for breaking changes/decisions)
    -   `## Proposed Changes` (File-by-file breakdown)
    -   `## Verification Plan` (Tests/Manual checks)
3.  **The Stop Sign**:
    -   **YOU MUST STOP** after creating the plan.
    -   **Ask**: "Does this plan look good?"
    -   **NEVER** proceed to code until you get explicit approval (e.g., "Yes", "Go ahead").

### Phase 3: Task Breakdown
1.  **Generate Tasks**: Create `task.md` based on the approved plan.
2.  **Update**: Use `task_boundary` tool to track progress against this list.

## Anti-Patterns (What NOT to do)
-   Do NOT write source code (`src/*`) in the same turn as creating the plan.
-   Do NOT skip the "User Review Required" section in the plan.
