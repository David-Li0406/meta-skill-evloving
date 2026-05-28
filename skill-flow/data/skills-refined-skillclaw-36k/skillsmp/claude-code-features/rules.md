# Rules

**Trigger**: Conditional (when `paths:` specified) or always

## Characteristics

- **Can apply to specific files only** via `paths:` frontmatter
- Modular decomposition to prevent CLAUDE.md bloat
- Placed in `.claude/rules/`

## Best For

- Content regarding the entire repository
    - Project glossary
    - Usecase
    - User persona
- Content that should be documented in the root directory for application across multiple projects, but which becomes lengthy and difficult to maintain.
    - Accessibility Guidelines
    - Security requirements
    - Coding guidelines

## Not Suitable For

- Execution procedures (→ Commands)
- Automated processing (→ Hooks)
