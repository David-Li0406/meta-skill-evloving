# Reviewing Plugin Marketplace

Review Claude Code plugin marketplace configurations against official best practices.

## Required Permissions

To enable automatic execution of this skill's commands, add to `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Skill(reviewing-plugin-marketplace)",
      "Bash(skills/reviewing-plugin-marketplace/scripts/verify-marketplace.sh:*)",
      "Bash(cat .claude-plugin/marketplace.json)",
      "Bash(git remote -v)",
      "Bash(grep:*)",
      "Bash(ls:*)"
    ]
  }
}
```

**Note**: Adjust the script path if your skill is in a different location.

## Usage

This skill helps you review plugin marketplace configurations by checking:
- marketplace.json structure against Anthropic's official format
- Repository URL consistency with git remote
- Source path validation
- Plugin.json validation (if present)
- Common configuration errors

Trigger this skill when:
- Analyzing marketplace.json files
- Validating plugin configurations
- Detecting structural issues
- Ensuring compliance with official format

## Validation Script

The skill includes a validation script that performs comprehensive checks:

```bash
bash skills/reviewing-plugin-marketplace/scripts/verify-marketplace.sh [marketplace-dir]
```

If no directory is provided, it defaults to the current directory.

## Documentation

- **SKILL.md**: Main instructions for Claude
- **references/anthropic-format.md**: Official marketplace.json structure
- **references/common-errors.md**: Detailed error patterns and solutions

## Learn More

For complete guidance, see the official Claude Code documentation on plugin marketplace configurations.
