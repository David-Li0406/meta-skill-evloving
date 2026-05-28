---
name: skill-creator
description: Use this skill when you want to create or improve Claude Code Skills, providing guidance on structure, best practices, and templates for SKILL.md files.
---

# Skill Creator for Claude Code Skills

This skill provides a comprehensive guide for creating and improving Claude Code Skills, ensuring high-quality and consistent outputs.

## Goals
- Clarify the purpose, activation conditions, and outputs of the skill based on user input.
- Generate a correct `SKILL.md` (YAML frontmatter + Markdown body).
- Use progressive disclosure to include auxiliary files (reference/examples/templates) as needed.
- Output in a format ready to be placed in `.claude/skills/` or `~/.claude/skills/`.

## When to Activate
This skill activates when users express the need to:
- Create a new skill.
- Add a skill to the `.claude/skills/` directory.
- Improve or expand an existing skill.

## Core Principles

### 1. Context is Public Good
- Include only the necessary information for Claude to function effectively.
- Assume Claude has a high level of understanding and only add context that is essential.

### 2. Keep SKILL.md Under 500 Lines
- If the content exceeds this limit, split it into multiple skills or move detailed information to `references/`.

### 3. Clear Triggers
- Ensure the `description` includes specific trigger keywords that indicate when to use the skill.

## Structure of SKILL.md

### Required Files
```
.claude/skills/your-skill-name/
├── SKILL.md          # Main skill definition (required)
├── reference.md      # Detailed reference (optional)
├── examples.md       # Specific examples (optional)
└── templates/        # Template files (optional)
```

### Example SKILL.md Structure
```markdown
---
name: skill-name
description: A concise description of the skill's function and activation conditions.
---

# Skill Title

## Purpose
Explain the purpose of this skill in 1-2 paragraphs.

## When to Activate
- List specific conditions for activation.
- Include file paths or keywords.

## Quick Checklist
Items to confirm before/after the task:
- [ ] Checklist item 1
- [ ] Checklist item 2

## Detailed Guidelines
### Section 1
Content

### Section 2
Content

## Templates
(If templates directory exists)

## References
(If reference.md exists)

## Examples
(If examples.md exists)
```

## Skill Creation Steps

### Step 1: Clarify the Skill's Purpose
Answer the following questions:
1. What does the skill assist with? (e.g., report generation, architecture checks)
2. When should it be used? (file paths, keywords, situations)
3. What are the main checkpoints? (quality standards, best practices)

### Step 2: Create Directory Structure
```bash
mkdir -p .claude/skills/your-skill-name/templates
```

### Step 3: Create SKILL.md
1. Write the frontmatter (name, description).
2. Describe the purpose section.
3. List activation conditions.
4. Create a quick checklist.
5. Write detailed guidelines.

### Step 4: Create Auxiliary Files as Needed
- **reference.md**: Detailed technical references and best practices.
- **examples.md**: Good and bad examples for comparison.
- **templates/**: Reusable code templates.

## Best Practices

### ✅ DO
- Provide concise and specific descriptions.
- Include practical checklists.
- Offer rich code examples.
- Provide templates for common patterns.
- Include reference links.

### ❌ DON'T
- Use overly abstract descriptions.
- Write excessively long paragraphs.
- Include unverifiable checklist items.
- Duplicate content from existing skills.

## Quality Checklist
Before sharing a new skill, ensure:
- [ ] The `description` is specific and includes trigger keywords.
- [ ] The SKILL.md body is under 500 lines.
- [ ] Additional details are in separate files as needed.
- [ ] All references are at a single level of depth.
- [ ] The skill has clear steps in the workflow.

## References
For detailed guidelines and templates, refer to [reference.md](reference.md) and [examples.md](examples.md).