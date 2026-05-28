---
name: project-bead-status
description: Use this skill to provide concise project or bead status summaries based on user queries about current status or specific bead details.
---

# Status

## Overview

Provide a concise, human-friendly summary of project status or a specific bead. When no bead id is provided, run the `waif` CLI tool to summarize recent work and current work in progress. When a bead id is provided, run `bd show <bead-id> --json` to provide a detailed explanation of that bead, including title, status, assignee, description, blockers, and related links.

## When To Use

- User asks general project status (e.g., "What is the current status?", "Status of the project?", "audit the project", "audit").
- User asks about a specific bead id (e.g., "What is the status of bd-123?", "audit bd-123").

## Behavior

1. Detect whether the user provided a bead id in the request.
2. If no bead id is provided:
   - Run `waif in-progress --json` to fetch in-progress work.
   - Present a one-line summary of the overall project status based on the JSON data.
   - Summarize actively in-progress beads, starting with the one deepest in the dependency chain, including the last updated date and a summary of the most recent comment if applicable.
   - List the files referenced in the in-progress beads.
   - Suggest to run `audit <bead-id>` against the most important in-progress bead.
3. If a bead id is provided:
   - Run `bd show <bead-id> --json` and `bd show <bead-id> --thread --refs --json` to fetch bead details.
   - Parse and present: title, status, assignee, priority, description, blockers, dependencies, summary of all comments, and relevant links.
   - Walk through all open and in-progress subtasks, children, and blockers, summarizing their status.
   - Clearly state whether the bead can be closed or not, explaining why if it cannot.
   - Provide three numbered actionable next steps based on the status information.

## Notes

- Keep the output concise and actionable for quick human consumption.
- Handle errors gracefully: if `waif`, `bd`, or any other command is not available or returns invalid JSON, present a helpful error and possible remediation steps.