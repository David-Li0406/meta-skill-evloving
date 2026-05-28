---
name: skill-creation-guide
description: Use this skill when you need to create or improve Claude Agent Skills by following best practices for structuring SKILL.md files and ensuring effective communication.
---

# Skill Creation Guide

This skill provides a structured approach to creating and improving Claude Agent Skills, ensuring clarity and effectiveness in the SKILL.md documentation.

## Goals
- Clearly define the **purpose, triggers, and outputs** of the skill based on user input.
- Generate a correct `SKILL.md` file (YAML frontmatter + Markdown content).
- Utilize progressive disclosure to include supplementary files (reference/examples/templates/scripts) as needed.
- Output the skill in a format ready to be placed in `.claude/skills/` or `~/.claude/skills/`.

## Non-goals
- Development of implementation code itself (provide templates or pseudocode if necessary).
- Guessing company-specific confidential information (based solely on user input).

---

## How it works

### Step 1: Classify User Input
Determine which category the user input falls into:
1. **Documentation Generation** (PRD, mockups, specifications, etc.)
2. **Review** (PR reviews, document reviews, etc.)
3. **Transformation** (Markdown formatting, template application, etc.)
4. **Research** (summarizing, creating comparison tables, etc.)
5. **Operational Procedures** (deployment steps, runbooks, etc.)

### Step 2: Fill in Missing Information
Assume and clarify any missing information without excessive questioning:
- **Outputs**: What will the skill produce?
- **Target Users**: Who will use it?
- **Input Format**: What format will the input take?
- **Output Format**: What format will the output be in?
- **Constraints**: Any specific requirements for the output?
- **Examples**: Phrasing that should trigger the skill.

### Step 3: Determine Skill Name (Slug)
Create a `name` that is lowercase, numeric, and hyphenated, with a maximum of 64 characters. Use a gerund form for clarity.

### Step 4: Write the Description
Ensure the description includes:
- What the skill does.
- When to use it (trigger phrases).
- What it outputs.

### Step 5: Generate the SKILL.md Content
Include the following in the SKILL.md:
- **Goals / Non-goals**
- **Inputs**
- **Outputs**
- **Instructions**
- **Quality Checklist**
- **Examples**
- **References** (if necessary)

### Step 6: Use Progressive Disclosure
If the content is lengthy, separate additional details into:
- `reference.md`: Detailed procedures and guidelines.
- `examples.md`: A collection of examples and anti-patterns.
- `templates/`: Copy-paste templates.

---

## Output Format
The user will receive a **new skill folder structure** with the following:
1. Directory tree
2. `SKILL.md`
3. Additional files as needed (`reference.md`, `examples.md`, `templates/*`)

---

## Quality Checklist
- [ ] `name` is lowercase, numeric, hyphenated, and within 64 characters.
- [ ] `description` includes trigger phrases and is clear.
- [ ] Inputs/outputs/instructions are detailed enough for reproducibility.
- [ ] Expected output format is specified.