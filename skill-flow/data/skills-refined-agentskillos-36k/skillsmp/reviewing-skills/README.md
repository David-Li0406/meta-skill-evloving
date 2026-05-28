# Reviewing Skills

Review agent skills against Claude's official best practices.

## Required Permissions

To enable this skill, add to `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Skill(reviewing-skills)"
    ]
  }
}
```

This skill primarily uses Read and Glob tools which don't require additional Bash permissions.

## Usage

This skill helps you review existing agent skills by checking:
- Naming conventions (gerund form preferred)
- Description quality (what + when to use)
- SKILL.md size and structure
- Progressive disclosure patterns
- Workflows and validation patterns
- Reference file organization
- Content quality and conciseness

Trigger this skill when:
- Analyzing existing skills for compliance
- Providing feedback on skill design
- Identifying areas for improvement
- Ensuring skills follow best practices

## Review Process

1. **Initial Analysis**: Read SKILL.md and directory structure
2. **Core Compliance Checks**: Name, description, size, progressive disclosure
3. **Detailed Structure Review**: Files, references, workflows, validation
4. **Generate Feedback**: Critical issues, important issues, suggestions
5. **Provide Actionable Feedback**: Specific fixes with examples

## Documentation

- **SKILL.md**: Main instructions for Claude
- **references/checklist.md**: Comprehensive review criteria

## Learn More

For complete guidance, see the official Claude documentation:
- [Agent Skills Overview](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)
- [Best Practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices)
