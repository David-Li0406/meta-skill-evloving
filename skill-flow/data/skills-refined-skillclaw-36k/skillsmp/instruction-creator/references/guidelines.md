# Instruction Creation Guidelines

## Architecture Context

This file defines **Level 2: Custom Instruction** in the **Agent -> Instruction -> Skill** architecture.

- **Role**: The **Policy Maker**.
- **Responsibility**: Defines workflow steps, decision logic, and constraints.
- **Dependency**: Referenced by Agents (`*.agent.md`); References Skills (`skills/*/SKILL.md`).

## Frontmatter Guidelines

- **description**: Single-quoted string, 1-500 characters, clearly stating the purpose.
- **applyTo**: Glob pattern(s) specifying which files these instructions apply to.
  - Single pattern: `'**/*.ts'`
  - Multiple patterns: `'**/*.ts, **/*.tsx, **/*.js'`
  - Specific files: `'src/**/*.py'`
  - All files: `'**'`

## Content Guidelines

### Writing Style
- Use clear, concise language.
- Write in imperative mood ("Use", "Implement", "Avoid").
- Be specific and actionable.
- Avoid ambiguous terms like "should", "might", "possibly".
- Use bullet points and lists for readability.

### Semantic Linking
Use standard Markdown links to reference Skills and other Instructions.
- **Link to Skill**: `To perform [Task], execute the [Skill Name](skills/<skill-name>/SKILL.md).`
- **Link to Instruction**: `Follow the [Sub-Process](instructions/<name>.instructions.md).`

## Patterns to Avoid
- **Overly verbose explanations**: Keep it concise and scannable.
- **Outdated information**: Always reference current versions and practices.
- **Ambiguous guidelines**: Be specific about what to do or avoid.
- **Missing examples**: Abstract rules without concrete code examples.
- **Contradictory advice**: Ensure consistency throughout the file.
- **Copy-paste from documentation**: Add value by distilling and contextualizing.
