---
name: dev:skill
description: Create New Skill - generates a new skill definition for this repository
---

# Create New Skill

Generates a new skill definition following the repository's conventions and best practices. This meta-skill ensures consistency across all skills in the repository.

## When to use

Use this skill when the user needs to:
- Add a new skill to this repository
- Create a custom Claude Code skill following best practices
- Scaffold a skill definition with proper structure

## Instructions

### Step 1: Gather Information

Ask the user for the following information:

1. **Category** - Which category folder should contain this skill?
   - `spec/` - Specification-driven development skills
   - `utils/` - Utility skills
   - `dev/` - Development and meta skills
   - Or suggest a new category if none fit

2. **Skill name** - Short, descriptive name in kebab-case (e.g., `review-code`, `generate-tests`)

3. **Purpose** - What does this skill do? What problem does it solve?

4. **Trigger conditions** - When should a user invoke this skill?

5. **Arguments** (optional) - Does the skill accept any arguments?

### Step 2: Analyze Existing Skills

Before writing the new skill:
1. Read 2-3 existing skills from the repository to understand current patterns
2. Note the writing style, structure, and level of detail
3. Identify any patterns specific to the chosen category

### Step 3: Create the Skill Definition

Create the file at `<category>/<skill-name>/SKILL.md` with this structure:

```markdown
---
name: <category>:<skill-name>
description: <Short Title> - <brief description of what the skill does>
---

# <Short Title>

<1-2 sentence description of what this skill does and its value.>

## When to use

Use this skill when the user needs to:
- <Use case 1>
- <Use case 2>
- <Use case 3>

## Instructions

### Step 1: <First Step Name>

<Clear instructions for what to do in this step.>

### Step 2: <Second Step Name>

<Clear instructions for what to do in this step.>

[Continue with additional steps as needed]

### Step N: Confirm with User

<Instructions for presenting results and asking for feedback.>

## Arguments

- `<args>` - <Description of expected arguments>
  - <Format or example 1>
  - <Format or example 2>

Examples:
- `<skill-name> <example-arg>` - <What this does>
```

### Writing Guidelines

1. **Clear step-by-step structure** - Each step should be actionable and specific
2. **Use imperative mood** - "Create the file", "Ask the user", "Run the command"
3. **Include examples** - Show concrete examples wherever helpful
4. **Handle edge cases** - Describe what to do when things go wrong
5. **Keep it focused** - One skill should do one thing well
6. **Match existing tone** - Read other skills and follow the same style

### Step 4: Update CLAUDE.md

After creating the skill, update the repository structure section in `CLAUDE.md`:
1. Add the new skill to the appropriate category in the structure tree
2. If a new category was created, add a description for it

### Step 5: Validate and Confirm

Present to the user:
1. The path of the created SKILL.md file
2. A summary of the skill's purpose and steps
3. Any updates made to CLAUDE.md
4. Ask if they want to make any changes

## Arguments

- `<args>` - Can include the category and/or skill name
  - `utils/format-code` - Full path with category
  - `format-code` - Just the skill name (will ask for category)

Examples:
- `dev:skill utils/format-code` - Create a skill in the utils category
- `dev:skill code-review` - Create a skill (will prompt for category)

## Skill Structure Reference

A well-structured skill typically includes:

| Section | Required | Purpose |
|---------|----------|---------|
| Frontmatter | Yes | `name` and `description` for the skill |
| Title | Yes | H1 heading matching the description title |
| Description | Yes | Brief explanation of the skill's purpose |
| When to use | Yes | Bullet points of use cases |
| Instructions | Yes | Step-by-step guide for Claude Code |
| Arguments | If applicable | Description of accepted arguments |
| Examples | Recommended | Concrete usage examples |
| Edge cases | Recommended | How to handle unusual situations |

## Naming Conventions

- **Category names**: lowercase, single word preferred (e.g., `spec`, `utils`, `dev`)
- **Skill names**: kebab-case (e.g., `do-next`, `changelog`, `skill`)
- **Full skill name**: `category:skill-name` (e.g., `dev:skill`, `utils:changelog`)
