---
name: creating-skills
description: Creates new skill YAML definitions in the canonical format. Use when the user wants to create a new skill, command, or workflow for the AI config transpiler.
---

# Creating Skills

Creates new skill definitions in the canonical YAML format for the AI config transpiler.

## Output Location

All new skills are created in: `example/commands/`

## Canonical YAML Schema

All available fields for a skill/command definition:

```yaml
# Required Fields
name: "skill-name"                    # Identifier used to invoke the skill
content: |                            # Full skill instructions in markdown
  Skill content here...

# Optional Fields
description: "Brief one-line summary" # Shown in skill listings and discovery

# Claude Code Specific Options
disable_model_invocation: false       # Default: false
  # true  = Only the user can invoke this skill (via /skill-name)
  # false = Both user and Claude can invoke it

user_invocable: true                  # Default: true
  # true  = User can invoke with /skill-name
  # false = Only Claude can invoke (internal/automated skills)
```

## Field Reference

### `name` (required)
The identifier used to invoke the skill. Becomes the filename (`{name}.yaml`) and the invocation command (`/name`).

**Conventions:**
- Use gerund form: `analyzing-code`, `generating-tests`
- Lowercase letters, numbers, hyphens only
- Be specific: `reviewing-pull-requests` not `review`
- Avoid vague names: `helper`, `utils`, `tools`

### `description` (optional)
Brief one-line summary shown in skill listings. Claude uses this for skill discovery.

**Guidelines:**
- Write in third person: "Analyzes code for security issues"
- Include WHAT it does and WHEN to use it
- Keep under 100 characters

### `content` (required)
The full skill instructions in markdown. This is what Claude reads when the skill is invoked.

**Best practices:**
- Use `|` for multiline YAML strings
- Structure with `## Headers` and bullet points
- Include process steps, expected inputs/outputs
- Keep concise — Claude is already smart

### `disable_model_invocation` (optional, Claude Code)
Controls whether Claude can invoke the skill automatically.

| Value | Behavior |
|-------|----------|
| `false` (default) | Both user and Claude can invoke |
| `true` | Only user can invoke via `/skill-name` |

**Use `true` when:**
- Skill performs destructive actions
- Skill requires explicit user intent
- You want manual control over when it runs

### `user_invocable` (optional, Claude Code)
Controls whether the user can invoke the skill directly.

| Value | Behavior |
|-------|----------|
| `true` (default) | User can invoke with `/skill-name` |
| `false` | Only Claude can invoke (internal skill) |

**Use `false` when:**
- Skill is a helper for other skills
- Skill should only run as part of automated workflows
- Skill is an internal implementation detail

## Workflow

1. **Gather requirements** from the user:
   - What should the skill do?
   - What's a good name? (gerund form preferred)
   - Should it be user-invocable, model-invocable, or both?
   - What's the process/workflow?

2. **Draft the skill** following best practices:
   - Keep content concise
   - Use clear markdown structure
   - Include process steps
   - Specify expected output format

3. **Write the YAML file** to `example/commands/{name}.yaml`

4. **Verify** the file was created correctly

## Content Best Practices

**Be concise:**
- Only add context Claude doesn't already have
- Challenge each paragraph: "Does Claude need this?"

**Structure clearly:**
- Use `## Headers` for major sections
- Use bullet points for lists
- Include code examples where helpful

**Define process:**
- Number sequential steps
- Specify inputs and outputs
- Include success criteria

**Specify output format:**
- What should the final result look like?
- Should user confirm before action?

## Example: User-Only Skill

```yaml
name: "deploying-to-production"
description: "Deploys the application to production environment"
disable_model_invocation: true  # Only user can trigger deployments
content: |
  Deploy the application to production.

  ## Pre-deployment Checklist
  - [ ] All tests passing
  - [ ] Version bumped
  - [ ] Changelog updated

  ## Process
  1. Verify checklist items
  2. Run `pnpm build`
  3. Run `pnpm deploy:prod`
  4. Verify deployment success

  ## Output
  Deployment status and production URL.
```

## Example: Internal Helper Skill

```yaml
name: "validating-schema"
description: "Validates YAML against the canonical schema"
user_invocable: false  # Only used internally by other skills
content: |
  Validate a YAML file against the canonical schema.

  ## Process
  1. Read the YAML file
  2. Parse with Zod schema
  3. Return validation result

  ## Output
  - Success: "Valid"
  - Failure: List of validation errors
```

## Example: Standard Skill

```yaml
name: "formatting-code"
description: "Formats code according to project standards"
content: |
  Format the selected code according to project standards.

  ## Process
  1. Identify the language
  2. Apply appropriate formatter
  3. Show diff of changes

  ## Output
  Present formatted code and ask for confirmation.
```

## Reference

See `AI_NOTES/CLAUDE_PROMPT_ENGINEERING.md` for comprehensive best practices.
