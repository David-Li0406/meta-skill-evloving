---
name: status
description: "Provide concise project / bead status and run Beads/waif helpers to augment results. Trigger on user queries such as: 'What is the current status?', 'Status of the project?', 'What is the status of <bead-id>?', 'audit', 'audit <bead-id>'"
---

# Status

## Overview

Provide a concise, human-friendly summary of project status or a specific bead. When no bead id is provided, run `waif` CLI tool to summarize recent work and current work in progress. When a bead id is provided, run `bd show <bead-id> --json` and provide a detailed explanation of that bead (title, status, assignee, description, blockers, and related links).

## When To Use

- User asks general project status (e.g., "What is the current status?", "Status of the project?", "audit the project", "audit").
- User asks about a specific bead id (e.g., "What is the status of bd-123?", "audit bd-123").

## Behavior

1. Detect whether the user provided a bead id in the request.
2. Run git status to what branch we are on and whether there are uncommitted changes and include a note if any are found.
3. If no bead id is provided:
   - Run `waif in-progress --json` to fetch in-progress work JSON format to get more informatio, but do not display it.
   - Present a one line summary of the overall project status based on the JSON data.
   - Present a summary of actively in-progress beads (ignore beads that are open or closed). Start with the one deepest in the dependency chain and work upwards. Include the last updated date and a summary of the most recent comment if applicable.
   - List the files referenced in the in-progress beads.
4. If a bead id is provided:
   - Run `bd show <bead-id> --json` and `bd show <bead-id> --thread --refs --json` to fetch bead details.
   - Parse and present: title, status, assignee, priority, description, blockers, dependencies, summary of all comments, and relevant links.
   - Walk through all open and in-progress subtasks, children, and blockers, summarizing their status as well.
     - Never skip any related bead that is open or in-progress. 
   - Make a very clear statement about whether the bead can be closed or not. If it cannot be closed, explain why (e.g., blockers, dependencies, incomplete tasks).
5. Provide numbered actionable next steps based on the status information. 
  - If no bead id is provided, always offer to run `audit <bead-id>` (do not mention `bd show`) against the most important in-progress bead (show ID and title), add one or two  alternative next actions relevant to the current status. 
  - If a bead id is provided, suggest appropriate next steps to complete the bead (if not already completed).
  - Do not provide an alternative set of actions. There should only be 3 numbered next steps and a free-form response allowed.

## Notes

- Keep the output concise and actionable for quick human consumption.
- Handle errors gracefully: if `waif`, `bd` or any other command is not available or return invalid JSON, present a helpful error and possible remediation steps.
