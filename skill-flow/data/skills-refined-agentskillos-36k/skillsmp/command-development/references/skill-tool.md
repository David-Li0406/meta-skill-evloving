# Skill Tool Reference

How Claude programmatically invokes slash commands and skills during conversations.

## Overview

The Skill tool enables Claude to programmatically execute both slash commands and Agent Skills without user typing. This allows Claude to autonomously invoke these capabilities as part of complex workflows, chain them together, or use them in response to user requests.

> **Note:** In earlier versions of Claude Code, slash command invocation was provided by a separate `SlashCommand` tool. This has been merged into the `Skill` tool.

**Key concepts:**

- Claude can invoke both commands and skills via the Skill tool
- Commands need `description` frontmatter to be visible
- Skills can control visibility via `user-invocable` field
- Permission rules control which commands/skills Claude can invoke
- Character budget limits how many items Claude "sees"
- `disable-model-invocation` prevents programmatic invocation for both

## What the Skill Tool Can Invoke

| Type                  | Location                                     | Requirements                                   |
| --------------------- | -------------------------------------------- | ---------------------------------------------- |
| Custom slash commands | `.claude/commands/` or `~/.claude/commands/` | Must have `description` frontmatter            |
| Agent Skills          | `.claude/skills/` or `~/.claude/skills/`     | Must not have `disable-model-invocation: true` |
| Plugin commands       | `plugin-name/commands/`                      | Must have `description` frontmatter            |
| Plugin skills         | `plugin-name/skills/`                        | Must not have `disable-model-invocation: true` |

**Note:** Built-in commands like `/compact` and `/init` are NOT available through this tool.

## How the Skill Tool Works

### What It Does

When Claude determines a slash command or skill would help accomplish a task, it uses the Skill tool to invoke that capability. The tool:

1. Identifies available commands and skills based on permission rules
2. Selects appropriate item for the task
3. Executes the command or loads the skill with any arguments
4. Processes the output

### When Claude Uses It

Claude uses the Skill tool when:

- A command or skill directly addresses the user's request
- Multiple steps require chaining capabilities
- Automated workflows need command/skill execution
- User asks Claude to "run /command" or similar

**Example:** If a user says "review my code changes," Claude might use the Skill tool to invoke `/review` if such a command exists and is available.

## Visibility Requirements

### description Field Required

Commands **must** have a `description` frontmatter field to be visible to the Skill tool.

**Visible to Skill tool:**

```yaml
---
description: Review code for security issues
---
```

**NOT visible to Skill tool:**

```markdown
# No frontmatter - command only available via manual invocation

Review this code for security vulnerabilities...
```

**Why this requirement:**

- Claude uses descriptions to understand what commands do
- Descriptions help Claude select the right command
- Forces documentation of command purpose
- Prevents accidental programmatic invocation of undocumented commands

### Best Practices for Descriptions

Write descriptions that help Claude understand when to use the command:

**Good descriptions:**

```yaml
description: Review PR for code quality and security  # Clear purpose
description: Deploy application to staging environment  # Specific action
description: Run test suite and report failures  # Expected outcome
```

**Poor descriptions:**

```yaml
description: Review  # Too vague - Claude can't determine when to use
description: Does stuff  # Unhelpful - doesn't describe purpose
description: A command  # Obvious - provides no information
```

## Character Budget

### Default Budget

The Skill tool has a character budget limiting how many command/skill descriptions Claude receives. The default budget is **15,000 characters**.

### How Budget Works

1. Items are sorted by priority (project, then user, then plugin)
2. Descriptions are added until budget exhausted
3. Items exceeding budget are not visible to Claude
4. More concise descriptions = more items visible

### Configuring Budget

Set the `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable to adjust:

```bash
# Increase budget to show more commands/skills
export SLASH_COMMAND_TOOL_CHAR_BUDGET=30000

# Decrease budget for faster processing
export SLASH_COMMAND_TOOL_CHAR_BUDGET=8000
```

### Budget Optimization

**Keep descriptions concise:**

```yaml
# Good - concise (35 chars)
description: Review PR for security issues

# Bad - verbose (89 chars)
description: This command reviews pull requests for potential security vulnerabilities and issues
```

**Prioritize important items:**

- Project items appear before user items
- Keep critical commands/skills in project scope
- Move rarely-used items to user scope

## Permission Rules

### Overview

Permission rules control which commands and skills Claude can invoke via the Skill tool. Rules are configured in Claude Code settings.

### Rule Patterns

**Exact match (no arguments):**

```
Skill(commit)      # Only commit with no arguments
Skill(deploy)      # Only deploy with no arguments
```

**Prefix match (with arguments):**

```
Skill(review-pr:*)     # review-pr with any arguments
Skill(git:*)           # All items starting with git
Skill(plugin-name:*)   # All items from specific plugin
```

**Deny all:**

Add `Skill` to deny rules to prevent all programmatic invocation.

### Configuration Examples

**Allow specific commands:**

```json
{
  "allow": ["Skill(review:*)", "Skill(test:*)"]
}
```

**Deny dangerous commands:**

```json
{
  "deny": ["Skill(deploy-prod:*)", "Skill(delete:*)"]
}
```

**Deny all programmatic invocation:**

```json
{
  "deny": ["Skill"]
}
```

### Permission Precedence

1. Explicit deny rules take precedence
2. Explicit allow rules override defaults
3. Default behavior allows programmatic invocation
4. `disable-model-invocation` in frontmatter always blocks

## disable-model-invocation Field

### Purpose

The `disable-model-invocation` frontmatter field prevents Claude from programmatically invoking a command or skill, regardless of permission rules.

```yaml
---
description: Approve production deployment
disable-model-invocation: true
---
```

### When to Use

**Manual-only commands:**

```yaml
---
description: Approve production deployment
disable-model-invocation: true
---
# Production Deployment Approval

