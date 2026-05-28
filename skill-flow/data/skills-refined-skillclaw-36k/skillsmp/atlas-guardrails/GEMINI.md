# Atlas Guardrails - Gemini CLI Extension

This extension provides tools to navigate, index, and protect the codebase.

## Available Tools

The following tools are exposed via MCP:

*   **`atlas_index`**: Scans the repository to build a map of symbols and dependencies.
    *   *Usage*: Call this when you start a session or after significant file changes.
*   **`atlas_pack(task, budget)`**: Retrieves a deterministic set of files relevant to your task.
    *   *Usage*: Call this INSTEAD of manually reading files when starting a coding task. It saves tokens and ensures you see dependencies.
*   **`atlas_find_duplicates(intent)`**: Finds existing symbols that match a description.
    *   *Usage*: Call this BEFORE creating new files or functions to avoid duplication.

## Workflow

1.  **Start**: `atlas_index()` to ensure the map is fresh.
2.  **Context**: `atlas_pack(task="implement login")` to get your working set.
3.  **Plan**: Analyze the packed files.
4.  **Check**: `atlas_find_duplicates(intent="password hash")` if you need a utility.
5.  **Edit**: Perform your changes.
6.  **Verify**: `atlas_check` (via shell) or `atlas_index()` again.

## Configuration

### Environment Variables

*   `ATLAS_BUDGET`: Default character budget for context packing.

Ensure `atlas` is in your PATH.

## Agent Instructions

You are an expert software engineer. To maintain high code quality and minimize technical debt, you MUST follow these guardrails:

1.  **Index First**: If you are new to the repository or if significant changes have occurred, run `atlas_index()`.
2.  **Context Packing**: Before starting any task, run `atlas_pack(task="...")` to get the deterministic context. Do not manually read files until you have analyzed the pack.
3.  **Prevent Duplication**: Before creating new functions, classes, or utilities, run `atlas_find_duplicates(intent="...")` to see if similar logic already exists.
