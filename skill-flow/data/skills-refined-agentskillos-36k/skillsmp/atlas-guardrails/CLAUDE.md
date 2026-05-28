# Claude Code Context for Atlas Guardrails

This repository uses **Atlas Guardrails** to manage context and prevent technical debt.

## 🚨 Core Rules for Agent

1.  **Always Pack Before Editing**:
    Before modifying code, run `atlas pack` (CLI) or `atlas_pack` (MCP) to get the relevant context. Do NOT rely on global context or reading random files.
    ```bash
    atlas pack -t "description of task"
    ```

2.  **Search Before Creating**:
    Before creating a new utility, class, or helper function, search for duplicates using `atlas find-duplicates` (CLI) or `atlas_find_duplicates` (MCP).
    ```bash
    atlas find-duplicates -i "functionality description"
    ```

3.  **Respect Guardrails**:
    If `atlas check` fails, you have broken the public API or the index is stale. Fix the drift or update the index.

## MCP Server

This tool is available as an MCP server. When available, prefer using the MCP tools:
*   `atlas_index()`: Re-index.
*   `atlas_pack(task, budget)`: Get context.
*   `atlas_find_duplicates(intent)`: Find duplicates.

## Commands

*   `atlas index`: Re-index the repository (Run if you can't find symbols).
*   `atlas pack -t "<task>"`: Generate `pack.json`. Read this file to understand the codebase.
*   `atlas find-duplicates -i "<intent>"`: Find existing code.
*   `atlas check`: Verify API drift.

## Environment

*   Configuration is stored in `.ralphy/config.yaml` (if Ralphy is used).
*   Index data is in `.atlas/`. Do not edit manually.
