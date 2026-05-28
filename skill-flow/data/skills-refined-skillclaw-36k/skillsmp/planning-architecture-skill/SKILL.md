---
name: planning-architecture-skill
description: >
  Provides step‑by‑step planning and architectural guidance for the Tenzzen app.
  Uses codebase analysis, documentation reading, and web design inspiration.
---

# Planning & Architecture Skill

## Overview

This skill assists the agent in:

1. Locating the repository root and the `docs` directory.
2. Reading key documentation files (`PROJECT_OVERVIEW.md`, `DESIGN_SYSTEM.md`).
3. Performing web searches for modern UI/UX design patterns.
4. Generating a structured implementation plan (tasks, priorities, architecture diagrams).

## Execution Steps

1. **Locate Repository** – Use the provided workspace path to find the project root.
2. **Read Documentation** – Open `docs/PROJECT_OVERVIEW.md` and `docs/DESIGN_SYSTEM.md` to gather architectural context.
3. **Codebase Overview** – Generate an outline of important directories (`app/`, `convex/`, `components/`).
4. **Web Inspiration** – Search the web for "modern web app design patterns" and summarize key takeaways.
5. **Produce Plan** – Combine the gathered information into a markdown plan with sections:
   - High‑level architecture diagram (textual description).
   - Task breakdown (feature, backend, UI).
   - Prioritization and timeline.
   - References to design inspiration.

## References

- `references/codebase_overview.md` – Auto‑generated overview of the repo structure.
- `references/design_inspiration.md` – Summarized web search results for design patterns.

## Usage

When the agent receives a request to "plan" or "design" a new feature, it should:

- Load this SKILL.md (metadata triggers the skill).
- Follow the steps above, reading the referenced files as needed.
- Output the final plan to the user or save it to `output/plan.md`.

## Constraints

- Do not modify any existing project files unless explicitly instructed.
- Keep generated plans concise (< 2000 words) and include clear headings.
- Ensure all links to docs use absolute file URIs.

---
