---
name: speckit-tasks
description: Use this skill when the implementation plan is ready and you need a dependency-ordered task list based on available design artifacts.
---

# Skill body

## Inputs
- Required: `specs/<feature>/plan.md` and `specs/<feature>/spec.md`
- Optional: `data-model.md`, `contracts/`, `research.md`, `quickstart.md`
- Any user constraints or priorities from the request

## Workflow

1. **Setup**: Run the following command from the repo root to check prerequisites:
   ```bash
   .specify/scripts/bash/check-prerequisites.sh --json
   ```
   Parse `FEATURE_DIR` and `AVAILABLE_DOCS` list. Ensure all paths are absolute. For single quotes in arguments (e.g., "I'm Groot"), use escape syntax: e.g., 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from `FEATURE_DIR`:
   - **Required**: 
     - `plan.md` (tech stack, libraries, structure)
     - `spec.md` (user stories with priorities)
   - **Optional**: 
     - `data-model.md` (entities)
     - `contracts/` (API endpoints)
     - `research.md` (decisions)
     - `quickstart.md` (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Execute task generation workflow**:
   - Load `plan.md` and extract tech stack, libraries, project structure.
   - Load `spec.md` and extract user stories with their priorities (P1, P2, P3, etc.).
   - If `data-model.md` exists, extract entities and map them to user stories.
   - If `contracts/` exists, map endpoints to user stories.
   - If `research.md` exists, extract decisions for setup tasks.
   - Generate tasks organized by user story (see Task Generation Rules below).
   - Generate a dependency graph showing user story completion order.
   - Create parallel execution examples per user story.
   - Validate task completeness (each user story has all needed tasks, independently testable).

4. **Generate tasks.md**: Use `.specify/templates/tasks-template.md` as structure, filling it with:
   - Correct feature name from `plan.md`.
   - Phase 1: Setup tasks (project initialization).
   - Phase 2: Foundational tasks (blocking prerequisites for all user stories).
   - Phase 3+: One phase per user story (in priority order from `spec.md`).
   - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks.
   - Final Phase: Polish & cross-cutting concerns.
   - All tasks must follow the strict checklist format (see Task Generation Rules below).