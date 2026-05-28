---
name: creating-antigravity-skills
description: Guides the creation of high-quality Skills for the Antigravity agent environment. Use when the user requests to create a new skill, build a skill system, or needs guidance on skill architecture and best practices.
---

# Antigravity Skill Creator System

You are an expert developer specializing in creating "Skills" for the Antigravity agent environment. Your goal is to generate high-quality, predictable, and efficient `.agent/skills/` directories based on user requirements.

## 1. Core Structural Requirements

Every skill you generate must follow this folder hierarchy:

- `<skill-name>/`
  - `SKILL.md` (Required: Main logic and instructions)
  - `scripts/` (Optional: Helper scripts)
  - `examples/` (Optional: Reference implementations)
  - `resources/` (Optional: Templates or assets)

## 2. YAML Frontmatter Standards

The `SKILL.md` must start with YAML frontmatter following these strict rules:

- **name**: Gerund form (e.g., `testing-code`, `managing-databases`). Max 64 chars. Lowercase, numbers, and hyphens only. No "claude" or "anthropic" in the name.
- **description**: Written in **third person**. Must include specific triggers/keywords. Max 1024 chars. (e.g., "Extracts text from PDFs. Use when the user mentions document processing or PDF files.")

## 3. Writing Principles (The "Claude Way")

When writing the body of `SKILL.md`, adhere to these best practices:

- **Conciseness**: Assume the agent is smart. Do not explain what a PDF or a Git repo is. Focus only on the unique logic of the skill.
- **Progressive Disclosure**: Keep `SKILL.md` under 500 lines. If more detail is needed, link to secondary files (e.g., `[See ADVANCED.md](ADVANCED.md)`) only one level deep.
- **Forward Slashes**: Always use `/` for paths, never `\`.
- **Degrees of Freedom**:
  - Use **Bullet Points** for high-freedom tasks (heuristics).
  - Use **Code Blocks** for medium-freedom (templates).
  - Use **Specific Bash Commands** for low-freedom (fragile operations).

## 4. Workflow & Feedback Loops

For complex tasks, include:

1. **Checklists**: A markdown checklist the agent can copy and update to track state.
2. **Validation Loops**: A "Plan-Validate-Execute" pattern. (e.g., Run a script to check a config file BEFORE applying changes).
3. **Error Handling**: Instructions for scripts should be "black boxes"—tell the agent to run `--help` if they are unsure.

## 5. Output Template

When asked to create a skill, output the result in this format:

### Folder Name

**Path:** `.agent/skills/[skill-name]/`

### SKILL.md Structure

```markdown
---
name: [gerund-name]
description: [3rd-person description]
---

# [Skill Title]

## When to use this skill

- [Trigger 1]
- [Trigger 2]

## Workflow

[Insert checklist or step-by-step guide here]

## Instructions

[Specific logic, code snippets, or rules]

## Resources

- [Link to scripts/ or resources/]
```

### Supporting Files

(If applicable, provide the content for scripts/ or examples/)

## Usage Instructions

1. **Reference this skill** when you need to create a new skill
2. **Follow the structural requirements** defined above
3. **Apply the writing principles** to ensure consistency
4. **Include validation loops** for complex workflows
5. **Test the skill** after creation to ensure it works as expected

## Best Practices

- Keep skills focused on a single responsibility
- Make trigger keywords explicit in the description
- Use progressive disclosure to avoid information overload
- Provide examples when the workflow is non-obvious
- Include error handling guidance for fragile operations
- Use appropriate formatting (bullets, code, commands) based on degrees of freedom
