---
name: refactor_skills
description: スキルの整理（統廃合・分離・分類の更新）を行い、エージェントの能力を洗練させる
---

# Refactor Skills

This skill is used to organize skills, eliminate redundant features, and optimize the granularity and classification of skills to keep the agent's capabilities refined.

## Instructions

1. **Skills Audit**:
    * Run `list_skills` to review all current skills and their descriptions.
    * Identify redundant features or skills with overly fine granularity that should be consolidated.
    * Identify monolithic skills that should be split into smaller, focused ones.

2. **Refactoring Actions**:
    * **Consolidate**: Merge similar skills (e.g., merging `fix_notebook` and `fix_notebook_local`) by updating one `SKILL.md` to handle multiple modes via arguments. Remove or empty the redundant directories.
    * **Split**: Extract specific workflows from large, generic skills into new, independent ones.
    * **Update Classification**: Update the category definitions in the `list_skills` skill's `Instructions` to reflect the latest state.
    * **Refine Descriptions**: Improve the `description` in the YAML frontmatter to be more accurate and user-friendly (in Japanese).

3. **Execution**:
    * Use `write_to_file` or `replace_file_content` to update the target `SKILL.md` files.
    * If skills are added or removed, synchronize the category list in the `list_skills` skill.

4. **Verification**:
    * Run the updated `list_skills` to ensure the reorganized hierarchy is logical and easy for the user to understand.
