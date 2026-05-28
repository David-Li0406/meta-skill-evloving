---
name: stack-sketch
description: Create visual JSON diagrams for full-stack web app planning including navigation flows, state machines, infrastructure maps, and UI mockups. Use when asked to draw a diagram, create a flowchart, visualize architecture, or mock up a UI.
license: MIT
metadata:
  author: jmush16
  version: "1.0.0"
---

# StackSketch

## Overview
Create and edit StackSketch JSON diagrams that serve as a visual source of truth for full-stack web app planning, including navigation flows, state machines, infrastructure maps, and UI mockups.

## When to Activate
- Use when the user asks for visual planning, flowcharts, UI mockups, architecture diagrams, or system design diagrams.
- Use when the user mentions StackSketch, JSON-based diagrams, or a Figma-like editor backed by versioned JSON files.
- Use when the work requires a visual feedback loop before implementation.

## Workflow: Visual Feedback Loop
1. Establish diagram set and file locations (default: `.stacksketch/` directory).
2. Author StackSketch JSON using the schema reference.
3. Iterate: accept user edits from the viewer and update JSON with minimal diffs.
4. Mirror the visuals back into requirements or implementation plans before coding.

## Diagram Types and Intent
- **Flow**: Navigation, state machines, decision trees, and logic branches.
- **Infrastructure**: Frontend, backend, database, cache, queue, external services, and data flows.
- **UI Mockups**: Device frames plus UI components (cards, buttons, inputs, progress, badges).

## Authoring Rules
- Preserve stable `id` values for nodes, edges, and groups across iterations.
- Use a grid (8 or 16) and avoid overlaps or edge crossings.
- Prefer `node.type` for shape and `node.kind` for semantic role (frontend, backend, database, etc.).
- Keep `label` short; place long descriptions in `data.notes`.
- Maintain one diagram per file, and avoid rewriting unrelated sections.
- Use 2-space indentation and keep key ordering consistent within each object.

## File Layout Defaults
- Store diagrams in `.stacksketch/` unless the user requests a different location.
- Use descriptive filenames: `navigation-flow.json`, `gameplay-flow.json`, `infra-map.json`, `ui-mockups.json`.
- Include `diagram.type` in every file so the viewer can render correctly.

## Output Expectations
- Output valid JSON only when asked to generate or modify a diagram.
- Do not output ASCII art.
- When asked to describe a diagram, summarize key nodes/edges instead of pasting the full file.

## References
- [Schema](./references/schema.md) - StackSketch JSON structure and field definitions.
- [Examples](./references/examples.md) - Sample flow, infra, and UI mockup diagrams.
