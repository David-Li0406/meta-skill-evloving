---
name: skill-creator
description: Creates well-formatted Claude Code skills from descriptions. Use when the user wants to create a new skill, generate a skill, or build a skill for a specific task.
allowed-tools: WebSearch, WebFetch, Write, Read, Glob
---

# Skill Creator

Create well-structured Claude Code skills from natural language descriptions.

## Instructions

When the user describes a skill they want to create, follow these steps:

### Step 1: Understand the Request
Parse the user's description to identify:
- What task the skill should accomplish
- Who will use it
- What the expected output looks like

### Step 2: Research Best Practices
Use WebSearch to find:
- Best practices for the creating cloude skills
- Best practices for creating the skill's domain
- Common patterns and conventions
- Edge cases to consider

Summarize 2-3 key insights that should inform the skill design.

### Step 3: Design the Skill Metadata

**Name**: Lowercase, hyphenated, action-oriented, under 64 characters

**Description**: Include what it does, trigger keywords, and when to use it (under 1024 chars)

**Derive Required Tools**:
| Skill Needs | Tools |
|-------------|-------|
| Read files | Read, Glob, Grep |
| Modify files | Read, Edit, Write |
| Run commands | Bash |
| Python scripts | Bash(python:*) |
| Git operations | Bash(git:*) |
| Web research | WebSearch, WebFetch |

Only include tools actually needed.

### Step 4: Write the SKILL.md

Use this structure:

```yaml
---
name: [derived-name]
description: [Description with trigger keywords. Use when...]
allowed-tools: [Only necessary tools]
---

# [Skill Title]

## Purpose
[One sentence]

## Instructions
1. [Step 1]
2. [Step 2]
3. [Continue as needed]

## Output Format
[Expected output structure]

## Best Practices
- [Guideline 1]
- [Guideline 2]

## Example
[Concrete input → output]
```

### Step 5: Validate with Checklist

Before presenting, verify ALL items:

**Frontmatter**
- [ ] Name is lowercase with hyphens only
- [ ] Name is under 64 characters
- [ ] Description under 1024 characters
- [ ] Description has trigger keywords
- [ ] Description explains WHEN to use
- [ ] Tools list is minimal

**Body**
- [ ] Instructions are numbered and actionable
- [ ] No over-engineering
- [ ] Includes concrete example
- [ ] Under 500 lines total

**Contract**
- [ ] Does ONE thing well
- [ ] User knows when to invoke from description
- [ ] Claude can execute from instructions alone
- [ ] No placeholders remaining

### Step 6: Present and Save
1. Show the complete SKILL.md
2. Display the completed checklist
3. Ask where to save (default: .claude/skills/[skill-name]/SKILL.md)
4. Use Write tool to create the file

## Example
User: "Create a skill for generating TypeScript interfaces from JSON"
Result: Researches TS best practices, creates generating-ts-interfaces skill, validates, saves to .claude/skills/
