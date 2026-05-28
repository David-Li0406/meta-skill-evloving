---
name: opencode-config-validation
description: Validates OpenCode configuration files for correctness and best practices
---

# OpenCode Configuration Validation

This skill provides comprehensive validation rules for OpenCode configurations.

## Overview

Use this skill to validate agent, skill, and command configurations before finalizing them. It ensures configurations follow OpenCode standards and will work correctly.

## When to Use

Load this skill when:

- Creating new OpenCode configurations
- Validating existing configurations
- Checking for naming convention compliance
- Ensuring configuration completeness

## Agent Validation

### Required Elements

1. **Frontmatter Fields**:
   - `description`: Required, 1-200 characters
   - `mode`: Required for agents (`primary`, `subagent`, or `all`)

2. **Optional Fields**:
   - `model`: Format must be `provider/model-id`
     - To get a list of valid model IDs, run: `opencode models`
     - This command shows all available models with their providers
   - `temperature`: Must be between 0.0 and 1.0
   - `tools`: Object with boolean values
   - `permissions`: Object with `allow`, `ask`, or `deny` values
   - `maxSteps`: Positive integer for iteration limits

3. **File Structure**:
   - Location: `~/.config/opencode/agent/[name].md` or `.opencode/agent/[name].md`
   - Must have frontmatter section (between `---` markers)
   - Should include agent instructions after frontmatter

### Naming Rules

- Lowercase letters only
- Hyphens allowed (not at start/end)
- No spaces, underscores, or special characters
- Valid: `code-review`, `otto-analyzer`
- Invalid: `Code_Review`, `otto analyzer`, `review-`

### Tool Configuration

Valid tool names:

- `read`, `write`, `edit`
- `bash`, `glob`, `grep`
- `skill`, `task`, `webfetch`
- `todowrite`, `todoread`
- MCP server tools (format: `servername_toolname`)

### Permission Configuration

```yaml
permissions:
  edit: allow|ask|deny
  bash:
    "git *": allow
    "npm *": ask
    "*": deny
  webfetch: allow
```

## Skill Validation

### Required Elements

1. **Directory Structure**:
   - Must be in `skill/[name]/SKILL.md`
   - Directory name must match skill name

2. **Frontmatter Fields**:
   - `name`: Required, must match directory
   - `description`: Required, 1-1024 characters

3. **Optional Fields**:
   - `license`: SPDX identifier
   - `compatibility`: String value
   - `metadata`: Key-value pairs

### Naming Rules

- Must match: `^[a-z0-9]+(-[a-z0-9]+)*$`
- No consecutive hyphens (`--`)
- No leading/trailing hyphens
- Valid: `git-workflow`, `code-review-process`
- Invalid: `git--workflow`, `-review`, `review-`

### Content Structure

Should include:

- Overview section
- "When to Use" criteria
- Clear instructions
- Examples (optional but recommended)

## Command Validation

### Required Elements

1. **File Location**:
   - Must be in `command/[name].md`
   - File name becomes command name

2. **Frontmatter Fields**:
   - At least one of: `template` or `description`

3. **Optional Fields**:
   - `agent`: Which agent handles the command
   - `model`: Model override
   - `subtask`: Boolean for subagent invocation

### Template Syntax

- `$ARGUMENTS`: All arguments as string
- `$1`, `$2`, etc.: Individual arguments
- `!`command``: Shell command interpolation
- `@filename`: File reference

### Naming Rules

- Short, memorable names
- Lowercase only
- No special characters
- Should be easy to type

## Common Validation Errors

### Agent Errors

1. **Missing description**: Every agent needs a description
2. **Invalid mode**: Must be primary, subagent, or all
3. **Bad tool names**: Check spelling of tool names
4. **Invalid temperature**: Must be 0.0-1.0

### Skill Errors

1. **Name mismatch**: Directory and name field must match
2. **Invalid characters**: Only lowercase and hyphens
3. **Missing SKILL.md**: File must be named exactly `SKILL.md`
4. **Description too long**: Keep under 1024 characters

### Command Errors

1. **No template**: Commands need content
2. **Invalid placeholders**: Check $ syntax
3. **Bad shell syntax**: Use !`command` not just !command

## Validation Process

1. **Structure Check**:
   - Verify file locations
   - Check directory structure
   - Validate file naming

2. **Frontmatter Validation**:
   - Parse YAML correctly
   - Check required fields
   - Validate field values

3. **Content Validation**:
   - Ensure instructions exist
   - Check for placeholder syntax
   - Verify example validity

4. **Cross-Reference Check**:
   - No duplicate names
   - Valid agent references
   - Existing skill dependencies

## Best Practices

1. **Descriptions**:
   - Be specific about purpose
   - Use action-oriented language
   - Keep concise but informative

2. **Naming**:
   - Use descriptive names
   - Follow conventions consistently
   - Avoid overly generic names

3. **Documentation**:
   - Include usage examples
   - Document special behaviors
   - Explain configuration choices

4. **Testing**:
   - Test configurations before deployment
   - Verify in isolation first
   - Check integration with other components
