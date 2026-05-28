---
name: skill-importer
description: Standardized procedure to import external skills (e.g. from anthropics/skills) into the workspace.
---

# Skill Importer Skills

Use this skill when asked to "import a skill", "port a skill", or "add the X skill from Y".

## 1. Source Analysis & Fetch
First, understand what you are importing.
1.  **List Files**: Get a file listing of the remote skill directory.
2.  **Read Content**: Read the `SKILL.md` and any key scripts to understand the logic.

## 2. Quality Evaluation (CRITICAL)
**Goal:** Keep the skills library **lean and effective**. Avoid bloat.

Assess the skill against these strict criteria:
-   **Redundancy**: Does *any* existing skill cover the main intent? If yes -> **REJECT**.
    -   *Example*: Don't import a "manual skill creation guide" if we have a "skill creator tool".
-   **Utility**: Is this skill highly relevant to *this specific workspace*?
-   **Safety**: Does it require dangerous permissions?

**Recommendation Step**:
-   **REJECT**: If the skill is redundant, low quality, or not strictly necessary. **Default to rejection** for borderline cases to maintain leanness.
-   **MERGE / UPDATE**: If the skill overlaps with an existing one but offers improvements (e.g., better docs, new scripts). Recommend **updating the existing skill** instead of importing a new one.
-   **MODIFY**: Only if the skill provides unique value but needs adapting.
-   **ACCEPT**: Only if high quality, unique, and immediately useful.

## 3. Adaptation Planning
Identify necessary tweaks to make it compatible with this workspace:
-   **Frontmatter**: Ensure `SKILL.md` has valid YAML frontmatter (`name`, `description`).
-   **Provenance**: Add a `source` field to the `metadata` block (or create one) pointing to the original URL.
    ```yaml
    metadata:
      source: https://github.com/org/repo/tree/main/skills/some-skill
    ```
-   **Terminology**: If the skill references "Claude" explicitly in user-facing strings, consider changing to "Agent" or "Assistant".
-   **Paths**: Ensure scripts use relative paths or configurable arguments, not hardcoded `/home/user` paths.

**Output**: Create a short `import_plan.md` artifact (or just a clear plan in the chat) listing the files and the "Status" (Keep/Modify/Delete).

## 4. Execution & Verification
1.  **Import**: Write the files to `.agent/skills/<skill-name>/`.
2.  **Verify**: Run the standard validator:
    ```bash
    python3 .agent/skills/skill-creator/scripts/quick_validate.py .agent/skills/<skill-name>
    ```
3.  **Report**: Notify the user that the skill is ready.
