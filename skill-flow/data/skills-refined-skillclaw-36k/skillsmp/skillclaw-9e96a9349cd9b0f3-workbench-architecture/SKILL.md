---
name: workbench-architecture
description: Use this skill when documenting system design, decisions, tradeoffs, or rationale that must be tracked over time using the Workbench CLI.
---

# Skill body

## Key settings

- `.workbench/config.json`: paths.docsRoot, git.defaultBaseBranch.
- Use `workbench config show --format json` to confirm defaults.

## Core workflows

1. **Planning phase**: Create architecture docs for design intent and scope.
2. **Decision making**: When a decision is made or changes occur, create or update an Architecture Decision Record (ADR).
3. **Linking**: Link ADRs and architecture docs to work items and specifications.

## Commands

- **Create an architecture doc**:
    ```bash
    workbench doc new --type doc --title "Subsystem overview" --path docs/20-architecture/subsystem-overview.md --work-item TASK-0001
    ```

- **Create an ADR**:
    ```bash
    workbench doc new --type adr --title "Decision title" --path docs/40-decisions/ADR-YYYY-MM-DD-title.md --work-item TASK-0001
    ```

- **Link existing docs to a work item**:
    ```bash
    workbench item link TASK-0001 --spec /docs/10-product/spec.md --adr /docs/40-decisions/ADR-YYYY-MM-DD-title.md
    ```

- **Sync backlinks**:
    ```bash
    workbench doc sync --all
    ```

## Output

- Architecture docs and ADRs with consistent front matter.
- Work items that reference related specifications and ADRs.

## Guardrails

- Use ADRs for decisions and architecture docs for structure and flows.
- Keep ADR status updated (proposed, accepted, superseded, deprecated).
- If an ADR does not exist for a significant decision, create one.