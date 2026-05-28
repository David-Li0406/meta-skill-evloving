---
name: openspec-verify-change
description: Use this skill when you want to validate that an implementation is complete, correct, and coherent before archiving it.
---

# Skill body

Verify that an implementation matches the change artifacts (specs, tasks, design).

**Input**: Optionally specify a change name. If omitted, prompt for available changes.

**Steps**

1. **If no change name provided, prompt for selection**
   - Run `openspec list --json` to get available changes. Use the **AskUserQuestion tool** to let the user select.
   - Show changes that have implementation tasks (tasks artifact exists).
   - Include the schema used for each change if available.
   - Mark changes with incomplete tasks as "(In Progress)".
   - **IMPORTANT**: Do NOT guess or auto-select a change. Always let the user choose.

2. **Check status to understand the schema**
   ```bash
   openspec status --change "<name>" --json
   ```
   - Parse the JSON to understand:
     - `schemaName`: The workflow being used (e.g., "spec-driven", "tdd").
     - Which artifacts exist for this change.

3. **Get the change directory and load artifacts**
   ```bash
   openspec instructions apply --change "<name>" --json
   ```
   - This returns the change directory and context files. Read all available artifacts from `contextFiles`.

4. **Initialize verification report structure**
   - Create a report structure with three dimensions:
     - **Completeness**: Track tasks and spec coverage.
     - **Correctness**: Track requirement implementation and scenario coverage.
     - **Coherence**: Track design adherence and pattern consistency.
   - Each dimension can have CRITICAL, WARNING, or SUGGESTION issues.

5. **Verify Completeness**
   - **Task Completion**:
     - If tasks.md exists in contextFiles, read it.
     - Parse checkboxes: `- [ ]` (incomplete) vs `- [x]` (complete).
     - Count complete vs total tasks.
     - If incomplete tasks exist:
       - Add CRITICAL issue for each incomplete task.
       - Recommendation: "Complete task: <description>" or "Mark as done if already implemented".

   - **Spec Coverage**:
     - If delta specs exist in `openspec/changes/<name>/specs/`:
       - Extract all requirements (marked with "### Requirement:").
       - For each requirement:
         - Search codebase for keywords related to the requirement.
         - Assess if implementation likely exists.
       - If requirements appear unimplemented:
         - Add CRITICAL issue: "Requirement not found: <requirement name>".