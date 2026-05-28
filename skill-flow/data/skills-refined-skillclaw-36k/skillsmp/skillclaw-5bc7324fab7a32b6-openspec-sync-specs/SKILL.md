---
name: openspec-sync-specs
description: Use this skill when you want to update main specs with changes from a delta spec, without archiving the change.
---

# Skill body

Sync delta specs from a change to main specs.

This is an **agent-driven** operation - you will read delta specs and directly edit main specs to apply the changes. This allows intelligent merging (e.g., adding a scenario without copying the entire requirement).

**Input**: Optionally specify a change name. If omitted, prompt for available changes.

**Steps**

1. **If no change name provided, prompt for selection**

   Run `openspec list --json` to get available changes. Use the **AskUserQuestion tool** to let the user select.

   Show changes that have delta specs (under `specs/` directory).

   **IMPORTANT**: Do NOT guess or auto-select a change. Always let the user choose.

2. **Find delta specs**

   Look for delta spec files in `openspec/changes/<name>/specs/*/spec.md`.

   Each delta spec file contains sections like:
   - `## ADDED Requirements` - New requirements to add
   - `## MODIFIED Requirements` - Changes to existing requirements
   - `## REMOVED Requirements` - Requirements to remove
   - `## RENAMED Requirements` - Requirements to rename (FROM:/TO: format)

   If no delta specs found, inform user and stop.

3. **For each delta spec, apply changes to main specs**

   For each capability with a delta spec at `openspec/changes/<name>/specs/<capability>/spec.md`:

   a. **Read the delta spec** to understand the intended changes.

   b. **Read the main spec** at `openspec/specs/<capability>/spec.md` (may not exist yet).

   c. **Apply changes intelligently**:

      **ADDED Requirements:**
      - If requirement doesn't exist in main spec → add it.
      - If requirement already exists → update it to match (treat as implicit MODIFIED).

      **MODIFIED Requirements:**
      - Find the requirement in main spec.
      - Apply the changes - this can be:
        - Adding new scenarios (don't need to copy existing ones).
        - Modifying existing scenarios.
        - Changing the requirement description.
      - Preserve scenarios/content not mentioned in the delta.

      **REMOVED Requirements:**
      - Remove the entire requirement block from main spec.

      **RENAMED Requirements:**
      - Find the FROM requirement, rename to TO.

   d. **Create new main spec** if capability doesn't exist yet:
      - Create `openspec/specs/<capability>/spec.md`.