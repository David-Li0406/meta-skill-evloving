---
name: list_skills
description: 登録されているスキル一覧をカテゴリー別に分類して表示する
---

# List Skills

This skill scans all available agent skills in the project and displays them categorized by purpose.

## Instructions

1. **Scan**:
    * Check all subdirectories within the `.agent/skills/` directory.
    * Read the `name` and `description` from each directory's `SKILL.md`.

2. **Categorize**:
    Categorize skills according to the latest categories defined in the project's `index.md` (Workflow, Development, Science, QA, Documentation, etc.).

3. **Display**:
    * Create a heading for each category and display the skills in a table format.
    * Format example:

      ### [Category Name]

        | Skill Name | Description |
        | :--- | :--- |
        | `skill_name` | Description text |
