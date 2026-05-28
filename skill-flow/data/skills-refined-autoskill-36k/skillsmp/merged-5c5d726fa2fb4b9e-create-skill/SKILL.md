---
name: create-skill
description: Use this skill when you need to create a new skill with a proper structure and best practices, or when the user asks to scaffold a reusable agent capability.
---

# Skill Creation Guide

This skill guides the creation of new skills with a structured approach to ensure clarity and effectiveness.

## Understanding Skills vs Commands

**IMPORTANT**: The agent autonomously decides when to use skills based on context, differing from explicit slash commands.

- **Descriptions must be discoverable**: Include keywords users would naturally say.
- **Agent matches intent**: Write descriptions that help the agent recognize when the skill applies.
- **No explicit invocation**: Users don't type a command; the agent activates skills automatically.

## Step 1: Gather Requirements

Extract skill details from the user's message:

- **Skill name**: Look for kebab-case identifiers (e.g., `code-reviewer`, `test-runner`).
- **Skill description**: Identify what the skill does and when to use it.
- **Trigger phrases**: Determine when this skill should activate.

If any required information is missing, ask the user to complete it.

## Step 2: Create Directory Structure

```
~/.config/ai/skills/<skill-name>/
├── SKILL.md          (required - main instructions)
├── reference.md      (optional - detailed documentation)
├── examples.md       (optional - usage examples)
├── scripts/          (optional - utility scripts)
└── templates/        (optional - file templates)
```

## Step 3: Write SKILL.md

### Required YAML Frontmatter

```yaml
---
name: <skill-name>
description: <what-it-does>. <when-to-use-it>.
license: Complete terms in LICENSE.txt
---
```

### Frontmatter Rules

- **name**: Max 64 chars, lowercase letters/numbers/hyphens only.
- **description**: Max 1024 chars, MUST include:
  - What the skill does (functionality).
  - When to use it (trigger conditions/keywords).
  - **IMPORTANT**: The description is critical for skill activation.

### Content Section

After the frontmatter, write clear instructions for the agent:

- Step-by-step workflow.
- Expected inputs/outputs.
- Error handling guidance.
- Quality criteria.

## Skill Excellence Guidelines

Focus on:

- **Frontmatter**: Ensure it includes `name`, `description`, and `license`.
- **Thinking Section**: Include strategic questions to guide skill development.
- **CRITICAL Callout**: State non-negotiable principles clearly.
- **Guidelines Section**: Provide actionable techniques in a concise format.
- **NEVER Section**: List anti-patterns to avoid in a dense paragraph.

## Best Practices Checklist

- [ ] **Single focus**: One skill = one capability.
- [ ] **Clear triggers**: Description includes specific keywords users would say.
- [ ] **Discoverable**: Use terminology that matches user intent.
- [ ] **Tested**: Verify the skill activates correctly.
- [ ] **Versioned**: Include version history for team transparency.

## Output Location

Create skills in: `~/.config/ai/skills/<skill-name>/SKILL.md`.

For project-specific skills: `.ai/skills/<skill-name>/SKILL.md`.

### Reference files

If users request code examples or detailed patterns, create a `references/` folder with concrete examples. Keep SKILL.md lean—reference files hold the detail.

**IMPORTANT**: Match skill tone to domain culture. Technical skills use precise language, while creative skills permit more latitude.

Remember: Skills must be deterministic, not aspirational. Every instruction should constrain output to ensure consistent, high-quality results.