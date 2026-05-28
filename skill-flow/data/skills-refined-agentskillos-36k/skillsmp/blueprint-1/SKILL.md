---
name: blueprint
description: Standardized workflow for managing technical blueprints in the .blueprints/ directory.
---

# Blueprint Skill

Use this skill when the user explicitly requests a "Blueprint" workflow (e.g., via `/blueprint`).

## Workflow Rules

1. **Source of Truth**: All formal blueprints live in the `.blueprints/` directory.
2. **Delegation**: Do not edit `.blueprints/` files directly. Always delegate to the `@blueprint-manager` subagent using the `Task` tool.
3. **Idea Integrity**: The **Idea** section of a blueprint is immutable once the status moves past `capture`.
4. **Lifecycle**:
   - `capture`: Use `@blueprint-manager` to record initial notes.
   - `planning`: Use the Plan agent to architect, then delegate to `@blueprint-manager` to document the strategy and execution steps.
    - `executing`: Use the Build agent to implement and delegate checklist updates to `@blueprint-manager`. Before completion, run `/review` to ensure quality.
    - `completed`: Use `@blueprint-manager` to finalize the implementation summary and record the review findings.


## Session Protocol
Once this skill is loaded, you must proactively suggest using `@blueprint-manager` for any non-trivial tasks. Ensure all architectural decisions are documented before implementation begins.