This deployment requires human judgment and sign-off.
Verify all checks have passed before approving.
```

**Destructive operations:**

```yaml
---
description: Delete all test data
disable-model-invocation: true
---

# Test Data Deletion

WARNING: This permanently deletes all test data.
This operation cannot be undone.
```

**Interactive workflows:**

```yaml
---
description: Setup wizard for new project
disable-model-invocation: true
---
# Project Setup Wizard

This wizard requires interactive user input at each step.
```

### How It Differs from Permission Rules

| Aspect   | disable-model-invocation  | Permission Rules     |
| -------- | ------------------------- | -------------------- |
| Scope    | Single command/skill      | Global/pattern-based |
| Location | Frontmatter               | Settings file        |
| Override | Cannot be overridden      | Can be adjusted      |
| Use case | Item-specific restriction | Policy enforcement   |

**Use `disable-model-invocation` when:**

- Item should NEVER be programmatically invoked
- Restriction is inherent to item's purpose
- Decision made by author

**Use permission rules when:**

- Organization policy restricts certain patterns
- User wants to control Claude's autonomy
- Temporary or adjustable restrictions needed

## user-invocable Field (Skills Only)

Skills have an additional `user-invocable` field that controls slash menu visibility:

```yaml
---
name: internal-review-standards
description: Apply internal code review standards
user-invocable: false
---
```

**Important distinctions:**

| Setting                          | Slash Menu | Skill Tool | Auto-Discovery |
| -------------------------------- | ---------- | ---------- | -------------- |
| `user-invocable: true` (default) | Visible    | Allowed    | Yes            |
| `user-invocable: false`          | Hidden     | Allowed    | Yes            |
| `disable-model-invocation: true` | Visible    | Blocked    | Yes            |

The `user-invocable` field only controls whether users see the skill in the `/` menu. It does NOT prevent Claude from using the skill via the Skill tool or auto-discovery.

## Integration Patterns

### Commands Designed for Programmatic Use

Some commands work well when invoked by Claude:

```yaml
---
description: Get current git status summary
allowed-tools: Bash(git:*)
---

# Git Status

Branch: `git branch --show-current`
Status: `git status --short`
Recent: `git log -3 --oneline`
```

This command:

- Has clear, specific description
- Produces useful output for Claude
- No destructive operations
- Quick execution

### Commands for Manual-Only Use

Some commands should remain manual:

```yaml
---
description: Force push to protected branch (DANGEROUS)
disable-model-invocation: true
allowed-tools: Bash(git:*)
---
# Force Push

WARNING: This will overwrite remote history.

Are you absolutely sure? Type the branch name to confirm: $1
```

This command:

- Uses `disable-model-invocation: true`
- Has clear warning in description
- Requires explicit confirmation
- Documents danger level

### Workflow Commands

Commands that chain others should consider visibility:

```yaml
---
description: Complete release workflow
---

# Release Workflow

Execute the following steps:
1. Run tests via /test
2. Update version via /version-bump $1
3. Create changelog via /changelog
4. Tag release via /tag-release $1

Verify each step before proceeding.
```

If sub-commands have `disable-model-invocation: true`, this workflow command will need user interaction at those steps.

## Troubleshooting

### Command/Skill Not Available to Claude

**Check description field:**

```yaml
---
description: Must have description # Required for visibility
---
```

**Check character budget:**

- Too many items may exceed budget
- Shorten descriptions or increase budget
- Check if item appears with `SLASH_COMMAND_TOOL_CHAR_BUDGET=100000`

**Check permission rules:**

- Verify no deny rules match the item
- Check if allow rules are too restrictive

### Claude Won't Invoke Command/Skill

**Check disable-model-invocation:**

```yaml
disable-model-invocation: true # Blocks programmatic invocation
```

**Check permission rules:**

- Look for deny patterns matching item
- Verify Skill not in global deny list

### Too Many Items Visible

**Reduce character budget:**

```bash
export SLASH_COMMAND_TOOL_CHAR_BUDGET=8000
```

**Shorten descriptions:**

- Keep under 60 characters
- Remove redundant words
- Focus on key purpose

**Use disable-model-invocation:**

- Add to items that shouldn't be auto-invoked
- Keep only essential items visible

## Best Practices

### For Authors

1. **Always include description** - Required for visibility
2. **Keep descriptions concise** - Respect character budget
3. **Use `disable-model-invocation` thoughtfully** - Only when truly needed
4. **Document dangerous operations** - Make risks clear in description
5. **Design for both uses** - Items should work manually and programmatically

### For Users/Organizations

1. **Set appropriate permission rules** - Balance autonomy and safety
2. **Adjust character budget** - Based on item volume
3. **Review descriptions** - Ensure Claude can understand them
4. **Test programmatic invocation** - Verify items work as expected
5. **Monitor usage** - Track which items Claude invokes
