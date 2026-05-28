---
name: Issue Triage
description: Scan overlay repositories for GitHub issues and triage them into the workspace roadmap.
---

# Issue Triage Skill

Use this skill when asked to "check for issues", "scan the repos", or "triage bugs".

## Scope
This skill operates on **Overlay Repositories** only (excluding the `underlay.repos`). It connects upstream GitHub issues to the local `.agent/ROADMAP.md`.

## Prerequisites
-   **GitHub MCP**: Must be configured and active.
-   **Helper Script**: `scripts/list_overlay_repos.py` must exist.

## Core Operations

### 1. Scan Issues
**Trigger**: "Scan for new issues" or "Triage issues"
**Procedure**:
1.  Run `python3 scripts/list_overlay_repos.py` to get a JSON list of `{name, url, version}`.
2.  For each repository:
    -   Parse the owner/repo from the URL.
    -   Use the GitHub MCP tool `search_issues` (or `list_issues`) to find **open** issues.
    -   *Filter*: Ignore issues already referenced in `.agent/ROADMAP.md`.
3.  **Report**: Present a list of *new, untracked* issues to the User.

### 2. Triage (Interactive)
**Trigger**: (Continuation of Scan)
**Procedure**:
1.  Ask the User: "Which of these should be added to the Roadmap?"
2.  For selected issues:
    -   Use the **Project Management Skill** to "Add Task".
    -   Title format: `[Upstream] <Issue Title> (Link: <url>)`
    -   Status: `Planned` (Backlog).

## Example Output
"I found 3 new issues in `depthai_marine`:
1.  `Crash on startup when no camera connected` (#42)
2.  `Add graceful shutdown` (#45)

Do you want to add these to the backlog?"
