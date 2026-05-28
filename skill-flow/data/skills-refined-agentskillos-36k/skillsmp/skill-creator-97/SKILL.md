---
name: skill-creator
description: Create new Agent Skills with the proper directory structure and SKILL.md format. Use when the user wants to create a new skill or learn how to make one.
---

# Skill Creator

This skill helps you create new Agent Skills for the system.

## When to use this skill
Use this skill when:
- The user asks to create a new skill.
- The user wants to start a new skill project.
- You need to generate the boilerplate structure for a skill.

## How to use
1. **Understand requirements**: Ask the user what the skill should do if not already clear.
2. **Determine skill name**: Choose a concise, kebab-case name (e.g., `pdf-reader`, `data-analysis`).
3. **Initialize skill**: Call the initialization API/Tool to create the directory structure.
   - Directory: `backend/skills/<skill-name>`
   - File: `SKILL.md` (with template)
   - Subdirectories: `scripts/`, `references/`, `assets/`
4. **Guide the user**: Inform the user that the skill template has been created at `backend/skills/<skill-name>/SKILL.md` and they should edit it to add instructions.

## Tools
The system provides a tool `create_skill` (or API endpoint `/api/skills/init`) to perform the initialization.

## Example
User: "Make a skill for analyzing stock data."
Action:
1. Determine name: `stock-analysis`
2. Call `create_skill(name="stock-analysis")`
3. Response: "Created skill 'stock-analysis'. You can now edit `backend/skills/stock-analysis/SKILL.md`."
