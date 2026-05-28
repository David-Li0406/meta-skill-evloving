---
name: creating-ai-agent-skills
description: Use this skill when you need to create new AI agent skills following best practices and comprehensive documentation.
---

# Creating AI Agent Skills Guide

## Purpose

This skill helps you create new Agent Skills for AI Agents by following a structured workflow based on best practices and comprehensive documentation.

## When to Create a New Skill

Create a skill when:
- A module has patterns that differ from generic best practices.
- AI frequently needs context about a specific area.
- Documentation would benefit from on-demand loading.
- The pattern is used repeatedly across the project.

Do NOT create a skill for:
- One-off tasks.
- Trivial patterns already well-documented.
- Generic technology patterns (use existing skills).

## Skill Structure

Every skill must have the following directory structure:

```
.claude/skills/skill-name/
├── SKILL.md                 # Required - main instructions
└── references/              # Optional - detailed docs
    ├── detailed-topic.md
    └── another-topic.md
```

## SKILL.md Template

```yaml
---
name: skill-name
description: Brief description of what this skill covers. Include trigger keywords that should activate it.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, Task
---

# Skill Title

## Overview

One paragraph explaining the module/pattern this skill covers.

## Core Patterns

### Pattern 1 Name

Explain the pattern with code examples:

```typescript
// Example code
```

**Why this matters:** Explanation of consequences.

### Pattern 2 Name

...

## Key Files

| File | Purpose |
|------|---------|
| `path/to/file.ts` | Description |

## Common Pitfalls

1. **Mistake name:** What goes wrong and how to fix it
2. ...

## Additional Resources

For detailed documentation:
- [topic.md](references/topic.md) - Description
```

## Naming Conventions

- **Reclip-specific:** `reclip-{module}` (e.g., `reclip-editor`)
- **Technology:** `{tech}-patterns` (e.g., `zustand-patterns`)
- **Meta:** Descriptive name (e.g., `skill-creator`)

## Writing Effective Descriptions

The description determines when Claude loads the skill. Include:
1. **What it covers:** "PixiJS video rendering, timeline editing"
2. **Trigger keywords:** "Use when working on PixiCanvas, zoom effects"
3. **File hints:** "or any editor canvas functionality"

**Good:**
```yaml
description: PixiJS video rendering engine, timeline editing, zoom effects. Use when working on PixiCanvas.tsx, Timeline.tsx, or video playback.
```

**Bad:**
```yaml
description: Editor stuff.
```

## Skill Creation Workflow

### Step 1: Define the Skill's Purpose

Ask the user these questions:
1. What task or domain should this skill cover?
2. When should Claude use this skill? (triggers)
3. What expertise or workflows need to be captured?
4. Does it need scripts, templates, or other resources?

Document the answers for reference.

### Step 2: Create the Skill Directory Structure

Create skills in the project's `.claude/skills/` directory for team sharing:

```bash
mkdir -p .claude/skills/<skill-name>
```

**Naming conventions:**
- **Use gerund form** (verb + -ing): `processing-pdfs`, `analyzing-spreadsheets`, `managing-databases`
- Must contain only **lowercase letters, numbers, and hyphens**
- Maximum 64 characters
- Cannot contain XML tags or reserved words ("anthropic", "claude")
- Avoid generic names like `helper`, `utils`, `tools`

### Step 3: Design the SKILL.md Structure

Every skill must have:
```yaml
---
name: Your Skill Name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
[Clear, step-by-step guidance for Claude]

## Examples
[Concrete examples of using this Skill]
```

### Step 4: Write the Instructions Section

**Structure the instructions as:**
1. **Prerequisites** - Required dependencies, tools, environment setup
2. **Workflow** - Step-by-step process (numbered steps)
3. **Supporting Details** - Additional context, script usage, error handling

**Best Practices:**
- Use clear, actionable language
- Number sequential steps
- Use bullet points for options/lists
- Include code blocks with bash commands
- Reference supporting files with relative links: `[reference.md](reference.md)`
- Keep focused on one capability
- **Keep SKILL.md body under 500 lines** for optimal performance

### Step 5: Write the Examples Section

Provide 2-4 concrete examples showing:
- Different use cases
- Various input formats
- Step-by-step execution
- Expected outcomes

### Step 6: Add Supporting Files (Optional)

If the skill needs additional context:
1. Create files alongside SKILL.md
2. Reference them from instructions: `[forms.md](forms.md)`
3. Use progressive disclosure - split by topic/scenario

### Step 7: Test the Skill

1. Verify file structure:
   ```bash
   ls -la .claude/skills/<skill-name>/
   ```

2. Check YAML frontmatter is valid:
   ```bash
   head -10 .claude/skills/<skill-name>/SKILL.md
   ```

3. Test with relevant queries:
   - Ask questions matching the skill's description
   - Verify Claude loads and uses the skill
   - Check that instructions are clear and actionable

4. Iterate based on testing:
   - Refine description if skill doesn't trigger
   - Clarify instructions if Claude struggles
   - Add examples for common edge cases

### Step 8: Commit to Version Control

Since project skills are automatically shared with your team, commit them to git:

```bash
git add .claude/skills/<skill-name>
git commit -m "Add <skill-name> skill"
git push
```

## Summary

Creating skills is about packaging expertise into discoverable, composable capabilities. Follow these principles:
1. **Read the docs first** - Understand progressive disclosure and skill architecture.
2. **Write clear descriptions** - Include what AND when.
3. **Keep instructions focused** - Use supporting files for additional context.
4. **Test thoroughly** - Verify Claude discovers and uses the skill correctly.
5. **Iterate with feedback** - Refine based on actual usage.

Skills transform general-purpose Claude into a specialist for your domain. Start small, test early, and expand as needed.