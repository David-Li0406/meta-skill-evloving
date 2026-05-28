---
name: create-skill
description: Create a new Claude Code skill following best practices and guidelines
argument-hint: <skill-name> [context]
disable-model-invocation: true
---

# Create Skill

## Overview

Create a new Claude Code skill following the established guidelines and best practices. This skill guides you through creating a properly structured SKILL.md file with YAML frontmatter and markdown content. Use this when you need to add new functionality to Claude Code as a reusable, invocable skill.

## Arguments

### Definitions

- **`<skill-name>`** (required): The name for the new skill in kebab-case (e.g., `review-code`, `analyze-deps`)
- **`[context]`** (optional): Additional context about what the skill should do

### Values

\$ARGUMENTS

## Additional Resources

- For the skill template structure, see [template.md](template.md)

## Core Principles

- Every skill must be a `SKILL.md` file wrapped in a directory
- Directory name should match the skill name
- Use the template at `plugins/agentic-sdlc/skills/create-skill/template.md` as the base
- Follow the exact section order defined in the template
- Use US English spelling in all content
- Keep descriptions concise (max 200 characters)
- Keep SKILL.md under 500 lines; move detailed reference material to separate files
- See template.md for complete YAML frontmatter field reference
- Code files must use ASCII only; markdown files may use minimal functional emojis

## Skill-Specific Guidelines

### Directory Structure

Skills must follow this directory structure:

```
skills/
  my-skill/
    SKILL.md           # Required - main skill definition
    reference.md       # Optional - detailed reference docs
    examples.md        # Optional - usage examples
    scripts/
      helper.py        # Optional - utility scripts
```

The `SKILL.md` file is required. Supporting files are optional and should be referenced from SKILL.md so Claude knows when to load them.

### Argument-Hint Conventions

- Use `<arg>` for required positional arguments (angle brackets)
- Use `[arg]` for optional positional arguments (square brackets)
- Use `[--flag]` for boolean flags (always optional - flags toggle behavior)
- Use `[arg...]` for variadic arguments
- The `[context]` argument must ALWAYS come last when present
- Flags MUST be boolean-only - NEVER use `--flag <value>` pattern

Examples:

- `<context>` - required context only
- `[type] <context>` - optional type, required context
- `[paths...] [context]` - optional paths, optional context
- `[--verbose] <context>` - boolean flag, required context

### When to Use Invocation Controls

**disable-model-invocation: true** - Only you can invoke:

- Skills with side effects (commit, deploy, send-message)
- Skills where timing matters
- Skills that should not run automatically

**user-invocable: false** - Only Claude can invoke:

- Background knowledge skills
- Context skills that aren't actionable commands
- Skills like `legacy-system-context` that explain how things work

### Forked Context Skills

Add `context: fork` when a skill should run in isolation without conversation history. The skill content becomes the prompt for the subagent. Only use this for skills with explicit task instructions, not just guidelines.

## Instructions

1. **Validate the skill name**
   - Ensure it uses kebab-case (lowercase with hyphens)
   - Verify it doesn't conflict with existing skills
   - Name should be descriptive of the action

2. **Create the skill directory**
   - Create `plugins/<plugin-name>/skills/<skill-name>/` directory
   - The directory name should match the skill name

3. **Read the template**
   - Load `plugins/agentic-sdlc/skills/create-skill/template.md`
   - Use it as the base structure for the new skill

4. **Create SKILL.md**
   - Add YAML frontmatter with required fields
   - Fill in all required sections from the template
   - Remove optional sections that don't apply
   - Replace all `{{placeholders}}` with actual content
   - Remove all HTML comment instructions

5. **Validate the skill**
   - Ensure all required sections are present
   - Verify frontmatter fields are correct
   - Check that argument-hint matches Arguments section
   - Confirm description is under 200 characters

6. **Add supporting files (if needed)**
   - Create reference.md for detailed documentation
   - Create examples.md for usage examples
   - Reference these files from SKILL.md

## Output Guidance

After creating the skill, output a JSON object:

```json
{
  "status": "created",
  "skill": {
    "name": "<skill-name>",
    "location": "plugins/<plugin>/skills/<skill-name>/SKILL.md",
    "description": "<description>",
    "invocation": "/<skill-name>"
  },
  "files_created": [
    "SKILL.md",
    "reference.md (if applicable)",
    "examples.md (if applicable)"
  ],
  "next_steps": [
    "Test the skill with /<skill-name>",
    "Verify Claude loads it appropriately",
    "Add to plugin README if user-facing"
  ]
}
```
