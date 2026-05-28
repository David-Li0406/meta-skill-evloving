---
name: adr-manager
description: Manage Architecture Decision Records (ADR). Use this when a change impacts the project's long-term structure, data flow, or security posture.
---

# ADR Manager Protocol

## When to load this skill
- Introducing a new library or framework (e.g., Pydantic AI).
- Modifying the database schema or storage engine.
- Changing the communication protocol between agents.

## Instructions
1. **Search**: Look for existing ADRs in `docs/architecture/adr/`.
2. **Propose**: If a decision is new, generate a filename using the format `NNNN-short-description.md` (e.g., `0005-use-devdb-mcp.md`).
3. **Template**: Use the template found at `./templates/madr-v3.md`.
4. **Drafting**: Ensure the 'Context', 'Decision Drivers', and 'Consequences' sections are fully populated based on the current conversation.

## Definition of Done
- The ADR is written to `docs/architecture/adr/`.
- The user has explicitly approved the "Consequences" section.
