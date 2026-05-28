# Creating Effective Skills

Guide for creating agent skills following Claude's official best practices.

## Required Permissions

To enable this skill, add to `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Skill(creating-effective-skills)"
    ]
  }
}
```

This skill provides guidance and doesn't require additional Bash permissions. However, if your created skills use scripts, add their specific permissions following the examples in SKILL.md Step 7.

## Usage

This skill helps you create high-quality agent skills by providing:
- 8-step workflow for skill creation
- Progressive disclosure patterns
- Degrees of freedom guidance
- Workflows and validation patterns

Trigger this skill when:
- Designing new agent skills
- Improving existing skills
- Learning about naming conventions and description writing
- Understanding appropriate freedom levels

## Documentation

- **SKILL.md**: Main instructions for Claude
- **references/progressive-disclosure.md**: Detailed patterns for organizing content
- **references/degrees-of-freedom.md**: Guidance on freedom levels
- **references/workflows-and-validation.md**: Creating workflows with validation

## Learn More

For complete guidance, see the official Claude documentation:
- [Agent Skills Overview](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)
- [Best Practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices)
