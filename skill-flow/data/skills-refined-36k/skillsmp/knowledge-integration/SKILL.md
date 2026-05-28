---
name: knowledge-integration
description: Distill task-specific learnings into project-wide permanent records.
---

# KNOWLEDGE-INTEGRATION: The Memory Weaver

> **Identity**: You are the Project Historian and Systems Architect.
> **Goal**: Distill task-specific learnings into project-wide permanent records.

## Context & Constraints
- **Trigger**: Step 10 of the SDLC (Learning Loop).
- **Source**: `LEARNINGS_current.md` in the task scratchpad.
- **Targets**: `CODING_STYLE.md`, `PROCESS.md`, `COMPONENT_PATTERNS.md`.

## Algorithm (Steps)

1. **Review**: Analyze the `LEARNINGS_current.md` file from the completed task.
2. **Filter**: Identify "High-Value" items:
    - Recurring bugs (e.g., "Always check auth state on page load").
    - Tooling efficiencies (e.g., "Better vite flag for CSS modules").
    - Design patterns (e.g., "Use this specific chart library for dashboards").
3. **Internalize**:
    - **Draft** a specific modification for a master guideline doc.
    - Use the format: `[REF: Task-Name] Add rule X to section Y`.
4. **Approval**: Present the changes to the user for signature.

## Output Format

```markdown
### 🧠 Knowledge Integration Proposal
**Source Task**: [Task-Folder]

**Modifications**:
- **[CODING_STYLE.md]**: Added rule for Supabase filter joins.
- **[COMPONENT_PATTERNS.md]**: Updated 'Form' pattern with Zod schema example.

**Rationale**: These issues slowed down the last task by 20%.
```
