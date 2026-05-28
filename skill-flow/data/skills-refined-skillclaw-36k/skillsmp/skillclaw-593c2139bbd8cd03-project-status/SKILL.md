---
name: project-status
description: Use this skill to provide a concise summary of project or bead status when users inquire about current progress or specific bead details.
---

# Skill body

## Overview

This skill provides a human-friendly summary of project status or a specific bead. It utilizes the `waif` and `bd` CLI tools to fetch and present relevant information based on user queries.

## When To Use

- User asks for the general project status (e.g., "What is the current status?", "Status of the project?", "audit the project", "audit").
- User inquires about a specific bead id (e.g., "What is the status of bd-123?", "audit bd-123").

## Behavior

1. Detect whether the user provided a bead id in the request.
2. If no bead id is provided:
   - Run `waif in-progress --json` to fetch in-progress work.
   - Parse the returned JSON to summarize:
     - Number of in-progress beads.
     - Highest-priority items with a short description and their assignees.
     - Any items in a blocked state or missing assignees.
     - A one-line suggestion for the next action (e.g., "Review bd-123 assigned to @alice").
     - Run `waif recent --json` to fetch recently modified beads and summarize the last 3 completed beads with titles, most recent comments, and assignees.
3. If a bead id is provided:
   - Run `bd show <bead-id> --json` to fetch bead details.
   - Parse and present: title, status, assignee, priority, description, blockers, dependencies, comments count, and relevant links.
   - Walk through all open and in-progress subtasks, children, and blockers, summarizing their status.
   - Clearly state whether the bead can be closed or not, explaining any blockers or dependencies.
4. Handle errors gracefully: if `waif` or `bd` are not available or return invalid JSON, present a helpful error and possible remediation steps.
5. Provide numbered actionable next steps based on the status information. If no bead id is provided, always offer to run `audit <bead-id>` against the most important in-progress bead.

## Notes

- Keep the output concise and actionable for quick human consumption.