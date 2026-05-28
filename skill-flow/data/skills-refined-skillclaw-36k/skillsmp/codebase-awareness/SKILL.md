---
name: codebase-awareness
description: Best practices for exploring and understanding an existing codebase before planning or coding.
---

# Codebase Awareness & Discovery

## CRITICAL: Deep Discovery
Before proposing a PRD, technical plan, or new feature implementation, you MUST perform a deep discovery of the existing codebase.

1.  **Never Assume Greenfield**: Even if it's the start of a conversation, assume the user might have already started.
2.  **Verify via Content, Not Just Names**: Don't just `dir` or `ls`. Open core files (e.g., `app/_layout.tsx`, `index.tsx`, `package.json`, `lib/`) to understand existing logic.
3.  **Map Existing Features**: Create an internal mental map (or state in your thoughts) of:
    - What screens are already built?
    - What API clients/services are already initialized?
    - What data schemas are being used?
4.  **Fit, Don't Replace**: New features must fit into the existing architecture. If the user asks for a feature that is 50% done, your plan must be "Complete the X feature" rather than "Implement the X feature".

## Workflow: The "Pre-Plan" Audit
Whenever the `/plan` workflow or a similar "what should we do next" request is triggered:
- **Step 1**: Run `ls -R` or `find . -maxdepth 2`. Avoid `dir /s /b`.
- **Step 2**: Identify "Core Files" (entry points, main features).
- **Step 3**: `view_file` at least 2-3 of these core files to gauge the "maturity" of the project.
- **Step 4**: **Skill Check**: Briefly check `.agent/skills` and `view_file` any that seem relevant to the broad feature area (e.g. `product-design`, `supabase`).
- **Step 5**: Acknowledge existing work specifically in your response (e.g., "I see you've already implemented X in `file.tsx`").
- **Step 6 (Sub-Agent Option)**: For very large codebases, spawn a "Cartographer" agent to map the project:
  - `claude -p "Generate a high-level architecture map of this project and save it to specs/project_map.md" --agent "scribe"`

## Refactoring Hygiene
- **Delete While Replacing**: If you refactor a component to replace another (e.g., creating `ProductDetailModal` to replace `PantryItemDetail`), you MUST proactively identify and delete the obsolete file in the *same* coding session. Do not leave "zombie code" for a future cleanup pass.

## Phase Discipline: Read-Only Planning
- **CRITICAL**: During the `/plan` workflow or any "Discovery/Planning" phase, you are in **READ-ONLY MODE**.
- **Forbidden Actions**: Do NOT use `write_to_file`, `replace_file_content`, or `run_command` (except for `ls`, `cat`, or read-only tools) on project code.
- **Exception**: You may ONLY write to `specs/issue_*.md`, `specs/active_PRD.md`, or `.agent` files.
- **Why**: Writing code before the plan is approved causes "rogue" behavior, wasted effort, and violates the "Measure Twice, Cut Once" principle.
