---
name: creator
description: Creates a new skill based on user description. Use when user wants to create a skill about a specific topic or functionality.
---

# Skill Creation Command

This command helps you create a new skill based on your description. It will guide you through the process and generate the necessary files.

## Usage

Run this command with a description of the skill you want to create:
```
/skill-creator:creator 帮我创建一个关于 [skill description] 的 skill
```

## Process

1. **Extract skill name and description** from your request
2. **Generate skill structure** using the init_skill.py script
3. **Create initial SKILL.md** with appropriate content based on your description
4. **Set up plugin configuration** files

## Implementation

When this command is triggered:

1. Parse the user's request to extract the skill topic/description
2. Convert the topic to a hyphenated skill name (e.g., "PDF处理" → "pdf-processor")
3. Run the init_skill.py script with the generated skill name
4. Customize the generated SKILL.md based on the user's specific requirements
5. Provide instructions for next steps

## Examples

- `/skill-creator:creator 帮我创建一个关于PDF处理的skill` → Creates a PDF processing skill
- `/skill-creator:creator 帮我创建一个关于前端设计的skill` → Creates a frontend design skill
- `/skill-creator:creator 帮我创建一个关于数据分析的skill` → Creates a data analysis skill

## Notes

- The skill name will be automatically generated from your description
- Skills will be created in the current directory unless specified otherwise
- You can customize the generated skill files after creation